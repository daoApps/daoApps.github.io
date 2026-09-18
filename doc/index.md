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

<div class="cta">
<a class="btn btn-primary" href="https://github.com/daoApps/daoNexus">浏览应用枢纽</a>
<a class="btn btn-ghost" href="https://github.com/daoApps">进入 GitHub 组织</a>
</div>

</div>
</div>

## 子站点

<p class="lead">组织主页之外，还有一处长期维护的公共客厅</p>

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

## 定位

<div class="manifesto">
<p>
这里的 <span class="key">DAO</span> 不是编程语言里常见的 Data Access Object，而是
<em>帛书《老子》</em>中那个「道」。以此命名，取的是一句老实话：<span class="key">顺其本然，不强求，不造作</span>。
</p>
<p>
所以这是一个开源的项目集合，而不是一件产品：每个应用各自独立可部署，各自能被单独拿走，
彼此之间靠「有无相生」的接口连起来——需要时聚合，不需要时互不打扰。
</p>
<p>
做减法比做加法难。这里更愿意把复杂度留在必要处，把界面留在安静处。
</p>
</div>

## 应用

<p class="lead">十四个仓库，五类用法——每个条目都指向一个可直接阅读源码的仓库</p>

<!-- 应用清单。中文名与描述取自 daoApps/daoNexus 的 src/data/apps.ts（该仓库为唯一事实来源），
     新增应用时同步修改该文件与本页对应分组；分组与计数由 tests/test_site_contract.py 守护。 -->

<div class="group" style="--accent: var(--g-shequ)">
<div class="group-head">
<h3>社区交流</h3>
<span class="count">2</span>
<span class="desc">连接用户，分享知识</span>
</div>
<div class="cards">
<a class="card" href="https://github.com/daoApps/forum">
<span class="name">知识社区 · Nexus Forum</span>
<span class="repo">forum</span>
<p class="desc">现代社区论坛，讨论、提问、分享知识。</p>
</a>
<a class="card" href="https://github.com/daoApps/xinyu">
<span class="name">心语互动 · Xinyu</span>
<span class="repo">xinyu</span>
<p class="desc">话题互动，惊喜分享，游戏化响应。</p>
</a>
</div>
</div>

<div class="group" style="--accent: var(--g-xiaolv)">
<div class="group-head">
<h3>效率工具</h3>
<span class="count">3</span>
<span class="desc">提升效率，追踪成长</span>
</div>
<div class="cards">
<a class="card" href="https://github.com/daoApps/growth-tracker">
<span class="name">成长追踪器 · Growth Tracker</span>
<span class="repo">growth-tracker</span>
<p class="desc">目标设定，成就系统，数据分析。</p>
</a>
<a class="card" href="https://github.com/daoApps/habit-tracker">
<span class="name">习惯追踪器 · Habit Tracker</span>
<span class="repo">habit-tracker</span>
<p class="desc">习惯打卡，日历统计，进度追踪。</p>
</a>
<a class="card" href="https://github.com/daoApps/moodflow">
<span class="name">情绪流动 · MoodFlow</span>
<span class="repo">moodflow</span>
<p class="desc">情绪记录，日记撰写，洞察分析。</p>
</a>
</div>
</div>

<div class="group" style="--accent: var(--g-gongju)">
<div class="group-head">
<h3>实用工具</h3>
<span class="count">2</span>
<span class="desc">便捷工具，简化生活</span>
</div>
<div class="cards">
<a class="card" href="https://github.com/daoApps/time-capsule">
<span class="name">时光胶囊 · Time Capsule</span>
<span class="repo">time-capsule</span>
<p class="desc">胶囊创建，内容存档，时间解锁。</p>
</a>
<a class="card" href="https://github.com/daoApps/qrcode-studio">
<span class="name">二维码工作室 · QRCode Studio</span>
<span class="repo">qrcode-studio</span>
<p class="desc">批量生成，样式定制，数据导出。</p>
</a>
</div>
</div>

<div class="group" style="--accent: var(--g-zhifu)">
<div class="group-head">
<h3>支付与链路</h3>
<span class="count">3</span>
<span class="desc">让智能体在有约束的前提下完成支付</span>
</div>
<div class="cards">
<a class="card" href="https://github.com/daoApps/monad-agentic-payment">
<span class="name">Safe 多签支付 · Monad Agentic Payment</span>
<span class="repo">monad-agentic-payment</span>
<p class="desc">把出资与执行解耦：人控 Safe 与限额白名单，智能体持零余额私钥签名，合约核对策略后放款；含 MCP Server 与人机协同（HITL）中断恢复。</p>
</a>
<a class="card" href="https://github.com/daoApps/agentic-payment">
<span class="name">代理支付系统 · Agentic Payment</span>
<span class="repo">agentic-payment</span>
<p class="desc">面向智能体的支付审批流程：多维策略引擎（单笔／每日／每周限额）、支付会话隔离、链上执行与完整审计日志。</p>
</a>
<a class="card" href="https://github.com/daoApps/daoPayment">
<span class="name">支付服务 · daoPayment</span>
<span class="repo">daoPayment</span>
<p class="desc">非托管钱包管理、预算与策略、x402 协议接入、审计与安全日志，以及 MCP Server 集成。</p>
</a>
</div>
</div>

<div class="group" style="--accent: var(--g-jizuo)">
<div class="group-head">
<h3>系统与基座</h3>
<span class="count">4</span>
<span class="desc">生态的骨架与入口</span>
</div>
<div class="cards">
<a class="card" href="https://github.com/daoApps/daoApps">
<span class="name">单体主仓库 · DAO Apps</span>
<span class="repo">daoApps</span>
<p class="desc">开源项目集合的主仓库：Flexloop 智能体协作平台、DaoMind 治理框架、DeepResearch 深度研究工具链，以及各应用的源码与部署脚本。</p>
</a>
<a class="card" href="https://github.com/daoApps/daoNexus">
<span class="name">应用枢纽 · daoNexus</span>
<span class="repo">daoNexus</span>
<p class="desc">前端的统一入口，一站访问全部可用应用，按社区／效率／工具／管理四类归置。</p>
</a>
<a class="card" href="https://github.com/daoApps/config-center">
<span class="name">配置中心 · Config Center</span>
<span class="repo">config-center</span>
<p class="desc">配置管理，版本管理，审计日志。</p>
</a>
<a class="card" href="https://github.com/daoApps/oauth-admin">
<span class="name">认证后台 · OAuth Admin</span>
<span class="repo">oauth-admin</span>
<p class="desc">连接管理，活动监控，权限控制。</p>
</a>
</div>
</div>

<p class="org-note">
本页收录 14 个仓库。另有 <a href="https://github.com/daoApps/dao-research-assistant">dao-research-assistant</a>
尚在筹备，暂不入列。本站源码即本仓库的 <code>doc/</code>，改内容直接编辑 Markdown，构建与发布由 GitHub Actions 完成。
</p>

```{toctree}
:hidden:

jieban/index
```

</div>