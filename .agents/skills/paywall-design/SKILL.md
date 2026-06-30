---
name: paywall-design
description: 付费卡点设计。分析大纲找最优切割点，设计过渡章节奏。
---

# paywall-design（付费卡点设计）

> **用途**：分析大纲和张力曲线，找到最优付费切割点，设计过渡章节奏。
> **前置条件**：
> - `settings/outline.yaml` 存在（大纲已完成）
> - `settings/chapters_index.yaml` 存在（细纲已完成）
> - 黄金三章已完成（可选但推荐）
> **输出文件**：`paywall_report.yaml`

---

## 1. 架构与行为规范 (System Rules)

> **[系统强制]** 本板块定义 Agent 必须遵守的操作流转规则，绝对不可违背或删减。
1. **防暴走与启发式交互 (UX)**：严禁一次性执行多个 Phase 或连发开放式提问。每个 Phase 结束前必须停下等待用户。提问时必须基于上下文提供 **2-3 个具体预设方案 (Option A/B/C)** 供用户选择或微调。
2. **多智能体编排 (Orchestration)**：在涉及重度脑暴或深度执行的 Phase 中，主 Agent 必须使用 `invoke_subagent` 唤醒对应的专业子 Agent（如 `story-architect`, `character-designer`）来负责具体的交互与生成，主 Agent 仅负责流程统筹与最终落盘。
3. **上下文闭环 (Context Loop)**：如果在 Phase 中要求读取上游文件（如 worldbuilding），则最终落盘的数据结构中，必须有对应的联动字段（如 schema 中的可选阵营字段）进行支撑，不能读而不用。
4. **实时进度保存 (State Persistence)**：进入任何一个新的 Phase，必须立即更新根目录下的 `_progress.md` 文件。

## 2. 创作与业务准则 (Domain Rules)

> **[业务核心]** 本板块定义该 Skill 独有的领域知识、创作契约和设定标准。重构时必须**全量保留**原有的业务逻辑。
1. **爽点兑现**：付费切割点必须在爽点兑现之后，不在低谷期切。
2. **双重保险**：免费末章必须做到"爽点兑现 + 致命悬念"。
3. **即时反馈**：付费首章 200 字内必须给出爽感反馈。
4. **平台适配**：不同平台的付费模式影响切割策略。
5. **读者心理**：利用损失厌恶和沉没成本设计付费动机。
6. **素材库联动 (Ecosystem)**：当遇到生僻设定或需要寻找灵感时，主动向用户推荐或直接使用 `/nm` 系列命令查询上游素材库。

---

## Phase 定义 (Phase State Machine)

> **【架构强制要求】**：
> 1. 生成任何结构化数据前，**必须使用 `view_file` 强制读取对应的 `data/schemas/*.schema.yaml`**。
> 2. 严禁按己意图捏造不在 Schema 中的顶级字段。
> 3. Reference 文件应当按需在具体的 Phase 中加载，不要在 Phase 1 一次性全读完。

### Phase 1：大纲分析

**入口条件**：outline.yaml + chapters_index.yaml 存在
**目标**：分析张力曲线，标记候选切点

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 1。
2. 读取上游关键文件 `settings/outline.yaml` 和 `settings/chapters_index.yaml`。
3. 提取张力曲线数据。
4. 读取 `references/cut-point-method.md`，加载切点选择方法论。
5. 标记候选切点（张力 ≥ 4 的章节后）。
6. 排除不适合的切点（主角低谷期、无悬念章节）。
7. **预警机制**：如果在预期的付费字数/章节区间内（如前20-30章）未能找到合格的候选切点，**必须暂停流程**。
8. **回退方案**：主动向用户提出警告，并建议用户退回 `/design-chapters` 或 `/design-outline`，采用“卡点倒推法”重新设计大纲的高潮节点。（需同时输出包含“核心反派锚定”与“冗余剔除”原则的 Summary，供用户带给上游 Agent）
9. 展示候选切点列表。
10. **停顿确认**：等待用户确认候选列表后进入下一阶段。

**出口条件**：候选切点列表已确认
**加载 References**：`cut-point-method.md`

---

### Phase 2：切点决策

**入口条件**：候选切点列表已确认
**目标**：评估候选切点，确定最优切点

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 2。
2. 读取 `references/paywall-psychology.md`，加载付费心理分析。
3. 按评估维度打分每个候选切点：
   - 爽点兑现度（前章是否有爽点）
   - 悬念强度（切割后的悬念是否足够）
   - 读者情感（切割时读者的情感状态）
   - 平台适配（是否符合目标平台模式）
4. **启发式提问**：基于评估结果，提供 2-3 个具体的预设切点方案（Option A/B/C）供用户选择。
5. **停顿确认**：与用户多轮迭代，直到最优切点被用户确认。

**出口条件**：最优切点已确定
**加载 References**：`paywall-psychology.md`

---

### Phase 3：过渡设计

**入口条件**：切点已确定
**目标**：设计免费末章和付费首章的节奏

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 3。
2. 读取 `references/transition-guide.md`，加载过渡章设计指南。
3. 设计免费末章：
   - 爽点兑现（让读者满足）
   - 致命悬念（让读者不花钱就难受）
4. 设计付费首章：
   - 200 字内爽感反馈
   - 展开新弧线/新悬念
5. **启发式提问**：提供 2-3 个具体的过渡章设计方案（Option A/B 节奏组合）供用户选择。
6. **停顿确认**：等待用户确认过渡章设计方案后进入下一阶段。

**出口条件**：过渡章设计方案已确认
**加载 References**：`transition-guide.md`

---

### Phase 4：平台适配

**入口条件**：过渡章设计方案已确认
**目标**：根据目标平台调整付费策略

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 4。
2. 读取 `references/platform-paywall.md`，加载各平台付费模式。
3. 根据项目情况调整策略：
   - 番茄（免费+广告）：不需要付费切割，但需要设计广告插入点
   - 起点（千字付费）：优化切割点，确保读者愿意付费
   - 晋江（VIP付费）：考虑女性读者偏好
4. 生成平台适配方案。
5. **停顿确认**：等待用户确认平台适配方案后进入下一阶段。

**出口条件**：平台适配完成
**加载 References**：`platform-paywall.md`

---

### Phase 4.5：架构师商业复核 (Subagent Review)

**入口条件**：过渡章设计及平台适配已确认
**目标**：借助专家视角评估付费吸引力

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 4.5。
2. 提示用户：“为了确保付费转化率，建议由【故事架构师】进行复核”。
3. 若用户允许，使用 `invoke_subagent` 唤醒 `story-architect`。
4. 提交任务：“请基于当前的过渡设计方案（免费末章悬念 + 付费首章反馈），评估其是否构成了不可抗拒的付费动机，是否存在逻辑硬伤或情绪断档？”
5. 根据架构师的反馈吸收建议并微调方案。
6. **停顿确认**：等待用户对最终方案确认。

**出口条件**：商业复核完成，方案最终定稿
**加载 References**：无

---

### Phase 5：落盘验证

**入口条件**：所有设计已完成
**目标**：生成 paywall_report.yaml

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 5。
2. 汇总所有设计数据，并在内存中审查其是否符合数据输出范式要求。
3. 写入 `paywall_report.yaml`（注意：文件根节点必须包含 `paywall_chapter: <数字>` 字段）。
4. **门禁校验**：运行 `node .agents/skills/paywall-design/scripts/check-paywall.js settings/chapters_index.yaml paywall_report.yaml` 验证切点合理性。
5. 若脚本抛出 blocking 错误则打回修改，否则展示最终报告。
6. **状态清理**：验证通过后，清理 `_progress.md` 文件，宣告本技能完成。

**出口条件**：paywall_report.yaml 已生成，且通过脚本验证
**加载 References**：无

---

## 断点恢复 (Recovery)

**状态文件**：`_progress.md`（位于项目根目录）

**格式范例**：
```markdown
# paywall-design Progress
- current_phase: <1-5>
- status: in_progress | completed
- last_updated: <timestamp>
```

**恢复逻辑**：
- 启动时检查 `_progress.md`。
- 若状态非 completed，主动询问用户是否继续中断的进度，跳到对应的 current_phase。

---

## 质量门禁 (Quality Gates)

- **脚本一**：`node .agents/skills/paywall-design/scripts/check-paywall.js settings/chapters_index.yaml paywall_report.yaml` 验证切点章张力值 > 全章均值，前后悬念密度达标，以及前方是否有过长平淡期。
- **拦截逻辑**：若切点张力 < 4 或无法提取 `paywall_chapter`，返回 blocking 错误，必须阻断流程；若前期存在长平淡期，返回 advisory 警告，建议用户修改。

---

## References 索引

> ⚠️ **警告**：编写或更新此表时，必须确保 `references/` 目录下真实存在引用的文件。严禁引用幽灵文件或保留完全冗余的重复文件。

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | `cut-point-method.md` | 切点选择方法论 |
| 2 | `paywall-psychology.md` | 付费心理分析 |
| 3 | `transition-guide.md` | 过渡章设计 |
| 4 | `platform-paywall.md` | 平台付费模式 |
| 4.5 | — | 架构师商业复核 |
| 5 | — | 落盘验证 |

---

## 下一步 (Next Steps)

付费卡点设计完成后，推荐进入下一步骤：
- `/daily-write`：开始日更写作。在启动 `/daily-write` 写过渡章节时，务必提醒 Agent 优先读取 `paywall_report.yaml` 以严格遵循节奏设计和即时爽感反馈要求。从切割点开始写作。

---

## 数据输出范式示例

> ⚠️ **警告**：大模型往往会优先模仿当前上下文中的示例。此处提供 YAML 格式的参考示例，其层级结构（嵌套的数组、对象）与具体键名必须 100% 贴合脚本校验与下游调用的约束。

```yaml
# paywall_report.yaml 示例：
paywall_chapter: 25  # [必填] 必须放在根节点，供 check-paywall.js 提取
paywall_evaluation:
  satisfaction:
    score: 8/10
    source: "主角击败小反派"
  curiosity:
    score: 9/10
    source: "大反派登场，悬念拉满"
  expectation:
    score: 8/10
    source: "暗示更大的冲突即将展开"
  attachment:
    score: 7/10
    source: "读者已认同主角"
  total: 32/40
  recommendation: "强烈推荐"

transition_design:
  free_chapter_end:
    rhythm: "快→更快→悬念"
    satisfaction_hook: "当众碾压曾经看不起自己的人"
    fatal_hook: "一个更强大的存在注意到了他"
  paid_chapter_start:
    rhythm: "反馈→展开→钩子"
    instant_feedback: "对手的震惊反应"
    new_arc: "新的悬念展开"
```
