---
name: skill-name-placeholder
description: 一句话描述该 Skill 的核心用途和触发场景。
---

# skill-name-placeholder（中文名称）

> **用途**：明确指出本技能解决什么具体问题。
> **前置条件**：例如 `settings/scout_report.yaml` 存在（明确数据的上下文依赖）。
> **输出文件**：列出本技能执行完毕后会修改或创建哪些文件。

---

## 核心原则 (Core Principles)

1. **防暴走与启发式交互 (UX)**：严禁一次性执行多个 Phase 或连发开放式提问。每个 Phase 结束前必须停下等待用户。提问时必须基于上下文提供 **2-3 个具体预设方案 (Option A/B/C)** 供用户选择或微调。
2. **多智能体编排 (Orchestration)**：在涉及重度脑暴或深度执行的 Phase 中，主 Agent 必须使用 `invoke_subagent` 唤醒对应的专业子 Agent（如 `story-architect`, `character-designer`）来负责具体的交互与生成，主 Agent 仅负责流程统筹与最终落盘。
3. **商业对齐 (Commercial Alignment)**：必须基于 `scout_report.yaml` 中的 `competition_analysis` (竞争分析) 和 `core_hooks` (核心卖点) 进行设计，刻意制造差异化。
4. **素材库联动 (Ecosystem)**：当遇到生僻设定或需要寻找灵感时，主动向用户推荐或直接使用 `/nm` 系列命令查询上游素材库。
5. **上下文闭环 (Context Loop)**：如果在 Phase 中要求读取上游文件（如 worldbuilding），则最终落盘的数据结构中，必须有对应的联动字段（如 schema 中的可选阵营字段）进行支撑，不能读而不用。
6. **实时进度保存 (State Persistence)**：进入任何一个新的 Phase，必须立即更新根目录下的 `_progress.md` 文件。

---

## Phase 定义 (Phase State Machine)

> **【架构强制要求】**：
> 1. 生成任何结构化数据前，**必须使用 `view_file` 强制读取对应的 `data/schemas/*.schema.yaml`**。
> 2. 严禁按己意图捏造不在 Schema 中的顶级字段。
> 3. Reference 文件应当按需在具体的 Phase 中加载，不要在 Phase 1 一次性全读完。

### Phase 1：准备与上下文对齐

**入口条件**：前置条件满足
**目标**：拉取基础上下文，确认本技能的操作范围

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 1。
2. **强制读取 Schema**：使用 `view_file` 读取本次目标输出对应的 `data/schemas/*.schema.yaml`。
3. 读取上游关键文件（如 `scout_report.yaml`），提取商业分析与品类核心要素。
4. （如有）读取当前 Phase 所需的 `references/xxx.md`。
5. 综合以上信息，向用户清晰展示本技能即将涵盖的设计/执行范围。
6. **停顿确认**：等待用户确认后进入下一阶段。

**出口条件**：操作范围已与用户确认。
**加载 References**：按需列出

---

### Phase 2：核心任务拆解一（示例）

**入口条件**：Phase 1 已完成
**目标**：执行本技能的第一块核心任务

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 2。
2. （如有）读取专属 `references/xxx.md` 指南。
3. **编排指令**：[可选] 唤醒子 Agent (如 `story-architect`) 承接具体工作。
4. **启发式提问**：子 Agent / 主 Agent 提供 Option A/B/C 的方案。
5. **停顿确认**：与用户多轮迭代，直到本环节内容被用户 Accept。

**出口条件**：任务一的数据已在内存中准备就绪。
**加载 References**：按需列出

---

*(根据需要横向扩展 Phase 3, Phase 4 ... 直到核心任务完成)*

---

### Phase N：落盘验证 (Quality Gate)

**入口条件**：所有必须的设计/执行 Phase 均已完成
**目标**：生成最终文件并通过自动化门禁检查

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 N。
2. **最终检查**：汇总所有内存中的设定，审查是否严格符合 Phase 1 中读取的 Schema 结构。
3. **写入文件**：生成并写入对应的目标文件。
4. **门禁校验**：运行该 Skill 专属的 `scripts/*.js` 门禁脚本进行强制校验（如 `node .agents/skills/<skill_name>/scripts/check-completeness.js`）。
5. 根据脚本输出的 `[blocking]` 或 `[advisory]` 信息，决定是否需要退回重做。如有阻断性错误，**必须阻断流程并修正**。
6. 验证通过后，清理 `_progress.md` 文件（如适用），宣告本技能完成。

**出口条件**：目标文件已合规生成并写入硬盘。
**加载 References**：无

---

## 断点恢复 (Recovery)

**状态文件**：`_progress.md`（位于项目根目录）

**格式范例**：
```markdown
# <skill_name> Progress
- current_phase: <1-N>
- status: in_progress | completed
- last_updated: <timestamp>
```

**恢复逻辑**：
- 启动时检查 `_progress.md`。
- 若状态非 completed，主动询问用户是否继续中断的进度，跳到对应的 current_phase。

---

## 质量门禁 (Quality Gates)

- **脚本一**：描述 `scripts/xxx.js` 检查什么（如标签冲突、字段缺失）。
- **拦截逻辑**：明确脚本返回何种代码/关键字时属于阻断性错误。

---

## References 索引

> ⚠️ **警告**：编写或更新此表时，必须确保 `references/` 目录下真实存在引用的文件。严禁引用幽灵文件或保留完全冗余的重复文件。

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | `xxx.md` | 用途说明 |
| 2 | `yyy.md` | 用途说明 |

---

## 下一步 (Next Steps)

本技能完成后，推荐执行的操作或进入的下一步 Skill：
- `/next-skill-1`：简述理由
- `/next-skill-2`：简述理由

---

## 数据输出范式示例 (可选，但必须合规)

> ⚠️ **警告**：大模型往往会优先模仿当前上下文中的示例。如果在此处提供 YAML/JSON 格式的参考示例，**其层级结构（嵌套的数组、对象）与具体键名必须 100% 贴合目标 Schema 的定义**。
> - 严禁将深层嵌套结构错误提权为顶层数组。
> - 严禁捏造 Schema 不支持的独立顶层键。

```yaml
# 示例：
# 这里填入经过严格审查，与 schema.yaml 分毫不差的结构示范...
```
