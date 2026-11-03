# Gmeek 配置参考

`config.json` 放在博客仓库根目录。Gmeek 读取它，并合并到内置默认值。修改配置后，执行一次手动全局生成，或等待下一次 Issue 事件。

## 最小配置

```json
{
  "title": "我的博客",
  "subTitle": "记录技术与生活",
  "avatarUrl": "https://example.com/avatar.jpg"
}
```

`homeUrl`、`displayTitle`、`faviconUrl`、`ogImage` 可以省略，Gmeek 会推导默认值。

## 站点字段

| 字段 | 默认值 | 说明 |
|---|---|---|
| `title` | 必填 | 站点标题，用于页脚、RSS 和浏览器标题。 |
| `displayTitle` | `title` | 首页头部显示的文字。 |
| `subTitle` | 必填 | 首页副标题，也是 RSS 描述。 |
| `avatarUrl` | 必填 | 头像地址，也是 RSS 图片。 |
| `homeUrl` | 自动 | 站点根地址。仓库名为 `<owner>.github.io` 时为 `https://<repo>`，否则为 `https://<owner>.github.io/<repo>`。 |
| `faviconUrl` | `avatarUrl` | 站点图标。 |
| `ogImage` | `avatarUrl` | 默认社交预览图。 |
| `primerCSS` | Primer 21.0.7 CDN | 页面样式表。 |
| `UTC` | `8` | 构建时间和文章日期的时区偏移，单位为小时。 |

## 页面与导航

| 字段 | 默认值 | 说明 |
|---|---|---|
| `singlePage` | `[]` | 独立页面的标签列表。第一个标签在列表中的 Issue 不进入首页，而是生成 `<标签名>.html`，并作为首页图标链接。 |
| `onePageListNum` | `25` | 首页每页文章数。必须是大于 0 的整数。 |
| `i18n` | `CN` | 界面语言：`CN`、`RU`，其他值使用英文。 |
| `themeMode` | `manual` | `manual` 显示主题切换按钮，并用 `localStorage` 记住选择；`fix` 使用固定主题并隐藏按钮。 |
| `dayTheme` | `light` | Primer 亮色主题名。 |
| `nightTheme` | `dark` | Primer 暗色主题名。 |
| `startSite` | `""` | 页脚运行天数的起点日期，例如 `02/16/2015`。空字符串隐藏天数。 |
| `filingNum` | `""` | 页脚备案号。空字符串隐藏备案信息。 |
| `exlink` | `{}` | 首页右上角额外链接。键为名称，值为 URL。 |
| `iconList` | `{}` | 自定义 SVG 图标。键为名称，值为 `path` 的 `d` 属性。 |

`exlink` 的每个键都需要在 `iconList` 中有同名图标，否则链接没有可见图形：

```json
{
  "exlink": {"github": "https://github.com/your-name"},
  "iconList": {"github": "M8 0c4.42 0 8 3.58 8 8a8.013 ..."}
}
```

## 文章与内容

| 字段 | 默认值 | 说明 |
|---|---|---|
| `urlMode` | `pinyin` | 文章文件名规则。`pinyin` 使用标题拼音，`issue` 使用 Issue 编号，`ru_translit` 使用俄文转写。文件名末尾总会带上 Issue 编号。 |
| `needComment` | `1` | `1` 显示评论按钮，点击后加载 utteranc.es；`0` 关闭评论。 |
| `showPostSource` | `1` | `1` 在文章页显示 Issue 源码链接；`0` 隐藏。 |
| `commentLabelColor` | `#006b75` | 评论数标签的背景色。文字颜色自动取黑或白。 |
| `yearColorList` | `["#bc4c00", "#0969da", "#1f883d", "#A333D0"]` | 文章日期标签的背景色，按年份对列表长度取模。 |
| `rssSplit` | `sentence` | RSS 摘要规则。`sentence` 截取第一句；其他值作为分隔符字符串。中文句子用 `。`，其他语言用 `.`。 |
| `bottomText` | `""` | 文章底部文字，允许 HTML。独立页面不显示。 |
| `script` | `""` | 追加到文章页底部的 HTML，允许 `<script>`。 |
| `style` | `""` | 追加到文章页样式区的 HTML，允许 `<style>`。 |
| `head` | `""` | 追加到文章页 `<head>` 的 HTML。 |
| `indexScript` | `""` | 追加到首页分页底部的 HTML。 |
| `indexStyle` | `""` | 追加到首页分页样式区的 HTML。 |
| `allHead` | `""` | 追加到每个页面 `<head>` 的 HTML。 |

## 文章级参数

Issue 作者是仓库所有者时，可以在正文中加一行 JSON，覆盖当前文章的部分设置：

```markdown
正文内容

##{"timestamp": 1759593599, "ogImage": "https://example.com/cover.png"}##
```

也可以包在 HTML 注释中，渲染时不会显示：

```markdown
<!-- ##{"style": "<style>blockquote{color:teal}</style>"}## -->
```

| 键 | 类型 | 说明 |
|---|---|---|
| `timestamp` | 整数 | Unix 时间戳，覆盖 Issue 创建时间。它决定文章排序和显示的日期。 |
| `style` | 字符串 | 追加到这篇文章的样式。 |
| `script` | 字符串 | 追加到这篇文章的脚本。 |
| `head` | 字符串 | 追加到这篇文章的 `<head>`。 |
| `ogImage` | 字符串 | 覆盖这篇文章的社交预览图。 |

Gmeek 从正文末尾向上查找标记，使用最后一个标记。JSON 无效时打印错误并忽略该标记。非仓库所有者的文章不能使用文章级参数。

## 构建产物

| 路径 | 内容 |
|---|---|
| `docs/index.html`、`docs/pageN.html` | 首页和分页。 |
| `docs/tag.html` | 标签筛选和站内搜索页。 |
| `docs/post/<slug>.html` | 普通文章。 |
| `docs/<标签名>.html` | 独立页面。 |
| `docs/rss.xml` | RSS 订阅源。 |
| `docs/sitemap.txt` | 纯文本站点地图。 |
| `docs/postList.json` | 标签页使用的文章索引。 |
| `backup/<编号>-<标题>.md` | Issue 正文备份。 |
| `blogBase.json` | 上一次构建的条目缓存和模板哈希。保留它可以跳过未变化文章的重渲染。 |
| `static/` | 存在时，整个目录复制到 `docs/`。 |

构建有变化时，Gmeek 还会改写当前目录的 `README.md`，写入文章数、评论数、字数和构建时间。GitHub Actions 的 `schedule` 事件不会改写它。
