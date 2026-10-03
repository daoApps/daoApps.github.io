<div class="fp-seal">复盘</div>

# 方法论编排复盘

<p class="fp-sub">七概念 R·I·E·C·A·F·V 的完整执行记录 —— 可复制的一次实践</p>

<div class="fp-quote">
<q>教一个人学会，是给他答案；教一个人学会怎么学，是给他尺子。</q>
<cite>本次复盘的核心命题</cite>
</div>

:::{container} fp-cta

[看执行流水](pipeline.md){.fp-btn .fp-btn-primary}
[看质量门记录](gates.md){.fp-btn .fp-btn-ghost}

:::

<p class="fp-eyebrow">壹 · 这次做了什么</p>

## 一次「三人 → 四包 → 一套 Skill」的完整闭环

<p class="fp-lead">不是写了几篇文档，是走完一条带质量门的链路</p>

<div class="fp-manifesto">
<p>2026 年 10 月 3 日，接到一个复合任务：<span class="key">调研陶行知、游本昌、胡歌三人，为每个人创建 OKF wiki 教程，并洞察三人的关联、萃取通用 Skill、生成可复制的复盘报告。</span></p>
<p>任务表面是「写教程」，实际是四个类型的工作叠在一起——<em>知识沉淀</em>（建三个可发布的知识包）、<em>创新突破</em>（从素材中抽框架）、<em>流程追踪</em>（全过程可复现）、<em>站点产出</em>（落到 daoApps 站点）。</p>
<p>因此没有直接开写，而是先走了一遍<strong>方法论编排</strong>：识别场景 → 选择概念链路 → 逐概念执行 → 串质量门 → 原子交付。本页是这条链路的<em>执行快照</em>。</p>
</div>

<p class="fp-eyebrow">贰 · 为什么值得复盘</p>

## 三条被验证的方法，以及一个真实的失误

<p class="fp-lead">复盘的价值不在「做成了」，在「下次能少走哪一步」</p>

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} 链路可编排
一条链路（R→I→F→E→A→V→C）跑四个 bundle，**质量门不是形式**——它真的拦下了 11 处 toctree 断链和 1 处编码错误。
:::

:::{grid-item-card} 证据分层救场
254 条事实全部四级分层（A/B/C/D）。**后果是**：伪事实与二手来源在成文前就被隔离，而不是发出去再更正。
:::

:::{grid-item-card} 推断层显式标注
每个 bundle 的 concepts 与 examples 全部标注为推断层。**这让「本包是读法不是结论」成为可核查的事实，而不是免责声明。**
:::

:::{grid-item-card} 真实失误
枢纽包根 <code>index.md</code> 漏写 toctree，被门禁拦下 11 处不可达。**如果没跑门禁，这 11 个文件会静默丢失在导航之外。**
:::

::::

<p class="fp-eyebrow">叁 · 这次的可复用产物</p>

## 四份 OKF 知识包 · 一套 Skill · 一份复盘

<div class="fp-artifacts">
<a class="fp-card" href="pipeline.md">
<span class="fp-card-tag">流水</span>
<span class="fp-card-body">
<span class="fp-card-name">执行流水</span>
<span class="fp-card-desc">七概念逐阶段记录：场景识别、链路选择、四包产出、质量门通过情况、门禁实测数据</span>
</span>
<span class="fp-card-go">进入 →</span>
</a>
<a class="fp-card" href="gates.md">
<span class="fp-card-tag">门禁</span>
<span class="fp-card-body">
<span class="fp-card-name">质量门与可复制清单</span>
<span class="fp-card-desc">G1–G4 + V 门的逐项判定、三道官方门禁的实测结果、下次可直接复用的检查清单</span>
</span>
<span class="fp-card-go">进入 →</span>
</a>
</div>

<div class="fp-metrics">
<div class="fp-metric">
<span class="fp-metric-num">4</span>
<span class="fp-metric-label">OKF 知识包</span>
<span class="fp-metric-note">三人各一 + 关联枢纽包</span>
</div>
<div class="fp-metric">
<span class="fp-metric-num">61</span>
<span class="fp-metric-label">新建文档</span>
<span class="fp-metric-note">concepts + examples + references</span>
</div>
<div class="fp-metric">
<span class="fp-metric-num">254</span>
<span class="fp-metric-label">四级分层事实</span>
<span class="fp-metric-note">A/B/C/D 分层登记</span>
</div>
<div class="fp-metric">
<span class="fp-metric-num">10</span>
<span class="fp-metric-label">可填写工作表</span>
<span class="fp-metric-note">四问方案 / 诊断表 / 台账 / 试点</span>
</div>
<div class="fp-metric">
<span class="fp-metric-num">3</span>
<span class="fp-metric-label">自研框架</span>
<span class="fp-metric-note">真问题真需求真目标 / 品质技能身份 / 正面解读师</span>
</div>
<div class="fp-metric">
<span class="fp-metric-num">3</span>
<span class="fp-metric-label">官方门禁</span>
<span class="fp-metric-note">utf8 / toctrees / bundles 全绿</span>
</div>
</div>

<p class="fp-eyebrow">肆 · 方法论从哪来</p>

## 不是七条命令，是一条链路

<p class="fp-lead">每种任务有它的链路，强行全走是过度工程</p>

<div class="fp-manifesto">
<p>七概念是：<strong>R 复盘 · I 洞察 · E 萃取 · C 原子提交 · A 原子化 · F 第一性原理 · V 对抗审查</strong>。它们不是七个步骤，是<em>七种可按需组合的能力</em>。</p>
<p>本次任务被识别为<strong>复合场景</strong>——主干是「知识沉淀」（R→I→E→V），叠加「创新突破」层（F→V→I）。所以实际链路是 <code>R → I → F → E → A → V → C</code>，而不是把七个概念全走一遍。</p>
<p>其中 <strong>V 对抗审查在 F 之后是强制</strong>：因为第一性原理推导出的方案天然缺乏历史校验——<em>先有方案再攻击，攻击的才是新东西</em>。本次 V 阶段确实拦下了实质问题（见<a href="gates.md">质量门记录</a>）。</p>
</div>

<p class="fp-eyebrow">伍 · 一条纪律</p>

## 质量门不通过就不要推进

<p class="fp-lead">它是硬关卡，不是建议</p>

<div class="fp-manifesto">
<p>本次最有价值的一次拦截发生在最后一刻：四个包全部写完、索引也接好了，<strong>跑 toctree 门禁时跳出 11 处「未收录（不可达）」</strong>——枢纽包的根 <code>index.md</code> 漏写了 <code>toctree</code> 块。</p>
<p>如果这一步跳过，这 11 个文档（Sphinx 不会为它们生成页面、也不会有任何警告）会<em>静默地留在导航之外</em>：文件存在、能打开，但站点上没有任何入口能到达它们。</p>
<p>这就是质量门的意义：<span class="key">它不是流程仪式，是把「已完成」这个词从主观判断变成机器判定。</span></p>
</div>

---

**本子站的三页**：[执行流水](pipeline.md) · [质量门记录](gates.md)

**产出主体**：四个 OKF 知识包位于 `awesome-okf-xs` 仓库的 `doc/bundles/sheke/personal-growth/` 下。

```{toctree}
:hidden:
:maxdepth: 2

pipeline
gates
```
