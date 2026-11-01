import sys
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Gmeek import parsePostConfig, postDescription, safeFileName, textColor


def test_parse_post_config_accepts_lf_marker_on_first_line():
    body = '<!-- ##{"timestamp":1759593599}## -->\r\n\nPost body'
    assert parsePostConfig(body) == {"timestamp": 1759593599}


def test_parse_post_config_accepts_crlf_marker_on_last_line():
    body = "Post body\r\n\r\n##{\"style\":\"<b>x</b>\"}##"
    assert parsePostConfig(body) == {"style": "<b>x</b>"}


def test_parse_post_config_ignores_invalid_json(capsys):
    assert parsePostConfig("Text\n##{oops}##") == {}
    assert "Invalid post config JSON" in capsys.readouterr().out


def test_post_description_strips_marker_and_navigation():
    body = (
        '<!-- ##{"timestamp":1}## -->\n'
        "[<< Day1](/post/38.html) | [Day3 >>](/post/40.html)\n\n"
        "> 本篇由蓝蓝记录\n\n"
        "川西自驾正式开始第一天。后面还有。"
    )
    assert postDescription(body, "。") == "本篇由蓝蓝记录 川西自驾正式开始第一天。"


def test_post_description_splits_at_configured_separator():
    assert postDescription("First part. Second part.", ".") == "First part."


def test_post_description_drops_code_blocks():
    body = "## vcs\n\n```bash\n-full64 +v2k\n```\n\nRest of text。Tail。"
    assert postDescription(body, "。") == "vcs Rest of text。"


def test_safe_file_name_replaces_reserved_characters():
    assert safeFileName('a/b:c*?"<>|') == "a-b-c------"


@pytest.mark.parametrize(
    "background, expected",
    [("#FBCA04", "#1f2328"), ("#006b75", "#fff"), ("#0969da", "#fff")],
)
def test_text_color_picks_readable_ink(background, expected):
    assert textColor(background) == expected


def test_post_template_reads_single_page_metadata():
    base = {
        "title": "Blog",
        "subTitle": "",
        "homeUrl": "https://example.com",
        "avatarUrl": "",
        "nightTheme": "dark",
        "dayTheme": "light",
        "i18n": "CN",
        "primerCSS": "",
        "allHead": "",
        "faviconUrl": "",
        "themeMode": "manual",
        "GMEEK_VERSION": "last",
        "displayTitle": "Blog",
        "exlink": {},
        "singeListJson": {
            "P2": {
                "labels": ["About"],
                "postTitle": "About <b>",
                "postUrl": "/About.html",
                "dateLabelColor": "#0969da",
                "dateLabelTextColor": "#fff",
                "createdDate": "2026-01-02",
                "commentNum": 0,
            }
        },
        "indexScript": "",
        "startSite": "",
        "filingNum": "",
        "sourceCodeUrl": "",
        "build_time": "2026-01-02T00:00:00+08:00",
        "postUrl": "/About.html",
        "postTitle": "About <b>",
        "description": 'desc "quoted"',
        "ogImage": "",
        "postBody": "<p>Body</p>",
        "commentNum": 0,
        "needComment": 0,
        "highlight": 0,
        "postNum": "P2",
        "bottomText": "",
        "script": "",
        "style": "",
        "head": "",
        "showPostSource": 1,
        "postSourceUrl": "",
        "repoName": "owner/repo",
        "labelColorDict": {"About": "#0969da"},
        "labelTextColorDict": {"About": "#fff"},
        "postListJson": {},
    }
    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html"]))
    html = env.get_template("post.html").render(
        blogBase=base,
        postListJson={},
        i18n={
            "Search": "Search",
            "switchTheme": "switch theme",
            "home": "home",
            "comments": "comments",
            "run": "run ",
            "days": " days",
            "Previous": "Previous",
            "Next": "Next",
        },
        IconList={},
    )
    assert "2026-01-02" in html
    assert "About &lt;b&gt;" in html
    assert "<b>" not in html
    assert "<p>Body</p>" in html
