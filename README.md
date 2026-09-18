# daoApps.github.io

> **道用（daoApps）组织站点** —— Sphinx + MyST 静态站，GitHub Actions 构建并发布。
> 线上：<https://daoapps.github.io/>

本仓库是站点的**源码仓库**，不是产物仓库。`_build/` 由 CI 每次重建，不入库。

## 站点结构

| 路由 | 源文件 | 内容 |
|---|---|---|
| `/` | `doc/index.md` | 组织主页：印章首屏 → 子站点入口 → 定位 → 14 个仓库 / 5 类用法 → 收录说明 |
| `/jieban/` | `doc/jieban/index.md` | 结伴：品牌首页（六屏长卷） |
| `/jieban/origin.html` | `doc/jieban/origin.md` | 缘起：四个群，一间客厅 |
| `/jieban/covenant.html` | `doc/jieban/covenant.md` | 社群公约：六条底线 + 引文版本说明 |
| `/jieban/channels/*.html` | `doc/jieban/channels/*.md` | 四频道详情：知足 / 恒与 / 知和 / 愈多 |

## 目录结构

```
daoApps.github.io/
├── .github/workflows/pages.yml   gates（契约测试 + actionlint）→ build（Sphinx -W）→ deploy
├── AGENTS.md                     智能体入口：任务路由表 + 各类纪律
├── requirements.txt              构建依赖
├── doc/                          站点源目录（唯一事实来源）
│   ├── conf.py                   Sphinx 配置 + 构建期守卫 + 按页页脚
│   ├── index.md                  组织主页
│   ├── jieban/                   结伴子站
│   └── _static/{dao.css,dao.js}  全站样式与渐进增强行为层
├── tests/test_site_contract.py   站点契约测试
└── _build/                       构建产物（gitignored）
```

## 构建与本地预览

```bash
python -m pip install -r requirements.txt

# 契约测试
python -m pytest tests -q

# 构建（-W：警告即失败）
python -m sphinx -b html -d _build/doctrees --keep-going -W doc _build/html

# 本地预览
python -m http.server -d _build/html 8931
```

## 发布

推送到 `main` 触发 `.github/workflows/pages.yml`：

1. **gates** —— actionlint 校验 workflow YAML；跑站点契约测试；
2. **build** —— `python -m sphinx -W` 构建，上传 Pages 产物；
3. **deploy** —— `actions/deploy-pages@v5` 发布到 GitHub Pages。

> 仓库 Settings → Pages 的 Source 必须是 **GitHub Actions**（不是分支）。
> 若仍是「Deploy from a branch」，部署 job 会失败。

## 内容纪律（摘要）

完整纪律见 [AGENTS.md](AGENTS.md)，要点：

- 组织主页清单的唯一事实来源是 `daoApps/daoNexus` 的 `src/data/apps.ts`；本页是超集，共 14 个仓库 / 5 类用法，计数由测试守护。
- 结伴站的引文版本身份证是**构建期硬约束**：出现「己愈多」必须同页出现「帛书乙本」，出现「知和曰明」必须同页出现「帛书甲本」。
- 「结伴」二字不见于今本与帛书本《老子》原文，站点不宣称其典出《道德经》。
- 内部群昵称不上公开页；结伴站不设表单、不收集信息。
- 页脚分两层：全站层（组织入口）+ 合规层（仅 `/jieban/` 下）。

## 技术选型说明

- **主题**：`sphinx_book_theme`（阅读优先）。原选型报告写的是 furo 定制为纸感，但构建环境未装 furo，改用同为阅读优先、纸感定制成本更低的 book 主题。
- **纸感 token**：暖灰纸面 `--paper` / 米白卡片 `--card` / 深灰褐文字 `--ink` + 朱砂 `--cinnabar` 与黛 `--dai`。明确不要深色模式。
- **MyST**：`colon_fence` / `substitution` / `attrs_inline` 等；正文用 MyST，组件化版块（卡片网格、印章首屏）用 raw HTML + CSS 类，与结伴站既有写法一致。
- **Mermaid**：由 `sphinxcontrib-mermaid` 渲染，版本固定 11.4.1；缘起页的图**前端从 CDN 加载**，离线打开只显示图表源码。
- **样式特异性**：`pydata-sphinx-theme` 的 `--pst-color-*` 定义在 `html[data-theme="light"]` 上，只写 `:root` 会被盖掉；sphinx-design 自带 Bootstrap 定义了 `.card` / `.btn` / `.lead`，组织主页规则统一用 `article.bd-article .org-home` 前缀抬高特异性。