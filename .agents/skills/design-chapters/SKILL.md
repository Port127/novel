---
name: design-chapters
description: 细纲设计。按大纲拆分章节，生成节拍表，检查结构。
---

# design-chapters（细纲设计）

> **用途**：将大纲（outline.yaml）转化为章节计划（chapters_index.yaml）。每章包含摘要、节拍表、张力值、出场人物。
> **前置条件**：
> - `settings/outline.yaml` 存在（大纲已设计）
> - `settings/scout_report.yaml` 存在（品类已确定）
> **输出文件**：
> - `settings/chapters_index.yaml`（章节总索引和跨 Skill 调度表）
> - `settings/chapter_outlines/chapter_*.md`（单章详细蓝图，可选但推荐）

`settings/chapters_index.yaml` 必须遵循 `data/schemas/chapters.schema.yaml`；每章使用 `file` 指向 `content/chapter_XXX.md`，使用 `outline_file` 指向 `settings/chapter_outlines/chapter_XXX.md`。

---

## 1. 架构与行为规范 (System Rules)

> **[系统强制]** 本板块定义 Agent 必须遵守的操作流转规则，绝对不可违背或删减。
1. **防暴走与启发式交互 (UX)**：严禁一次性执行多个 Phase 或连发开放式提问。每个 Phase 结束前必须停下等待用户。提问时必须基于上下文提供 **2-3 个具体预设方案 (Option A/B/C)** 供用户选择或微调。
2. **多智能体编排 (Orchestration)**：在涉及重度脑暴或深度执行的 Phase 中，若需复杂的细纲脑暴，必须使用 `invoke_subagent` 唤醒子 Agent `story-architect` 承接具体工作（必须遵循下方的 Sub-agent 调用约束）。主 Agent 仅负责流程统筹与最终落盘。
3. **上下文闭环 (Context Loop)**：强制读取 `chapters.schema.yaml`，保障输出结果准确对应下游 `daily-write` 需求，不能读而不用。
4. **实时进度保存 (State Persistence)**：进入任何新的 Phase，必须立即更新根目录下的 `_progress.md` 文件。

## 2. 创作与业务准则 (Domain Rules)

> **[业务核心]** 本板块定义该 Skill 独有的领域知识、创作契约和设定标准。
1. **商业对齐 (Commercial Alignment)**：必须基于 `scout_report.yaml` 的要求分配单章节奏和爽点，刻意制造差异化。
2. **素材库联动 (Ecosystem)**：当缺乏具体情节或需要寻找灵感时，主动向用户推荐或直接使用 `/nm` 查询上游同类题材的经典细纲写法。
3. **节拍驱动**：每章由 3-15 个节拍组成，节拍是剧情最小单位。
4. **密度标记**：用"密/疏"标注每章节奏密度。密=多事件高压，疏=单事件沉淀。
5. **张力曲线**：每章分配张力值（1-5），整体形成波浪形曲线。
6. **字数预算**：每章 2000-5000 字，根据事件复杂度分配。
7. **品类感知**：根据 `scout_report.yaml` 调整章节策略。

---

## Phase 定义 (Phase State Machine)

> **【架构强制要求】**：
> 1. 生成任何结构化数据前，**必须使用 `view_file` 强制读取对应的 `data/schemas/chapters.schema.yaml`**。
> 2. 严禁按己意图捏造不在 Schema 中的顶级字段。

### Phase 1：大纲解析

**入口条件**：`outline.yaml` 存在
**目标**：解析大纲结构，提取所有节拍

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 1。
2. **强制读取 Schema**：读取本次目标输出对应的 `data/schemas/chapters.schema.yaml`。
3. 读取 `outline.yaml`，解析 acts → sequences → beats 层级。
4. 统计总节拍数、总幕数、转折点位置。
5. 读取 `scout_report.yaml` 的 `genre` 和 `required_elements`。
6. **启发式提问**：展示大纲概览与转化范围，提供 2-3 种转化选项 (Option A/B) 供用户选择。
7. **停顿确认**：等待用户确认转化范围后进入下一阶段。

**出口条件**：节拍列表已提取，转化范围已确认
**加载 References**：无

---

### Phase 2：章节拆分

**入口条件**：节拍列表已提取
**目标**：将节拍分配到各章，确定每章的节拍组

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 2。
2. 读取 `references/chapter-beat-guide.md`，加载节拍设计方法论。
3. 读取 `references/chapter-functions.md`，理解章节定位。
4. 按规则拆分：
   - 每章 3-15 个节拍
   - 密章：8-15 节拍，3000-5000 字
   - 疏章：3-7 节拍，2000-3000 字
   - 转折点章节必须为密章
   - 每 3-5 章形成一个"小高潮-沉淀"循环
5. **启发式提问**：展示 2-3 种章节拆分方案（偏快节奏/偏慢节奏）。
6. **停顿确认**：等待用户确认。

**出口条件**：章节拆分方案已确认
**加载 References**：`chapter-beat-guide.md`

---

### Phase 3：章节摘要

**入口条件**：章节拆分方案已确认
**目标**：为每章生成结构化摘要

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 3。
2. 读取 `references/chapter-template.md`，加载章节模板。
3. 读取 `references/hooks-guide.md`，用于章首和章尾钩子设计。
4. **批处理循环输出（防截断）**：
   - **执行限制**：由于 LLM 输出限制，绝对不能一次性生成全卷细纲。必须采用批处理模式。
   - 每次最多生成 3-5 章的细纲详情，严格按照 `references/chapter-template.md` 提供的 Frontmatter 和 Markdown 格式要求，写入 `settings/chapter_outlines/chapter_{N}.md`。
   - 当前批次生成完毕后，**立刻停顿**，向用户确认：“第 X-Y 章生成完毕，是否继续生成下一批？”
   - 收到用户继续指令后，循环执行，直至 Phase 2 拆分出的所有章摘要全部生成完毕。
5. 将每章的基本信息、五要素摘要提取后，保留在内存中供后续 Phase 处理。
6. **启发式提问**：在批处理过程中，抽取最重要的高潮章节展示其细化契约，提供不同的修改方案 (Option A/B) 供微调，询问是否满足预期。
7. **停顿确认**：全部细纲生成完毕，且与用户多轮迭代被最终确认后，进入下一阶段。

> **【Sub-agent 调用约束】**
> 若在细纲设计时需要唤醒 `story-architect` 辅助，**必须**使用以下 Prompt 模板，以防核心规则在 Agent 间传递时丢失：
> `Agent(subagent_type: "story-architect", prompt: "项目目录：{dir}\n任务类型：单章细纲设计\n查询参数：{需规划的具体章节与事件}\n章节定位契约：每章按它在一级结构里的位置标定位（高压/推进/修炼试错/关系回收/低压生活/信息整理；详见 references/chapter-functions.md）。只有高压/推进章配齐强钩子+密点爽点，低压章允许无显性爽点/0密点，但必须给读者阶段目标/期待。\n细纲字数预算契约：情节序列按字数预算编排，每点标密/疏并给预算（密≥250，疏≈40，铺垫≈120-150），各点求和Σ必须落在[章目标, 章目标×1.1]。每点写清『谁做了什么 + 功能标签』。")`

**出口条件**：所有章节摘要已生成
**加载 References**：`chapter-template.md`

---

### Phase 4：张力曲线

**入口条件**：章节摘要已生成
**目标**：为每章分配张力值，形成整体张力曲线

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 4。
2. 读取 `references/tension-design.md`，加载张力设计方法。
3. 按规则分配张力值：
   - 开篇章（第1章）：2-3
   - 转折点章节：4-5
   - 高潮章节：5
   - 沉淀章节：1-2
   - 相邻章节张力差不超过 2
4. **启发式提问**：展示张力曲线图（ASCII），提供 2-3 种调整方案 (Option A/B) 供选择，询问是否需要调整。
5. **停顿确认**：与用户多轮迭代，等待用户确认后完成。

**出口条件**：张力曲线已确认
**加载 References**：`tension-design.md`

---

### Phase 5：落盘验证 (Quality Gate)

**入口条件**：所有章节摘要和张力值已生成
**目标**：生成 outputs 并通过质量检查

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 5。
2. **最终检查**：汇总数据，确保结构严格符合 `chapters.schema.yaml`。
3. **写入文件**：
   - 写入 `settings/chapters_index.yaml`
   - 确保所有 `settings/chapter_outlines/chapter_*.md` 已落盘
4. **门禁校验**：
   - 运行 `node .agents/skills/design-chapters/scripts/check-chapters.js settings/chapters_index.yaml`
   - 运行 `node .agents/skills/design-chapters/scripts/check-outlines.js settings/chapter_outlines/`
5. 根据脚本输出的 `[blocking]` 或 `[advisory]` 信息，决定是否需要退回重做。如遇 `[blocking]` 错误，**必须阻断流程并要求退回修正**。
6. 验证通过后，清理 `_progress.md` 文件，宣告本技能完成。

**出口条件**：chapters_index.yaml 已生成且通过验证
**加载 References**：无

---

## 质量门禁 (Quality Gates)

- **`check-chapters.js`**：检查每章节拍数（3-15）、字数（2000-5000）、必填字段（file/outline_file/words_target/density/beats）完整性，以及正文路径和细纲路径格式。
- **`check-outlines.js`**：遍历检查所有细纲 Markdown 文件，验证结构完整性（必须有特定标题），并对正文中的所有密疏节点字数执行求和计算，确保与目标字数误差不超过 15%。
- **拦截逻辑**：如发现字段缺失、或者字数严重不符规定，将抛出 `[blocking]` 错误，此时视为阻断性错误，Agent 必须停下修正。

---

## 断点恢复 (Recovery)

**状态文件**：`_progress.md`（位于项目根目录）

**格式范例**：
```markdown
# design-chapters Progress
- current_phase: <1-5>
- status: in_progress | completed
- last_updated: <timestamp>
```

**恢复逻辑**：
- 启动时检查 `_progress.md`。
- 若状态非 completed，主动询问用户是否继续中断的进度，跳到对应的 current_phase。

---

## 输出文件

- `settings/chapters_index.yaml`：章节总索引和跨 Skill 调度表
- `settings/chapter_outlines/chapter_*.md`：每一章的细纲蓝图与字数预算

---

## References 索引

> ⚠️ **警告**：编写或更新此表时，必须确保 `references/` 目录下真实存在引用的文件。严禁引用幽灵文件或保留完全冗余的重复文件。

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | — | 大纲解析 |
| 2/3 | chapter-functions.md | 章节定位与张弛法则 |
| 2 | chapter-beat-guide.md | 节拍设计方法论 |
| 3 | chapter-template.md | 章节摘要模板 |
| 3 | hooks-guide.md | 章首/章尾钩子指南 |
| 4 | tension-design.md | 张力值分配方法 |
| 5 | — | 落盘验证 |

---

## 下一步 (Next Steps)

本技能完成、chapters_index.yaml 与单章蓝图生成后，推荐执行的操作或进入的下一步 Skill：
- `/daily-write`：日更正文写作，AI将依细纲完成写作闭环。
- `/golden-chapters`：黄金三章专属打磨。
