#!/usr/bin/env python3
"""生成「小红书小工具」版发布包。

与主站 `web/` 的差异（全部自动处理，避免手工漏改导致整站 JS 崩）：

1. **去 PWA**：`index.html` 的 manifest / apple-touch-icon 链接；`script.js` 的 serviceWorker 注册
   （小红书包不带 `sw.js`，留着会 404）。
2. **去「误区」入口**：`index.html` 的 `pitsBtn` 按钮 + `pitsView` 区块；`script.js` 的
   `renderPits()`、`pitsBtn` 监听、路由里的 `pits` 分支、`VIEWS` 里的 `pitsView`。
3. **图标缩到 78px**（显示尺寸 39px 的 2x）：原图 722×733 / 487KB，缩后约几 KB；
   文件名保持 `brand-icon.png`，因此 `index.html` 无需改 src。
4. **顶部原生遮挡补白**：小红书内嵌网页顶部压着两层原生浮层——iOS 状态栏 + 小红书自己的
   悬浮工具条（‹ 分享 ⋯）。工具条高度网页侧读不到，按 44px 预算；`env(safe-area-inset-top)`
   在部分 webview 返回 0，故给它 44px 下限。追加在 `style.css` 末尾（源码次序靠后 → 覆盖
   基础规则与手机媒体查询），主站不受影响。

用法：
    python3 tools/build_xhs.py                 # 输出 web-小红书-品牌版-YYYYMMDD.zip
    python3 tools/build_xhs.py --out foo.zip
    python3 tools/build_xhs.py --keep-dir      # 保留解包目录（便于本地起服务验证）

设计纪律：每处改动都 assert 命中，源文件变了就**报错停住**，不静默产出坏包。
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
PLAIN_FILES = ["words.json"]
ICON = "brand-icon.png"
ICON_DISPLAY_PX = 78

# 小红书原生浮层高度预算：工具条 44px；状态栏取下限 44px（env() 在部分 webview 报 0）
XHS_CHROME_CSS = """
/* ---------- 小红书内嵌网页专用：顶部原生遮挡补白 ----------
   iOS 状态栏与小红书悬浮工具条（‹ 分享 ⋯）都是原生浮层，网页侧拿不到高度，
   故按「状态栏 ≥44px + 工具条 44px」预留。规则必须在文件最末：
   同选择器下源码次序靠后者胜，才能覆盖基础规则与 max-width:480px 媒体查询。 */
.site-header { padding-top: calc(12px + max(env(safe-area-inset-top), 44px) + 44px); }
"""


def patch_html(src: str) -> str:
    out = src

    def cut(pattern, label, count=1, flags=0):
        nonlocal out
        new, n = re.subn(pattern, "", out, count=count, flags=flags)
        assert n == count, f"index.html: 未命中「{label}」（源文件可能已改，请更新 build_xhs.py）"
        out = new

    cut(r'\n<link rel="manifest"[^\n]*', "manifest 链接")
    cut(r'\n<link rel="apple-touch-icon"[^\n]*', "apple-touch-icon 链接")
    cut(r'\n[ \t]*<button id="pitsBtn".*?</button>', "误区按钮")
    cut(
        r'\n[ \t]*<!--[^\n]*AI 常见误区（聚合页）[^\n]*-->\n[ \t]*<section id="pitsView".*?</section>\n',
        "误区聚合页区块",
        flags=re.S,
    )
    assert "pits" not in out, "index.html: 仍残留 pits 相关标记"
    return out


def patch_js(src: str) -> str:
    out = src

    def cut(pattern, label, count=1, flags=0):
        nonlocal out
        new, n = re.subn(pattern, "", out, count=count, flags=flags)
        assert n == count, f"script.js: 未命中「{label}」（源文件可能已改，请更新 build_xhs.py）"
        out = new

    # 1) VIEWS 数组里的 pitsView
    #    用 ", 'pitsView'" 匹配，不写死它后面还有没有别的视图（VIEWS 会长）
    new, n = re.subn(r", 'pitsView'", "", out, count=1)
    assert n == 1, "script.js: 未命中 VIEWS 里的 pitsView"
    out = new
    # 2) 路由的 pits 分支
    cut(r"  \} else if \(h === 'pits'\) \{\n(?:.*\n)*?    showView\('pitsView'\);\n", "路由 pits 分支")
    # 3) renderPits() 函数 + pitsBtn 监听
    cut(
        r"/\* -+ AI 常见误区.*?\n\}\n\$\('#pitsBtn'\)\.addEventListener\('click', \(\) => \{ location\.hash = 'pits'; \}\);\n\n",
        "renderPits 与 pitsBtn 监听",
        flags=re.S,
    )
    # 4) serviceWorker 注册整段（小红书包无 sw.js）
    #    这段现在先算 isLocalPreview 再分支，所以从注释头一直吃到文件末尾那个顶格的 }
    cut(
        r"/\* -+ PWA：注册 Service Worker.*?\n\}\n",
        "serviceWorker 注册（含本地预览判断）",
        flags=re.S,
    )
    assert "pits" not in out.lower(), "script.js: 仍残留 pits 相关代码"
    assert "serviceWorker" not in out, "script.js: 仍残留 serviceWorker"
    return out


def patch_css(src: str) -> str:
    assert ".site-header {" in src, "style.css: 未找到 .site-header 规则（源文件可能已改）"
    assert "XHS_CHROME" not in src, "style.css: 已含小红书包补丁"
    return src.rstrip("\n") + "\n" + XHS_CHROME_CSS


def shrink_icon(src: Path, dst: Path) -> str:
    """优先用 macOS 的 sips，其次 PIL，都不可用则原样复制（并提示）。"""
    if shutil.which("sips"):
        subprocess.run(
            ["sips", "-Z", str(ICON_DISPLAY_PX), str(src), "--out", str(dst)],
            check=True, capture_output=True,
        )
        return "sips"
    try:
        from PIL import Image  # type: ignore
        im = Image.open(src)
        im.thumbnail((ICON_DISPLAY_PX, ICON_DISPLAY_PX))
        im.save(dst, optimize=True)
        return "PIL"
    except Exception:
        shutil.copy2(src, dst)
        print("⚠️  未能缩放图标（sips/PIL 都不可用），已原样复制", file=sys.stderr)
        return "copy"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=f"web-小红书-品牌版-{date.today():%Y%m%d}.zip")
    ap.add_argument("--keep-dir", action="store_true", help="保留解包目录")
    ap.add_argument("--dir", help="指定解包目录（隐含保留；便于本地起服务验证）")
    args = ap.parse_args()

    out_zip = (ROOT / args.out) if not Path(args.out).is_absolute() else Path(args.out)
    if args.dir:
        build = Path(args.dir)
        shutil.rmtree(build, ignore_errors=True)
        build.mkdir(parents=True)
        args.keep_dir = True
    else:
        build = Path(tempfile.mkdtemp(prefix="xhs-build-"))

    (build / "index.html").write_text(patch_html((WEB / "index.html").read_text(encoding="utf-8")), encoding="utf-8")
    (build / "script.js").write_text(patch_js((WEB / "script.js").read_text(encoding="utf-8")), encoding="utf-8")
    (build / "style.css").write_text(patch_css((WEB / "style.css").read_text(encoding="utf-8")), encoding="utf-8")
    for name in PLAIN_FILES:
        shutil.copy2(WEB / name, build / name)
    how = shrink_icon(WEB / ICON, build / ICON)

    out_zip.unlink(missing_ok=True)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(build.iterdir()):
            z.write(p, p.name)

    print(f"✅ {out_zip.name}  ({out_zip.stat().st_size / 1024:.0f} KB)")
    print(f"   文件：{', '.join(sorted(p.name for p in build.iterdir()))}")
    print(f"   图标：{ICON} 缩放到 {ICON_DISPLAY_PX}px（{how}，{(build / ICON).stat().st_size / 1024:.1f} KB）")
    print("   顶栏：已注入小红书原生浮层补白 calc(12px + max(env(safe-area-inset-top),44px) + 44px)")
    if args.keep_dir:
        print(f"   解包目录保留在：{build}")
    else:
        shutil.rmtree(build)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
