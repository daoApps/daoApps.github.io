"""道用（daoApps）站点契约测试。

校验五件事：
1. 组织主页的仓库清单与分组计数正确（14 个仓库 / 5 类用法）；
2. 结伴子站的页面与六条公约内容齐备；
3. `conf.py` 的「版本身份证」构建期守卫真的会拦截未标注版本的引文
   （防止守卫写成永不触发的装饰品）；
4. 页脚合规声明只挂在 /jieban/ 下，不上组织主页；
5. 控件配色纪律——按钮锁死链接四态，正文链接规则不声明 `color`
   （色值统一由 token 提供）并以 `:not()` 绕开控件，表面色 token 遵循主题语义
   （`on-background` 是表面、`on-surface` 是文字）；
6. 侧栏开关的行为绑定——主题渲染两份同名开关而脚本只认 DOM 中第一个（被隐去的
   那份），可见的那份必须由 `dao.js` 补绑，否则宽屏点不动、窄屏唤不出抽屉；
7. 行为脚本的执行时机——`dao.js` 由 Sphinx 注入 `<head>`，必须等 DOM 就绪再取节点，
   否则选择器全部落空且不报错（开关点了没反应、淡入类也挂不上）。

运行（需含 Sphinx 依赖的 Python 环境，本项目为 py314）：

    pytest tests
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_DIR = REPO_ROOT / "doc"
JIEBAN_DIR = DOC_DIR / "jieban"
CSS_FILE = DOC_DIR / "_static" / "dao.css"
JS_FILE = DOC_DIR / "_static" / "dao.js"

CHANNEL_SLUGS = ("zhizu", "hengyu", "zhihe", "yuduo")

# 组织主页收录的 14 个仓库（唯一事实来源为 daoApps/daoNexus 的 src/data/apps.ts，
# 本页为超集：apps.ts 只覆盖前端的 9 个应用，支付与链路、系统与基座另计）。
ORG_REPOS = (
    "forum",
    "xinyu",
    "growth-tracker",
    "habit-tracker",
    "moodflow",
    "time-capsule",
    "qrcode-studio",
    "monad-agentic-payment",
    "agentic-payment",
    "daoPayment",
    "daoApps",
    "daoNexus",
    "config-center",
    "oauth-admin",
)

ORG_GROUPS = ("社区交流", "效率工具", "实用工具", "支付与链路", "系统与基座")


def _load_conf():
    """直接加载 conf.py，以便对构建期守卫做真实调用。"""
    spec = importlib.util.spec_from_file_location("dao_conf", DOC_DIR / "conf.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["dao_conf"] = module
    spec.loader.exec_module(module)
    return module


# -- 组织主页 --------------------------------------------------------------


def test_org_home_exists():
    assert (DOC_DIR / "index.md").is_file()


def test_org_home_lists_fourteen_repos():
    text = (DOC_DIR / "index.md").read_text(encoding="utf-8")
    hrefs = re.findall(r'href="https://github\.com/daoApps/([\w.-]+)"', text)
    # 去重：首屏 CTA 也会链到 daoNexus，重复出现不等于多收录一个仓库
    listed = [h for h in dict.fromkeys(hrefs) if h != "dao-research-assistant"]
    assert len(listed) == 14, f"组织主页应收录 14 个仓库，实为 {len(listed)}"
    for repo in ORG_REPOS:
        assert repo in listed, f"组织主页缺少仓库：{repo}"


def test_org_home_five_groups_with_matching_counts():
    text = (DOC_DIR / "index.md").read_text(encoding="utf-8")
    assert len(re.findall(r'class="group"', text)) == 5, "组织主页应有 5 类用法分组"
    for group in ORG_GROUPS:
        assert f"<h3>{group}</h3>" in text, f"组织主页缺少分组：{group}"

    counts = [int(n) for n in re.findall(r'class="count">(\d+)<', text)]
    assert counts == [2, 3, 2, 3, 4], f"分组计数与清单不符：{counts}"
    assert sum(counts) == 14
    assert len(re.findall(r'class="card"', text)) == 14, "组织主页卡片数应为 14"


def test_org_home_links_to_jieban_subsite():
    text = (DOC_DIR / "index.md").read_text(encoding="utf-8")
    assert 'href="jieban/"' in text, "组织主页缺少结伴子站入口"


def test_org_home_in_site_toctree():
    """子站必须在站点导航树里，否则从任一页都回不到 /jieban/。"""
    text = (DOC_DIR / "index.md").read_text(encoding="utf-8")
    assert "\njieban/index\n" in text


# -- 结伴子站 --------------------------------------------------------------


def test_jieban_pages_exist():
    assert (JIEBAN_DIR / "index.md").is_file()
    assert (JIEBAN_DIR / "origin.md").is_file()
    assert (JIEBAN_DIR / "covenant.md").is_file()


def test_four_channels_present():
    text = (JIEBAN_DIR / "index.md").read_text(encoding="utf-8")
    for channel in ("知足", "恒与", "知和", "愈多"):
        assert channel in text


def test_four_channel_colors_defined():
    css = CSS_FILE.read_text(encoding="utf-8")
    for token in ("--zhizu", "--hengyu", "--zhihe", "--yuduo"):
        assert token in css


def _css_flat() -> str:
    """把样式表压成单行，便于按选择器做断言（多行选择器列表会被折行）。"""
    return re.sub(r"\s+", " ", CSS_FILE.read_text(encoding="utf-8"))


def test_buttons_lock_all_link_states():
    """按钮必须显式声明 :link/:visited/:visited:hover/:active。

    主题有两条会反噬控件配色的规则：
      `a:active,a:visited{color:var(--pst-color-link)}`     → (0,1,1)
      `a:visited:hover{color:var(--pst-color-link-hover)}`  → (0,2,1)
    前者高于 `.jb-btn-primary` 的 (0,1,0)，后者高于 `:hover` 的 (0,2,0)。
    两个状态都真实踩过坑：先是「深底色 + 朱砂红字」，补了 :visited 之后
    又漏掉 :visited:hover，导致已访问按钮悬停时文字不变白、朱砂底压深朱砂字。
    """
    css = _css_flat()
    for base in (
        ".jb-btn-primary",
        ".jb-btn-ghost",
        "article.bd-article .org-home .cta .btn-primary",
        "article.bd-article .org-home .cta .btn-ghost",
    ):
        for state in (":link", ":visited", ":visited:hover", ":active"):
            assert f"{base}{state}" in css, f"{base}{state} 未声明，链接态会反噬控件配色"


def test_surface_tokens_follow_theme_semantics():
    """`--pst-color-X` 是表面色，`--pst-color-on-X` 才是其上的文字色。

    主题默认 `--pst-color-on-background:#fff`（浅色主题）——变量名里的 “on”
    指的是「叠在页面背景之上的那张面」，而不是「背景之上的文字」。主题把
    `kbd`、`.bd-content .sd-card-body`、`.admonition`、`.bd-header`、表格斑马纹
    的 `background-color` 统统绑在它上面；一旦按字面赋成深墨，这些控件会成片变黑。
    实测踩坑：四频道卡片的卡体被刷成黑底，卡面文字直接不可读（`.jb-card` 的
    `background !important` 只盖住了卡片外壳，盖不住卡体）。

    这条断言守护根因，而不是禁止某个变量出现——之前 kbd 冒黑方块时打的是
    「kbd 不许用该变量」的治标补丁，结果同类黑块又从卡片、告示块上冒出来。
    """
    css = _css_flat()
    assert "--pst-color-on-background: var(--card)" in css, (
        "--pst-color-on-background 必须赋表面色；赋成 --ink 会让卡片体、kbd、"
        "告示块、表格斑马纹整体变黑"
    )
    assert "--pst-color-on-surface: var(--ink)" in css, (
        "--pst-color-on-surface 才是表面之上的文字色，不应与表面色混用"
    )


def test_prose_link_rules_do_not_capture_controls():
    """正文链接规则不得声明 color，且必须用 :not() 绕开控件按钮。

    色值已由 token 统一提供（主题基础规则 `a{color:var(--pst-color-link)}` →
    --cinnabar，`a:hover` → --cinnabar-deep），正文规则再声明一次就是纯冗余；
    而 `article.bd-article a` 带类型选择器 article，特异性 (0,2,1) 会压过所有
    单类组件规则 (0,2,0)——按钮前景色被抢（渲染出「朱砂底 + 深朱砂字」），
    卡片内链接的频道色也被盖成朱砂。此前两头都在打补丁（给按钮堆特异性、给正文
    规则加 :not()），删掉冗余 color 才是根治：组件配色按各自特异性自然各归其位。
    """
    css = re.sub(r"/\*.*?\*/", "", _css_flat(), flags=re.S)
    checked = 0
    for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        for sel in selectors.split(","):
            sel = sel.strip()
            if not sel.startswith("article.bd-article a"):
                continue
            checked += 1
            assert not re.search(r"(?<![\w-])color\s*:", body), (
                f"正文链接规则声明了 color，会以 (0,2,1) 压制组件配色：{sel}"
            )
            assert ":not(.jb-btn)" in sel, f"正文链接规则未排除控件按钮：{sel}"
            assert ":not(.btn)" in sel, f"正文链接规则未排除通用按钮：{sel}"
    assert checked >= 1, "未找到正文链接规则，断言形同虚设"


def test_visible_sidebar_toggles_get_bound():
    """可见的侧栏开关必须由 dao.js 补上行为。

    主题把两侧开关各渲染两份：`header.bd-header` 里一份（被主题自己的样式隐去，
    因为 book 主题把开关搬到了正文栏）、`.bd-header-article` 里一份（用户实际看到的）。
    两套主题脚本都用 `querySelector(".primary-toggle")` 只认 DOM 里第一个，也就是被
    隐去的那份——于是可见开关点不动：宽屏不折叠、窄屏不出抽屉，控制台还一片安静。
    这条缺陷无法在样式层断言，只能在行为层守护。
    """
    js = re.sub(r"/\*.*?\*/", "", JS_FILE.read_text(encoding="utf-8"), flags=re.S)
    assert "header.bd-header ." in js and ".bd-header-article ." in js, (
        "dao.js 未定位主题渲染的两份侧栏开关，可见开关会没有行为"
    )
    assert re.search(r"\bhidden\.click\(\)", js), (
        "dao.js 未把可见开关的点击转发给主题已绑定的节点"
    )
    for kind in ("primary", "secondary"):
        assert f'"{kind}"' in js, f"dao.js 未处理 {kind} 侧栏开关"


def test_behavior_script_waits_for_dom():
    """dao.js 在 <head> 里同步执行，取节点必须等 DOM 就绪，否则静默空跑。

    Sphinx 把 `html_js_files` 注入到 `<head>`（产物里在 `<meta name="viewport">`
    之前），且不带 defer：脚本执行时 `<body>` 尚未开始解析。此时 `querySelector`
    一律返回空——侧栏开关的绑定会走 `if (!hidden || !shown) return;` 短路；滚动淡入
    的 `querySelectorAll` 得到空集，连 `.jb-reveal` 类都不会挂上。两处都**不报错**，
    浏览器控制台一片干净，只有「点了没反应」「没有入场动效」这种哑症状。

    这条断言守护的是执行时机，而不是某个函数名：文件里的取节点动作必须都在函数
    体内（即挂在 DOM 就绪闸门下），且顶层不得再有裸跑的 IIFE。
    """
    js = re.sub(r"/\*.*?\*/", "", JS_FILE.read_text(encoding="utf-8"), flags=re.S)
    assert "DOMContentLoaded" in js, "dao.js 未等 DOM 就绪，取节点会全部落空"

    gated = len(re.findall(r"domReady\(function", js))
    assert gated >= 2, f"dao.js 只有 {gated} 个入口挂在就绪闸门下，滚动淡入与开关绑定都要挂"

    depths, depth = [], 0
    for i, ch in enumerate(js):
        if js.startswith("document.querySelector", i):
            depths.append(depth)
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
    assert depths and all(d > 0 for d in depths), (
        f"dao.js 存在裸在顶层执行的 querySelector（花括号深度 {depths}）——"
        "脚本在 <head> 里跑，取到的必是空集"
    )


def test_six_covenant_items_present():
    text = (JIEBAN_DIR / "covenant.md").read_text(encoding="utf-8")
    for item in (
        "真实",
        "善意",
        "不评判",
        "频道隔离 · 零收费导流",
        "隐私默认保护",
        "好好生活",
    ):
        assert item in text


def test_channel_pages_exist():
    for slug in CHANNEL_SLUGS:
        assert (JIEBAN_DIR / "channels" / f"{slug}.md").is_file()


def test_channel_pages_in_toctree():
    toc = (JIEBAN_DIR / "channels" / "index.md").read_text(encoding="utf-8")
    for slug in CHANNEL_SLUGS:
        assert f"\n{slug}\n" in toc


def test_channels_reachable_from_home():
    assert "channels/index" in (JIEBAN_DIR / "index.md").read_text(encoding="utf-8")


def test_no_pending_placeholder_left():
    """所有页面占位都应已填实，首页导航不应残留「待补」。"""
    for path in (JIEBAN_DIR / "index.md", JIEBAN_DIR / "origin.md",
                 JIEBAN_DIR / "covenant.md", JIEBAN_DIR / "channels" / "index.md"):
        text = path.read_text(encoding="utf-8")
        assert "（待补）" not in text, f"{path.name} 仍有未填内容"
        assert "TODO" not in text, f"{path.name} 仍有未填内容"


def test_top_pages_in_home_toctree():
    text = (JIEBAN_DIR / "index.md").read_text(encoding="utf-8")
    for page in ("origin", "covenant", "channels/index"):
        assert f"\n{page}\n" in text


def test_internal_group_nicknames_not_on_site():
    """内部群昵称不上站点（含禁用词「变现」，以及官方机构误认风险）。"""
    forbidden = ("感恩小队", "民政局小分队", "玩转 AI 变现", "玩转AI变现")
    for md in DOC_DIR.glob("**/*.md"):
        text = md.read_text(encoding="utf-8")
        for name in forbidden:
            assert name not in text, f"{md.name} 出现内部群昵称：{name}"


def test_jieban_keeps_no_form_or_popup():
    """结伴站一期公开承诺「不设表单、不收集信息」——源码里不得有表单与弹窗标记。"""
    for md in JIEBAN_DIR.glob("**/*.md"):
        text = md.read_text(encoding="utf-8").lower()
        assert "<form" not in text, f"{md.name} 出现表单"
        assert "modal" not in text, f"{md.name} 出现弹窗标记"


# -- 构建期守卫：版本身份证 ------------------------------------------------


def test_version_guard_accepts_current_pages():
    _load_conf()._check_version_labels(None, None)


def test_version_guard_rejects_unlabelled_quote(tmp_path, monkeypatch):
    conf = _load_conf()
    monkeypatch.setattr(conf, "DOC_DIR", tmp_path)
    (tmp_path / "bad.md").write_text("既以予人矣，己愈多。", encoding="utf-8")
    with pytest.raises(RuntimeError, match="帛书乙本"):
        conf._check_version_labels(None, None)


def test_version_guard_tolerates_emphasis_markers(tmp_path, monkeypatch):
    """版本名被加粗排版包裹（帛书**乙本**）不应被误判为缺标注。"""
    conf = _load_conf()
    monkeypatch.setattr(conf, "DOC_DIR", tmp_path)
    (tmp_path / "ok.md").write_text(
        "帛书**乙本**《老子》：「既以予人矣，己愈多。」", encoding="utf-8"
    )
    conf._check_version_labels(None, None)


def test_version_guard_rejects_unlabelled_jia_ben_quote(tmp_path, monkeypatch):
    conf = _load_conf()
    monkeypatch.setattr(conf, "DOC_DIR", tmp_path)
    (tmp_path / "bad.md").write_text("和曰常，知和曰明。", encoding="utf-8")
    with pytest.raises(RuntimeError, match="帛书甲本"):
        conf._check_version_labels(None, None)


# -- 页脚分层 --------------------------------------------------------------


def _footer_for(pagename: str) -> str:
    conf = _load_conf()
    context: dict[str, object] = {}
    conf._inject_footer(None, pagename, None, context, None)
    return str(context["theme_extra_footer"])


def test_footer_has_org_links_on_every_page():
    for pagename in ("index", "jieban/index"):
        footer = _footer_for(pagename)
        assert "github.com/daoApps" in footer
        assert 'href="/jieban/"' in footer


def test_compliance_line_only_on_jieban_pages():
    """合规声明属于结伴站，不能出现在组织主页上。"""
    assert "婚恋中介" not in _footer_for("index")
    assert "婚恋中介" in _footer_for("jieban/index")
    assert "婚恋中介" in _footer_for("jieban/covenant")