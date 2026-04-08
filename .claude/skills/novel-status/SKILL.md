---
name: novel-status
description: 查看当前项目的详细状态
when_to_use: 用户想了解当前小说项目的整体情况
---

# 任务

显示当前小说项目的完整状态。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 如果 `current_path` 为空，提示用户先使用 `/novel-init` 创建项目

## 执行步骤

### 1. 读取项目状态

从 `{current_path}/.novel/state.yaml` 读取非推导字段（project、protagonist、ingestion、plot.structure、current_focus）。

### 2. 从源文件动态统计各模块数据

- **角色**: 读取 `characters/character_index.yaml` 或扫描 `characters/*.yaml`，统计角色数量和分类
- **剧情**: 读取 `plot/outline.md` 和 `chapters/index.yaml`，统计章节数
- **时间线**: 读取 `timeline/main.yaml`，统计事件数和时间范围
- **世界观**: 读取 `worldbuilding/worldbuilding.yaml` 和 `worldbuilding/entries/*.yaml`，统计设定条目数和确认状态
- **关系**: 读取 `characters/relations.yaml`，统计关系对数

### 3. 检查待处理事项

- 时间线冲突警告
- 角色信息不完整
- 伏笔未揭示

## 输出格式

```
📊 项目状态：《{{name}}》

┌─────────────────────────────────────┐
│ 基本信息                              │
├─────────────────────────────────────┤
│ 类型：{{genre}}                       │
│ 创建：{{created}}                     │
│ 更新：{{updated}}                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 内容统计                              │
├─────────────────────────────────────┤
│ 👥 角色：{{count}}个                  │
│    主角：{{protagonists}}             │
│    配角：{{supporting}}               │
│    反派：{{antagonists}}              │
│                                      │
│ 📖 剧情：                             │
│    结构：{{structure}}                │
│    章节：已规划{{chapters}}章          │
│    当前：{{current_focus}}            │
│                                      │
│ 📅 时间线：                           │
│    范围：{{start}} ~ {{end}}          │
│    事件：{{events_count}}个           │
│                                      │
│ 🌍 世界观：{{worldbuilding_status}}   │
└─────────────────────────────────────┘

{{#if warnings}}
⚠️ 待处理：
{{#each warnings}}
- {{this}}
{{/each}}
{{/if}}

💡 建议：
   /timeline-check    检查时间线
   /consistency-check 全面一致性检查
```

## 注意事项

- 显示关键信息，避免过长
- 标注待处理事项
- 给出下一步建议