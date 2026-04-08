---
name: novel-switch
description: 切换当前工作的小说项目
when_to_use: 用户想要切换到另一本小说继续写作
argument-hint: "[项目名]"
arguments: name
---

# 任务

切换当前工作的小说项目。

## 前置检查

1. 读取 `.projects.yaml` 获取项目列表
2. 如果 `$0` 未提供，显示项目列表让用户选择

## 输入参数

- `$0` (name): 项目名称（必需，或在交互中选择）

## 执行步骤

### 1. 检查项目是否存在

读取 `.projects.yaml`，查找 `name: $0` 的项目。

如果不存在：
- 列出所有可用项目
- 询问用户选择或创建新项目

### 2. 更新当前项目

写入 `.current.yaml`：

```yaml
current_project: $0
current_path: projects/$0
last_updated: {{今天日期}}
```

**成功标准**: `.current.yaml` 更新完成

### 3. 同步 Cursor Rules

检查 `projects/$0/.novel/rules/` 目录是否存在。

如果存在，将项目专属规则同步到 `.cursor/rules/`：

1. 读取 `projects/$0/.novel/rules/context.md`
2. 写入 `.cursor/rules/novel-project-context.mdc`，包裹 YAML 前置：
   ```
   ---
   description: 当前小说项目的上下文信息，帮助 AI 快速进入状态
   alwaysApply: true
   ---
   
   {{context.md 内容}}
   ```

3. 读取 `projects/$0/.novel/rules/constraints.md`
4. 写入 `.cursor/rules/novel-core-constraints.mdc`，包裹 YAML 前置：
   ```
   ---
   description: 已确认的核心世界观约束，任何创作、大纲修改、章节写作都不得违反
   alwaysApply: true
   ---
   
   {{constraints.md 内容}}
   ```

如果不存在：
- 提示用户该项目尚未配置专属规则
- 建议运行 `/project-reindex` 生成

**成功标准**: `.cursor/rules/` 中的项目专属规则已更新为目标项目的内容

### 4. 显示项目状态

读取 `projects/$0/.novel/state.yaml`，显示简要状态。

## 输出格式

```
✅ 已切换到项目《$0》

📊 项目状态：
   类型：{{genre}}
   角色：{{characters_count}}个
   章节：已规划{{chapters}}章
   当前焦点：{{current_focus}}

🔄 Cursor Rules 已同步（context + constraints）

继续工作：
   /character-add ...   添加角色
   /plot-add ...        添加情节
   /novel-status        查看详情
```

## 注意事项

- 切换前可提示保存当前工作
- 如果只有一个项目，无需切换
- 支持模糊匹配项目名
- `.cursor/rules/novel-workflow.mdc` 是通用规则，切换项目不改动
- 项目专属规则的源文件在 `projects/$0/.novel/rules/`，修改后需重新切换或运行 `/project-reindex` 同步