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
> - `settings/chapters_index.yaml`
> - `settings/chapter_outlines/chapter_*.md`

---

## 核心原则 (Core Principles)

1. **防暴走与启发式交互 (UX)**：严禁一次性执行多个 Phase 或连发开放式提问。每个 Phase 结束前必须停下等待用户确认。
2. **多智能体编排 (Orchestration)**：若需复杂的细纲脑暴，可呼叫 `story-architect` 辅助章节结构优化。
3. **商业对齐 (Commercial Alignment)**：必须基于 `scout_report.yaml` 的要求分配单章节奏和爽点。
4. **素材库联动 (Ecosystem)**：缺乏具体情节时，可使用 `/nm` 查询上游同类题材的经典细纲写法。
5. **上下文闭环 (Context Loop)**：强制读取 `chapters.schema.yaml`，保障输出结果准确对应下游 `daily-write` 需求。
6. **实时进度保存 (State Persistence)**：进入任何新的 Phase，必须更新根目录下的 `_progress.md` 文件。

### 业务核心规则
7. **节拍驱动**：每章由 3-15 个节拍组成，节拍是剧情最小单位。
8. **密度标记**：用"密/疏"标注每章节奏密度。密=多事件高压，疏=单事件沉淀。
9. **张力曲线**：每章分配张力值（1-5），整体形成波浪形曲线。
10. **字数预算**：每章 2000-5000 字，根据事件复杂度分配。
11. **品类感知**：根据 `scout_report.yaml` 调整章节策略。

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
6. **启发式提问**：展示大纲概览与转化范围，提供转化选项。
7. **停顿确认**：等待用户确认转化范围。

**出口条件**：节拍列表已提取，转化范围已确认
**加载 References**：无

---

### Phase 2：章节拆分

**入口条件**：节拍列表已提取
**目标**：将节拍分配到各章，确定每章的节拍组

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 2。
2. 读取 `references/chapter-beat-guide.md`，加载节拍设计方法论。
3. 按规则拆分：
   - 每章 3-15 个节拍
   - 密章：8-15 节拍，3000-5000 字
   - 疏章：3-7 节拍，2000-3000 字
   - 转折点章节必须为密章
   - 每 3-5 章形成一个"小高潮-沉淀"循环
4. **启发式提问**：展示 2-3 种章节拆分方案（偏快节奏/偏慢节奏）。
5. **停顿确认**：等待用户确认。

**出口条件**：章节拆分方案已确认
**加载 References**：`chapter-beat-guide.md`

---

### Phase 3：章节摘要

**入口条件**：章节拆分方案已确认
**目标**：为每章生成结构化摘要

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 3。
2. 读取 `references/chapter-template.md`，加载章节模板。
3. 按《细纲蓝图》模板为每章生成详情，并写入 `settings/chapter_outlines/chapter_{N}.md`：

```markdown
## 细纲（第 N 章）
### 第 N 章：{章名}
- 核心事件：{一句话}
- 字数目标：{X} 字
- 目标情绪：{情绪}
- 章节定位：{高压/推进/修炼试错/关系回收/低压生活/信息整理}
- 章首钩子：{类型} — {内容}
- 爽点：{内容；低压章可写"无显性爽点，功能是…"}

#### 内容概括（五段式）
- 起因：{本章事件为什么发生}
- 发展：{冲突如何推进}
- 转折：{信息/关系/局势哪里改变}
- 高潮：{本章情绪或动作峰值}
- 结尾：{收束到什么状态}

#### 情节安排（多线）
- 主线推进：{本章对主目标的推进}
- 辅线推进：{可写"无"，不能凭空制造}
- 事件线 / 任务线：{外部事件链}
- 感情线 / 关系线：{无显性时写"无显性，但关系变化为…"}
- 逻辑线：原因 → 行动 → 结果 → 后果/新问题

#### 人物关系和出场顺序
- 出场顺序：{角色/势力/关键物件按实际出现顺序列出}
- 人物关系变化：{本章前 → 本章后}
- 视角/信息差：{谁知道什么；读者知道什么；主角误判什么}

#### 情节细化与字数预算（质量门禁核心）
- 细化契约：按字数预算编排情节点。每个点标明「密/疏」与「字数预算」。
  - 密（爽点/打脸/反转/情绪高潮，须展开）：≥250 字（慢镜头 400-600字）
  - 疏（过场/赶路/信息交代，须带过）：≈40 字
  - 铺垫/日常：120-150 字
- 预算校验：各点预算求和 Σ 必须落在 [章目标, 章目标×1.1]。末尾写一行 `预算合计：X字（目标Y，范围Y-Z）`。
- 情节点序列示例：{谁做了什么 + 功能标签 + [密/疏·X字]}
- 代价兑现 / 收益兑现：{谁付出什么代价；谁获得什么收益}

#### 结尾设定和钩子
- 结尾设定：{收束状态；未解决问题；下一章推动力}
- 章尾钩子：{类型} — {内容；期待度：强/中/弱}
```

4. 将每章的基本信息、五要素摘要提取后更新至 `settings/chapters_index.yaml`。
5. **启发式提问**：抽取最重要的高潮章节展示其细化契约，询问是否满足预期。
6. **停顿确认**：等待用户确认并微调。

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
4. **启发式提问**：展示张力曲线图（ASCII），询问是否需要调整。
5. **停顿确认**：等待用户确认。

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
   - 运行 `scripts/check-chapters.js settings/chapters_index.yaml`
5. 如遇 `[blocking]` 错误，阻断并要求退回修正。
6. 验证通过后，清理 `_progress.md` 文件。

**出口条件**：chapters_index.yaml 已生成且通过验证
**加载 References**：无

---

## 质量门禁

- `check-chapters.js`：检查每章节拍数（3-15）、字数（2000-5000）、必填字段完整性

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

- `settings/chapters_index.yaml`：章节索引
- `settings/chapter_outlines/chapter_*.md`：每一章的细纲蓝图与字数预算

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | — | 大纲解析 |
| 2 | chapter-beat-guide.md | 节拍设计方法论 |
| 3 | chapter-template.md | 章节摘要模板 |
| 4 | tension-design.md | 张力值分配方法 |
| 5 | — | 落盘验证 |

---

## 下一步 (Next Steps)

chapters_index.yaml 与单章蓝图生成后，可进入：
- `/daily-write`：日更正文写作，AI将依细纲完成写作闭环。
- `/golden-chapters`：黄金三章专属打磨。
