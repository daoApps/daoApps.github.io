<div class="xx-lab">

<div class="xx-seal">环</div>

# 教学相长：一个学习循环是怎么转起来的

<p class="xx-sub">三个命题不是三条口号——它们咬合在一起，才是一个真实的学习闭环</p>

<p class="xx-lead">下面是这个循环的结构图。<strong>点任意一个节点</strong>，展开它为什么在这、不转会怎样。</p>

<div id="xx-cycle">

<div class="xx-ring">

<div class="xx-node" data-key="proxy">
<div class="xx-node-title">学不可代理</div>
<div class="xx-node-sub">一切的起点</div>
</div>

<div class="xx-node" data-key="condition">
<div class="xx-node-title">教是条件工程</div>
<div class="xx-node-sub">外部的角色</div>
</div>

<div class="xx-node" data-key="output">
<div class="xx-node-title">输出驱动输入</div>
<div class="xx-node-sub">合流的机制</div>
</div>

</div>

<div class="xx-detail" id="xx-detail">
<p class="xx-detail-hint">点上面三个节点，看每一环的机制与反例</p>
</div>

</div>

<div class="xx-panel" data-for="proxy" hidden>
<h3>命题一 · 学不可代理</h3>
<p>学习者的改变只能发生在自己的神经系统里。没有人、没有 AI、没有一门课能替你长出新的突触连接——这就是为什么"听懂了"不等于"学会了"。</p>
<p><strong>反例</strong>：把学习外包给 AI 生成笔记、总结、答案，感觉全程顺滑——但建构从未发生，下次同类题仍然不会。</p>
<p><strong>操作含义</strong>：任何"替你完成思考"的步骤，都是在透支学习主权。</p>
</div>

<div class="xx-panel" data-for="condition" hidden>
<h3>命题二 · 教是条件工程</h3>
<p>教不能直接产生学习。教者能做的是创设条件——好的问题、合适的难度（ZPD 最近发展区）、及时的反馈、安全的氛围。评价教的唯一标准不是讲得精彩，而是<strong>学是否发生</strong>。</p>
<p><strong>反例</strong>：一堂满分的公开课，学生上完说不出任何要点——教的动作完成了，学没有发生。</p>
<p><strong>操作含义</strong>：好教者的终极目标是让自己"退场"（叶圣陶：教是为了不教）。</p>
</div>

<div class="xx-panel" data-for="output" hidden>
<h3>命题三 · 输出驱动输入</h3>
<p>《学记》说"学然后知不足，教然后知困"——输出（讲解、作答、写作）会暴露你以为懂了其实没懂的地方，这个"卡壳"就是下一轮学习的方向。这就是费曼学习法与检索练习效应共同证明的机制。</p>
<p><strong>反例</strong>：只读不写、只听不讲、只收藏不输出——输入量很大，但因为没有输出暴露漏洞，学习停在表面。</p>
<p><strong>操作含义</strong>：每学完一个东西，立刻找一个"听众"（哪怕是 AI 或一张白纸）讲一遍。讲不顺的地方，就是你下一轮要学的。</p>
</div>

<p class="xx-eyebrow">这个循环为什么能转起来</p>

## 三句话闭环

<div class="xx-loop">
<div class="xx-loop-step"><span>1</span><p>因为学不可代理，所以外部的教只能做条件（命题二是命题一的推论）。</p></div>
<div class="xx-loop-step"><span>2</span><p>因为学不可代理，所以唯一能让"我"发生建构的方法，是让我自己输出（命题三是命题一的另一推论）。</p></div>
<div class="xx-loop-step"><span>3</span><p>条件创设得越好，输出暴露的漏洞越清晰，下一轮输入越精准——循环就转起来了。</p></div>
</div>

<div class="xx-note">
<p>回到 <a href="checkup.md">学习体检器</a> 看看自己这三环卡在哪；去 <a href="playbook.md">循证策略手册</a> 把"输出驱动"落成每天一次的动作。</p>
</div>

```{raw} html
<script>
document.addEventListener('DOMContentLoaded', function () {
  var nodes = document.querySelectorAll('.xx-node');
  var detail = document.getElementById('xx-detail');
  var panels = document.querySelectorAll('.xx-panel');
  nodes.forEach(function (n) {
    n.addEventListener('click', function () {
      nodes.forEach(function (x) { x.classList.remove('active'); });
      n.classList.add('active');
      panels.forEach(function (p) {
        p.hidden = (p.getAttribute('data-for') !== n.getAttribute('data-key'));
      });
      detail.innerHTML = '<p class="xx-detail-hint">当前展开：<strong>' + n.querySelector('.xx-node-title').textContent + '</strong>（点其他节点切换）</p>';
    });
  });
});
</script>
```

</div>
