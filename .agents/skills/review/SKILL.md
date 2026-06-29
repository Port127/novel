---
name: review
version: 1.0.0
description: >-
  多视角对抗式审查。full 模式并行 spawn 4 个 agent（story-architect / narrative-writer /
  character-designer / consistency-checker），lean 模式只 spawn architect + checker，
  solo 模式由主线程直接审查。agent 不可用时自动降级。
  触发方式：/review、/审查、「审查一下」「帮我审一下」
---

# review：多视角对抗式审查

你是审查协调器。你的职责是找出小说文本中的结构、角色、文字、设定问题，并给出可执行修改建议。

**执行铁律：审查是找问题，不是验证正确性。**

---

## Review Mode 选择

- `/review` 或 `/review full` → 优先 spawn 全部 4 个 Agent；缺失时自动降级
- `/review lean` → 优先 spawn story-architect + consistency-checker
- `/review solo` → 不 spawn Agent，由当前会话执行基础审查
- 未指定 → 默认 full，并在报告里写明最终实际执行模式

---

## Phase 0：预检与降级（必须先执行）

1. **确定请求模式**：解析用户输入中的 `full`、`lean`、`solo`；未指定时为 `full`
2. **检查 Agent 定义文件**：检查 `.agents/agents/` 下所需 agent 定义是否存在
   - full 必需：`story-architect.md`、`character-designer.md`、`narrative-writer.md`、`consistency-checker.md`
   - lean 必需：`story-architect.md`、`consistency-checker.md`
3. **降级判定**：
   - 4 个都存在 → full
   - 缺 narrative-writer 或 character-designer → lean（如果请求 full）
   - 缺 story-architect 或 consistency-checker → solo
4. **确认 Agent 工具可用**：如果当前环境没有 Agent 工具，直接降级 solo
5. **嵌套保护**：如果当前已在 subagent 内，不再 spawn，直接 solo
6. **确定实际模式**：报告中必须列出 `Requested Mode` 与 `Effective Mode`

---

## Phase 1：收集待审查内容

1. **确定审查范围**：
   - 用户指定了章节/文件 → 只审查指定内容
   - 用户未指定 → 审查最近修改的正文文件（`git diff --name-only` 中的正文文件），或当前书写进度最新章节
2. **读取支撑材料**：正文、相关设定（`settings/characters.yaml`、`settings/outline.yaml`）、大纲、追踪文件
3. **识别目标平台并加载 rubric**：
   - 优先使用用户显式指定的平台
   - 其次读取项目配置中的 `目标平台` 字段
   - 番茄 → 读取 `references/rubrics/fanqie.md`
   - 起点 → 读取 `references/rubrics/qidian.md`
   - 知乎 → 读取 `references/rubrics/zhihu.md`
   - 未识别 → 读取 `references/quality-rubric.md`
4. **形成审查基准包摘要**：把加载的 rubric 压缩为 5-12 条审查标准
5. **确定性预检**：运行脚本（如可用）
   ```bash
   node .agents/skills/daily-write/scripts/check-ai-patterns.js --check <正文文件>
   node .agents/skills/daily-write/scripts/check-degeneration.js --check <正文文件>
   ```
   将结果作为 findings 合并进报告

---

## Phase 2：并行 Spawn Agent（full/lean 模式）

使用 Agent 工具并行调用。每个 Agent 的 prompt 必须自包含：项目路径、审查范围、文件路径、审查基准包摘要。

**调用规则**：只有实际模式仍为 full/lean 时才 spawn。不要 spawn 缺失定义的 Agent。

### Agent 1: story-architect（full/lean 均调用）

读取 `.agents/agents/story-architect.md` 内容，拼接：
```
{agent 定义内容}

---
当前任务：审查
项目路径：{项目根}
审查范围：{文件路径/章节}
审查基准包摘要：{Phase 1 形成的 rubric 摘要}
相关文件路径：{settings/outline.yaml, settings/arcs.yaml, settings/pacing.yaml}
```

审查视角：主题对齐、大纲结构、钩子/反转质量、范围控制、平台期待。

### Agent 2: character-designer（仅 full）

读取 `.agents/agents/character-designer.md` 内容，拼接：
```
{agent 定义内容}

---
当前任务：审查
项目路径：{项目根}
审查范围：{文件路径/章节}
审查基准包摘要：{Phase 1 形成的 rubric 摘要}
相关角色文件：{settings/characters.yaml}
```

审查视角：角色语言风格一致性、对话质量、人物弧线、关系推进。

### Agent 3: narrative-writer（仅 full）

读取 `.agents/agents/narrative-writer.md` 内容，拼接：
```
{agent 定义内容}

---
当前任务：审查
项目路径：{项目根}
审查范围：{文件路径/章节}
审查基准包摘要：{Phase 1 形成的 rubric 摘要}
AI 味 / 禁用词摘要：{从 daily-write/references/banned-words.md 提取高频项}
```

审查视角：AI味检测、情绪烈度、格式合规、节奏均匀度、文字自然度。

### Agent 4: consistency-checker（full/lean 均调用）

读取 `.agents/agents/consistency-checker.md` 内容，拼接：
```
{agent 定义内容}

---
当前任务：审查
项目路径：{项目根}
审查范围：{文件路径/章节}
已知角色：{从 settings/characters.yaml 提取角色名列表}
```

审查视角：角色属性一致性、世界规则违反、时间线冲突、伏笔断线。

---

## Phase 3：综合裁决

1. 收集实际执行的 agent VERDICT 和 FINDINGS
2. 合并去重：按 severity 排序（S1 > S2 > S3 > S4），同级内按影响范围排序
3. **分歧呈现**：如果 agent 间有冲突意见，明确呈现分歧让用户裁决
4. 输出综合审查报告

---

## Phase 4：输出报告

### full / lean 模式报告模板

```markdown
=== 故事审查报告 ===
Requested Mode: {full | lean}
Effective Mode: {full | lean}
Fallback: none
审查范围: {章节/文件}

## 结论汇总
- story-architect:      APPROVE / CONCERNS(n) / REJECT / NOT_RUN
- character-designer:   APPROVE / CONCERNS(n) / REJECT / NOT_RUN
- narrative-writer:     APPROVE / CONCERNS(n) / REJECT / NOT_RUN
- consistency-checker:  APPROVE / CONCERNS(n) / REJECT / NOT_RUN

## 严重度统计
- S1: n
- S2: n
- S3: n
- S4: n

## 综合评定
APPROVE / CONCERNS / REJECT

## 发现的问题
（按统一 Findings Schema 列出，S1→S4 排序）

## Agent 分歧（如有）

## 修改建议（按优先级排列）
```

### solo 模式报告模板

```markdown
=== 故事审查报告（solo）===
Requested Mode: {full | lean | solo}
Effective Mode: solo
Fallback: agent unavailable -> solo
审查范围: {章节/文件}

## 基础检查结果

### 格式合规性
- 段落/对话/空行检查

### 设定一致性
- 字面事实冲突

### AI 味 / 禁用词
- 问题列表（附 evidence）

### Findings
（按统一 Findings Schema）

### 修改建议
```

---

## solo 模式基础检查

不 spawn Agent 时，必须执行以下基础检查：

1. **格式合规性**：段落按戏剧单元断开、对话独立成行、无空行
2. **设定一致性 grep**：角色名、属性、关键设定、伏笔关键词
3. **AI 味与禁用词**：对照 `daily-write/references/banned-words.md` 检查
4. **通用评分**：对照 `references/quality-rubric.md` 逐项检查
5. 按统一 Findings Schema 输出简化版报告

---

## 降级逻辑

```
4 个 agent 定义都存在 → full
缺 narrative-writer 或 character-designer → lean（如果请求 full）
缺 story-architect 或 consistency-checker → solo
任何 agent spawn 失败 → solo
当前已在 subagent 内 → solo
```

---

## 流程衔接

**流水线：** 通用
**位置：** 审查（写作之后）

| 时机 | 跳转到 | 命令 |
|---|---|---|
| 要修改查出的问题 | 对应写作 skill | 返回对应 skill 修改 |
| 发现 AI 味需清理 | daily-write | `/daily-write` 去 AI 味流程 |

---

## 语言

- 跟随用户的语言回复
- 中文回复遵循《中文文案排版指北》
