# AI Harness Engineering 研究总结

> 基于 OpenAI 和 Anthropic 2025-2026 年发布的 6 篇工程博客，提炼 AI agent harness（智能体脚手架）的核心概念，并分析对本项目的适用性。

---

## 一、文章索引

| # | 来源 | 标题 | 日期 | 核心主题 |
|---|------|------|------|---------|
| 1 | OpenAI | [Harness Engineering: Leveraging Codex in an Agent-First World](https://openai.com/zh-Hans-CN/index/harness-engineering/) | 2026-02-11 | 100% AI 生成的百万行代码项目，工程师角色从"写代码"转变为"设计环境" |
| 2 | OpenAI | [Unlocking the Codex Harness: How We Built the App Server](https://openai.com/index/unlocking-the-codex-harness/) | 2026-02-04 | Codex 技术架构：Agent Loop + App Server + JSON-RPC 协议 |
| 3 | Anthropic | [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 2026-01-09 | Agent 评估体系：评估类型、评分器设计、从零建立 eval 的路线图 |
| 4 | Anthropic | [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | 2025-11-26 | 长时间运行 agent 的 harness 设计：初始化 agent + 编码 agent + 增量推进 |
| 5 | Anthropic | [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 2025-09-29 | 上下文是有限资源：压缩、笔记、子 agent、just-in-time 检索 |
| 6 | Anthropic | [Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | 2026-03-24 | 三 agent 架构（Planner + Generator + Evaluator），GAN 式反馈循环 |

---

## 二、七个核心概念

### 2.1 Harness = 给 AI 搭的"脚手架"

**定义**：Harness 不是 AI 本身的能力，而是包裹 AI 的系统——告诉 AI 该做什么、怎么做、做完怎么验证的整套基础设施。

> OpenAI 原文："保持代码库一致性的工具、抽象和反馈回路变得越发重要。"

**Harness 的五层组成**：

| 层 | 功能 | 本项目对应 |
|----|------|-----------|
| 指令层 | AGENTS.md、系统提示词、skill 定义 | `.claude/skills/*/SKILL.md` |
| 工具层 | AI 可调用的工具（文件操作、搜索、测试） | Cursor IDE 内置工具 |
| 约束层 | linter、架构规则、CI 检查 | `_protocols/*.md`（软约束） |
| 评估层 | 验证 AI 输出是否正确 | `chapter-review`, `anti-ai-check` 等（建议性） |
| 上下文层 | AI 能看到的信息管理 | `.cursor/rules/`, `GUIDE.md` |

**关键差距**：我们在指令层和上下文层做得较好，但约束层是"软约束"（纯文档），评估层是建议性的不形成硬闸。

---

### 2.2 AGENTS.md 是目录，不是百科全书

OpenAI 的核心发现：

> "情境是一种稀缺资源。一个巨大的指令文件会挤掉任务、代码和相关文档——因此智能体要么会错过关键约束条件，要么开始针对错误的约束条件进行优化。"

> "过多的指导反而变得无效。当一切都'重要'时，一切都不重要了。智能体最终会在本地进行模式匹配，而不是有意识地进行导航。"

> "它会立即腐烂。一本庞杂的手册会变成陈旧规则的坟场。智能体无法判断哪些信息仍然有效。"

> "这很难核实。单个 blob 不适合进行机械检查（覆盖率、新鲜度、所有权、交叉链接），因此漂移是不可避免的。"

**OpenAI 的做法**：AGENTS.md 只有约 100 行，纯粹作为"地图"指向 `docs/` 目录下的深层文档。配合专门的 linter 和 CI 验证文档是否过时、交叉链接是否正确。还有定期运行的 "doc-gardening" agent 扫描过时文档。

**本项目现状**：AGENTS.md 已遵循此原则（49 行纯导航）。但缺少机械化检查文档新鲜度的手段。

---

### 2.3 仓库即真相源（Repository as System of Record）

> OpenAI 原文："从智能体的角度来看，它在运行时无法在情境中访问的任何内容都是不存在的。存储在 Google Docs、聊天记录或人们头脑中的知识都无法被系统访问。代码仓库本地的、已版本化的工件就是它所能看到的全部。"

**关键洞察**：所有知识必须在仓库内、版本化、可被 AI 发现。Slack 讨论、口头约定、作者脑中的设定——如果没写进文件，对 AI 就不存在。

**OpenAI 的实践**：
- 代码仓库的知识库位于结构化的 `docs/` 目录中
- 设计讨论、架构决策全部以 Markdown 形式落地到仓库
- "那次让团队在架构模式上达成一致的 Slack 讨论？如果智能体无法发现它，那么它就会像迟了三个月入职的新员工一样，对其一无所知。"

**对本项目的启示**：这正是 `draft-ingest` 的意义——把作者脑中的想法变成仓库内的结构化文件。但很多创作决策（"为什么选这个名字"、"这个角色的灵感来源"、"某个设定的创作意图"）目前没有落地的地方。

---

### 2.4 渐进式披露（Progressive Disclosure）

> Anthropic 上下文工程原文："Agents 通过层层探索逐步发现相关上下文……每次交互产生的上下文为下一个决策提供信息。"

**原理**：不要一次性把所有信息塞给 AI。给一个小而稳定的入口，让 AI 按需深入。就像人类不会把整个图书馆搬到桌上，而是先看目录，再取需要的书。

**两家公司的实践对比**：

| 策略 | OpenAI | Anthropic |
|------|--------|-----------|
| 入口点 | `AGENTS.md` -> `docs/index.md` -> 具体设计文档 | `CLAUDE.md` 作入口，grep/glob 按需检索 |
| 检索策略 | 预计算 + 按需 | "Just-in-time" 按需加载 |
| 核心思想 | 渐进式导航 | 轻量标识符 + 运行时加载 |

**Anthropic 的"Just-in-time"策略**：Agent 维护轻量标识符（文件路径、查询、链接），用这些引用在运行时动态加载数据到上下文，而不是预先加载所有内容。Claude Code 就是这样工作的——`CLAUDE.md` 被直接加载，其余文件通过 glob 和 grep 按需检索。

**本项目现状**：`GUIDE.md -> AGENTS.md -> SKILL.md` 已形成层次结构。但 skill 执行时读取的文件量可能过大（如 `consistency-check` 要读十几个文件），缺少 just-in-time 策略来控制上下文预算。

---

### 2.5 机械化约束（Mechanical Enforcement）

> OpenAI 原文："在以人为本的工作流程中，这些规则可能会让人感到迂腐或束缚。有了智能体，它们就成了倍增器：一旦编码，就能立即应用于所有地方。"

**OpenAI 的具体做法**：
- 自定义 linter 强制执行架构规则（层间依赖方向、文件大小限制、命名约定）
- Linter 的错误消息中直接注入修复指令（AI 读到错误就知道怎么修）
- CI 验证知识库是否过时、交叉链接是否正确
- 定期运行 "doc-gardening" agent 扫描过时文档并发起修复 PR
- 结构测试（structural tests）验证架构不变量

> "我们倾向于选择那些可以完全内化于在仓库中进行推理的依赖项和抽象。对智能体来说，通常被称为'枯燥'的技术，由于其可组合性、API 稳定性和在训练集里的表现，往往更容易建立模型。"

**核心原则**："当文档不够完善时，我们会将规则转化为代码。"（When docs aren't enough, turn rules into code.）

**本项目的差距**：这是我们最大的短板。所有 protocols 都是"软约束"——写在 Markdown 里的规则，AI 可能遵守也可能不遵守。没有任何机械化验证手段：
- `preflight-integrity` 规定要检查文件完整性，但没有脚本真正执行检查
- `name-resolution` 规定命名规则，但没有 linter 验证违反情况
- `operation-journal` 规定要记日志，但没有检查遗漏
- 交叉索引的一致性完全依赖人工运行 `/project-reindex`

---

### 2.6 分离生成与评估（Generator-Evaluator Pattern）

Anthropic 最新文章（2026-03）的核心发现——受 GAN（生成对抗网络）启发的架构：

> "当被要求评估自己的工作时，agents 倾向于自信地赞扬自己的作品——即使对人类观察者来说，质量明显平庸。"

> "将执行的 agent 和评判的 agent 分开，是解决这个问题的强力杠杆。分离不会立即消除自我宽容——评估者仍是一个对 LLM 输出偏向宽容的 LLM。但调节一个独立的评估者使其持怀疑态度，比让生成者对自己的作品持批判态度要容易得多。"

**三 agent 架构**：

| Agent | 职责 | 关键特征 |
|-------|------|---------|
| Planner | 把一句话需求扩展成完整规格 | 关注产品上下文和高层设计，不陷入实现细节 |
| Generator | 按规格逐步实现 | 每次只做一个 sprint，做完自评后交给 QA |
| Evaluator | 用真实工具测试结果，打分、写反馈 | 独立评判，有明确的评分维度和阈值 |

**Sprint Contract**：Generator 和 Evaluator 在开工前先协商"什么算完成"，避免模糊验收。这存在于因为产品规格是故意高层次的，需要一个步骤来弥合用户故事与可测试实现之间的差距。

**评分维度（前端设计示例）**：
1. 设计质量：是否像一个连贯的整体？
2. 原创性：是否有定制决策，还是模板默认值？
3. 工艺：技术执行质量（排版、间距、色彩）
4. 功能性：可用性

**本项目的映射**：

| Anthropic 架构 | 本项目对应 | 差距 |
|---------------|-----------|------|
| Planner | `pipeline-outline-bootstrap` | 基本对齐 |
| Generator | `chapter-draft` | 基本对齐 |
| Evaluator | `chapter-review` + `anti-ai-check` + `voice-check` | 审查是建议性的，不形成通过/不通过的硬闸；评估结果不自动回馈给生成器 |
| Sprint Contract | `pipeline-chapter-kickoff` 的场景大纲 | 缺少 Generator-Evaluator 之间的明确"验收标准协商" |

---

### 2.7 长时间运行的增量策略

Anthropic 的长运行 agent 框架解决的核心问题：

> "Agent 每次启动都是'失忆'的新员工。想象一个软件项目由轮班工程师负责，每个新工程师到来时对上一班发生的事没有任何记忆。"

**两个关键失败模式**：
1. **One-shotting**：Agent 试图一次性完成所有事情，耗尽上下文窗口，留下半完成的工作
2. **过早宣布完成**：Agent 看到已有进展就认为工作已经结束

**解决方案（五件套）**：

| 组件 | 作用 | 本项目对应 |
|------|------|-----------|
| Feature List（JSON 格式） | 所有需求列成可勾选清单，状态 pass/fail | `plot/outline.yaml`（章节清单 + 状态追踪） |
| Progress File | 每次 session 结束时写进度笔记 | `chapters/index.yaml` 的 summary + `.novel/ops_log.yaml` |
| Git 提交 | 每完成一个功能就 commit，描述性消息 | 有，但依赖人工触发 |
| 增量原则 | 每次只做一个功能，做完再做下一个 | `chapter-scope-guard`（每次一章，不贪多） |
| 启动仪式 | 每次开始先读进度、读 git log、跑基本测试 | `preflight-integrity`（操作前检查状态） |

**Anthropic 的启动仪式**：
```
1. 运行 pwd 确认工作目录
2. 读 git log 和 progress file，了解最近做了什么
3. 读 feature list，选择最高优先级的未完成项
4. 运行 init.sh 启动开发服务器
5. 跑基本端到端测试，确认环境没坏
6. 才开始实现新功能
```

**上下文跨 session 的三种策略（Anthropic 上下文工程文）**：

| 策略 | 原理 | 适用场景 |
|------|------|---------|
| Compaction（压缩） | 总结当前对话，用摘要重启新 context | 需要大量来回交互的任务 |
| Structured Note-taking（结构化笔记） | Agent 定期写笔记到外部文件，后续 session 读取 | 有明确里程碑的迭代开发 |
| Sub-agent（子 agent） | 主 agent 协调，子 agent 深入处理具体任务，只返回摘要 | 需要并行探索的复杂研究/分析 |

---

## 三、对本项目的五个可行改进方向

> **实施状态**：以下五个方向已全部落地（2026-04-09）。  
> 新增文件：`_protocols/eval-gate.md`、`_protocols/context-budget.md`、`project-lint/SKILL.md`  
> 修改文件：`chapter-review`、`voice-check`、`anti-ai-check`、`pipeline-draft-polish`、`chapter-draft`、`consistency-check`、`novel-doctor`

### A. 评估闸门硬化

**来源**：Anthropic Evals 文 + GAN 架构文

**现状**：`chapter-review`、`anti-ai-check`、`voice-check` 给建议但不阻断流程。审查结果是终端输出，不回流到下次生成。

**改进思路**：
- 给 `pipeline-draft-polish` 加评分阈值：anti-ai 分数低于某值时不推进到 revise 状态
- 审查发现的问题写入结构化文件（如 `chapters/{id}_review.yaml`），下次 `chapter-draft` 时自动读取
- 参考 Anthropic 的 Sprint Contract，在 `pipeline-chapter-kickoff` 阶段让"规划"和"审查标准"同步生成

**预期收益**：防止低质量内容无感推进；审查结果可追溯、可累积

### B. 机械化约束（project-lint）

**来源**：OpenAI 的自定义 linter + CI

**现状**：所有 protocols 是纯文档，AI 可能遵守也可能不遵守

**改进思路**：
- 创建一个 `project-lint` skill（或增强 `novel-doctor`），用脚本检查：
  - 文件完整性：`chapters/index.yaml` 的每个条目在 `chapters/` 下都有对应文件（反之亦然）
  - 索引一致性：`character_index.yaml` 与 `characters/*.yaml` 文件对齐
  - 命名规范：检查 `meta.yaml` 中 `forbidden_patterns` 是否被违反
  - 操作日志完整性：`ops_log.yaml` 中没有 `in_progress` 状态的遗留条目
  - 交叉引用健康：角色的 `cross_references` 与设定的 `character_links` 是否对齐
- 将检查结果输出为结构化报告，错误消息中嵌入修复建议

**预期收益**：把"希望 AI 遵守的规则"变成"AI 必须通过的检查"

### C. 上下文预算控制

**来源**：Anthropic 上下文工程文

**现状**：skill 执行时读文件没有限制，`consistency-check` 可能一次读十几个文件

**改进思路**：
- 高频 skill（如 `chapter-draft`）设定"最多读 N 个相关文件"的策略
- 用 summary 替代全文读取：读 `chapters/index.yaml` 的 summary 字段而不是打开每个 `.md`
- 参考 Anthropic 的 "Just-in-time" 策略：先读索引/摘要，发现需要时再深入读原文
- 在 SKILL.md 中标注每步的"上下文成本"，让 AI 意识到读取是有代价的

**预期收益**：减少 AI 的信息过载，提高长 session 的稳定性

### D. 知识新鲜度检查

**来源**：OpenAI 的 doc-gardening agent

**现状**：无机制检测长期未更新的设定、过时的角色状态、与已写章节不符的大纲描述

**改进思路**：
- `novel-doctor` 增加"新鲜度"维度：
  - 设定条目：`tentative` 状态超过 N 章仍未 confirm
  - 角色状态：`characters/*.yaml` 的 `last_updated` 与最新章节的差距
  - 大纲节点：`outline.md` 中标记为"待定"的节点超过 N 章未处理
  - 钩子健康：`planted` 状态超过截止章节仍未回收
- 定期在 `pipeline-chapter-kickoff` 或 `pipeline-draft-polish` 时触发轻量新鲜度扫描

**预期收益**：防止"陈旧信息"误导写作，相当于项目级的"垃圾回收"

### E. 反馈循环闭合

**来源**：Anthropic Generator-Evaluator 反馈循环

**现状**：审查结果是终端输出，生成器（`chapter-draft`）下次运行时看不到上次审查的反馈

**改进思路**：
- `chapter-review` 和 `anti-ai-check` 的结果写入 `chapters/{id}_feedback.yaml`
- `chapter-draft` 在生成前自动读取该章节已有的 feedback 文件（如果存在）
- feedback 文件包含：具体问题、严重程度、修改建议、是否已解决
- 形成 "生成 -> 审查 -> 反馈落盘 -> 再生成时读取" 的闭环

**预期收益**：审查不再是一次性事件，而是持续改进的输入

---

## 四、要点与原文金句

### Harness 的本质

> "构建软件仍然需要纪律，但纪律更多地体现在支撑结构上，而不是代码上。" —— OpenAI

> "Harness 的每个组件都编码了一个关于模型做不到什么的假设，这些假设值得压力测试，因为它们可能是错误的，也因为它们会随着模型改进而过时。" —— Anthropic

### 评估的价值

> "没有 eval 的团队会陷入被动循环——修复一个故障，引发另一个，无法区分真正的回退和噪音。投资 eval 的团队发现相反的结果：开发加速，因为故障变成测试用例，测试用例防止回退，指标替代猜测。" —— Anthropic

> "评估最有用的时机之一是在 agent 开发之初，用来明确编码预期行为。两个工程师读同一份规格说明，可能对 AI 应如何处理边缘情况有不同的理解。一个 eval suite 可以消除这种歧义。" —— Anthropic

### 约束即加速

> "在以人为本的工作流程中，这些规则可能会让人感到迂腐。有了智能体，它们就成了倍增器：一旦编码，就能立即应用于所有地方。" —— OpenAI

> "人类的品味一旦被捕捉，就会持续应用于每一行代码。" —— OpenAI

### 上下文管理

> "Context rot：随着上下文窗口中 token 数量增加，模型准确回忆信息的能力下降。" —— Anthropic

> "给 Codex 的是一张地图，而不是一本 1,000 页的说明书。" —— OpenAI

---

## 五、一句话总结

> **Harness = 指令 + 工具 + 约束 + 评估 + 上下文管理。** 本项目在指令层（SKILL.md）和上下文管理（protocols + GUIDE.md）上做得不错，但在**机械化约束**（把规则变成可执行检查）和**评估闭环**（审查结果回馈给生成器）上有明显短板。最值得借鉴的是 OpenAI 的"当文档不够时，将规则转化为代码"和 Anthropic 的"生成与评估分离 + Sprint Contract"。
