---
name: design-chapters
description: 细纲设计。按大纲拆分章节，生成节拍表，检查结构。
---

# 细纲设计

按大纲拆分章节，每章生成节拍表，检查结构合理性。

---

## 前置依赖

- 大纲已设计（`settings/outline.yaml` 存在）

---

## 工作流程

### 1. 检查大纲

展示大纲结构，确认转化范围（全部 / 前 N 章）。

### 2. 确认参数

- 章节数
- 每章字数（短章 1500-2000 / 标准 2000-3000 / 长章 3000-5000）

### 3. 生成章节计划

基于大纲节拍，转化为章节摘要。每章包含：
- number（章节号）
- title（标题）
- summary（摘要）
- tension（张力值）
- beats（节拍表）

### 4. 结构检查

调用引擎检查每章结构：

```python
from novel.core.skills.flesh_out_chapter import FleshOutChapterSkill
skill = FleshOutChapterSkill()
verdict = skill.evaluate(outline)
```

检查项：
- 必要字段是否齐全？
- 节拍数量是否合理（3-15 个）？
- 目标字数是否合理（2000-5000）？

### 5. 展示与调整

展示前 5-10 章预览 + 张力曲线。询问是否合并/拆分/调整。

### 6. 生成章节文件

Agent 生成 `settings/chapters_index.yaml`。

---

## 章节状态

| 状态 | 含义 |
|------|------|
| planned | 已规划，有摘要，无正文 |
| draft | 有正文草稿 |
| written | 正文完成 |
| revised | 已润色 |

## 输出文件

- `settings/chapters_index.yaml`

## 参考

- Schema: `data/schemas/chapters.schema.yaml`
- 引擎: `src/novel/core/skills/flesh_out_chapter.py`
