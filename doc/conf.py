"""道用（daoApps）站点 Sphinx 配置。

本仓库是 daoapps.github.io 的**源码仓库**：全站（组织主页 + `/jieban/` 结伴子站）
由 Sphinx + MyST 构建，产物由 GitHub Actions 发布到 GitHub Pages。
站点根 `doc/index.md` → `/`，`doc/jieban/index.md` → `/jieban/`。

内容边界：结伴站的所有文案纪律（引文版本身份证、内部群昵称不上公开页）
由本文件的构建期守卫与 `tests/test_site_contract.py` 共同守护。
"""

from __future__ import annotations

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
}

# -- 搜索 ------------------------------------------------------------------
# 中文站内搜索有两道 Sphinx 默认不放行的坎，缺一道搜索就整个不可用：
#
#   1. 分词：SearchChinese 把中文切词交给 jieba；未安装时 cut_for_search 返回空集，
#      中文内容一个字都进不了索引。构建期不报任何错，只是搜不到——requirements.txt
#      已列入 jieba。
#   2. 词干器：SearchChinese 声明 js_stemmer_rawcode = 'english-stemmer.js'（服务端
#      同样用 snowball 的 english 词干器处理拉丁词，两端必须一致，否则索引里的词
#      与查询串的词形对不上）。但 Sphinx 生成 language_data.js 时按 language_name
#      拼全局名，中文站是 'Chinese' → 拼出 `window.Stemmer = ChineseStemmer;`，
#      而该文件里定义的是 EnglishStemmer。引用落空后 window.Stemmer 为 undefined，
#      searchtools.js 的 `new Stemmer()` 随即抛错——搜索框彻底打不开，而且每页都
#      在控制台报 "ChineseStemmer is not defined"（Sphinx 9.1.0 与 8.2.3 同此）。
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


def setup(app):  # noqa: ANN001
    app.connect("config-inited", _check_version_labels)
    app.connect("html-page-context", _inject_footer)
    return {"parallel_read_safe": True, "parallel_write_safe": True}