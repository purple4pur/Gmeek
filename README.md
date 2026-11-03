**简体中文** | **[English](README-en.md)** | **[Русский](README-ru.md)**
# Gmeek

Gmeek 是一个博客生成器，也是一个超轻量级的个人博客模板。它基于 `Github Pages`、`Github Issues` 和 `Github Actions`。你不需要本地部署，创建仓库后即可在 Issue 中写作。

本仓库是 [Meekdai/Gmeek](https://github.com/Meekdai/Gmeek) 的 fork。当前版本使用 uv 管理依赖，按 Issue 更新时间缓存构建结果，并使用相对链接。

- [Demo 页面](http://meekdai.github.io/)
- [Gmeek更新日志](https://meekdai.github.io/post/Gmeek-geng-xin-ri-zhi.html)
- [Gmeek快速上手](https://blog.meekdai.com/post/Gmeek-kuai-su-shang-shou.html)

![light](img/light.jpg)

## 工作方式

每个带标签的 Issue 是一篇文章。Gmeek 读取仓库的 Issue 和标签，把 Markdown 渲染成 HTML，并写入 `docs/`。首页、分页、标签页、RSS 和站点地图由模板生成。

- Issue 打开或编辑时，GitHub Actions 触发构建和发布。
- Issue 更新时间未变化的文章会跳过重新渲染。
- 页面链接使用相对路径，可部署在 `XXX.github.io` 或 `XXX.github.io/repo`。
- 评论使用 [utteranc.es](https://utteranc.es/)，点击按钮后才加载。
- 只有仓库所有者的文章可以使用文章级参数。

## 安装

1. 【创建仓库】点击[通过模板创建仓库](https://github.com/new?template_name=Gmeek-template&template_owner=Meekdai)，建议仓库名称为`XXX.github.io`，其中`XXX`为你的github用户名。

2. 【启用 Pages】在仓库的`Settings`中`Pages->Build and deployment->Source`下面选择`Github Actions`。

3. 【开始写作】打开一篇 issue，开始写作，并且**必须**添加一个`标签Label`（至少添加一个），再保存issue后会自动创建博客内容，片刻后可通过https://XXX.github.io 访问（可进入 Actions 页面查看构建进度）。

4. 【手动全局生成】修改`config.json`文件或者出现异常时，通过`Actions->build Gmeek->Run workflow`全局重新生成一次。

## 配置

`config.json` 放在博客仓库根目录。最小配置如下：

```json
{
  "title": "我的博客",
  "subTitle": "记录技术与生活",
  "avatarUrl": "https://example.com/avatar.jpg"
}
```

`homeUrl`、`displayTitle`、`faviconUrl` 和 `ogImage` 可以省略，Gmeek 会推导默认值。全部字段、默认值和文章级参数见 [CONFIG.md](CONFIG.md)。

## 本地构建

需要 [uv](https://docs.astral.sh/uv/) 和 Python 3.14+。依赖版本记录在`uv.lock`。

```bash
uv sync
uv run python Gmeek.py <github_token> <owner/repo>
uv run pytest
```

`Gmeek.py` 从当前目录读取 `config.json` 和 `templates/`，并写入 `docs/`、`backup/` 和 `blogBase.json`。构建有变化时还会改写当前目录的 `README.md`。请在单独的构建目录中运行，避免覆盖本仓库的 README。

## 仓库结构

| 路径 | 内容 |
|---|---|
| `Gmeek.py` | 生成器入口：读取 Issue，渲染页面，写入 `docs/`。 |
| `templates/` | Jinja2 模板：基础布局、首页、文章、标签页和页脚。 |
| `plugins/` | 可选浏览器插件：目录、灯箱、浏览量统计。 |
| `tests/` | pytest 单元测试。 |
| `pyproject.toml` | 项目元数据和 uv 依赖声明。 |
| `uv.lock` | 锁定后的依赖版本。 |
| `CONFIG.md` | 配置字段参考。 |
| `img/` | README 截图。 |

`plugins/` 不会自动加载。把需要的文件放进博客仓库的 `static/`，或在 `config.json` 的 `script`、`style` 字段中引用。

## 特性

- UI 界面和 Github 同源，只引入了 Github 原生 CSS：[primer.style](https://primer.style/css)
- 博客写作在 Issues 中完成后，自动触发 Actions 执行部署任务
- 首页分页、标签筛选和站内搜索
- RSS、`sitemap.txt` 和文章索引 `postList.json`
- 支持 MathJax 公式、GitHub alert 样式、代码高亮和复制按钮
- 评论系统引入[utteranc.es](https://utteranc.es/)
- 使用`jinja2`对 html 进行渲染，可通过模板自定义 UI 主题
- 界面支持中文、英文和俄文

## 测试

`uv run pytest` 运行单元测试。测试覆盖文章级参数解析、摘要提取、文件名清洗、文字对比色和文章模板渲染。

## 提交问题

1. 如果有问题可参考[Gmeek快速上手](https://blog.meekdai.com/post/Gmeek-kuai-su-shang-shou.html)
2. 在本仓库提交[Issues](https://github.com/Meekdai/Gmeek/issues)之前，请手动全局生成一次。如果还有错误，提交`Issues`后，我会帮忙查看构建流程，定位问题出处。

## 赞赏

如果本项目对你有帮助，可以用微信赞赏一下作者，让项目有继续更新维护下去的动力，谢谢！

![赞赏码](img/赞赏码.jpg)

## 鸣谢
- [jinja2](https://jinja.palletsprojects.com/)
- [utteranc.es](https://utteranc.es/)
- [primer.style](https://primer.style/css)
- [gitblog](https://github.com/yihong0618/gitblog)

## License

请保留页面底部和console界面版权信息，谢谢！
