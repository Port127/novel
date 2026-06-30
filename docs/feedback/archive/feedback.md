# bug

# 阶段行优化
- 审查.agents/skills所有定义schema：
第一层：是否都已经跟项目对齐。
第二层：不同的skills，使用同一份schema的时候是否存在冲突。
第三层：判断这些schema是否够用，是否需要补充？参考本项目同级项目other/oh-story-claudecode。

# 长期优化（暂时不管）

## 对于项目的疑问（学习提升）

# 常用话术
- 好，使用commit-msg，帮我commit，然后push


# 小说skill
你先阅读.agents/skills/paywall-design（skill、references、scripts），注意：每个字符都要看！
（参考内容，本项目同级项目other/oh-story-claudecode，是否使用它的提示词，照抄了还是进行针对本项目的改造？有没有缺漏关键能力）
帮我看看有哪些欠缺，包括但不限于描述、提示词、上下文、引用文件
你要整体的审查这个skill，放在我们整个系统、agent中所起到的作用，整体审查
------
请帮我深度审查 `.agents/skills/daily-write`。为了保证审查质量，请严格按照以下步骤执行：
**1. 设定目标与上下文**
- **目标检索**：完整读取目标 Skill 目录下的所有核心文件（`SKILL.md`, `references/`, `scripts/`）。
- **参考标的路径**：`../oh-story-claudecode/`
- **全局上下文**：请先回顾 `.agents/AGENTS.md` 中的系统架构，理解该 Skill 在整个 V4 创作流或协作系统中的定位。
**2. 信息收集（强制使用工具）**
- 使用文件读取工具，完整读取目标 Skill 目录下的所有文件，包括 `SKILL.md`（核心提示词与流程）、`references/`（知识库）、`scripts/`（验证脚本）以及任何相关联的数据字典（`schemas/`）。
- 跨项目查阅 `oh-story-claudecode` 中对应或类似功能的实现。
**3. 执行深度对比与审查**
请从以下四个维度进行诊断，并指出欠缺之处：
- **能力对比**：相比 `oh-story-claudecode`，当前的实现是照搬还是做了针对性改造？是否遗漏了对方的某个关键能力或优秀的 Prompt 技巧？
- **提示词与描述质量**：`SKILL.md` 中的 Phase 划分是否合理？指令是否足够明确且具有确定性？描述（Description）能否精准触发该能力？
- **上下文与数据流**：该 Skill 的前置依赖是否清晰？产出的格式是否符合下游 Schema 规范？
- **系统集成度**：站在整个系统 Agent 协同的高度，这个 Skill 的定位是否越界？是否有效地调用了子 Agent（如 review 机制）或上游素材库（如 nm）？
**4. 交付要求**
请以结构化的 Markdown 报告输出你的审查结果。报告需包含：【核心结论】、【能力缺失盘点】、【同级项目对比分析】以及【具体的优化修改建议（含 Prompt 示例）】。
------

现在参考 .agents/skills/SKILL_TEMPLATE.md，对当前 Skill 进行非破坏性合并。请你只把模板里的架构要求（UX、进度保存、门禁等）穿插进去，绝对不要删减、概括或修改任何原有的业务逻辑、细化标准和模板格式！

再审查一次.agents/skills/daily-write（skill、references、scripts），从多角度、全局考虑，有任何问题都可以提出来

反思、提炼的改动，然后分析是否有可以落实到.agents/skills/SKILL_TEMPLATE.md的内容

好，帮我使用commit-msg进行commit，然后push

