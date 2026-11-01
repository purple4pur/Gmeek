# -*- coding: utf-8 -*-
import os
import re
import json
import time
import datetime
import shutil
import hashlib
import urllib
import requests
import argparse
import html
from github import Github
from xpinyin import Pinyin
from feedgen.feed import FeedGenerator
from jinja2 import Environment, FileSystemLoader, select_autoescape
from transliterate import translit
from collections import OrderedDict
######################################################################################
i18n={"Search":"Search","switchTheme":"switch theme","home":"home","comments":"comments","run":"run ","days":" days","Previous":"Previous","Next":"Next"}
i18nCN={"Search":"搜索","switchTheme":"切换主题","home":"首页","comments":"评论","run":"本站存活 ","days":" 天","Previous":"上一页","Next":"下一页"}
i18nRU={"Search":"Поиск","switchTheme": "Сменить тему","home":"Главная","comments":"Комментарии","run":"работает ","days":" дней","Previous":"Предыдущая","Next":"Следующая"}
IconBase={
    "post":"M0 3.75C0 2.784.784 2 1.75 2h12.5c.966 0 1.75.784 1.75 1.75v8.5A1.75 1.75 0 0 1 14.25 14H1.75A1.75 1.75 0 0 1 0 12.25Zm1.75-.25a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-8.5a.25.25 0 0 0-.25-.25ZM3.5 6.25a.75.75 0 0 1 .75-.75h7a.75.75 0 0 1 0 1.5h-7a.75.75 0 0 1-.75-.75Zm.75 2.25h4a.75.75 0 0 1 0 1.5h-4a.75.75 0 0 1 0-1.5Z",
    "link":"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z",
    "about":"M10.561 8.073a6.005 6.005 0 0 1 3.432 5.142.75.75 0 1 1-1.498.07 4.5 4.5 0 0 0-8.99 0 .75.75 0 0 1-1.498-.07 6.004 6.004 0 0 1 3.431-5.142 3.999 3.999 0 1 1 5.123 0ZM10.5 5a2.5 2.5 0 1 0-5 0 2.5 2.5 0 0 0 5 0Z",
    "sun":"M8 10.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5zM8 12a4 4 0 100-8 4 4 0 000 8zM8 0a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0V.75A.75.75 0 018 0zm0 13a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0v-1.5A.75.75 0 018 13zM2.343 2.343a.75.75 0 011.061 0l1.06 1.061a.75.75 0 01-1.06 1.06l-1.06-1.06a.75.75 0 010-1.06zm9.193 9.193a.75.75 0 011.06 0l1.061 1.06a.75.75 0 01-1.06 1.061l-1.061-1.06a.75.75 0 010-1.061zM16 8a.75.75 0 01-.75.75h-1.5a.75.75 0 010-1.5h1.5A.75.75 0 0116 8zM3 8a.75.75 0 01-.75.75H.75a.75.75 0 010-1.5h1.5A.75.75 0 013 8zm10.657-5.657a.75.75 0 010 1.061l-1.061 1.06a.75.75 0 11-1.06-1.06l1.06-1.06a.75.75 0 011.06 0zm-9.193 9.193a.75.75 0 010 1.06l-1.06 1.061a.75.75 0 11-1.061-1.06l1.06-1.061a.75.75 0 011.061 0z",
    "moon":"M9.598 1.591a.75.75 0 01.785-.175 7 7 0 11-8.967 8.967.75.75 0 01.961-.96 5.5 5.5 0 007.046-7.046.75.75 0 01.175-.786zm1.616 1.945a7 7 0 01-7.678 7.678 5.5 5.5 0 107.678-7.678z",
    "search":"M15.7 13.3l-3.81-3.83A5.93 5.93 0 0 0 13 6c0-3.31-2.69-6-6-6S1 2.69 1 6s2.69 6 6 6c1.3 0 2.48-.41 3.47-1.11l3.83 3.81c.19.2.45.3.7.3.25 0 .52-.09.7-.3a.996.996 0 0 0 0-1.41v.01zM7 10.7c-2.59 0-4.7-2.11-4.7-4.7 0-2.59 2.11-4.7 4.7-4.7 2.59 0 4.7 2.11 4.7 4.7 0 2.59-2.11 4.7-4.7 4.7z",
    "rss":"M2.002 2.725a.75.75 0 0 1 .797-.699C8.79 2.42 13.58 7.21 13.974 13.201a.75.75 0 0 1-1.497.098 10.502 10.502 0 0 0-9.776-9.776.747.747 0 0 1-.7-.798ZM2.84 7.05h-.002a7.002 7.002 0 0 1 6.113 6.111.75.75 0 0 1-1.49.178 5.503 5.503 0 0 0-4.8-4.8.75.75 0 0 1 .179-1.489ZM2 13a1 1 0 1 1 2 0 1 1 0 0 1-2 0Z",
    "upload":"M2.75 14A1.75 1.75 0 0 1 1 12.25v-2.5a.75.75 0 0 1 1.5 0v2.5c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25v-2.5a.75.75 0 0 1 1.5 0v2.5A1.75 1.75 0 0 1 13.25 14Z M11.78 4.72a.749.749 0 1 1-1.06 1.06L8.75 3.811V9.5a.75.75 0 0 1-1.5 0V3.811L5.28 5.78a.749.749 0 1 1-1.06-1.06l3.25-3.25a.749.749 0 0 1 1.06 0l3.25 3.25Z",
    "github":"M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z",
    "home":"M6.906.664a1.749 1.749 0 0 1 2.187 0l5.25 4.2c.415.332.657.835.657 1.367v7.019A1.75 1.75 0 0 1 13.25 15h-3.5a.75.75 0 0 1-.75-.75V9H7v5.25a.75.75 0 0 1-.75.75h-3.5A1.75 1.75 0 0 1 1 13.25V6.23c0-.531.242-1.034.657-1.366l5.25-4.2Zm1.25 1.171a.25.25 0 0 0-.312 0l-5.25 4.2a.25.25 0 0 0-.094.196v7.019c0 .138.112.25.25.25H5.5V8.25a.75.75 0 0 1 .75-.75h3.5a.75.75 0 0 1 .75.75v5.25h2.75a.25.25 0 0 0 .25-.25V6.23a.25.25 0 0 0-.094-.195Z",
    "sync":"M1.705 8.005a.75.75 0 0 1 .834.656 5.5 5.5 0 0 0 9.592 2.97l-1.204-1.204a.25.25 0 0 1 .177-.427h3.646a.25.25 0 0 1 .25.25v3.646a.25.25 0 0 1-.427.177l-1.38-1.38A7.002 7.002 0 0 1 1.05 8.84a.75.75 0 0 1 .656-.834ZM8 2.5a5.487 5.487 0 0 0-4.131 1.869l1.204 1.204A.25.25 0 0 1 4.896 6H1.25A.25.25 0 0 1 1 5.75V2.104a.25.25 0 0 1 .427-.177l1.38 1.38A7.002 7.002 0 0 1 14.95 7.16a.75.75 0 0 1-1.49.178A5.5 5.5 0 0 0 8 2.5Z",
    "copy":"M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z",
    "check":"M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"
}
######################################################################################
def safeFileName(name):
    return re.sub(r'[<>:/\\|?*"]|[\0-\31]', '-', name)

def textColor(hexColor):
    """Return black or white, whichever has the higher contrast on hexColor."""
    try:
        channels=[int(hexColor[i:i+2], 16)/255 for i in (1, 3, 5)]
    except (ValueError, IndexError):
        return '#fff'
    linear=[c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4 for c in channels]
    luminance=0.2126*linear[0]+0.7152*linear[1]+0.0722*linear[2]
    return '#fff' if 1.05/(luminance+0.05) >= (luminance+0.05)/0.05 else '#1f2328'

def parsePostConfig(body):
    for line in reversed((body or "").splitlines()):
        match=re.search(r'##\s*(\{.*\})\s*##', line)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError as error:
                print("Invalid post config JSON: %s" % error)
                return {}
    return {}

def postDescription(body, period):
    lines=[]
    for line in (body or "").splitlines():
        if re.fullmatch(r'(\[[^\]]*\]\([^)]*\)\s*[|｜]?\s*)+', line.strip()):
            continue
        lines.append(line)
    text=re.sub(r'<!--.*?-->', '', "\n".join(lines), flags=re.S)
    text=re.sub(r'```.*?```', '', text, flags=re.S)
    text=re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)
    text=re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text=re.sub(r'^\s*#{1,6}\s*', '', text, flags=re.M)
    text=re.sub(r'^\s*>\s?', '', text, flags=re.M)
    text=re.sub(r'[*_`~]', '', text)
    text=re.sub(r'\s+', ' ', text).strip()
    if period in text:
        text=text.split(period)[0]+period
    return text.replace('"', "'")

######################################################################################
class GMEEK():
    def __init__(self,options):
        self.options=options
        
        self.root_dir='docs/'
        self.static_dir='static/'
        self.post_folder='post/'
        self.backup_dir='backup/'
        self.post_dir=self.root_dir+self.post_folder

        user = Github(self.options.github_token)
        self.repo = self.get_repo(user, self.options.repo_name)
        self.oldFeedString=''
        self.changed=False
        self.generated=set()
        self.cacheEntries={}
        self.cacheRenderHash=''
        if os.path.exists("blogBase.json"):
            with open("blogBase.json", "r", encoding="utf-8") as cacheFile:
                oldBlogBase=json.load(cacheFile)
            self.cacheRenderHash=oldBlogBase.get("renderHash", '')
            for listName in ("postListJson", "singeListJson"):
                self.cacheEntries.update(oldBlogBase.get(listName, {}))

        self.labelColorDict=json.loads('{}')
        for label in self.repo.get_labels():
            self.labelColorDict[label.name]='#'+label.color
        print(self.labelColorDict)
        self.renderHash=self.computeRenderHash()
        self.defaultConfig()
        
    def writeIfChanged(self, path, content, ignoreBuildTime=False):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as existing:
                old=existing.read()
            if ignoreBuildTime:
                pattern=r'<div id="footer3">.*?</div>'
                old=re.sub(pattern, '', old)
                content=re.sub(pattern, '', content)
            if old==content:
                return False
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.changed=True
        return True

    def cleanFile(self):
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.post_dir, exist_ok=True)

        if os.path.exists(self.static_dir):
            for item in os.listdir(self.static_dir):
                src = os.path.join(self.static_dir, item)
                dst = os.path.join(self.root_dir, item)
                if os.path.isfile(src):
                    shutil.copy(src, dst)
                    self.generated.add(os.path.normpath(dst))
                    print(f"Copied {item} to docs")
                elif os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                    for root, _, files in os.walk(dst):
                        for name in files:
                            self.generated.add(os.path.normpath(os.path.join(root, name)))
                    print(f"Copied directory {item} to docs")
        else:
            print("static does not exist")

    def pruneDocs(self):
        for folder in (self.root_dir, self.post_dir):
            for name in os.listdir(folder):
                path=os.path.normpath(os.path.join(folder, name))
                if os.path.isfile(path) and name.endswith(".html") and path not in self.generated:
                    os.remove(path)
                    print("remove stale "+path)

        keepBackups=set()
        for listName in ("postListJson", "singeListJson"):
            for entry in self.blogBase[listName].values():
                if entry.get("backupFile"):
                    keepBackups.add(os.path.normpath(entry["backupFile"]))
        for name in os.listdir(self.backup_dir):
            path=os.path.normpath(os.path.join(self.backup_dir, name))
            if os.path.isfile(path) and path not in keepBackups:
                os.remove(path)
                print("remove stale "+path)

    def defaultConfig(self):
        dconfig={"singlePage":[],"startSite":"","filingNum":"","onePageListNum":25,"commentLabelColor":"#006b75","yearColorList":["#bc4c00", "#0969da", "#1f883d", "#A333D0"],"i18n":"CN","themeMode":"manual","dayTheme":"light","nightTheme":"dark","urlMode":"pinyin","script":"","style":"","head":"","indexScript":"","indexStyle":"","bottomText":"","showPostSource":1,"iconList":{},"UTC":+8,"rssSplit":"sentence","exlink":{},"needComment":1,"allHead":"","linkPrefix":"","pageNum":1,"totalPages":1}
        config=json.loads(open('config.json', 'r', encoding='utf-8').read())
        self.blogBase={**dconfig,**config}.copy()
        self.blogBase["postListJson"]=json.loads('{}')
        self.blogBase["singeListJson"]=json.loads('{}')
        self.blogBase["labelColorDict"]=self.labelColorDict
        self.blogBase["labelTextColorDict"]={name: textColor(color) for name, color in self.labelColorDict.items()}
        self.blogBase["commentLabelTextColor"]=textColor(self.blogBase["commentLabelColor"])
        if not isinstance(self.blogBase["onePageListNum"], int) or self.blogBase["onePageListNum"] < 1:
            raise ValueError("onePageListNum must be a positive integer")
        self.blogBase["sourceCodeUrl"]="https://github.com/"+self.options.repo_name
        if "displayTitle" not in self.blogBase:
            self.blogBase["displayTitle"]=self.blogBase["title"]

        if "faviconUrl" not in self.blogBase:
            self.blogBase["faviconUrl"]=self.blogBase["avatarUrl"]

        if "ogImage" not in self.blogBase:
            self.blogBase["ogImage"]=self.blogBase["avatarUrl"]

        if "primerCSS" not in self.blogBase:
            self.blogBase["primerCSS"]="<link href='https://mirrors.sustech.edu.cn/cdnjs/ajax/libs/Primer/21.0.7/primer.css' rel='stylesheet' />"

        if "homeUrl" not in self.blogBase:
            if str(self.repo.name).lower() == (str(self.repo.owner.login) + ".github.io").lower():
                self.blogBase["homeUrl"] = f"https://{self.repo.name}"
            else:
                self.blogBase["homeUrl"] = f"https://{self.repo.owner.login}.github.io/{self.repo.name}"
        print("GitHub Pages URL: ", self.blogBase["homeUrl"])

        if self.blogBase["i18n"]=="CN":
            self.i18n=i18nCN
        elif self.blogBase["i18n"]=="RU":
            self.i18n=i18nRU
        else:
            self.i18n=i18n
        
        self.TZ=datetime.timezone(datetime.timedelta(hours=self.blogBase["UTC"]))
        self.blogBase["build_time"]=datetime.datetime.now(self.TZ).isoformat(timespec='seconds')

    def computeRenderHash(self):
        digest=hashlib.sha256()
        for name in sorted(os.listdir('templates')):
            with open(os.path.join('templates', name), 'rb') as templateFile:
                digest.update(name.encode('utf-8'))
                digest.update(templateFile.read())
        with open('config.json', 'rb') as configFile:
            digest.update(configFile.read())
        digest.update(json.dumps(self.labelColorDict, sort_keys=True).encode('utf-8'))
        return digest.hexdigest()

    def get_repo(self,user:Github, repo:str):
        return user.get_repo(repo)

    def markdown2html(self, mdstr):
        payload = {"text": mdstr, "mode": "gfm"}
        headers = {"Authorization": "token {}".format(self.options.github_token)}
        try:
            response = requests.post("https://api.github.com/markdown", json=payload, headers=headers, timeout=(10, 60))
            response.raise_for_status()  # Raises an exception if status code is not 200
            return response.text
        except requests.RequestException as e:
            raise Exception("markdown2html error: {}".format(e))

    def renderHtml(self,template,blogBase,postListJson,htmlDir,icon):
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader, autoescape=select_autoescape(['html']))
        template = env.get_template(template)
        output = template.render(blogBase=blogBase,postListJson=postListJson,i18n=self.i18n,IconList=icon)
        self.writeIfChanged(htmlDir, output, ignoreBuildTime=True)
        self.generated.add(os.path.normpath(htmlDir))

    def createPostHtml(self,issue):
        f = open(issue["backupFile"], 'r', encoding='UTF-8')
        post_body=self.markdown2html(f.read())
        f.close()

        postBase=self.blogBase.copy()

        if '<math-renderer' in post_body:
            post_body=re.sub(r'<math-renderer.*?>','',post_body)
            post_body=re.sub(r'</math-renderer>','',post_body)
            issue["script"]=issue["script"]+'<script>MathJax = {tex: {inlineMath: [["$", "$"]]}};</script><script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'
        
        if '<p class="markdown-alert-title">' in post_body:
            issue["style"]=issue["style"]+'<style>.markdown-alert{padding:0.5rem 1rem;margin-bottom:1rem;border-left:.25em solid var(--borderColor-default,var(--color-border-default));}.markdown-alert .markdown-alert-title {display:flex;font-weight:var(--base-text-weight-medium,500);align-items:center;line-height:1;}.markdown-alert>:first-child {margin-top:0;}.markdown-alert>:last-child {margin-bottom:0;}</style>'
            alerts = {
                'note': 'accent',
                'tip': 'success',
                'important': 'done',
                'warning': 'attention',
                'caution': 'danger'
            }

            for alert, style in alerts.items():
                if f'markdown-alert-{alert}' in post_body:
                    issue["style"] += (
                        f'<style>.markdown-alert.markdown-alert-{alert} {{'
                        f'border-left-color:var(--borderColor-{style}-emphasis, var(--color-{style}-emphasis));'
                        f'background-color:var(--color-{style}-subtle);}}'
                        f'.markdown-alert.markdown-alert-{alert} .markdown-alert-title {{'
                        f'color: var(--fgColor-{style},var(--color-{style}-fg));}}</style>'
                    )

        if issue.get("trusted") and '<code class="notranslate">Gmeek-html' in post_body:
            post_body = re.sub(r'<code class="notranslate">Gmeek-html(.*?)</code>', lambda match: html.unescape(match.group(1)), post_body, flags=re.DOTALL)

        postBase["postTitle"]=issue["postTitle"]
        postBase["postUrl"]=issue["postUrl"]
        postBase["linkPrefix"]="../" if issue["htmlDir"].startswith(self.post_dir) else ""
        postBase["description"]=issue["description"]
        postBase["ogImage"]=issue["ogImage"]
        postBase["postBody"]=post_body
        postBase["commentNum"]=issue["commentNum"]
        postBase["style"]=issue["style"]
        postBase["script"]=issue["script"]
        postBase["head"]=issue["head"]
        postBase["top"]=issue["top"]
        postBase["postSourceUrl"]=issue["postSourceUrl"]
        postBase["postNum"]=issue["postNum"]
        postBase["repoName"]=self.options.repo_name
        
        if issue["labels"][0] in self.blogBase["singlePage"]:
            postBase["bottomText"]=''

        if '<pre class="notranslate">' in post_body:
            keys=['sun','moon','sync','home','github','copy','check']
            if '<div class="highlight' in post_body:
                postBase["highlight"]=1
            else:
                postBase["highlight"]=2
        else:
            keys=['sun','moon','sync','home','github']
            postBase["highlight"]=0

        postIcon=dict(zip(keys, map(IconBase.get, keys)))
        self.renderHtml('post.html',postBase,{},issue["htmlDir"],postIcon)
        print("create postPage title=%s file=%s " % (issue["postTitle"],issue["htmlDir"]))

    def createPlistHtml(self):
        self.blogBase["postListJson"]=dict(sorted(self.blogBase["postListJson"].items(),key=lambda x:(x[1]["top"],x[1]["createdAt"]),reverse=True))#使列表由时间排序
        keys=list(OrderedDict.fromkeys(['sun', 'moon','sync', 'search', 'rss', 'upload', 'post'] + self.blogBase["singlePage"]))
        plistIcon={**dict(zip(keys, map(IconBase.get, keys))),**self.blogBase["iconList"]}
        keys=['sun','moon','sync','home','search','post']
        tagIcon=dict(zip(keys, map(IconBase.get, keys)))

        entries=list(self.blogBase["postListJson"].items())
        perPage=self.blogBase["onePageListNum"]
        totalPages=max(1, (len(entries)+perPage-1)//perPage)
        self.blogBase["totalPages"]=totalPages
        for pageIndex in range(totalPages):
            self.blogBase["pageNum"]=pageIndex+1
            onePageList=dict(entries[pageIndex*perPage:(pageIndex+1)*perPage])
            htmlDir=self.root_dir+("index.html" if pageIndex==0 else "page%d.html" % (pageIndex+1))
            self.renderHtml('plist.html',self.blogBase,onePageList,htmlDir,plistIcon)
            print("create "+htmlDir)

        self.renderHtml('tag.html',self.blogBase,{},self.root_dir+"tag.html",tagIcon)
        print("create tag.html")

    def createFeedXml(self):
        self.blogBase["postListJson"]=dict(sorted(self.blogBase["postListJson"].items(),key=lambda x:x[1]["createdAt"],reverse=False))#使列表由时间排序
        feed = FeedGenerator()
        feed.title(self.blogBase["title"])
        feed.description(self.blogBase["subTitle"])
        feed.link(href=self.blogBase["homeUrl"] + "/")
        feed.image(url=self.blogBase["avatarUrl"],title="avatar", link=self.blogBase["homeUrl"] + "/")
        feed.copyright(self.blogBase["title"])
        feed.managingEditor(self.blogBase["title"])
        feed.webMaster(self.blogBase["title"])
        feed.ttl("60")

        for num in self.blogBase["singeListJson"]:
            item=feed.add_item()
            item.guid(self.blogBase["homeUrl"]+"/"+self.blogBase["singeListJson"][num]["postUrl"],permalink=True)
            item.title(self.blogBase["singeListJson"][num]["postTitle"])
            item.description(self.blogBase["singeListJson"][num]["description"])
            item.link(href=self.blogBase["homeUrl"]+"/"+self.blogBase["singeListJson"][num]["postUrl"])
            item.pubDate(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(self.blogBase["singeListJson"][num]["createdAt"])))

        for num in self.blogBase["postListJson"]:
            item=feed.add_item()
            item.guid(self.blogBase["homeUrl"]+"/"+self.blogBase["postListJson"][num]["postUrl"],permalink=True)
            item.title(self.blogBase["postListJson"][num]["postTitle"])
            item.description(self.blogBase["postListJson"][num]["description"])
            item.link(href=self.blogBase["homeUrl"]+"/"+self.blogBase["postListJson"][num]["postUrl"])
            item.pubDate(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(self.blogBase["postListJson"][num]["createdAt"])))

        if self.oldFeedString!='':
            feed.rss_file(self.root_dir+'new.xml')
            newFeed=open(self.root_dir+'new.xml','r',encoding='utf-8')
            new=newFeed.read()
            newFeed.close()

            new=re.sub(r'<lastBuildDate>.*?</lastBuildDate>','',new)
            old=re.sub(r'<lastBuildDate>.*?</lastBuildDate>','',self.oldFeedString)
            os.remove(self.root_dir+'new.xml')
            
            if new==old:
                print("====== rss xml no update ======")
                feedFile=open(self.root_dir+'rss.xml',"w")
                feedFile.write(self.oldFeedString)
                feedFile.close()
                return

        print("====== create rss xml ======")
        feed.rss_file(self.root_dir+'rss.xml')

    def createSitemap(self):
        self.blogBase["postListJson"]=dict(sorted(self.blogBase["postListJson"].items(),key=lambda x:x[1]["createdAt"],reverse=False))#使列表由时间排序
        print("====== create sitemap txt ======")
        lines=[self.blogBase["homeUrl"]]
        for num in self.blogBase["singeListJson"]:
            lines.append(self.blogBase["homeUrl"] + "/" + self.blogBase["singeListJson"][num]["postUrl"])
        for num in self.blogBase["postListJson"]:
            lines.append(self.blogBase["homeUrl"] + "/" + self.blogBase["postListJson"][num]["postUrl"])
        self.writeIfChanged(self.root_dir + "sitemap.txt", "\n".join(lines) + "\n")

    def addOnePostJson(self,issue):
        if len(issue.labels)<1:
            return None
        if issue.labels[0].name in self.blogBase["singlePage"]:
            listJsonName='singeListJson'
            htmlFile='{}.html'.format(self.createFileName(issue,useLabel=True))
            gen_Html = self.root_dir+htmlFile
        else:
            listJsonName='postListJson'
            htmlFile='{}.html'.format(self.createFileName(issue))
            gen_Html = self.post_dir+htmlFile

        trusted=issue.user is not None and issue.user.login == self.repo.owner.login
        postNum="P"+str(issue.number)
        entry={}
        entry["trusted"]=trusted
        entry["htmlDir"]=gen_Html
        entry["labels"]=[label.name for label in issue.labels]
        entry["postTitle"]=issue.title
        entry["postUrl"]=urllib.parse.quote(gen_Html[len(self.root_dir):])
        entry["postSourceUrl"]="https://github.com/"+self.options.repo_name+"/issues/"+str(issue.number)
        entry["postNum"]=postNum
        entry["updatedAt"]=issue.updated_at.isoformat()
        entry["needsRender"]=True
        entry["commentNum"]=issue.comments

        if issue.body==None:
            entry["description"]=''
            entry["wordCount"]=0
        else:
            entry["wordCount"]=len(issue.body)
            if self.blogBase["rssSplit"]=="sentence":
                period="。" if self.blogBase["i18n"]=="CN" else "."
            else:
                period=self.blogBase["rssSplit"]
            entry["description"]=postDescription(issue.body, period)

        entry["top"]=0
        for event in issue.get_events():
            if event.event=="pinned":
                entry["top"]=1
            elif event.event=="unpinned":
                entry["top"]=0

        postConfig=parsePostConfig(issue.body) if trusted else {}
        if postConfig:
            print("Has Custom JSON parameters")
            print(postConfig)
        elif not trusted and "##" in (issue.body or ""):
            print("Ignore custom JSON from untrusted author: %s" % issue.title)

        if "timestamp" in postConfig:
            entry["createdAt"]=int(postConfig["timestamp"])
        else:
            entry["createdAt"]=int(issue.created_at.replace(tzinfo=datetime.timezone.utc).timestamp())

        for key in ("style", "script", "head"):
            entry[key]=self.blogBase[key]+str(postConfig.get(key, ""))
        entry["ogImage"]=postConfig.get("ogImage", self.blogBase["ogImage"])

        thisTime=datetime.datetime.fromtimestamp(entry["createdAt"]).astimezone(self.TZ)
        entry["createdDate"]=thisTime.strftime("%Y-%m-%d")
        dateLabelColor=self.blogBase["yearColorList"][int(thisTime.year)%len(self.blogBase["yearColorList"])]
        entry["dateLabelColor"]=dateLabelColor
        entry["dateLabelTextColor"]=textColor(dateLabelColor)
        self.blogBase[listJsonName][postNum]=entry

        mdFileName=("%d-%s" % (issue.number, safeFileName(issue.title)))
        entry["backupFile"]=self.backup_dir+mdFileName+".md"
        self.writeIfChanged(entry["backupFile"], issue.body or '')
        return listJsonName

    def runAll(self):
        print("====== start create static html ======")
        self.cleanFile()

        useCache=self.cacheRenderHash==self.renderHash
        issues=self.repo.get_issues()
        for issue in issues:
            if issue.pull_request:
                continue
            key="P"+str(issue.number)
            cached=self.cacheEntries.get(key) if useCache else None
            if cached and cached.get("updatedAt")==issue.updated_at.isoformat() and os.path.exists(cached.get("htmlDir", "")):
                listJsonName="singeListJson" if issue.labels and issue.labels[0].name in self.blogBase["singlePage"] else "postListJson"
                entry=dict(cached)
                entry.pop("needsRender", None)
                self.blogBase[listJsonName][key]=entry
                self.generated.add(os.path.normpath(entry["htmlDir"]))
                continue
            self.addOnePostJson(issue)

        for issue in self.blogBase["postListJson"].values():
            if issue.get("needsRender") or not os.path.exists(issue["htmlDir"]):
                self.createPostHtml(issue)

        for issue in self.blogBase["singeListJson"].values():
            if issue.get("needsRender") or not os.path.exists(issue["htmlDir"]):
                self.createPostHtml(issue)

        self.createPlistHtml()
        self.createFeedXml()
        self.createSitemap()
        self.pruneDocs()
        print("====== create static html end ======")

    def createFileName(self,issue,useLabel=False):
        if useLabel==True:
            fileName=issue.labels[0].name
        else:
            if self.blogBase["urlMode"]=="issue":
                fileName=str(issue.number)
            elif self.blogBase["urlMode"]=="ru_translit": 
                fileName="%s-%d" % (str(translit(issue.title, language_code='ru', reversed=True)).replace(' ', '-'), issue.number)
            else:
                fileName="%s-%d" % (Pinyin().get_pinyin(issue.title), issue.number)
        
        return safeFileName(fileName)

######################################################################################
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    options = parser.parse_args()

    blog=GMEEK(options)

    if os.path.exists(blog.root_dir+'rss.xml'):
        oldFeedFile=open(blog.root_dir+'rss.xml','r',encoding='utf-8')
        blog.oldFeedString=oldFeedFile.read()
        oldFeedFile.close()

    print("runAll")
    blog.runAll()

    blog.blogBase["renderHash"]=blog.renderHash
    for listName in ("postListJson", "singeListJson"):
        for entry in blog.blogBase[listName].values():
            entry.pop("needsRender", None)
    blogBaseJson=re.sub(r'"build_time": "[^"]*"', '"build_time": ""', json.dumps(blog.blogBase))
    if os.path.exists("blogBase.json"):
        with open("blogBase.json", "r", encoding="utf-8") as listFile:
            oldBlogBaseJson=re.sub(r'"build_time": "[^"]*"', '"build_time": ""', listFile.read())
    else:
        oldBlogBaseJson=None
    if blogBaseJson!=oldBlogBaseJson:
        with open("blogBase.json", "w", encoding="utf-8") as listFile:
            listFile.write(json.dumps(blog.blogBase))
        blog.changed=True

    commentNumSum=0
    wordCount=0
    print("====== create postList.json file ======")
    blog.blogBase["postListJson"]=dict(sorted(blog.blogBase["postListJson"].items(),key=lambda x:x[1]["createdAt"],reverse=True))#使列表由时间排序
    for i in blog.blogBase["postListJson"]:
        del blog.blogBase["postListJson"][i]["description"]
        del blog.blogBase["postListJson"][i]["postSourceUrl"]
        del blog.blogBase["postListJson"][i]["postNum"]
        del blog.blogBase["postListJson"][i]["htmlDir"]
        del blog.blogBase["postListJson"][i]["createdAt"]
        del blog.blogBase["postListJson"][i]["script"]
        del blog.blogBase["postListJson"][i]["style"]
        del blog.blogBase["postListJson"][i]["top"]
        del blog.blogBase["postListJson"][i]["ogImage"]

        if 'head' in blog.blogBase["postListJson"][i]:
            del blog.blogBase["postListJson"][i]["head"]

        if 'commentNum' in blog.blogBase["postListJson"][i]:
            commentNumSum=commentNumSum+blog.blogBase["postListJson"][i]["commentNum"]
            del blog.blogBase["postListJson"][i]["commentNum"]

        if 'wordCount' in blog.blogBase["postListJson"][i]:
            wordCount=wordCount+blog.blogBase["postListJson"][i]["wordCount"]
            del blog.blogBase["postListJson"][i]["wordCount"]

    blog.blogBase["postListJson"]["labelColorDict"]=blog.labelColorDict
    blog.blogBase["postListJson"]["labelTextColorDict"]=blog.blogBase["labelTextColorDict"]

    blog.writeIfChanged(blog.root_dir+"postList.json", json.dumps(blog.blogBase["postListJson"]))

    if os.environ.get('GITHUB_EVENT_NAME')!='schedule' and (blog.changed or not os.path.exists((os.environ.get('GITHUB_WORKSPACE') or os.getcwd())+"/README.md")):
        print("====== update readme file ======")
        workspace_path = os.environ.get('GITHUB_WORKSPACE') or os.getcwd()
        postNumSum=sum(1 for key in blog.blogBase["postListJson"] if key.startswith("P"))
        readme="# %s :link: %s \r\n" % (blog.blogBase["title"],blog.blogBase["homeUrl"])
        readme=readme+"### :page_facing_up: [%d](%s/tag.html) \r\n" % (postNumSum,blog.blogBase["homeUrl"])
        readme=readme+"### :speech_balloon: %d \r\n" % commentNumSum
        readme=readme+"### :hibiscus: %d \r\n" % wordCount
        readme=readme+"### :alarm_clock: %s \r\n" % datetime.datetime.now(blog.TZ).strftime('%Y-%m-%d %H:%M:%S')
        readme=readme+"### Powered by :heart: [Gmeek](https://github.com/Meekdai/Gmeek)\r\n"
        readmeFile=open(workspace_path+"/README.md","w")
        readmeFile.write(readme)
        readmeFile.close()

if __name__ == "__main__":
    main()
######################################################################################
