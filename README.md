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
├── pyproject.toml                依赖分组（docs / test / dev）
├── .readthedocs.yml              Read the Docs 构建配置（第二发布通道）
├── doc/                          站点源目录（唯一事实来源）
│   ├── conf.py                   Sphinx 配置 + 构建期守卫 + 按页页脚
│   ├── index.md                  组织主页
│   ├── jieban/                   结伴子站
│   ├── _static/{dao.css,dao.js,switcher.json}  全站样式、渐进增强行为层、通道切换清单
├── tests/test_site_contract.py   站点契约测试
└── _build/                       构建产物（gitignored）
```

## 构建与本地预览

```bash
python -m pip install "pip>=25.1"
python -m pip install --group dev

# 契约测试
python -m pytest tests -q

# 构建（-W：警告即失败）
python -m sphinx -b html -d _build/doctrees --keep-going -W doc _build/html

# 本地预览
python -m http.server -d _build/html 8931
```

依赖采用与玄境相同的标准 `[dependency-groups]` 分组：`docs` 用于构建，
`test` 用于契约测试，`dev` 组合前两组而不重复声明。只构建站点可用
`python -m pip install --group docs`；本仓库仍不构建 Python 发行包，
不需要 `pip install .`，也不强制使用 PDM。

## 发布

推送到 `main` 触发 `.github/workflows/pages.yml`：

1. **gates** —— actionlint 校验 workflow YAML；跑站点契约测试；
2. **build** —— `python -m sphinx -W` 构建，上传 Pages 产物；
3. **deploy** —— `actions/deploy-pages@v5` 发布到 GitHub Pages。

> 仓库 Settings → Pages 的 Source 必须是 **GitHub Actions**（不是分支）。
> 若仍是「Deploy from a branch」，部署 job 会失败。

## 发布（第二通道）：Read the Docs

同一份 `doc/` 源另由 Read the Docs 构建，配置见 `.readthedocs.yml`：

| 配置项 | 取值 | 理由 |
|---|---|---|
| `build.tools.python` | `3.14` | 与 CI 的 `setup-python` 对齐，避免只在一边复现的构建差异 |
| `sphinx.configuration` | `doc/conf.py` | 源目录是 `doc/`（单数），不在 RTD 默认探测的 `docs/`，必须写死 |
| `sphinx.fail_on_warning` | `true` | 等价 CI 的 `-W --keep-going`，平台侧不放宽质量门 |
| `formats` | 仅 `htmlzip` | `pdf` 走 latex builder（默认 pdflatex 不认中文），`epub` 要求 conf.py 有 `version`（本站无版本号），两者均会失败 |
| `build.jobs.pre_install` | 升级至 `pip>=25.1` 后安装 `--group docs` | 与本地、CI 共用 pyproject.toml；本站不构建 Python 发行包，不执行 `pip install .` |

> **平台侧必做（一次性）**：RTD 项目 Admin → Settings → **Language 选 Simplified Chinese**。
> RTD 构建时用 `-D language=<平台语言>` 覆盖 `conf.py` 的 `language`，平台留在默认英文会让
> 中文分词（jieba）静默失效——构建一条警告都不报，只是中文搜不到。
> `doc/conf.py` 的 `_check_rtd_language` 守卫会直接把这种构建打红，不会让它悄悄上线。

## 通道切换按钮

左侧栏底部有一个下拉按钮，让读者在两条通道间跳到**同一页**（目标页不存在时自动回退到该通道首页）。
实现是 pydata 系主题（`sphinx_book_theme` 继承 `pydata_sphinx_theme`）内置的 version-switcher，
本站只用它承载「通道」而非「版本」：

| 环节 | 落点 | 说明 |
|---|---|---|
| 清单 | `doc/_static/switcher.json` | 两条目：`gh-pages`→GitHub Pages、`rtd`→Read the Docs。基址必须**以 `/` 结尾**——前端拼的是「基址 + 当前页路径」 |
| 数据源 | `conf.py` 的 `switcher.json_url` | 必须用**相对路径** `_static/switcher.json`。换成 http(s) 绝对 URL 后，pydata 会在构建期对它发 HTTP 请求校验，读不到即 warning，本站 `-W`（RTD 侧 `fail_on_warning`）会直接构建失败；且首次部署前该文件尚不存在，必然自举死锁 |
| 当前通道 | `conf.py` 的 `switcher.version_match` | 按构建环境分流：RTD 构建（带 `READTHEDOCS`）→ `rtd`，其余（GitHub Actions / 本地预览）→ `gh-pages`。同一份 HTML 部署到两处，页面自己认不出身在何处 |
| 挂载点 | `conf.py` 的 `primary_sidebar_end` | 取 `["version-switcher", "sidebar-ethical-ads"]`；主题默认只有后者，覆盖时把它带上，免得顺手砍掉 RTD 侧的伦理广告位 |

> RTD 项目 slug 是 `daoappsgithubio`——RTD 按仓库名 `daoapps.github.io` **自动派生**（不是 `daoapps`，
> 后者实测打开是 404 Project not found），故站点基址为 `https://daoappsgithubio.readthedocs.io/zh-cn/latest/`。
> 清单里只写这个**裸基址**（以 `/` 结尾），别把浏览器地址栏里的 `index.html` 一起抄进来：
> 前端拼的是「基址 + 当前页路径」，多一段 `index.html` 会拼出坏 URL。

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
