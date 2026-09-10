# ai-vocab 改版落地核对（真源码 vs handover vs demo）

> **性质**：只读核对，未改任何代码。日期 2026-09-10。
> **对象**：`web/style.css`(485 行) / `web/index.html`(155 行) / `web/script.js`(581 行) ↔ `REDESIGN-HANDOVER.md` ↔ 两个 demo。
> **一句话结论**：品牌层**已落地并提交**（`c612b20`），handover 的「⏳ 未改真源码」已过期；真源码**缺 2 项、偏离 7 项**，另有 **4 处文档与代码互相打架**需裁决、**6 处冷/暖 token 不齐**。

---

## A. 已落地（handover 对应待办可勾掉）

| 项 | 证据 |
|---|---|
| 品牌 token 全套（奶油底/深紫/暖黑/描边/圆角/阴影/缓动） | `style.css:6-42` |
| 头部品牌：图标 39px + 「AI 词汇本」22/800 + AI 紫；home 键隐藏 | `index.html:21-24`、`style.css:73-76,86` |
| hero「从这 3 个词开始」可折叠 + 三词 | `index.html:61-71`、`style.css:161-186` |
| 六大主题纵览 + 小节标签紫 13/600 + 主题彩条关闭 | `style.css:187-191` |
| 词条胶囊 14px、进阶徽标、热门行弱化 | `style.css:219-236` |
| 旧蓝清零 | 全仓 grep `#0064FA`：0 命中 |

## B. 缺失（handover/demo 有，真源码完全没有）

- **B1 背景装饰层** ✅ 已补（2026-09-10）：demo 有 `.blob`(#EDE4D3) + `.spark`(✳)（`ai-vocab-brand-v2-demo.html:22,84-85`）；真源码**无对应元素**，只留了没用的 `--a1..--a6` 紫阶（`style.css:40`）。
- **B2 词条页「上一词/下一词」** ✅ 已补（2026-09-10）：demo 有 `.np` 两块导航（`ai-vocab-entry-demo.html:74-77,124-125`）；`script.js` 无渲染、`style.css` 无 `.np`。

## C. 偏离（两边都有，规格不一致）

| # | handover / demo 规格 | 真源码现状 | 证据 |
|---|---|---|---|
| C1 | 词条标题 28 / 800 | 24 / 600 | `style.css:373` |
| C2 | 词条 meta 12.5px | 14px | `style.css:374` |
| C3 | 词条小节标签：紫 + 13/700 + 短线 | 灰 `--muted` + 14/600 | `style.css:384` vs `entry-demo:47-48` |
| C4 | 类比块：底 `#F6F1E9` + 紫描边 + 左 3px 紫 | 冷灰 `rgba(46,50,56,.05)` + 冷描边、无左紫条 | `style.css:387-390` vs `entry-demo:53-55` |
| C5 | 相关词标题 紫 13/700 | 灰 `--muted` | `style.css:409` vs `entry-demo:59` |
| C6 | 主题名 15 / 700 | 14 / 600 | `style.css:206` |
| C7 | 页脚 12px | 14px（复用 `.small`） | `style.css:138`、`index.html:120` |

## D. 文档与代码互相打架

> **裁决（2026-09-10，用户已定）**：**D1 保持浅灰**、**D2 保持默认展开** —— 两项均以代码为准，回写 handover；
> **D3+D4 顶栏与页脚 emoji 全去**（`✨ 新手教程`/`⚠️ 误区` 去 emoji、按钮本身保留；页脚去 🦜）；handover 未提的「⚠️ 误区」按钮**保留功能**，不在视觉层删功能。
> 下列四条保留原始分歧记录，供回写文档时对照。

- **D1 进阶徽标颜色**：handover §3「紫色只在小节标签 / **进阶徽标** / hover」↔ 源码**刻意做浅灰**（`style.css:226-231`，提交信息 `c612b20` 明写「进阶徽标浅灰」）。→ 裁决：**浅灰**。
- **D2 更多小提示**：handover §5「`details` 折叠」↔ 源码 `open` **默认展开**（`script.js:353`）。
- **D3 顶栏按钮**：handover 只提 搜索 + 新手教程 ↔ 源码多一个「⚠️ 误区」，且两个按钮带 emoji（`index.html:34-35`）；demo 无 emoji（`brand-v2-demo:95`）。
- **D4 页脚**：源码保留 🦜 emoji（`index.html:124`）；品牌方向是「现代简约 + 去 emoji」。

## E. 冷/暖 token 不齐（审计杠杆③「收敛越档位 token」的实体清单）

- **E1** ✅ chip 改走 `var(--card)` + `var(--line)`（原 `#ffffff` + `rgba(0,0,0,.12)`）
- **E2** ✅ 搜索输入改 `var(--line)` + `var(--radius-btn)` + `var(--card)`（原 `rgba(0,0,0,.15)` + 4px）
- **E3** ✅ `.tree-head:hover` 改暖色 `rgba(42,39,34,.05)`（原冷灰 `rgba(46,50,56,.05)`）
- **E4** ✅ `.modal-overlay` 改暖黑 `rgba(42,39,34,.45)`（原冷灰 `rgba(31,35,41,.45)`）
- **E5** ✅ 圆角归一到 12 / 9999 / 3：`.st` 10→`var(--radius)`、`.hbtn` 8→`var(--radius-btn)`；复扫后 `style.css` 只剩语义性例外（`50%` 圆形图标按钮、`2px` 小节短线、blob 有机圆角）
- **E6** `script.js:39-43` 六层 `#0075de` 死色条 + 过期注释「Notion Blue」，被 `style.css:190` 的 `display:none` 关掉 ← **✅ 已清（2026-09-10）**：删掉 `LAYER_COLOR` 常量与 `tree-color` span 渲染，连带清掉 `style.css` 两条已死的 `.tree-color` 规则；headless Chrome 实测 6 层/111 胶囊/18 小节全部正常渲染，DOM 中 `tree-color` 0 命中。

## F. 附带发现（不在本次范围，仅记录）

- handover 词数过期：实际 应用层 **23**（写 20）、生态与前沿 **33**（写 32）、漏「训练方法」整节 6 词、总 **111** vs 107。
- `台账.md` 称「git status 保持干净」，实际未跟踪：`REDESIGN-HANDOVER.md`、`web/*.bak-0906`、`previews/` 4 张已删未提交。
- demo 用 `--surface`，源码用 `--surface-alt`（同值不同名），迁移时别照抄变量名。

## G. 建议顺序（等你点头再动手，改一处验一处）

1. ~~E6 清死码~~ ✅ 已完成（2026-09-10，见 E6）
2. ~~D1–D3 裁决 → 冻结规格~~ ✅ 已完成（见 D）
3. ~~B1 / B2 补齐~~ ✅ 已完成（见 H）
4. ~~C1–C7 对齐~~ ✅ 已完成（见 H）
5. ~~E1–E5 token 收口~~ ✅ 已完成（见 H 第三批）
6. 回写 handover 词数与状态；更新权威笔记 ← 尚未做（权威笔记已更新；handover 待你点头）

---

## H. 执行记录（2026-09-10 第二批：B + C + D3/D4）

**改动文件**：`web/index.html`、`web/style.css`、`web/script.js`（只碰视觉/布局与词条页导航渲染，未动搜索/折叠/路由逻辑）。

- **B1 装饰层** ✅ `index.html` 加 `.deco`（2 blob + 2 紫✳）；`style.css` 加 `.deco/.blob/.b1/.b2/.spark/.sp1/.sp2`（blob `#EDE4D3`/`.55`、星刺 `.4`）；`.container/.site-footer` 提 `position:relative;z-index:1` 压住装饰层，`body` 加 `overflow-x:hidden`。demo 里的 `.dash/.dot` 属 handover §1 明令不要的「人人都有」装饰，**未采用**。
- **B2 上下词导航** ✅ `script.js` 加 `makeNavItem()`，`renderEntry()` 内按 `state.data.words` 顺序渲染 `<nav class="entry-nav">`；`bindEntryClicks` 选择器加 `.np`；`style.css` 加 `.entry-nav/.np`。**边界语义**：首词只显示「下一词」、末词只显示「上一词」，缺的一侧不占位（非禁用态）。
- **C1–C7** ✅ 词条标题 28/800 并新增 `.entry-en` 16/500 与词名同行；`.meta-line` 12.5px；词条内小节标签改 **紫 13/700 + `::before` 16×2 短线**；类比块改 `--surface-alt`(`#F6F1E9`) + 紫描边 `rgba(91,76,231,.28)` + 左 3px 紫条 + 正文 14/1.7；`.related-title` 紫 13/700；`.tree-name` 15/700；页脚 12px（`.site-footer .small`）。移动端词条标题 20→**22**（不取 28，避免窄屏断行过多）。
- **D3/D4 emoji** ✅ 顶栏「新手教程」「误区」+ 页脚三处（添加到桌面／反馈 & 纠错／页脚文案）已去 emoji；「误区」按钮功能保留。
- **圆角取舍**：`.np` 用 `var(--radius)`(12px) 而非 demo 的 10px，与 E5「圆角归一」方向一致。

**验证**（不是"看着对"）：`node --check` 通过；headless Chrome 实测——
- 首页：6 层 / 111 胶囊 / 18 小节；`.deco` 1 组（2 blob + 2 星刺）；`tree-color` 0 命中；顶栏按钮文字为纯文字。
- 词条页 `#llm`：`.entry-nav` 2 项（GPU／生成式 AI）、`.entry-en` 1 个、紫小节标签 2 个、紫边类比块 1 个。
- 边界：`#ai`（首词）导航只有 1 项（图灵测试）。
- 截图目视（1280×1100）：奶油底 + 紫标签 + hero 卡 + 桌面分栏 + 底部导航 + 装饰层均正常。

**范围边界（2026-09-10 已裁决：一并清）**：`🔥 热门：`、`🚀 零基础看懂 AI（18 步）`、`🚀 第 N / 18 步`、`🎉 完成`、`⚠️ AI 常见误区`、误区条目 `❌`、弹窗 `📱 添加到桌面` / `💬 反馈 & 纠错` / `👇` / `🟢 到 GitHub Issues` / `✉️ 直接发邮件` —— **全部已去**。
**去 emoji 的统一规则**：导航/标题/按钮/弹窗等 **UI chrome 一律去 emoji**；词条正文内的分类标签 `📖/💡/📍/⚠️/🔀/🎯` 是 handover §5 明确的正文语言，**保留不动**。

---

## I. 执行记录（2026-09-10 第三批：E1–E5 + emoji 收尾）

- **E1–E5 token 收口** ✅ chip → `var(--card)`+`var(--line)`；搜索输入 → `var(--line)`+`var(--radius-btn)`+`var(--card)`；`.tree-head:hover` → 暖色 `rgba(42,39,34,.05)`；`.modal-overlay` → 暖黑 `rgba(42,39,34,.45)`；`.st` 10px→`var(--radius)`、`.hbtn` 8px→`var(--radius-btn)`。复扫：`style.css` 已无冷灰硬编码、无越档圆角（只剩 `50%` 圆形图标按钮 / `2px` 短线 / blob 有机圆角三类语义例外）。
- **emoji 收尾** ✅ 按上面「UI chrome 全去、正文标签保留」规则清掉 11 处。
- **顺手**：`.sp2` 星刺颜色由硬编码 `#9B4DCA` 改为 `var(--a3)`，让原本声明未用的装饰紫阶 token 有实义。

**验证**：`node --check` 通过；headless Chrome 实测——`#pits` 47 条误区、0 emoji、标题为「AI 常见误区」；`#learn/0` 进度为「第 1 / 18 步 · 总纲：AI 到底是什么」、按钮「下一步 →」、0 emoji；首页截图（1280×900）目视：chip 改暖白+暖描边、头部图标按钮圆角归一后仍协调、装饰层正常。

**仍未做**：`REDESIGN-HANDOVER.md` 的词数与「已落地」状态回写（权威笔记 `../.dsh-notes/design-audit-progress.md` 已更新）；三批改动**尚未 git commit**。

---

## J. 执行记录（2026-09-11：手机端验证 + 顶栏修复 + 视觉契约）

**验证方法纠错（重要教训）**：headless Chrome 的 `--window-size` **最小 500px**——设 `375` 会按 500px 布局渲染再裁到 375，造成"文字被切"的**假 bug**。窄屏必须用 **iframe 承载**（外层窗口 ≥500、iframe 设 375/320）来测量与截图。脚手架：`backups/tmp-harness/{_probe2,_shot}.html`（用时复制回 `web/`）。

**实测结果**（iframe 探针，非目测）：375 / 320 下 `docScrollWidth == clientWidth`（**零页面溢出**）；首页 / 词条页 / 误区（47 条）/ 学习模式四页渲染正常；`entry-nav` 两列在 320 也单行不折；顶栏三按钮单行。

**修复旧 bug**（`c612b20` 起就有、**线上同样存在**）：`@media(max-width:480px)` 里 `.site-header { padding: 12px 0 8px }` 把左右内边距清成 0 → 品牌贴左边缘、搜索贴右边缘，与下方 16px 边距的卡片明显不齐。修法：加回 16px 内边距 + 移动端品牌缩一档（图标 32px / 字 18px）+ 按钮间距 6px、CTA 12px（否则 320px 会挤爆）。复测：`brandLeft = 16`、搜索右缘距边 16px、仍零溢出。

**装饰层裁决落地**：`.deco` 由 `fixed` 改 **`absolute`**（随页面滚动）；同时撤掉 `body{overflow-x:hidden}`，改为 `.deco{overflow:hidden}` —— 不给真实溢出戴眼罩。

**颜色全部收进 `:root`**：新增 `--deco-blob / --fill-0 / --overlay / --on-main / --main-line`，7 处裸色值改走 token；复扫 `style.css` 已无裸色值（仅剩注释说明）。深色主题若做，只换这一层。

**视觉契约补齐**：新增 `DESIGN.md`（`design/19` 模板的 8 小节，含**来源分层**：品牌 override vs Semi 档位）与 `PRODUCT.md`；`README.md` 词数同步为 111 / 23 / 33。

**提交**：`6c7dc57`（代码）＋ `8b31b40`（文档），累计 4 笔。**仍未 push**；Cloudflare 那份是手动 zip，push 后需另行更新。


