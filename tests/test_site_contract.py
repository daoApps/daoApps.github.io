"""道用（daoApps）站点契约测试。

校验四件事：
1. 组织主页的仓库清单与分组计数正确（14 个仓库 / 5 类用法）；
2. 结伴子站的页面与六条公约内容齐备；
3. `conf.py` 的「版本身份证」构建期守卫真的会拦截未标注版本的引文
   （防止守卫写成永不触发的装饰品）；
4. 页脚合规声明只挂在 /jieban/ 下，不上组织主页。

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