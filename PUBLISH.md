# 发布指南：把词汇本分享给朋友

成品是 `web/` 目录下的 4 个文件：`index.html`、`style.css`、`script.js`、`words.json`。
发布 = 把这 4 个文件上传到免费托管平台，拿到一个公开链接，发给朋友即可。

## 方式一（最推荐，零代码）：Netlify Drop

1. 打开 https://app.netlify.com/drop （无需安装任何软件）
2. 把 `web/` 文件夹**直接拖进**浏览器页面
3. 几秒后自动部署完成，得到一个链接，形如 `https://随机名.netlify.app`
4. 把这个链接发给朋友（微信/QQ 直接发，手机电脑都能打开）

> 优点：拖拽即用，最简单。缺点：国内访问偶尔偏慢。
> 未登录时部署的链接是临时的；注册免费账号（可用邮箱）后链接长期有效，还能重复更新。

## 方式二（国内访问更稳）：Cloudflare Pages

1. 打开 https://dash.cloudflare.com 注册免费账号
2. 左侧菜单选 **Workers 和 Pages** → **创建** → **Pages** → **上传资产**
3. 项目名随便填（如 `ai-vocab`），把 `web/` 里的 4 个文件拖进去 → 部署
4. 得到链接 `https://ai-vocab.pages.dev`，发给朋友

> 国内访问速度通常优于 Netlify，适合朋友都在国内的情况。

## 方式三（会一点代码）：GitHub Pages

1. 在 GitHub 新建仓库（如 `ai-vocab`），把 `web/` 4 个文件推上去
2. 仓库 Settings → Pages → Source 选 `main` 分支
3. 得到链接 `https://你的用户名.github.io/ai-vocab/`

> 好处：以后更新直接 `git push`，全自动发布。

## 后续更新步骤（每次加词/改内容）

1. 改词条：编辑 `drafts/*.md`，然后运行 `python3 tools/build_words.py` 重新生成 `web/words.json`
   （嫌麻烦也可以直接编辑 `web/words.json`，格式照抄已有词条）
2. 重新上传 `web/` 里的 4 个文件：
   - Netlify：重新拖拽到 app.netlify.com/drop（或登录后在 Sites 里拖）
   - Cloudflare Pages：重新上传资产
   - GitHub：`git push`
3. 朋友刷新页面即看到最新内容（可能有几分钟缓存延迟）

## 小提醒

- 链接是公开的：拿到链接的人都能访问（只能看，不能改）
- 想改页面外观（颜色、字体）：编辑 `web/style.css` 顶部的 `:root` 变量，重新上传即可
