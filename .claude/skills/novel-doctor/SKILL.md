---
name: novel-doctor
description: 诊断项目健康状态
when_to_use: 用户想检查项目结构和配置是否正常
---

# 任务

诊断项目健康状态，检查结构和配置。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 如果为空，运行全局诊断

## 全局诊断（无当前项目时）

### 1. 基础配置

- `.current.yaml` 与 `.projects.yaml` 是否可解析
- `.projects.yaml` 项目列表格式是否正确

### 2. 共享资源健康度

检查以下文件是否存在且格式有效：
- `../novel-material/data/index.yaml`（素材库独立项目）
- `../novel-material/data/tags.yaml`
- `shared/styles/templates.yaml`

### 3. 技能与模板完整性

- `.claude/skills/*/SKILL.md` 是否齐全
- `templates/project/` 下关键索引文件是否存在

## 诊断项目

### 1. 目录结构检查

检查必需目录是否存在：
- `.novel/`
- `characters/`
- `plot/`
- `timeline/`
- `worldbuilding/`
- `chapters/`
- `compliance/`
- `quality/`

### 2. 配置文件检查

检查配置文件格式：
- `.novel/state.yaml` - YAML格式有效
- `.novel/materials.yaml` - 格式正确
- `timeline/main.yaml` - 格式正确
- `chapters/index.yaml` - 格式正确
- `characters/relations.yaml` - 格式正确
- `characters/relation_events.yaml` - 格式正确
- `compliance/inspiration_log.yaml` - 格式正确
- `compliance/risk_report.yaml` - 格式正确
- `quality/ai_trace_report.yaml` - 格式正确

### 3. 数据完整性

- 角色卡片格式正确
- 时间线事件格式正确
- 章节索引条目格式正确
- 借鉴日志条目格式正确
- 无孤立文件

### 4. 索引一致性

- state.yaml 中的角色列表与实际文件匹配
- 时间范围与事件匹配
- chapters/index.yaml 与 chapters/*.md 匹配
- relation_events.yaml 与 relations.yaml 的角色对可追溯

## 输出格式

```
🏥 项目诊断报告

项目：{{name}}

---

## 目录结构

✅ .novel/ - 存在
✅ characters/ - 存在
✅ plot/ - 存在
⚠️ timeline/ - 存在但 events/ 目录为空
❌ worldbuilding/ - 缺失

## 配置文件

✅ state.yaml - 格式正确
✅ materials.yaml - 格式正确

## 数据完整性

✅ 角色卡片 - 5个文件，格式正确
⚠️ 张三.md - 缺少「背景故事」部分
✅ 时间线 - 20个事件，格式正确

## 索引一致性

✅ 角色索引 - 与实际文件匹配
✅ 时间范围 - 与事件匹配

---

📊 健康评分：{{score}}/100

🔧 建议修复：
   1. 创建 worldbuilding/ 目录
   2. 补充 张三.md 的背景故事
   3. 在 timeline/events/ 添加事件详情

💡 可根据建议手动修复，或让 AI 逐项代修复
```

## 注意事项

- 显示健康评分
- 给出具体修复建议