---
name: show-project
description: 此技能仅在用户明确调用"/show-project"或直接提及技能名称时使用。
---

# 查看项目状态

展示项目详情和写作进度。

## 工作流程

### 1. 项目列表

```bash
python scripts/project.py list
```

### 2. 项目详情

```bash
python scripts/project.py show {project_id}
```

展示：基本信息、设定统计、章节统计。

### 3. 详细进度

```bash
python scripts/stats.py {project_id} --detail
```

展示每章详情。

### 4. 进度可视化

设定完成度、章节进度、总字数进度。

## 状态图标

○ planned | ◐ draft | ● written | ★ revised | ✓ 完成

## 参考

- Schema: `data/schemas/project.schema.yaml`