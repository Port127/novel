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

## 输入参数

- `--quick`: 只做索引一致性检查（§4），跳过目录结构和配置格式检查。适用于其他 skill 嵌入调用或快速排障。

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

- character_index.yaml 与 characters/*.yaml 实际文件匹配
- worldbuilding.yaml 的 entries 列表与 entries/*.yaml 实际文件匹配
- 时间范围与事件匹配
- chapters/index.yaml 与 chapters/*.md 匹配
- relation_events.yaml 与 relations.yaml 的角色对可追溯

> 注：更细致的机械化索引检查参见 `/project-lint`。

### 5. 知识新鲜度

> 灵感来源：OpenAI 的 "doc-gardening" agent——定期扫描过时文档并发起修复。

检测项目中"陈旧"或"可能过时"的信息，防止旧知识误导写作。

**5a. 设定新鲜度**

| 检查 | 条件 | 级别 |
|------|------|------|
| 长期 tentative | 设定 status 为 `tentative` 且项目已有 3+ 章 draft | 警告：应尽快确认或删除 |
| 过期无后继 | `valid_until` 已触发但 `superseded_by` 为空 | 警告：过期设定无新版本 |
| 过期仍被引用 | 已过期/被取代的设定仍在近期章节中出现 | 错误：需要更新章节或创建后继设定 |

**5b. 角色新鲜度**

| 检查 | 条件 | 级别 |
|------|------|------|
| 长期未出场 | 角色在 character_index 中注册但最后出场章节距最新章节 > 10 章 | 提示：是否遗忘？ |
| current_state 过时 | 角色的 `current_state` 最后更新时对应章节 < 最新已写章节 - 3 | 警告：状态可能已不准确 |
| 五件套未填 | fatal_flaw / obsession / soft_spot / misbelief / contrast_habit 有空值 | 警告：角色缺少深度 |

**5c. 钩子新鲜度**

| 检查 | 条件 | 级别 |
|------|------|------|
| Major 逾期 | `planted` 状态的 major 钩子已过 `recovery_deadline` | 错误：读者很可能记得 |
| Minor 逾期 | `planted` 的 minor 钩子已过 deadline | 警告 |
| 无截止日 | major/minor 钩子无 `recovery_deadline` | 警告：应设截止 |
| 密度异常 | 最近 3 章的 planted 钩子数 > 全书平均 ×2 | 提示：近期伏笔过密 |

**5d. 大纲新鲜度**

| 检查 | 条件 | 级别 |
|------|------|------|
| 未写章节过多 | outline.md 中规划的章节数 - 已写章节数 > 20 | 提示：大纲可能需要更新 |
| 偏离未同步 | 已知偏离的章节（consistency-check 曾报告）的大纲节点仍未更新 | 警告 |

**5e. 文档新鲜度**

| 检查 | 条件 | 级别 |
|------|------|------|
| PROJECT_MAP.md 过时 | state.yaml 的 `project.updated` 晚于 PROJECT_MAP.md 的 git 修改时间（若可获取）或内容明显不一致 | 提示：建议 /project-reindex |
| 风格模板过旧 | `meta.yaml` 的 `style.extracted_at_chapter` 距最新章节 > 15 章 | 提示：风格可能已漂移 |

## 输出格式

```
🏥 项目诊断报告

项目：{{name}}

---

## 目录结构

✅ .novel/ - 存在
✅ characters/ - 存在
✅ plot/ - 存在
⚠️ timeline/ - 存在但事件为空
❌ worldbuilding/ - 缺失

## 配置文件

✅ state.yaml - 格式正确
✅ materials.yaml - 格式正确

## 数据完整性

✅ 角色卡片 - 5个文件，格式正确
⚠️ 张三.yaml - 缺少「背景故事」部分
✅ 时间线 - 20个事件，格式正确

## 索引一致性

✅ 角色索引 - 与实际文件匹配
✅ 时间范围 - 与事件匹配

## 知识新鲜度

⚠️ 设定 rule_001 长期 tentative（5 章 draft 未确认）
⚠️ 角色 庄怀瑾 current_state 过时（最后更新 ch002，当前 ch008）
❌ Major 钩子「秘密」已过截止 ch010
✅ 大纲新鲜度 - 正常
✅ 文档新鲜度 - 正常

---

📊 健康评分：{{score}}/100

🔧 建议修复：
   1. 创建 worldbuilding/ 目录
   2. 补充 张三.yaml 的背景故事
   3. 在 timeline/main.yaml 添加事件详情

💡 可根据建议手动修复，或让 AI 逐项代修复
```

## 注意事项

- 显示健康评分
- 给出具体修复建议