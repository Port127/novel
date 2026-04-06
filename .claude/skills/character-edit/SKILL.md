---
name: character-edit
description: 编辑已有角色的信息，支持补充缺陷、执念、软肋、误判和反差特征，让角色更有可写性和人物弧光。
when_to_use: 用户想要修改或补充角色信息，尤其是把角色从“设定标签”补成“会出选择的人”
argument-hint: "[姓名] [修改内容]"
arguments: name changes
---

# 任务

编辑已有角色的信息。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 优先检查 `{current_path}/characters/$0.yaml` 是否存在，其次检查 `.md`
3. 不存在则提示：`角色 $0 不存在，使用 /character-add 创建`

## 输入参数

- `$0` (name): 角色姓名（必需）
- `$1+` (changes): 修改内容描述

支持的修改格式：
- `/character-edit 张三 年龄改为26岁`
- `/character-edit 张三 性格：表面温和，内心阴险`
- `/character-edit 张三 添加背景：曾是散修`
- `/character-edit 张三 致命缺陷：总以为自己能一个人扛过去`
- `/character-edit 张三 执念：一定要找回失踪的师父`

## 执行步骤

### 1. 读取角色档案

优先读取 `{current_path}/characters/$0.yaml`，兼容旧版 `.md`。

### 2. 解析修改意图

根据用户描述识别修改字段（`.yaml` 格式优先）：

| 关键词 | YAML 字段 |
|--------|-----------|
| 年龄/age | `profile.age` |
| 性格/特质 | `traits` |
| 外貌 | `appearance` |
| 背景/经历 | `backstory` |
| 能力/技能 | `abilities` |
| 别名/称号 | `aliases` |
| 原型 | `archetype` |
| 叙事功能 | `narrative_function` |
| 道德光谱 | `moral_spectrum` |
| 缺陷/致命缺陷 | `fatal_flaw` |
| 执念/目标执念 | `obsession` |
| 软肋/最在意 | `soft_spot` |
| 误判/错误信念 | `misbelief` |
| 反差习惯 | `contrast_habit` |
| 悲剧触发器 | `tragedy_trigger` |
| 首次登场 | `first_appearance` |
| 弧光/arc | `arc`（追加新阶段） |
| 备注 | `notes` |

### 3. 更新角色档案

修改 `.yaml` 文件中对应字段；若目标字段不存在，则补创建该字段。

同步更新 `character_index.yaml` 中的摘要信息。

### 4. 更新项目状态

更新 `{current_path}/.novel/state.yaml` 的 `project.updated`。

**成功标准**: 角色 `.yaml` 已更新，`character_index.yaml` 同步

## 输出格式

```
✅ 角色已更新

👤 $0
📝 修改内容：
   - {{字段}}：{{旧值}} → {{新值}}

📄 文件：characters/$0.yaml
```

## 注意事项

- 支持模糊匹配角色名
- `.yaml` 为主格式；如项目中只有 `.md` 文件，可先迁移或直接编辑 `.md`
- 复杂修改（如大段弧光补充）可引导用户直接编辑文件
- 修改弧光时追加新阶段，不覆盖已有阶段
- 优先补会影响决策和关系的字段，如缺陷、误判、软肋与执念