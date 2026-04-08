---
name: consistency-check
description: 全面一致性检查
when_to_use: 用户想确保小说设定没有矛盾
---

# 任务

全面检查项目一致性。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`

## 执行步骤

### 1. 收集所有数据

读取：
- `{current_path}/.novel/state.yaml`（仅取非推导字段：project、ingestion、plot.structure、current_focus）
- `{current_path}/characters/character_index.yaml`
- `{current_path}/characters/*.yaml`
- `{current_path}/characters/relations.yaml`
- `{current_path}/characters/relation_events.yaml`
- `{current_path}/timeline/main.yaml`
- `{current_path}/worldbuilding/setting.md`
- `{current_path}/worldbuilding/entries/*.yaml`（设定集条目）
- `{current_path}/ingestion_brief.md`（素材消化摘要，若存在）
- `{current_path}/plot/outline.md`
- `{current_path}/chapters/index.yaml`
- `{current_path}/compliance/inspiration_log.yaml`
- `{current_path}/compliance/risk_report.yaml`
- `{current_path}/quality/ai_trace_report.yaml`

### 2. 交叉检查

检查维度：

| 类别 | 检查项 |
|------|--------|
| 角色一致性 | 基本信息、关系、年龄与时间线 |
| 时间线一致性 | 顺序、位置、因果关系 |
| 设定一致性 | 世界规则、势力、地点 |
| 剧情一致性 | 章节匹配、伏笔遗漏 |
| 章节流一致性 | 章节状态推进、字数与目标、POV缺失 |
| 关系演进一致性 | 关系强度跳变、缺桥接事件、关系类型冲突 |
| 借鉴合规一致性 | 借鉴登记是否覆盖、风险章节是否有修复动作 |
| 文风质量一致性 | AI痕迹风险趋势、角色对白区分度 |

### 3. 生成报告

## 输出格式

```
🔍 一致性检查报告

---

## ✅ 通过项（{{count}}）
- {{通过项1}}
- {{通过项2}}

## ⚠️ 警告项（{{count}}）

### 角色：{{name}}
- {{问题描述}}
  {{详情}}
  建议：{{修复方法}}

## ❌ 错误项（{{count}}）

### 角色：{{name}}
- {{问题描述}}
  {{详情}}
  建议：{{修复方法}}

---

📊 统计：通过 {{pass}} / 警告 {{warn}} / 错误 {{error}}

🔧 修复优先级
   1. [高] {{修复建议}}
   2. [中] {{修复建议}}
   3. [低] {{修复建议}}

💡 修复命令：
   /character-edit {{name}} {{修改}}
   /timeline-add {{修正}}
   /chapter-update {{chapter_id}} --status {{status}}
   /relationship-log {{角色1}} {{角色2}} {{变化}} --chapter {{chapter}}
   /inspiration-log {{chapter_id}} {{material_id}} {{借鉴说明}}
   /anti-ai-rewrite {{chapter_id}} --level 2
```

## 注意事项

- 分级显示问题
- 给出具体修复建议
- 建议定期运行
- 对同一问题链路尽量给出“先修什么再修什么”