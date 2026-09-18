# daoApps.github.io

道用 · 组织主页 —— <https://daoapps.github.io/>

本仓库同时是**站点源码**与**发布产物**：GitHub Pages 直接从 `main` 分支根目录发布，改完即上线，无构建步骤。

## 文件

| 文件 | 用途 |
|---|---|
| `index.html` | 唯一的页面。内联样式，无外链、无依赖、无构建 |
| `.nojekyll` | 关闭 Jekyll 处理，避免静态文件被意外改写 |

## 新增一个应用

1. 在 `index.html` 中对应分组的 `.cards` 内追加一张卡片：

   ```html
   <a class="card" href="https://github.com/daoApps/<repo>">
     <span class="name">中文名 · English Name</span>
     <span class="repo">&lt;repo&gt;</span>
     <p class="desc">一句话说明。</p>
   </a>
   ```

2. 同步更新该分组的 `<span class="count">` 数量与页脚的收录总数。

应用的中文名与描述以 [daoNexus/src/data/apps.ts](https://github.com/daoApps/daoNexus/blob/main/src/data/apps.ts) 为准（该文件是应用清单的唯一事实来源）；不在其中的仓库，描述取自其自身 README。

## 分组

五个能力域，各有色条：

| 分组 | 色条变量 | 说明 |
|---|---|---|
| 社区交流 | `--g-shequ` | 连接用户，分享知识 |
| 效率工具 | `--g-xiaolv` | 提升效率，追踪成长 |
| 实用工具 | `--g-gongju` | 便捷工具，简化生活 |
| 支付与链路 | `--g-zhifu` | 智能体的受约束支付能力 |
| 系统与基座 | `--g-jizuo` | 生态的骨架与入口 |

## 视觉纪律

暖灰纸感（`--paper` / `--card` / `--ink`），朱砂点缀（`--cinnabar`），仅浅色模式。
色彩 token 与 [SpecWeave 结伴站点](https://github.com/xinetzone/SpecWeave) 共用一套，但本页只取 token 层，不含任何 Sphinx 主题相关规则。

忌大红大金、忌成功学大字报、忌收益承诺类措辞。