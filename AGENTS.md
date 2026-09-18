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