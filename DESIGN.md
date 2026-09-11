---
purpose: ai-vocab 的视觉契约（快照）——16-anti-slop 的 "outside DESIGN.md" 判定以此为界
project: AI 词汇本（ai-vocab）
baseline: Semi Design（唯一权威；本文件只记录"本项目选了哪些档位"）
version: 2026-09-11（品牌改版 + 收尾四批落地后）
---

# AI 词汇本 Design System

> **来源分层**：本文件大部分值 = **Semi 档位投影**（映射清单见 `design/11-semi切换-ai-vocab映射与改动清单.md`，基准见 `design/12-双层设计基准.md`）；标 **品牌 override** 的一组值**非 Semi 默认**，但**成体系、可溯源**（本文件即为出处）。
> 真源码：`web/style.css`（`:root` 即本表的实现）。改视觉前先改本文件，保证契约与实现一致。

## 1. Principles（设计原则）

1. **信息优先**：这是查词工具，正文可读性 > 装饰性；因此定为**浅色**（查词阅读舒适），**背景不加装饰层**（2026-09-11 裁决：blob/星刺全部移除，只留奶油底）。
2. **克制用色**：紫色**只**出现在强调位——小节标签、链接/hover、品牌元素、主 CTA；不做主题色块、不做彩虹分类。
3. **一条字号阶梯**：从品牌 22 到 meta 12，所有文字都落在这条阶梯上，不临时取值。
4. **暖色体系**：底/卡/文字/描边全部带暖（`#F6F1E9` / `#2A2722`），**禁止冷灰**（旧 `rgba(46,50,56,…)`、`rgba(31,35,41,…)` 已清除）。

## 2. Colors（颜色）

| token | 值 | 用途 | 来源 |
|---|---|---|---|
| `--main` | `#5B4CE7` | 主色：强调、链接、CTA、小节标签 | 品牌 override |
| `--main-dark` | `#4A3BD0` | 主色 hover | 品牌 override |
| `--main-soft` | `#ECE8FB` | 紫浅底：pill / tag / hover 底 | 品牌 override |
| `--main-text-soft` | `#5B4CE7` | 浅底上的文字 | 品牌 override |
| `--main-line` | `rgba(91,76,231,.28)` | 主色浅描边（类比块） | 品牌 override |
| `--bg` | `#F6F1E9` | 页面奶油底 | 品牌 override |
| `--card` | `#FCFBF8` | 暖白卡片 / 顶栏 / chip | 品牌 override |
| `--surface-alt` | `#F6F1E9` | 次级面（类比块、hero 内小卡） | 品牌 override |
| `--text` | `#2A2722` | 正文本（暖黑） | 品牌 override |
| `--muted` | `rgba(42,39,34,.62)` | 次要文本 | 品牌 override |
| `--text-3` | `rgba(42,39,34,.38)` | 第三文本（计数/meta） | 品牌 override |
| `--line` | `rgba(42,39,34,.10)` | 描边（whisper border） | 品牌 override |
| `--fill-0` | `rgba(42,39,34,.05)` | 最轻 hover 填充 | 品牌 override |
| `--overlay` | `rgba(42,39,34,.45)` | 弹窗遮罩 | 品牌 override |
| `--on-main` | `#ffffff` | 紫底上的文字 | 品牌 override |

> 规则：新增颜色一律先加 token 再引用；深色主题若做，只替换本表值（结构已按此分层）。

## 3. Typography（字体/字号）

| token / 元素 | 值 | 用途 |
|---|---|---|
| `font-family` | `-apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Segoe UI", Roboto, sans-serif`（系统无衬线栈，**未引入 Inter**） | 全局 |
| 品牌 `AI 词汇本` | 22 / 800（`AI` 紫） | 左上角 |
| hero 标题 | 20 / 800 | 「从这 3 个词开始」 |
| 章节标题 `.sec-h` | 16 / 700 | 「六大主题纵览」 |
| 主题名 `.tree-name` | 15 / 700 | 折叠层头 |
| 词条 capsule `.chip` | 14 | 目录胶囊 |
| 词条页标题 `.entry-title` | 28 / 800（移动端 ≤480：22） | 词条名 |
| 词条页英文 `.entry-en` | 16 / 500（`--muted`） | 词条名同行英文 |
| 正文 `.block-body` | 16 / 1.6 | 词条「是什么」 |
| 类比正文 `.analogy .block-body` | 14 / 1.7 | 通俗类比 |
| 小节标签 `.block-title` / `.tree-sub-title` | 13 / 700（紫，词条页带 16×2px 短线） | 小节名 |
| meta / 页脚 / 计数 | 12（词条页 meta 12.5） | 元信息 |

## 4. Spacing & Layout（间距/布局）

| token | 值 |
|---|---|
| `--space-1…5` | 4 / 8 / 16 / 24 / 32 |
| `.container` | `max-width: 760px`，左右 16px |
| 分栏（≥840px） | 容器 1180px；目录侧栏 `flex: 0 0 340px`，词条占剩余；目录 `sticky top:76px` |
| 断点 | **480px**（手机：顶栏/卡片/字号一档）/ **640px**（hero 三步折一列）/ **840px**（移动单栏 ↔ 桌面分栏） |
| 安全区 | `env(safe-area-inset-top/bottom)` 用于顶栏与页脚、弹窗底部 |

## 5. Border Radius & Shadows（圆角/阴影）

| token | 值 | 用途 |
|---|---|---|
| `--radius` / `--radius-lg` | 12px | 卡片、面板、弹层、导航块 |
| `--radius-btn` | 3px | 按钮、输入框 |
| 胶囊 | 9999px | chip / tag / 主 CTA / 相关词 |
| `--shadow` | `0 0 1px rgba(42,39,34,.22), 0 8px 24px rgba(42,39,34,.08)` | 卡片 |
| `--shadow-modal` | `… , 0 8px 24px rgba(42,39,34,.12)` | 弹窗 |

> **仅两类例外**（其余越档值视为违规）：圆形图标按钮 `border-radius:50%`（关闭/清除）、`2px` 细线（分隔/竖条）。

## 6. Motion（动效）

| token | 值 | 用途 |
|---|---|---|
| `--ease-out` | `cubic-bezier(0.23, 1, 0.32, 1)` | 进入/hover/按压反馈 |
| `--ease-in-out` | `cubic-bezier(0.77, 0, 0.175, 1)` | 分栏收放（220ms） |
| `--ease-drawer` | `cubic-bezier(0.32, 0.72, 0, 1)` | 抽屉类（预留） |

- 按压反馈：可点元素 `:active { transform: scale(.95~.97) }`，120ms。
- 分栏：点词条目录左收（760→340）、词条右滑入 220ms；关闭反向 180ms（退场用 `--ease-out`）。
- `@media (prefers-reduced-motion: reduce)`：全部过渡置 `none`（功能不受影响）。

## 7. Components（组件规范）

| 组件 | 规范要点 |
|---|---|
| 顶栏 `.site-header` | sticky；`--card` 底 + 下描边；左=图标 39px + 品牌文字；右=搜索/新手教程（紫实心 pill）/误区；无 home 键；移动端 ≤480 内边距 16px、图标 32px、品牌 18px |
| hero `.hero` | `--card`；`details` 可折叠，右侧「收起/展开」pill；三张 `.st`（`--bg` 底、12px 圆角）窄屏折一列 |
| 主题卡 `.tree-layer` | `--card` + 12px + shadow；层头可折叠（`--fill-0` hover）；**不设主题色块**；小节标签紫 13/700 |
| 词条胶囊 `.chip` | `--card` 底 + `--line` 描边 + 9999；hover 转主色；`.adv` 用浅灰「进阶」小字（**非**紫色） |
| 词条卡 `.entry-card` | `--card`；标题 28/800 + 同行英文；meta 12.5；分类 pill + 更新日期 |
| 类比块 `.analogy` | `--surface-alt` 底 + `--main-line` 描边 + **左 3px 主色竖条** + 14/1.7 |
| 相关词 `.related-chip` | `--main-soft` 底 + 主色字；hover 反白 |
| 上下词导航 `.entry-nav/.np` | 两块等宽卡片（12px 圆角），首/末词只显示存在的一侧 |
| 试试看 `.entry-practice` | 无底色 + `--line` 细边 + 左 4px 主色竖条 |
| 弹窗 `.modal-*` | `--overlay` 遮罩 + `--card` 盒 + 12px；主/次/幽灵三级按钮 |
| 页脚 `.site-footer` | 12px；含「添加到桌面」「反馈 & 纠错」入口；文案无 emoji |

## 8. Accessibility（无障碍）

- **对比度**：正文 `#2A2722` on `#FCFBF8` ≈ 14:1；紫 `#5B4CE7` on 奶油底 ≈ 5.2:1（正文级）、紫底白字 ≈ 5.2:1（均过 AA）。
- **触控目标**：小图标按钮用透明伪元素扩热区至 ~48px（`.search-close::before`、`.entry-close::before`）；列表项加 padding。
- **键盘**：搜索框 focus 有可见环（`0 0 0 2px var(--main-soft)`）；输入框可 Tab 进入；`aria-label` 已用于图标按钮与品牌链接。
- **动效**：尊重 `prefers-reduced-motion`；无自动播放/闪烁。
- **窄屏**：已在 320 / 375 / 1280 实测零横向溢出（iframe 探针，见 `LANDING-AUDIT.md`）。

---

> **判定链**：Semi 提供可用档位 → 本文件记录"本项目选了哪些" → `design/16-anti-slop` 的 "outside DESIGN.md" 检测以本文件为界；用到本文件之外的值 = 要么映射回档位，要么先改本文件（改前需用户确认）。
