<div class="org-home">

<div class="hero">
<div class="box">

<div class="seal" aria-hidden="true">道</div>

# 道用

<p class="sub">道法自然的智能化应用生态</p>

<blockquote class="quote">
<q>人法地，地法天，天法道，道法自然。</q>
<cite>《老子》第二十五章</cite>
</blockquote>

:::{container} cta

[浏览应用枢纽](https://github.com/daoApps/daoNexus){.btn .btn-primary}
[进入 GitHub 组织](https://github.com/daoApps){.btn .btn-ghost}

:::

</div>
</div>

## 子站点

<p class="lead">组织主页之外，还有一处长期维护的公共客厅</p>

<div class="subsite">
<a class="subsite-card" href="fupan/">
<span class="subsite-tag">/fupan/</span>
<span class="subsite-body">
<span class="subsite-name">复盘</span>
<span class="subsite-desc">方法论编排的执行记录 —— 七概念全链路的可复制复盘与质量门实测数据</span>
</span>
<span class="subsite-go">进入 →</span>
</a>
</div>

<div class="subsite">
<a class="subsite-card" href="jieban/">
<span class="subsite-tag">/jieban/</span>
<span class="subsite-body">
<span class="subsite-name">结伴</span>
<span class="subsite-desc">好好生活的人，终会相逢 —— 四个频道：知足 · 恒与 · 知和 · 愈多</span>
</span>
<span class="subsite-go">进入 →</span>
</a>
</div>

<div class="subsite">
<a class="subsite-card" href="xuexi/">
<span class="subsite-tag">/xuexi/</span>
<span class="subsite-body">
<span class="subsite-name">学以不教 · 学习实验室</span>
<span class="subsite-desc">AI 时代的学习体检 —— 认知外包度测试、教学相长机制图、循证策略手册</span>
</span>
<span class="subsite-go">进入 →</span>
</a>
</div>

## 定位

:::{container} manifesto

这里的 [DAO]{.key} 不是编程语言里常见的 Data Access Object，而是 <em>帛书《老子》</em>中那个「道」。以此命名，取的是一句老实话：[顺其本然，不强求，不造作]{.key}。

所以这是一个开源的项目集合，而不是一件产品：每个应用各自独立可部署，各自能被单独拿走，
彼此之间靠「有无相生」的接口连起来——需要时聚合，不需要时互不打扰。

做减法比做加法难。这里更愿意把复杂度留在必要处，把界面留在安静处。

:::

## 应用

<p class="lead">十四个仓库，五类用法——每个条目都指向一个可直接阅读源码的仓库</p>

<!-- 应用清单。中文名与描述取自 daoApps/daoNexus 的 src/data/apps.ts（该仓库为唯一事实来源），
     新增应用时同步修改该文件与本页对应分组；分组与计数由 tests/test_site_contract.py 守护。 -->

<!-- 分组卡片由 sphinx-design 的 {grid} + {grid-item-card} 生成（与结伴站同习语），
     卡片自带的 .sd-card 由 dao.css「十八 · 组织主页」节的适配层接管版式。
     两处别按直觉改：
       · 分组标题与计数保持裸 <h3>/<span>——写成 Markdown ### 会让组名进右侧页内 TOC；
       · {grid} 的 1 1 3 3 只是断点声明，列数实由 .cards 的 auto-fit 网格决定。 -->

<div class="group g-shequ">

<div class="group-head"><h3>社区交流</h3><span class="count">2</span><span class="desc">连接用户，分享知识</span></div>

::::{grid} 1 1 3 3
:gutter: 0
:class-container: cards

:::{grid-item-card} 知识社区 · Nexus Forum
:link: https://github.com/daoApps/forum
:link-alt: 知识社区 · Nexus Forum

[forum]{.repo}

现代社区论坛，讨论、提问、分享知识。
:::

:::{grid-item-card} 心语互动 · Xinyu
:link: https://github.com/daoApps/xinyu
:link-alt: 心语互动 · Xinyu

[xinyu]{.repo}

话题互动，惊喜分享，游戏化响应。
:::

::::

</div>

<div class="group g-xiaolv">

<div class="group-head"><h3>效率工具</h3><span class="count">3</span><span class="desc">提升效率，追踪成长</span></div>

::::{grid} 1 1 3 3
:gutter: 0
:class-container: cards

:::{grid-item-card} 成长追踪器 · Growth Tracker
:link: https://github.com/daoApps/growth-tracker
:link-alt: 成长追踪器 · Growth Tracker

[growth-tracker]{.repo}

目标设定，成就系统，数据分析。
:::

:::{grid-item-card} 习惯追踪器 · Habit Tracker
:link: https://github.com/daoApps/habit-tracker
:link-alt: 习惯追踪器 · Habit Tracker

[habit-tracker]{.repo}

习惯打卡，日历统计，进度追踪。
:::

:::{grid-item-card} 情绪流动 · MoodFlow
:link: https://github.com/daoApps/moodflow
:link-alt: 情绪流动 · MoodFlow

[moodflow]{.repo}

情绪记录，日记撰写，洞察分析。
:::

::::

</div>

<div class="group g-gongju">

<div class="group-head"><h3>实用工具</h3><span class="count">2</span><span class="desc">便捷工具，简化生活</span></div>

::::{grid} 1 1 3 3
:gutter: 0
:class-container: cards

:::{grid-item-card} 时光胶囊 · Time Capsule
:link: https://github.com/daoApps/time-capsule
:link-alt: 时光胶囊 · Time Capsule

[time-capsule]{.repo}

胶囊创建，内容存档，时间解锁。
:::

:::{grid-item-card} 二维码工作室 · QRCode Studio
:link: https://github.com/daoApps/qrcode-studio
:link-alt: 二维码工作室 · QRCode Studio

[qrcode-studio]{.repo}

批量生成，样式定制，数据导出。
:::

::::

</div>

<div class="group g-zhifu">

<div class="group-head"><h3>支付与链路</h3><span class="count">3</span><span class="desc">让智能体在有约束的前提下完成支付</span></div>

::::{grid} 1 1 3 3
:gutter: 0
:class-container: cards

:::{grid-item-card} Safe 多签支付 · Monad Agentic Payment
:link: https://github.com/daoApps/monad-agentic-payment
:link-alt: Safe 多签支付 · Monad Agentic Payment

[monad-agentic-payment]{.repo}

把出资与执行解耦：人控 Safe 与限额白名单，智能体持零余额私钥签名，合约核对策略后放款；含 MCP Server 与人机协同（HITL）中断恢复。
:::

:::{grid-item-card} 代理支付系统 · Agentic Payment
:link: https://github.com/daoApps/agentic-payment
:link-alt: 代理支付系统 · Agentic Payment

[agentic-payment]{.repo}

面向智能体的支付审批流程：多维策略引擎（单笔／每日／每周限额）、支付会话隔离、链上执行与完整审计日志。
:::

:::{grid-item-card} 支付服务 · daoPayment
:link: https://github.com/daoApps/daoPayment
:link-alt: 支付服务 · daoPayment

[daoPayment]{.repo}

非托管钱包管理、预算与策略、x402 协议接入、审计与安全日志，以及 MCP Server 集成。
:::

::::

</div>

<div class="group g-jizuo">

<div class="group-head"><h3>系统与基座</h3><span class="count">4</span><span class="desc">生态的骨架与入口</span></div>

::::{grid} 1 1 3 3
:gutter: 0
:class-container: cards

:::{grid-item-card} 单体主仓库 · DAO Apps
:link: https://github.com/daoApps/daoApps
:link-alt: 单体主仓库 · DAO Apps

[daoApps]{.repo}

开源项目集合的主仓库：Flexloop 智能体协作平台、DaoMind 治理框架、DeepResearch 深度研究工具链，以及各应用的源码与部署脚本。
:::

:::{grid-item-card} 应用枢纽 · daoNexus
:link: https://github.com/daoApps/daoNexus
:link-alt: 应用枢纽 · daoNexus

[daoNexus]{.repo}

前端的统一入口，一站访问全部可用应用，按社区／效率／工具／管理四类归置。
:::

:::{grid-item-card} 配置中心 · Config Center
:link: https://github.com/daoApps/config-center
:link-alt: 配置中心 · Config Center

[config-center]{.repo}

配置管理，版本管理，审计日志。
:::

:::{grid-item-card} 认证后台 · OAuth Admin
:link: https://github.com/daoApps/oauth-admin
:link-alt: 认证后台 · OAuth Admin

[oauth-admin]{.repo}

连接管理，活动监控，权限控制。
:::

::::

</div>

<p class="org-note">
本页收录 14 个仓库。另有 <a href="https://github.com/daoApps/dao-research-assistant">dao-research-assistant</a>
尚在筹备，暂不入列。本站源码即本仓库的 <code>doc/</code>，改内容直接编辑 Markdown，构建与发布由 GitHub Actions 完成。
</p>

```{toctree}
:hidden:

jieban/index
fupan/index
xuexi/index
```

</div>
