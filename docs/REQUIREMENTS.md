# 项目需求文档

> 本文档记录 Novel V2 当前的产品定位、维护边界和硬规则。所有后续文档、Skill 调整和数据结构设计都应服务于这里的原则。

## 一、项目定位

Novel V2 是一个面向中文网文作者的 **Skill 驱动人机协同创作工作台**。

它不是“自动生成小说”的 CLI 流水线，也不再追求让系统从选题到正文自动跑完。实践结论是：小说创作中的题材判断、爽点取舍、人设微调、节奏控制、付费卡点和正文质感，都需要作者实时监督和确认。自动化只能处理结构化检查、素材检索、格式化落盘和局部辅助，不能替代创作判断。

核心声明：

> 本项目已从“自动化小说生成流水线”转向“Skill 驱动的人机协同创作工作台”。CLI 与 Python pipeline 是历史遗留实现，仅保留作参考，不再作为主入口维护。所有创造性工作必须由 Agent 按 Skill 流程执行，并在关键节点等待用户确认。

## 二、维护边界

### 2.1 当前维护对象

| 路径 | 状态 | 说明 |
|------|------|------|
| `.agents/skills/` | 持续维护 | 当前主入口。每个 Skill 的 `SKILL.md` 定义具体 Phase、输入输出、门禁与确认点 |
| `.agents/agents/` | 持续维护 | 专业子 Agent 提示词，用于审查、设计和一致性检查 |
| `data/schemas/` | 持续维护 | YAML 文件结构与完善度标准 |
| `templates/` | 持续维护 | 新项目模板，应匹配当前扁平化 `settings/*.yaml` 结构 |
| `docs/` | 持续维护 | 当前规则、流程和用户手册 |
| `novels/` | 数据目录 | 写作项目数据，按当前 Skill 产物结构组织 |

### 2.2 冻结遗留对象

| 路径 | 状态 | 说明 |
|------|------|------|
| `src/novel/` | 冻结保留 | 历史 Python 引擎和基础设施参考，不再作为创作主入口扩展 |
| `scripts/` | 冻结保留 | 历史脚本，可能仍反映旧数据结构，不再作为当前流程依据 |
| `novel` CLI | 冻结保留 | 自动流水线方向已放弃，不再围绕 CLI 补齐创作功能 |

冻结不等于删除。旧代码可以作为历史实现、测试参考或将来拆取基础能力的素材，但不能继续用它定义产品主流程。

## 三、用户需求

### 3.1 作者真正需要什么

作者需要的是一个能陪同创作的系统：

1. 帮作者整理题材方向、读者预期和商业卖点。
2. 把世界观、人设、大纲、细纲拆成可确认的小步骤。
3. 在每个关键节点提出候选方案，而不是直接替作者决定。
4. 对结构化产物做确定性检查，及时提示缺口。
5. 对正文做去 AI 味、退化检测、钩子审查和一致性审查。
6. 在方向错误时支持回退，而不是在错误方向上继续自动生成。
7. 让所有设定、正文、审查结果可追踪、可复查、可修改。

### 3.2 作者不需要什么

1. 不需要无人监督的“从一句话生成整本书”。
2. 不需要 CLI 一次性自动跑完选题、设定、大纲和正文。
3. 不需要在未确认设定时自动写正文。
4. 不需要绕过作者判断的自动修复。
5. 不需要把旧代码的能力包装成当前推荐入口。

## 四、创作流程

当前完整流程如下：

```text
1. 选题侦察       /scout-topic
2. 世界观设计     /worldbuilding
3. 人设设计       /design-character
4. 大纲设计       /design-outline
5. 细纲设计       /design-chapters
6. 黄金三章       /golden-chapters
7. 付费卡点       /paywall-design
8. 日更写作       /daily-write
9. 导出作品       /export-novel
```

每个阶段都必须满足三类条件：

| 条件 | 说明 |
|------|------|
| 前置条件 | 上游设定或章节规划已完成，且当前阶段有足够上下文 |
| 用户确认 | 关键判断、候选方案、落盘前内容必须经用户确认 |
| 质量门禁 | JS 脚本或 LLM 评估发现 blocking 问题时必须先修正 |

## 五、Skills 系统

### 5.1 自包含结构

```text
.agents/skills/<skill-name>/
├── SKILL.md
├── references/
└── scripts/
```

| 组件 | 责任 |
|------|------|
| `SKILL.md` | 定义 Phase、入口条件、操作步骤、出口条件、确认点和落盘要求 |
| `references/` | 提供方法论、品类模板、写作技巧和检查依据 |
| `scripts/` | 执行确定性质量门禁 |

### 5.2 创作类 Skills

| Skill | 用途 | 输出 |
|-------|------|------|
| `scout-topic` | 品类、平台、读者、选题和标签策略 | `settings/scout_report.yaml` |
| `worldbuilding` | 世界观与规则体系 | `settings/worldbuilding.yaml` |
| `design-character` | 主角、反派、配角与关系网络 | `settings/characters.yaml` |
| `design-outline` | 全书结构、幕、序列、节拍与节奏 | `settings/outline.yaml`、`settings/arcs.yaml`、`settings/pacing.yaml` |
| `design-chapters` | 章节拆分、摘要、节拍和张力 | `settings/chapters_index.yaml` |
| `golden-chapters` | 前三章正文锻造 | `content/chapter_001.md` 至 `content/chapter_003.md` |
| `paywall-design` | 付费切点、过渡章和商业复核 | `paywall_report.yaml` |
| `daily-write` | 单章正文写作、检查和定稿 | `content/chapter_XXX.md` |
| `export-novel` | 作品导出 | `exports/` |

### 5.3 辅助类 Skills

| Skill | 用途 |
|-------|------|
| `nm` | 调用 novel-material 检索素材 |
| `review` | 多视角对抗式审查 |
| `data-diagnosis` | 平台数据诊断 |
| `stock-check` | 存稿水位检查 |
| `feature-planning` | 新功能规划 |
| `refactor-planning` | 重构规划 |
| `code-review-change` | 变动影响审查 |
| `commit-msg` | 规范化提交信息 |

## 六、品类感知质量门禁

不同品类需要不同元素。质量门禁不硬编码为某一种小说模板，而是由 `settings/scout_report.yaml` 中的 `required_elements` 声明当前作品需要什么。

```yaml
required_elements:
  worldbuilding:
    required: [era_details, locations, social_rules]
    optional: [business_opportunities]
  characters:
    protagonist: required
    love_interest: required
    rival: optional
  opening_hook:
    type: reborn_advantage
    description: "前世记忆+行业洞察"
  structure:
    type: 起承转合
    target_arcs: 4
```

三层结构：

| 层 | 位置 | 作用 |
|----|------|------|
| 品类模板 | Skill references | 提供默认建议，如玄幻需要力量体系，都市需要时代背景 |
| 小说声明 | `scout_report.yaml` | 声明当前作品实际需要检查的元素 |
| 实际数据 | `settings/*.yaml` | 保存作者确认后的设定 |

## 七、质量门禁

采用双层门禁：

| 层 | 工具 | 说明 |
|----|------|------|
| 确定性检查 | JS 脚本 | 检查字段、结构、张力、AI 味模式、退化等可规则化问题 |
| 语义检查 | LLM + 用户判断 | 检查爽感、钩子、商业吸引力、情绪连续性等语义问题 |

JS 结果分级：

| 级别 | 处理方式 |
|------|----------|
| blocking | 必须修到 0，否则不能进入下一阶段 |
| advisory | 必须展示给用户，由用户决定是否调整 |

## 八、项目数据结构

单本小说目录：

```text
novels/{project_id}/
├── project.yaml
├── settings/
│   ├── scout_report.yaml
│   ├── worldbuilding.yaml
│   ├── characters.yaml
│   ├── outline.yaml
│   ├── arcs.yaml
│   ├── pacing.yaml
│   ├── chapters_index.yaml
│   └── notes.yaml
├── references/
├── content/
│   └── chapter_*.md
├── drafts/
├── exports/
└── _progress.md
```

当前文档以扁平化 `settings/*.yaml` 为主。旧脚本中出现的模块化目录结构仅代表历史实现，不应作为新流程依据。

## 九、状态流转

### 9.1 项目状态

```text
planning → drafting → revising → completed
```

| 状态 | 说明 |
|------|------|
| planning | 选题、世界观、人设、大纲、细纲阶段 |
| drafting | 黄金三章、付费卡点、日更写作阶段 |
| revising | 改写、润色、补洞、一致性修复阶段 |
| completed | 正文完成，可导出 |

### 9.2 章节状态

```text
planned → draft → written → revised
```

| 状态 | 说明 |
|------|------|
| planned | 有摘要和节拍，无正文 |
| draft | 有正文草稿，未通过全部检查 |
| written | 正文完成并通过基础门禁 |
| revised | 已润色或人工确认定稿 |

## 十、硬规则

必须：

- 创作类操作使用 Skills 交互式完成。
- 关键节点必须询问用户，不跳过确认。
- 生成 YAML 前必须读取对应 schema 或 Skill 指定的数据结构。
- 生成内容前必须尊重已有设定。
- blocking 问题必须修正后才能进入下一阶段。
- 当下游发现根本性问题时，必须回退到上游阶段重做。

禁止：

- 把 CLI 自动流水线作为当前推荐入口。
- 在未完成选题和章节规划时直接写正文。
- 未经用户确认覆盖已有设定或正文。
- 跳阶段推进。
- 把 advisory 风险静默忽略。

## 十一、成功标准

本项目成功不以“自动生成了多少字”为标准，而以作者是否能稳定推进创作为标准：

1. 作者能清楚知道当前处于哪个阶段。
2. 每个阶段都有明确产物和确认点。
3. 设定、正文、卡点和审查结果可追踪。
4. 质量门禁能及时暴露结构缺口和文本问题。
5. 用户能随时中断、调整、回退。
6. 最终正文保持设定一致、商业节奏清楚、AI 痕迹可控。
