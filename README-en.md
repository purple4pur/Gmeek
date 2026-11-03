**[简体中文](README.md)** | **English** | **[Русский](README-ru.md)**
# Gmeek

Gmeek is a static blog generator and a lightweight personal blog template. It uses `GitHub Pages`, `GitHub Issues`, and `GitHub Actions`. You do not need a local server. Create a repository, then write in an Issue.

This repository is a fork of [Meekdai/Gmeek](https://github.com/Meekdai/Gmeek). It uses uv for dependencies, caches unchanged posts by Issue update time, and uses relative links.

- [Demo](http://meekdai.github.io/)
- [Update log](https://meekdai.github.io/post/Gmeek-geng-xin-ri-zhi.html)
- [Get started](https://blog.meekdai.com/post/Gmeek-kuai-su-shang-shou.html)

![dark](img/dark.jpg)

## How it works

Each Issue with a label becomes a post. Gmeek reads the Issues and labels, renders Markdown to HTML, and writes the result to `docs/`. Templates generate the home page, pagination, tag page, RSS feed, and site map.

- GitHub Actions builds and publishes the site when an Issue opens or changes.
- Posts with an unchanged update time skip rendering.
- Relative links work on `XXX.github.io` and on `XXX.github.io/repo`.
- Comments use [utteranc.es](https://utteranc.es/) and load after a click.
- Only the repository owner can set post-level options.

## Installation

1. Create a repository from the [Gmeek template](https://github.com/new?template_name=Gmeek-template&template_owner=Meekdai). Use `XXX.github.io` as the name, where `XXX` is your GitHub user name.

2. In `Settings`, open `Pages->Build and deployment->Source` and select `GitHub Actions`.

3. Open an Issue and write. Add at least one label. Save the Issue. Gmeek builds the post, and you can open it at `https://XXX.github.io` after a moment.

4. To rebuild every page, run `Actions->build Gmeek->Run workflow`. Do this after you change `config.json` or after an error.

## Configuration

Put `config.json` in the blog repository root. The minimum is:

```json
{
  "title": "My Blog",
  "subTitle": "Notes on code and life",
  "avatarUrl": "https://example.com/avatar.jpg"
}
```

Gmeek derives `homeUrl`, `displayTitle`, `faviconUrl`, and `ogImage` when they are absent. See [CONFIG.md](CONFIG.md) for every field, its default, and post-level options. CONFIG.md is in Chinese.

## Local build

You need [uv](https://docs.astral.sh/uv/) and Python 3.14+. `uv.lock` records the dependency versions.

```bash
uv sync
uv run python Gmeek.py <github_token> <owner/repo>
uv run pytest
```

`Gmeek.py` reads `config.json` and `templates/` from the current directory. It writes `docs/`, `backup/`, and `blogBase.json`. When the build changes, it also rewrites `README.md` in the current directory. Run it in a separate build directory to keep this README.

## Repository layout

| Path | Content |
|---|---|
| `Gmeek.py` | Generator entry point. It reads Issues, renders pages, and writes `docs/`. |
| `templates/` | Jinja2 templates for the layout, home page, post, tag page, and footer. |
| `plugins/` | Optional browser plugins for a table of contents, a lightbox, and view counts. |
| `tests/` | pytest unit tests. |
| `pyproject.toml` | Project metadata and uv dependencies. |
| `uv.lock` | Locked dependency versions. |
| `CONFIG.md` | Configuration reference. |
| `img/` | README images. |

Gmeek does not load `plugins/` automatically. Copy a plugin into the blog repository `static/` directory, or load it from the `script` or `style` field in `config.json`.

## Features

- The UI uses GitHub's own CSS: [primer.style](https://primer.style/css)
- Writing in Issues triggers the build and deploy workflow
- Home pagination, tag filter, and site search
- RSS feed, `sitemap.txt`, and the `postList.json` index
- MathJax formulas, GitHub alert styles, code highlighting, and a copy button
- Comments through [utteranc.es](https://utteranc.es/)
- HTML rendered with `jinja2`; you can change the theme in the templates
- Interface in Chinese, English, and Russian

## Tests

Run `uv run pytest`. The tests cover post option parsing, summary extraction, file name cleanup, text contrast, and post template rendering.

## Issues

Before you open an [Issue](https://github.com/Meekdai/Gmeek/issues), run a full rebuild. If the error remains, open an Issue and include the build log.

## Thanks

- [jinja2](https://jinja.palletsprojects.com/)
- [utteranc.es](https://utteranc.es/)
- [primer.style](https://primer.style/css)
- [gitblog](https://github.com/yihong0618/gitblog)

## License

Keep the copyright notice in the page footer and the browser console.
