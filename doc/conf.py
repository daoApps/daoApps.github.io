"""道用（daoApps）站点 Sphinx 配置。

本仓库是 daoapps.github.io 的**源码仓库**：全站（组织主页 + `/jieban/` 结伴子站）
由 Sphinx + MyST 构建，产物由 GitHub Actions 发布到 GitHub Pages。
站点根 `doc/index.md` → `/`，`doc/jieban/index.md` → `/jieban/`。

内容边界：结伴站的所有文案纪律（引文版本身份证、内部群昵称不上公开页）
由本文件的构建期守卫与 `tests/test_site_contract.py` 共同守护。
"""

import os
import re
from pathlib import Path

from sphinx.search import IndexBuilder

# -- 项目元信息 ------------------------------------------------------------

project = "道用"
author = "daoApps"
copyright = "2026, daoApps"
language = "zh_CN"

# -- 路径 ------------------------------------------------------------------
# doc/ 为唯一事实来源；构建产物落 _build/（.gitignore 已排除）

DOC_DIR = Path(__file__).resolve().parent
BUILD_DIR = DOC_DIR.parent / "_build"

# -- 扩展 ------------------------------------------------------------------

extensions = [
    "myst_parser",  # MyST Markdown 作为一等源格式
    "sphinx_book_theme",  # 阅读优先主题
    "sphinx_copybutton",  # 代码块一键复制
    "sphinx_design",  # 卡片 / 栅格 / 标签页
    "sphinxcontrib.mermaid",  # Mermaid 图（项目规范：图表优先）
]

# -- MyST ------------------------------------------------------------------

myst_enable_extensions = [
    "colon_fence",  # ::: 围栏，sphinx-design 卡片与 container 所需
    "deflist",
    "fieldlist",
    "tasklist",
    "substitution",  # 复用品牌名称与引文出处
    "attrs_inline",  # 行内属性：给按钮链接挂 class（[文字](页.md){.jb-btn}）
]
myst_heading_anchors = 3

myst_substitutions = {
    "brand": "结伴",
    "yiwei": "既以予人矣，己愈多",  # 帛书乙本·末章（唯一合规短引文）
}

source_suffix = {".md": "markdown"}
root_doc = "index"

# Mermaid 由 sphinxcontrib-mermaid 在前端加载 mermaid.js 渲染，
# 固定版本号避免上游更新导致图表样式漂移。
mermaid_version = "11.4.1"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md"]

# -- 发布通道切换 ----------------------------------------------------------
# 同一份 doc/ 源部署到两条通道（GitHub Pages 与 Read the Docs），左侧栏底部的
# 切换下拉让读者跳到**同一页**在另一条通道上的地址：前端把当前页路径拼到目标通道
# 的基址后面，目标页不存在时回退到该通道首页。两条目由 _static/switcher.json 描述。
#
# 这里的两个代号必须与 switcher.json 的 `version` 字段逐一对应（有测试守护）。
_CHANNEL_GH_PAGES = "gh-pages"
_CHANNEL_RTD = "rtd"

# 当前在哪条通道上构建，就高亮哪一条：同一份 HTML 会被部署到两处，页面自己认不出
# 身在何处，只能在构建期按环境变量分流——RTD 构建带 READTHEDOCS，GitHub Actions
# 带 GITHUB_ACTIONS，本地预览按 GitHub Pages 处理。
_CURRENT_CHANNEL = _CHANNEL_RTD if os.environ.get("READTHEDOCS") else _CHANNEL_GH_PAGES

# -- HTML 输出 -------------------------------------------------------------

html_theme = "sphinx_book_theme"
html_title = "道用 · daoApps"
html_static_path = ["_static"]
html_css_files = ["dao.css"]
html_js_files = ["dao.js"]
html_show_sourcelink = False
html_last_updated_fmt = ""

# 侧栏保留主题默认（左侧文档树 + 右侧本页目录）。
# 结伴首页是六屏长卷，没有右侧 TOC 就丢了页内锚点导航；左侧文档树负责跨页导航。
# 视觉改造因此只做「表皮」——配色、章节语言、卡片、印章、打印样式，不动骨架。
html_theme_options = {
    # 展示型站点，隐藏仓库/下载/编辑等与品牌无关的按钮
    "use_download_button": False,
    "use_fullscreen_button": False,
    "use_repository_button": False,
    "use_edit_page_button": False,
    "use_issues_button": False,
    "home_page_in_toc": False,
    "show_navbar_depth": 1,
    "show_toc_level": 3,
    "extra_footer": "",  # 实际内容由 _inject_footer 按页注入
    # 通道切换下拉：数据源用**相对路径**读本地 doc/_static/switcher.json。
    # 不要换成 http(s) 绝对 URL——pydata 在构建期会对绝对 URL 发 requests.get
    # 校验，读不到即 warning，本站开了 -W（RTD 侧 fail_on_warning）会直接构建失败；
    # 更糟的是首次部署前该文件还不存在，必然形成自举死锁。相对路径改为读本地文件：
    # 校验仍在（条目缺 url/version 会 warning → 被 -W 拦下），且无网络依赖；
    # 前端按站点根解析它，故 GitHub Pages 与 RTD 的 /zh-cn/latest/ 前缀下都取得到。
    "switcher": {
        "json_url": "_static/switcher.json",
        "version_match": _CURRENT_CHANNEL,
    },
    # 主题默认是 ["sidebar-ethical-ads"]（RTD 伦理广告位占位）；保留它、在它前面
    # 挂上切换下拉，既拿到按钮，也不改变 RTD 侧的既有行为。
    "primary_sidebar_end": ["version-switcher", "sidebar-ethical-ads"],
}

# -- 搜索 ------------------------------------------------------------------
# 中文站内搜索有两道 Sphinx 默认不放行的坎，缺一道搜索就整个不可用：
#
#   1. 分词：SearchChinese 把中文切词交给 jieba；未安装时 cut_for_search 返回空集，
#      中文内容一个字都进不了索引。构建期不报任何错，只是搜不到——requirements.txt
#      已列入 jieba。
#   2. 词干器：SearchChinese 若声明 js_stemmer_rawcode（服务端同样用 snowball 的
#      english 词干器处理拉丁词，两端必须一致，否则索引里的词与查询串的词形对不上），
#      Sphinx 生成 language_data.js 时会按 language_name 拼全局名：中文站是
#      'Chinese' → 拼出 `Stemmer = ChineseStemmer;`，而该词干器文件里定义的是
#      EnglishStemmer。引用落空后 window.Stemmer 为 undefined，searchtools.js 的
#      `new Stemmer()` 随即抛错——搜索框彻底打不开，且每页控制台报
#      "ChineseStemmer is not defined"。
#
#      ⚠️ 这条**分版本成立**，不要写成"所有版本都这样"：Sphinx 给不给 zh 设 rawcode
#      并不一致——8.2.3 的 zh 就没设（继承 SearchLanguage 的空串），只有
#      da/de/es/fi/fr/hu/it/nl/no/pt/ro/ru/sv/tr 设了；且 8.2.3 的 non-minified-js
#      目录里根本没有 english-stemmer.js。rawcode 为空时 get_js_stemmer_code 走
#      js_stemmer_code 分支，Stemmer 由那段代码自己定义（`var Stemmer = function`），
#      压根不产生引用行——搜索本来就是好的。因此下面的补丁在 8.2.3 上是空操作，
#      只在 zh 真的声明了 rawcode 的版本上才生效（防御性补丁，不是修复当前版本）。
#
# 这里按词干器文件名推导真实全局名（english-stemmer.js → EnglishStemmer）改正那一行。
# 上游若修好，赋值行上的名字与推导结果一致，本补丁自动失效。

_STEMMER_GLOBAL = re.compile(r"(?:window\.)?Stemmer\s*=\s*(\w+Stemmer);")


def _derive_stemmer_global(rawcode: str) -> str:
    """由词干器文件名推导其导出的全局名，遵循 Sphinx 自身命名约定。

    `english-stemmer.js` → `EnglishStemmer`，`dutch_porter-stemmer.js` →
    `DutchPorterStemmer`。
    """
    name = rawcode.removesuffix(".js").removesuffix("-stemmer")
    return "".join(part.capitalize() for part in re.split(r"[-_]", name)) + "Stemmer"


_original_get_js_stemmer_code = IndexBuilder.get_js_stemmer_code


def _get_js_stemmer_code(self) -> str:  # noqa: ANN001
    code = _original_get_js_stemmer_code(self)
    rawcode = self.lang.js_stemmer_rawcode
    if not rawcode:
        return code
    found = _STEMMER_GLOBAL.search(code)
    expected = _derive_stemmer_global(rawcode)
    # 只在赋值行上比对：词干器定义里本来就含这个名字，拿全量文本判断会永远命中。
    if found is None or found.group(1) == expected:
        return code
    return _STEMMER_GLOBAL.sub(f"window.Stemmer = {expected};", code)


IndexBuilder.get_js_stemmer_code = _get_js_stemmer_code

# -- 页脚 ------------------------------------------------------------------
# 站点页脚分两层：
#   1. 全站层（组织入口）——所有页面都有；
#   2. 合规层（结伴站声明）——只挂在 /jieban/ 下，避免出现在组织主页上。

_SITE_FOOTER = (
    "道用 · daoApps<br>"
    '<a href="https://github.com/daoApps">GitHub 组织</a> · '
    '<a href="https://github.com/daoApps/daoApps">主仓库</a> · '
    '<a href="https://github.com/daoApps/daoNexus">应用枢纽</a> · '
    '<a href="/jieban/">结伴 · 子站</a> · '
    '<a href="/fupan/">复盘 · 子站</a> · '
    '<a href="https://github.com/daoApps/daoApps.github.io">本站源码</a>'
)

_JIEBAN_FOOTER = (
    "<br>知足 · 恒与 · 知和 · 愈多<br>"
    "好好生活的人，终会相逢<br>"
    "本站不提供任何婚恋中介或投资理财服务。"
    "引文据马王堆帛书本《老子》，详见《社群公约》页的版本说明。"
)


def _inject_footer(app, pagename, templatename, context, doctree):  # noqa: ANN001
    """按页注入页脚：结伴子站的合规声明不上组织主页。"""
    footer = _SITE_FOOTER
    if pagename == "jieban" or pagename.startswith("jieban/"):
        footer = footer + _JIEBAN_FOOTER
    context["theme_extra_footer"] = footer


# -- 构建期一致性检查 ------------------------------------------------------


def _check_version_labels(app, config):  # noqa: ANN001
    """版本身份证（构建期硬检查）。

    两条正向不变量——引文出现在哪，版本标识就必须跟到哪：
    1. 出现末章短引文「己愈多」的页面，必须同时出现「帛书乙本」；
    2. 出现「知和曰明」的页面，必须同时出现「帛书甲本」。

    不做「帛书本」字样的负例扫描：公约页本身要引用这条规则，
    机械匹配必然误伤，故该纪律以文字条款形式写在公约页，不纳入自动检查。
    """
    problems: list[str] = []
    for md in sorted(DOC_DIR.glob("**/*.md")):
        if "_build" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        where = md.relative_to(DOC_DIR).as_posix()
        # 归一化：去掉强调标记与空白，避免「帛书**甲本**」这类排版绕过检查
        flat = re.sub(r"[*\s\u3000]", "", text)

        if "己愈多" in flat and "帛书乙本" not in flat:
            problems.append(f"{where}：引用了末章短引文，但未标注「帛书乙本」")
        if "知和曰明" in flat and "帛书甲本" not in flat:
            problems.append(f"{where}：引用了「知和曰明」，但未标注「帛书甲本」")

    if problems:
        raise RuntimeError("引文版本标注不合规：\n  - " + "\n  - ".join(problems))


# -- Read the Docs 平台语言守卫 --------------------------------------------
# RTD 构建时不读 conf.py 的 language，而是把**平台侧**项目语言拼进命令行：
# `-D language=<平台语言>` —— 见 readthedocs.org 的 doc_builder/backends/sphinx.py
# （get_language 取 project.language，经 OLD_LANGUAGES_CODE_MAPPING 把 `zh-cn`
# 映射回 Sphinx 认识的 `zh_CN`）。`-D` 优先级高于 conf.py，即平台设置说了算。
#
# 于是「平台语言留在默认英文」是一种**静默失效**：构建期一条警告都不报
# （fail_on_warning 也拦不住，实测 -D language=en 全程无告警），只是中文分词
# 不再加载 jieba，中文内容一个字都进不了搜索索引——与上面「搜索」一节记录的
# 两个坑同源，都是「构建不报错，只是搜不到」。
# 本站既有纪律是把陷阱变成机器可拦截的约束，故在此把它变成构建期硬错误。
#
# 平台侧动作（一次性）：RTD 项目 Admin → Settings → Language 选
# Simplified Chinese（RTD 代码 `zh-cn`，经映射后传给 Sphinx 的 `zh_CN` 与本文件同源）。


def _check_rtd_language(app, config):  # noqa: ANN001
    """RTD 平台语言必须与 conf.py 的 language 同源，否则中文搜索会静默失效。"""
    rtd_language = os.environ.get("READTHEDOCS_LANGUAGE")
    if not rtd_language:
        return  # 本地与 GitHub Actions 构建不经过 RTD，不设此变量
    # 归一化后比较：平台侧 zh-cn / 旧码 zh_CN 都与本文件的 zh_CN 等价
    if rtd_language.replace("_", "-").lower() != language.replace("_", "-").lower():
        raise RuntimeError(
            f"Read the Docs 平台语言为 {rtd_language!r}，与 doc/conf.py 的 {language!r} 不一致："
            f"RTD 会用 -D language={rtd_language} 覆盖 conf.py，中文分词依赖（jieba）不再加载，"
            "中文内容静默不进搜索索引。请在 RTD 项目 Admin → Settings → Language "
            "选择 Simplified Chinese。"
        )


def setup(app):  # noqa: ANN001
    app.connect("config-inited", _check_version_labels)
    app.connect("config-inited", _check_rtd_language)
    app.connect("html-page-context", _inject_footer)
    return {"parallel_read_safe": True, "parallel_write_safe": True}