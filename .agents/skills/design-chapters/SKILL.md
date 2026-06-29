---
name: design-chapters
description: 细纲设计。按大纲拆分章节，生成节拍表，检查结构。
---

# design-chapters（细纲设计）

> **用途**：将大纲（outline.yaml）转化为章节计划（chapters_index.yaml）。每章包含摘要、节拍表、张力值、出场人物。
> **前置条件**：
> - `settings/outline.yaml` 存在（大纲已设计）
> - `settings/scout_report.yaml` 存在（品类已确定）
> **输出文件**：`settings/chapters_index.yaml`

---

## 核心原则

1. **节拍驱动**：每章由 3-15 个节拍组成，节拍是剧情最小单位。
2. **密度标记**：用"密/疏"标注每章节奏密度。密=多事件高压，疏=单事件沉淀。
3. **张力曲线**：每章分配张力值（1-5），整体形成波浪形曲线。
4. **字数预算**：每章 2000-5000 字，根据事件复杂度分配。
5. **品类感知**：根据 `scout_report.yaml` 调整章节策略。

---

## Phase 定义

### Phase 1：大纲解析

**入口条件**：`outline.yaml` 存在
**目标**：解析大纲结构，提取所有节拍

**步骤**：
1. 读取 `outline.yaml`，解析 acts → sequences → beats 层级
2. 统计总节拍数、总幕数、转折点位置
3. 读取 `scout_report.yaml` 的 `genre` 和 `required_elements`
4. 展示大纲概览，让用户确认转化范围

**出口条件**：节拍列表已提取，转化范围已确认
**加载 References**：无

---

### Phase 2：章节拆分

**入口条件**：节拍列表已提取
**目标**：将节拍分配到各章，确定每章的节拍组

**步骤**：
1. 读取 `references/chapter-beat-guide.md`，加载节拍设计方法论
2. 按规则拆分：
   - 每章 3-15 个节拍
   - 密章：8-15 节拍，3000-5000 字
   - 疏章：3-7 节拍，2000-3000 字
   - 转折点章节必须为密章
   - 每 3-5 章形成一个"小高潮-沉淀"循环
3. 展示章节拆分方案，让用户确认

**出口条件**：章节拆分方案已确认
**加载 References**：`chapter-beat-guide.md`

---

### Phase 3：章节摘要

**入口条件**：章节拆分方案已确认
**目标**：为每章生成结构化摘要

**步骤**：
1. 读取 `references/chapter-template.md`，加载章节模板
2. 按模板为每章生成摘要：
   - 五要素摘要（主线推进/人物变化/伏笔/情绪/钩子）
   - 多线情节标注（主线/副线/暗线）
   - 出场人物列表
   - 字数预算
3. 每章摘要控制在 150-300 字

**出口条件**：所有章节摘要已生成
**加载 References**：`chapter-template.md`

---

### Phase 4：张力曲线

**入口条件**：章节摘要已生成
**目标**：为每章分配张力值，形成整体张力曲线

**步骤**：
1. 读取 `references/tension-design.md`，加载张力设计方法
2. 按规则分配张力值：
   - 开篇章（第1章）：2-3
   - 转折点章节：4-5
   - 高潮章节：5
   - 沉淀章节：1-2
   - 相邻章节张力差不超过 2
3. 展示张力曲线图（ASCII），让用户确认

**出口条件**：张力曲线已确认
**加载 References**：`tension-design.md`

---

### Phase 5：落盘验证

**入口条件**：所有章节摘要和张力值已生成
**目标**：生成 chapters_index.yaml 并通过质量检查

**步骤**：
1. 汇总所有章节数据，展示概览
2. 写入 `settings/chapters_index.yaml`
3. 运行 `scripts/check-chapters.js settings/chapters_index.yaml` 验证
4. 展示验证结果，如有问题则回到对应 Phase 修复
5. 清理 `_progress.md`

**出口条件**：chapters_index.yaml 已生成且通过验证
**加载 References**：无

---

## 质量门禁

- `check-chapters.js`：检查每章节拍数（3-15）、字数（2000-5000）、必填字段完整性

---

## 断点恢复

**状态文件**：`_progress.md`
**格式**：同 scout-topic
**恢复逻辑**：跳到最后一个 in_progress 的 Phase

---

## 输出文件

- `settings/chapters_index.yaml`：章节索引

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

## 下一步

chapters_index.yaml 生成后，可进入：
- `/golden-chapters`：黄金三章锻造（基于细纲生成前 3 章正文）
