# 道用 · daoApps 站点（AGENTS Manifest）

> **启动协议（PRIORITY ZERO）**
>
> ```
> 步骤 1：读取本文件全文
> 步骤 2：按「任务路由表」确定本次任务需要读取的规范
> 步骤 3：改内容 → doc/ 下的 Markdown；改样式 → doc/_static/dao.css
> 步骤 4：本地跑通门禁（pytest + sphinx -W）后才提交
> ```

## 项目性质

本仓库是 **daoapps.github.io 的源码仓库**，不是构建产物的存放地。

| 项 | 说明 |
|---|---|
| 站点根 | `doc/index.md` → `https://daoapps.github.io/`（组织主页） |
| 子站 | `doc/jieban/index.md` → `https://daoapps.github.io/jieban/`（结伴） |
| 源格式 | MyST Markdown（Sphinx），`source_suffix = {".md": "markdown"}` |
| 发布 | GitHub Actions 构建 → `actions/deploy-pages`（见 `.github/workflows/pages.yml`） |
| 第二通道 | Read the Docs（`.readthedocs.yml`，同源 `doc/`，仅出 htmlzip） |
| 产物 | `_build/`，**不入库**（`.gitignore` 已排除） |

**禁止**把 `_build/html` 的产物提交进本仓库：仓库承载源码，产物由每次 push 重新构建。

## 任务路由表

| 任务 | 落点 | 必读 |
|---|---|---|
| 增删应用条目 / 改分组 | `doc/index.md` | 本文件「组织主页纪律」 |
| 改结伴文案 | `doc/jieban/**/*.md` | 本文件「结伴内容纪律」 |
| 改全站配色 / 版式 | `doc/_static/dao.css` | 本文件「样式纪律」 |
| 改站点结构 / 页脚 / 构建守卫 | `doc/conf.py` | 本文件「构建期守卫」 |
| 改构建发布流程 | `.github/workflows/pages.yml` | `projects/awesome-okf-xs/.github/workflows/pages.yml`（同族模板） |
| 改 RTD 构建配置 / 平台语言 | `.readthedocs.yml` + `doc/conf.py`（`_check_rtd_language`） | 本文件「Read the Docs 构建纪律」 |
| 改通道切换按钮 / 清单 | `doc/_static/switcher.json` + `doc/conf.py`（`switcher` / `primary_sidebar_end`） | 本文件「Read the Docs 构建纪律」 |
| 改内容契约 | `tests/test_site_contract.py` | 先改测试再改内容，或同步改 |

## 组织主页纪律

- **仓库清单的唯一事实来源**是 `daoApps/daoNexus` 的 `src/data/apps.ts`；该文件只覆盖前端的
  9 个应用，组织主页是超集（另含支付与链路 3 个、系统与基座 4 个），共 **14 个仓库 / 5 类用法**。
- 分组标题 `<h3>`、计数 `<span class="count">`、卡片 `<a class="card">` 三者必须自洽，
  由 `tests/test_site_contract.py` 断言（`counts == [2, 3, 2, 3, 4]` 且卡片总数 14）。
- 空仓库（如 `dao-research-assistant`）只在收录说明里点名「筹备中」，**不列入卡片**。

## 结伴内容纪律

- **「结伴」二字不见于今本与帛书本《老子》原文**——站点不宣称其典出《道德经》。
  主名不背经典，slogan 与频道名承经义。
- 末章短引文一律用「既以予人矣，己愈多」（帛书乙本独见面貌）；甲本此句损掩。
- 「恒与善人」的帛书铁证是「恒」字（今本避汉文帝刘恒讳作「常」）。
- 「知和曰明」仅见帛书甲本，今本作「知常曰明」。
- 正式印刷前引文须再对勘高明《帛书老子校注》或文物出版社整理本。
- 内部群昵称（感恩小队 / 民政局小分队 / 玩转 AI 变现）**不上公开页**，站点只用频道名
  （知足 / 恒与 / 知和 / 愈多），由测试守护。
- 一期**不设任何表单、不收集信息**，加入途径统一写「微信端向管理员申请邀请」；
  源码中不得出现 `<form>` 或弹窗标记（有测试断言）。

## 构建期守卫

`doc/conf.py` 在 `config-inited` 阶段检查两条正向不变量——**引文出现在哪，版本标识就必须跟到哪**：

1. 页面出现末章短引文「己愈多」→ 必须同时出现「帛书乙本」
2. 页面出现「知和曰明」→ 必须同时出现「帛书甲本」

不满足则构建直接失败。这是把「截断引用冒充帛书面貌」的陷阱变成机器可拦截的约束——
引文合规不靠人记得，靠构建卡住。

「禁止笼统称帛书本」这条纪律以文字条款写在 `jieban/covenant.md`，**不**纳入自动检查：
公约页本身要引用这条规则，机械匹配必然误伤。

页脚分两层：全站层（组织入口）挂在所有页面；合规层（「本站不提供任何婚恋中介或投资理财服务」）
只挂在 `/jieban/` 下，避免出现在组织主页上。由 `_inject_footer` 实现，有测试断言。

## Read the Docs 构建纪律

第二发布通道由 `.readthedocs.yml` 驱动，与 GitHub Pages 共用同一份 `doc/` 源，**两边的质量门必须等价**。

- `sphinx.fail_on_warning: true` 就是 CI 的 `-W --keep-going`，平台侧不得放宽。
- `sphinx.configuration` 必须写死 `doc/conf.py`：RTD 只探测仓库根 `conf.py` 与 `docs/`，
  本站源目录是 `doc/`（单数），不写会被判成「无配置」而不产出任何东西。
- **平台语言必须设为 Simplified Chinese（一次性设置）**：RTD 构建时不读 conf.py 的 `language`，
  而是把平台侧语言拼成 `-D language=<平台语言>` 覆盖它。留在默认英文会让中文分词（jieba）
  静默失效——构建一条警告都不报，`fail_on_warning` 也拦不住，只是中文搜不到。
  `doc/conf.py` 的 `_check_rtd_language` 把这条平台设置错误变成构建期硬错误。
- `formats` 只列 `htmlzip`：`pdf` 走 latex builder 而默认 pdflatex 不认中文字符，
  `epub` 要求 conf.py 提供 `version`（本站无版本号），两者在当前配置下都会失败。
- 本站不是可安装的 Python 包（无 pyproject.toml），依赖走 `requirements.txt`，
  不用 `method: pip` + `path: .` + `extra_requirements`（同族项目 mystx 是包，走的是后者）。
- **通道切换按钮**：左侧栏底部的下拉由 `doc/_static/switcher.json` 驱动，两个条目就是两条通道
  （`gh-pages`→GitHub Pages、`rtd`→Read the Docs），点击跳到**同一页**在另一通道的地址。
  三条硬约束，破了按钮就哑：
  1. `switcher.json_url` 必须用**相对路径** `_static/switcher.json`。改成 http(s) 绝对 URL 后，
     pydata 会在构建期对它发 HTTP 请求校验，读不到即 warning——本站 `-W`（RTD 侧
     `fail_on_warning`）会直接构建失败，且首次部署前该文件尚不存在，必然自举死锁。
  2. `version_match` 按构建环境分流（带 `READTHEDOCS` → `rtd`，否则 → `gh-pages`）：
     同一份 HTML 部署到两处，页面自己认不出身在何处，只能构建期决定高亮谁。
  3. 条目基址必须**以 `/` 结尾**：前端拼的是「基址 + 当前页路径」，漏了会拼出
     `https://daoapps.github.iojieban/index.html` 这种坏 URL。
  另：`primary_sidebar_end` 覆盖了主题默认值，必须把 `sidebar-ethical-ads` 一起带上，
  否则等于顺手砍掉 RTD 侧的伦理广告位。

## 样式纪律

- 全站一份样式表 `doc/_static/dao.css`，分若干节：token → 主题表皮（纸感）→ 结伴组件（`.jb-*`）
  → 组织主页组件（`.org-home ...`）。
- **组织主页的所有规则必须限定在 `.org-home` 内**，不得外溢到结伴站。
- 覆盖主题规则时**先看特异性，再看顺序**：`pydata-sphinx-theme` 把 `--pst-color-*` 定义在
  `html[data-theme="light"]`（0,1,1）上，只写 `:root`（0,1,0）会被整块盖掉。
  同理 sphinx-design 自带 Bootstrap 定义了 `.card` / `.btn` / `.lead`，
  组织主页规则统一用 `article.bd-article .org-home` 前缀抬高特异性。
- 深色模式明确不要：CSS 已隐藏主题切换按钮并让 `[data-theme="dark"]` 回落到浅色 token。

## 本地构建与验证

```bash
python -m pip install -r requirements.txt

# 契约测试
python -m pytest tests -q

# 构建（-W：警告即失败）
python -m sphinx -b html -d _build/doctrees --keep-going -W doc _build/html

# 本地预览
python -m http.server -d _build/html 8931
```

提交前两条都必须通过。CI 的 `gates` job 跑测试，`build` job 跑 `-W` 构建，`deploy` job 才发布。

## 参考

- 上级区域入口：SpecWeave `projects/AGENTS.md`（本仓库以 git submodule 形式接入）
- 发布工作流同族模板：`projects/awesome-okf-xs/.github/workflows/pages.yml`