"""真实构建守护：设计文档可导航，Mermaid 围栏生成图节点而非高亮代码。"""

import os
from pathlib import Path
import re
import subprocess
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_DIR = REPO_ROOT / "doc"
DESIGN_DIRS = (DOC_DIR / "jieban" / "design", DOC_DIR / "xuexi" / "design")


@pytest.mark.parametrize("builder", ["html", "singlehtml"])
def test_site_builds_without_warnings(builder, tmp_path):
    """CI 与 RTD 对应的构建都不能靠告警抑制来通过。"""
    output = tmp_path / builder
    env = os.environ.copy()
    # 本测试验证本地构建；平台语言和通道分流由站点契约测试单独守护。
    env.pop("READTHEDOCS", None)
    env.pop("READTHEDOCS_LANGUAGE", None)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
            "-b",
            builder,
            "-d",
            str(tmp_path / "doctrees"),
            "--keep-going",
            "-W",
            "-q",
            str(DOC_DIR),
            str(output),
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "WARNING:" not in result.stderr, result.stderr

    if builder == "html":
        for directory in DESIGN_DIRS:
            for source in directory.rglob("*.md"):
                target = output / source.relative_to(DOC_DIR).with_suffix(".html")
                assert target.is_file(), f"设计文档未生成：{source}"
                html = target.read_text(encoding="utf-8")
                expected = len(re.findall(r"^```mermaid\s*$", source.read_text(encoding="utf-8"), re.M))
                actual = len(re.findall(r'<pre\b[^>]*class="[^"]*\bmermaid\b', html))
                assert actual == expected, f"{source.name}: 图节点 {actual}，源码围栏 {expected}"
        for section in ("jieban", "xuexi"):
            html = (output / section / "index.html").read_text(encoding="utf-8")
            assert 'href="design/index.html"' in html, f"{section} 缺少设计文档入口"
