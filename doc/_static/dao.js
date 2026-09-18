/* 道用 · daoApps 站点行为层
 *
 * 做两件事：
 *   1. 滚动淡入（IntersectionObserver），与落地页 .reveal 的节奏一致；
 *      纯渐进增强——JS 未执行时内容完整可见，只是没有入场动效。
 *   2. 侧栏开关的行为补绑（见文件末尾：主题渲染了两份同名开关，脚本只认第一个）。
 *
 * 本文件由 Sphinx 注入 <head>（`<meta name="viewport">` 之前），且没有 defer：
 * 执行到这里时 <body> 还没开始解析，任何 querySelector 都返回空。此时若照常跑，
 * 代码会静默短路——不生效，也不报错，只是「什么都没发生」。所以两个动作都挂在
 * domReady 之后（见下）。
 *
 * 曾在此注入「印章 + 品牌 + 菜单」顶栏：那是拆掉左侧栏后的补救。
 * 侧栏已恢复（品牌与主导航本就挂在左侧栏内），注入即重复，故移除。
 *
 * 刻意不做：落地页的频道选择器与入群弹窗——结伴站一期公开承诺「不设表单、不收集信息」，
 * 引入它们会与公约页自相矛盾（见 tests/test_site_contract.py 的相应断言）。
 */
/* DOM 就绪闸门：脚本在 <head> 里同步执行，早于 <body> 的存在。
 * 已经就绪（脚本被改成 defer、或将来移到页脚）时立即执行，不做无谓等待。 */
function domReady(fn) {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fn, { once: true });
  } else {
    fn();
  }
}

domReady(function () {
  "use strict";

  var REVEAL_SEL = [
    // 组织主页（doc/index.md）
    ".org-home .seal",
    ".org-home .card",
    ".org-home .manifesto",
    ".org-home .subsite-card",
    // 结伴子站（doc/jieban/**）
    ".jb-seal",
    ".jb-sub",
    ".jb-quote",
    ".jb-cta",
    ".jb-manifesto",
    ".jb-card",
    ".jb-rules",
    ".jb-origin-grid",
    ".jb-federal",
    ".jb-timeline",
    ".jb-choices",
    ".jb-privacy",
    // 通用正文元素
    "article.bd-article h2",
    "table",
    "pre.mermaid",
  ].join(",");

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("jb-in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    document.querySelectorAll(REVEAL_SEL).forEach(function (el) {
      el.classList.add("jb-reveal");
      io.observe(el);
    });
  }
});

/* 侧栏开关：把行为补到用户真正点得着的那一份上
 *
 * 主题把两侧的开关各渲染两份，且两套脚本都用
 * `document.querySelector(".primary-toggle")` 只认 DOM 里第一个：
 *   · header.bd-header 里一份 —— 位于文档更前，故被脚本选中；
 *     但它被主题自己的样式隐去（book 主题把开关搬到了正文栏，
 *     见 sphinx_book_theme 的 _header-primary.scss），用户看不见也点不着；
 *   · .bd-header-article 里一份 —— 用户实际看到的那个，反而没有任何绑定。
 * 表现就是：宽屏点不出折叠，窄屏也唤不出抽屉，且控制台无报错。
 *
 * 这里不重写折叠逻辑（宽屏切 pst-sidebar-hidden、窄屏开 dialog 各有一套），
 * 只把可见开关的点击转发给主题已经绑定过的那个节点，把两份重新对齐。
 * 捕获阶段加 stopImmediatePropagation，是为了主题将来若改为绑定可见开关时
 * 不出现「一次点击折叠两次」；若主题某天不再渲染顶栏那份，这里自行短路。
 */
domReady(function bindVisibleSidebarToggles() {
  "use strict";

  ["primary", "secondary"].forEach(function (kind) {
    var hidden = document.querySelector("header.bd-header ." + kind + "-toggle");
    var shown = document.querySelector(".bd-header-article ." + kind + "-toggle");

    if (!hidden || !shown || hidden === shown) {
      return;
    }

    shown.addEventListener(
      "click",
      function (event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        hidden.click();
      },
      true
    );
  });
});