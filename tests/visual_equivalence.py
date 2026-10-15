"""道用站点「改前 / 改后」视觉等价性比对工具（按需运行，非 pytest 用例）。

为什么要有它
------------
本页的版式知识大量寄居在 CSS 与生成 DOM 的耦合上：卡片、网格、页脚、淡入动效
分别由 dao.css、sphinx-design、dao.js 三方共同决定。改动其中一方（例如把卡片从
`<a class="card">` 换成 sphinx-design 生成的 `.sd-card`）时，**绝大多数回归都不会
报错**——页面照样能开、照样能点，只是悄悄少了几像素内边距、掉了一行动效。静态
断言（`tests/test_site_contract.py`）只能守住源码字面量，守不住渲染结果。

这个工具把「改前 / 改后」两份产物同时构建出来，再在真实浏览器里逐项对拍：
几何（文档坐标，容差 0.5px）、计算样式、14 张卡片的盒子、整卡可点的命中测试、
渲染文本 / 链接目标 / 字体栈、整页截图的像素强度分布。

判 FAIL 的只有「结构性差异」：数量/几何/样式/链接目标不一致，或高强度的像素差
超过容许预算。文字抗锯齿级的低强度噪声、以及 flex 容器里不参与渲染的空白文本
（innerText 会把它算进去）只报 WARN。Mermaid 图与滚动淡入是异步且有状态的，
所以工具会**把基线连拍两次**得到「噪声地板」，改前改后的像素差只与地板比较，
不直接判零——否则会把异步渲染的抖动当成回归。

用法
----
    # 与 HEAD（即上次提交）比：确认工作区改动没有视觉副作用
    python tests/visual_equivalence.py

    # 与某个历史提交比（例：复核一次版式重构）
    python tests/visual_equivalence.py --baseline HEAD~1 --pages index.html

    # 全站扫一遍，检查有没有改动外溢到别的页面
    python tests/visual_equivalence.py --pages all --widths 768,1280

前置依赖：Sphinx 构建依赖（requirements.txt）+ Playwright（`pip install playwright`）。
Playwright 自带浏览器未下载时会自动回退到系统已装的 Edge / Chrome。

退出码：0 全绿；1 有 FAIL 项；2 环境不就绪（依赖或浏览器缺失）。
"""

import argparse
import io
import pathlib
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[1]
DOC = REPO / "doc"

# 逻辑探针 → 候选选择器（取首个命中的）。
# 同一处版式在不同版本可能换了生成方式（卡片由 `<a class="card">` 变成
# sphinx-design 的 `.sd-card`），两代选择器并列，工具便不绑死某一代习语；
# 命中的那一代会打印出来，比对结果才可解释。
PROBES = {
    "seal": (".org-home .seal",),
    "quote": (".org-home .quote",),
    "cta_box": (".org-home .cta",),
    "cta_btn": (".org-home .cta p a", ".org-home .cta a.btn"),
    "subsite": (".org-home .subsite",),
    "manifesto": (".org-home .manifesto",),
    "group": (".org-home .group",),
    "group_head": (".org-home .group-head",),
    "grid": (".org-home .cards .sd-row", ".org-home .cards"),
    "card": (".org-home .cards .sd-card", ".org-home .cards .card"),
    "card_title": (".org-home .cards .sd-card .sd-card-title", ".org-home .cards .card .name"),
    "card_repo": (".org-home .cards .repo",),
    "card_desc": (".org-home .cards .sd-card .sd-card-text:last-child", ".org-home .cards .card .desc"),
    "card_reveal": (".org-home .cards .sd-card.jb-reveal", ".org-home .cards .card.jb-reveal"),
    "hero": (".org-home .hero",),
    "lead": (".org-home .lead",),
    "h2": (".org-home h2",),
    "org_note": (".org-home .org-note",),
    "reveal_all": (".jb-reveal",),
}

DEFAULT_PAGES = ["index.html"]
DEFAULT_WIDTHS = [375, 768, 1280]

# 几何容差：亚像素级的位置差（字体度量抖动）不算回归
BOX_TOL = 0.5
# 像素判据：只认高强度差（抗锯齿噪声集中在 <64），且与噪声地板比较
HARD_LEVEL = 64
HARD_BUDGET = 200

# 采集前注入的样式：滚动淡入是有状态的（命中元素位移 12px、透明到不透明），
# 不中和它，两次采集的几何就没有可比性。淡入覆盖面另由 card_reveal 计数守护。
NEUTRALISE = """
() => {
  const st = document.createElement("style");
  st.textContent = ".jb-reveal, .jb-reveal.jb-in { transform: none !important;"
    + " opacity: 1 !important; transition: none !important; }";
  document.head.appendChild(st);
}
"""

MEASURE = """
(cfg) => {
  const rnd = (v) => Math.round(v * 100) / 100;
  const sx = window.scrollX, sy = window.scrollY;
  const resolved = {}, counts = {}, styles = {}, boxes = {};

  for (const [key, cands] of Object.entries(cfg.probes)) {
    const sel = cands.find((s) => document.querySelector(s));
    resolved[key] = sel || null;
    const nodes = sel ? [...document.querySelectorAll(sel)] : [];
    counts[key] = nodes.length;
    boxes[key] = nodes.map((e) => {
      const r = e.getBoundingClientRect();
      return { x: rnd(r.x + sx), y: rnd(r.y + sy), w: rnd(r.width), h: rnd(r.height) };
    });
    const e = nodes[0];
    if (e) {
      const r = e.getBoundingClientRect(), s = getComputedStyle(e);
      styles[key] = {
        rect: { x: rnd(r.x + sx), y: rnd(r.y + sy), w: rnd(r.width), h: rnd(r.height) },
        display: s.display, padding: s.padding, margin: `${s.marginTop}/${s.marginBottom}`,
        radius: s.borderTopLeftRadius, border: `${s.borderTopWidth} ${s.borderTopColor}`,
        shadow: s.boxShadow, fontWeight: s.fontWeight, fontSize: s.fontSize,
        lineHeight: s.lineHeight, color: s.color, letterSpacing: s.letterSpacing,
        background: s.backgroundColor, gridCols: s.gridTemplateColumns, gap: s.gap,
      };
    }
  }

  // 整卡可点：卡片内多点命中测试（elementFromPoint 只在视口内有效，须先滚进来）
  const card = document.querySelector(resolved.card || "");
  const hits = [];
  if (card) {
    card.scrollIntoView({ block: "center" });
    const r = card.getBoundingClientRect();
    for (const [at, x, y] of [
      ["center", r.left + r.width / 2, r.top + r.height / 2],
      ["left_bar", r.left + 4, r.top + r.height / 2],
      ["bottom_right", r.right - 6, r.bottom - 6],
      ["top", r.left + r.width / 2, r.top + 3],
    ]) {
      const el = document.elementFromPoint(x, y);
      const a = el && el.closest("a");
      hits.push({ at, href: a ? a.getAttribute("href") : null });
    }
    window.scrollTo(0, 0);
  }

  // 渲染文本 / 链接目标 / 字体栈。拉伸链接里那段 font-size:0 的可访问名
  // 属于新增的无障碍文本，不算可见内容，比对前摘掉。
  const root = document.querySelector(".org-home");
  const norm = (s) => s.replace(/\\s+/g, " ").trim();
  const clone = root.cloneNode(true);
  clone.querySelectorAll(".sd-stretched-link").forEach((el) => el.remove());

  return {
    resolved, counts, boxes, styles, hits,
    text: norm(clone.innerText),
    links: [...root.querySelectorAll("a")].map((a) => a.getAttribute("href")),
    fonts: [...new Set([...root.querySelectorAll("*")].map((e) => getComputedStyle(e).fontFamily))],
  };
}
"""


# -- 构建 -------------------------------------------------------------------


def git_archive(ref: str, dest: pathlib.Path) -> None:
    """把某个提交的整棵树导出到 dest（用 tarfile 解，不依赖外部 tar）。"""
    proc = subprocess.run(
        ["git", "-C", str(REPO), "archive", "--format=tar", ref],
        capture_output=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"git archive {ref} 失败：{proc.stderr.decode('utf-8', 'replace')}")
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as tar:
        # filter="data"：只取普通文件与目录，且不保留可疑元数据（3.14 起为默认，
        # 这里显式声明，免得依赖版本行为并触发弃用告警）。
        tar.extractall(dest, filter="data")


def build(src_doc: pathlib.Path, out: pathlib.Path, doctrees: pathlib.Path) -> list[str]:
    """`-q -b html` 构建，返回警告行（不设 -W：门禁由 pytest/CI 负责，此处只管产物）。"""
    proc = subprocess.run(
        [sys.executable, "-m", "sphinx", "-b", "html", "-q", "--keep-going",
         "-d", str(doctrees), str(src_doc), str(out)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        raise SystemExit(f"Sphinx 构建失败（{src_doc}）：\n{proc.stdout}\n{proc.stderr}")
    return [ln for ln in (proc.stderr or "").splitlines() if "WARNING" in ln or "ERROR" in ln]


# -- 采集 -------------------------------------------------------------------


def launch(playwright):
    """优先用系统已装的 Edge / Chrome，避免非要下载 Playwright 自带浏览器。"""
    last = None
    for channel in ("msedge", "chrome", None):
        try:
            return playwright.chromium.launch(channel=channel) if channel else playwright.chromium.launch()
        except Exception as exc:  # noqa: BLE001
            last = exc
    raise SystemExit(
        f"无法启动浏览器（{last}）。请先 `pip install playwright` 并 "
        "`playwright install chromium`，或确保本机已装 Edge / Chrome。"
    )


def capture(page, url: str, shot: pathlib.Path) -> dict:
    """加载 → 等 Mermaid 画完 → 中和淡入 → 采样 → 存整页截图。"""
    page.goto(url)
    page.wait_for_load_state("load")
    try:
        page.wait_for_function(
            "() => document.querySelectorAll('pre.mermaid').length"
            " === document.querySelectorAll('pre.mermaid[data-processed]').length",
            timeout=15000,
        )
    except Exception:  # noqa: BLE001 - 无 Mermaid 或渲染超时都继续，交给噪声地板兜底
        pass
    page.wait_for_timeout(500)
    page.evaluate(NEUTRALISE)
    page.wait_for_timeout(120)
    data = page.evaluate(MEASURE, {"probes": {k: list(v) for k, v in PROBES.items()}})
    page.screenshot(path=str(shot), full_page=True)
    return data


# -- 比对 -------------------------------------------------------------------


def diff_probes(base: dict, new: dict, report: list[str], fail: list[str], warn: list[str]) -> None:
    generations = {k: (base["resolved"].get(k), new["resolved"].get(k)) for k in PROBES}
    switched = {k: v for k, v in generations.items() if v[0] != v[1]}
    for key, (b, n) in switched.items():
        report.append(f"    · 探针 {key} 换了生成方式：{b} → {n}")

    for key in PROBES:
        cb, cn = base["counts"][key], new["counts"][key]
        if cb == 0 and cn == 0:
            continue
        if cb != cn:
            fail.append(f"{key} 数量 {cb} → {cn}")
            continue
        fb, fn = base["styles"].get(key), new["styles"].get(key)
        if not fb or not fn:
            continue
        rect_delta = [f"{p}:{fb['rect'][p]}→{fn['rect'][p]}" for p in ("x", "y", "w", "h")
                      if abs(fb["rect"][p] - fn["rect"][p]) > BOX_TOL]
        if rect_delta:
            fail.append(f"{key} 几何偏移 " + ", ".join(rect_delta))
        for prop in ("display", "padding", "margin", "radius", "border", "shadow", "fontWeight",
                     "fontSize", "lineHeight", "color", "letterSpacing", "background",
                     "gridCols", "gap"):
            if fb[prop] != fn[prop]:
                fail.append(f"{key}.{prop} {fb[prop]!r} → {fn[prop]!r}")

    # 逐张卡片盒子：数量对不上之外，位置尺寸也要逐一相等
    cb, cn = base["boxes"]["card"], new["boxes"]["card"]
    if len(cb) == len(cn):
        bad = [(i, b, n) for i, (b, n) in enumerate(zip(cb, cn))
               if any(abs(b[p] - n[p]) > BOX_TOL for p in ("x", "y", "w", "h"))]
        if bad:
            fail.append(f"{len(bad)}/{len(cb)} 张卡片盒子不一致，例：#{bad[0][0]} {bad[0][1]} → {bad[0][2]}")
        else:
            report.append(f"    · {len(cb)} 张卡片盒子逐张一致")
    elif cb or cn:
        fail.append(f"卡片盒子数量 {len(cb)} → {len(cn)}")

    hb, hn = base["hits"], new["hits"]
    if hb and hn:
        if [h["href"] for h in hb] == [h["href"] for h in hn]:
            report.append(f"    · 整卡可点：{len(hb)} 个采样点命中同一链接")
        else:
            fail.append(f"整卡可点命中不同：{[h['href'] for h in hb]} → {[h['href'] for h in hn]}")


def diff_text(base: dict, new: dict, report: list[str], fail: list[str], warn: list[str]) -> None:
    if base["links"] != new["links"]:
        fail.append(f"链接目标不一致（{len(base['links'])} vs {len(new['links'])} 个）")
    else:
        report.append(f"    · {len(base['links'])} 个链接目标一致")
    if base["fonts"] != new["fonts"]:
        warn.append(f"字体栈不一致：{base['fonts']} → {new['fonts']}")
    if base["text"] == new["text"]:
        report.append("    · 渲染文本逐字一致")
    elif re.sub(r"\s+", "", base["text"]) == re.sub(r"\s+", "", new["text"]):
        warn.append("渲染文本只差空白（多为 flex 容器内不参与渲染的换行空白，innerText 会计入）")
    else:
        import difflib

        a, b = base["text"], new["text"]
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != "equal":
                fail.append(f"渲染文本差异 [{tag}] {a[max(0, i1 - 12):i2 + 12]!r} → {b[max(0, j1 - 12):j2 + 12]!r}")


def pixel_stats(a_path: pathlib.Path, b_path: pathlib.Path) -> dict:
    from PIL import Image, ImageChops

    a, b = Image.open(a_path).convert("RGB"), Image.open(b_path).convert("RGB")
    if a.size != b.size:
        return {"size_mismatch": f"{a.size} vs {b.size}"}
    d = ImageChops.difference(a, b).convert("L")
    hist = d.histogram()
    total = a.size[0] * a.size[1]
    return {
        "max": max(i for i, n in enumerate(hist) if n),
        "over8": sum(hist[9:]),
        "hard": sum(hist[HARD_LEVEL + 1:]),
        "total": total,
    }


# -- 主流程 -----------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description="道用站点改前/改后视觉等价性比对")
    ap.add_argument("--baseline", default="HEAD", help="基线 git 版本（默认 HEAD）")
    ap.add_argument("--pages", default=",".join(DEFAULT_PAGES),
                    help="页面列表（构建产物相对路径），或 all 表示全部页面")
    ap.add_argument("--widths", default=",".join(str(w) for w in DEFAULT_WIDTHS))
    ap.add_argument("--shots", help="截图落盘目录（默认临时目录，比对后删除）")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("缺少 Playwright：pip install playwright && playwright install chromium", file=sys.stderr)
        return 2

    widths = [int(w) for w in args.widths.split(",")]
    keep = pathlib.Path(args.shots).resolve() if args.shots else None
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="dao-visual-"))
    shots = keep or tmp / "shots"
    shots.mkdir(parents=True, exist_ok=True)

    try:
        print(f"[构建] 基线 {args.baseline} → 当前工作区")
        git_archive(args.baseline, tmp / "base")
        base_warn = build(tmp / "base" / "doc", tmp / "base-html", tmp / "base-ud")
        new_warn = build(DOC, tmp / "new-html", tmp / "new-ud")

        pages = sorted(p.relative_to(tmp / "new-html").as_posix()
                       for p in (tmp / "new-html").glob("**/*.html")
                       if p.name not in ("genindex.html", "search.html"))
        if args.pages != "all":
            pages = [p if p.endswith(".html") else p + ".html" for p in args.pages.split(",")]
        print(f"[采集] {len(pages)} 页 × {len(widths)} 档宽度（基线连拍两次估噪声地板）")

        fails: list[str] = []
        warns: list[str] = list(base_warn + new_warn)
        with sync_playwright() as pw:
            browser = launch(pw)
            for width in widths:
                page = browser.new_page(viewport={"width": width, "height": 900})
                for rel in pages:
                    # 截图名不带 .html 后缀：Playwright 会按扩展名推断图片类型，
                    # 见到 .html 会当作 text/html 而拒绝。
                    tag = pathlib.Path(rel).with_suffix("").as_posix().replace("/", "_")
                    b1 = capture(page, (tmp / "base-html" / rel).as_uri(), shots / f"base1-{width}-{tag}.png")
                    b2 = capture(page, (tmp / "base-html" / rel).as_uri(), shots / f"base2-{width}-{tag}.png")
                    nn = capture(page, (tmp / "new-html" / rel).as_uri(), shots / f"new-{width}-{tag}.png")

                    local_fail: list[str] = []
                    local_warn: list[str] = []
                    report: list[str] = []
                    if rel == "index.html":
                        diff_probes(b1, nn, report, local_fail, local_warn)
                        diff_text(b1, nn, report, local_fail, local_warn)

                    p1 = shots / f"base1-{width}-{tag}.png"
                    p2 = shots / f"base2-{width}-{tag}.png"
                    pn = shots / f"new-{width}-{tag}.png"
                    floor = pixel_stats(p1, p2)
                    delta = pixel_stats(p1, pn)
                    if delta.get("size_mismatch") or floor.get("size_mismatch"):
                        local_fail.append(
                            f"整页高度变化：噪声地板 {floor.get('size_mismatch', '一致')}；"
                            f"改前改后 {delta.get('size_mismatch', '一致')}"
                        )
                    elif delta["hard"] > floor["hard"] + HARD_BUDGET:
                        local_fail.append(
                            f"像素差超出噪声地板：高强度像素 {delta['hard']} > 地板 {floor['hard']} "
                            f"+ 预算 {HARD_BUDGET}（最大单像素差 {delta['max']}）"
                        )
                    else:
                        report.append(
                            f"    · 像素：最大差 {delta['max']}，高强度 {delta['hard']} 个"
                            f"（噪声地板 {floor['hard']}），低强度占比 {delta['over8'] / delta['total']:.3%}"
                        )

                    head = f"[{width}] {rel}"
                    if local_fail:
                        fails += [f"{head} {m}" for m in local_fail]
                    warns += [f"{head} {m}" for m in local_warn]
                    print(head + ("  ✗" if local_fail else "  ✓"))
                    for line in report:
                        print(line)
                    for m in local_fail:
                        print(f"    ✗ {m}")
                    for m in local_warn:
                        print(f"    ⚠ {m}")
                page.close()
            browser.close()

        print("\n" + "=" * 60)
        if fails:
            print(f"结论：✗ {len(fails)} 项结构性差异")
            for m in fails:
                print(f"  - {m}")
        else:
            print("结论：✓ 未发现结构性差异（数量/几何/样式/链接/可点区域/像素强度均等价）")
        if warns:
            print(f"另有 {len(warns)} 项提示（不作为失败）：")
            for m in warns[:12]:
                print(f"  - {m}")
        if keep:
            print(f"\n截图留存：{shots}")
        return 1 if fails else 0
    finally:
        if not keep:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
