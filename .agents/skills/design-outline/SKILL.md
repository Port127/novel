---
name: design-outline
description: 大纲设计。交互式设计整体故事走向，检测节奏问题。
---

# 大纲设计

交互式设计小说大纲，含节奏检测和张力曲线分析。

---

## 前置依赖

- 世界观已设计（`settings/worldbuilding.yaml` 存在）
- 品类已选择

---

## 工作流程

### 1. 确认项目

运行 `novel list`，选择项目。

### 2. 交互式询问（借鉴旧 generate-outline 模式）

按以下顺序逐步确认：

**核心设定**：一句话概括故事核心

**主角设定**：名字、起点状态、终点状态

**冲突设计**：
- 外部冲突（主要对手/障碍）
- 内部冲突（主角的心理矛盾）

**结构规划**：
- 总章数
- 幕数（建议三幕式）
- 每幕核心事件

**确认生成**：汇总后请用户确认

### 3. 节奏分析

生成大纲后调用引擎检测节奏：

```python
from novel.core.skills.ask_architect import AskArchitectSkill
skill = AskArchitectSkill()
verdict = skill.evaluate({"chapters": chapter_list})
```

检查项：
- 是否连续 3 章以上慢节奏？
- 张力曲线是否合理？
- 高潮节点分布是否均匀？

### 4. 生成大纲文件

Agent 直接生成 `settings/outline.yaml` 单文件，包含：
- premise（核心设定）
- acts（各幕结构）
- hooks（伏笔-回收）

### 5. 展示与调整

展示大纲结构 + 节奏分析报告。询问是否需要调整。

---

## 输出文件

- `settings/outline.yaml`
- `settings/arcs.yaml`
- `settings/pacing.yaml`

## 参考

- Schema: `data/schemas/outline.schema.yaml`
- 引擎: `src/novel/core/skills/ask_architect.py`
- 旧模式: 旧 generate-outline 的交互流程
