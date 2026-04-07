---
name: novel-edit
description: 编辑项目基础信息（书名、类型、视角、目标字数等），自动级联更新所有关联文件。
when_to_use: 用户想要修改书名、类型、写作视角、目标字数等项目级元信息
argument-hint: "[字段] [新值]"
arguments: field value
---

# 任务

编辑当前项目的基础元信息，并级联更新所有引用该信息的文件。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path` 和 `current_project`
2. 读取 `{current_path}/.novel/meta.yaml`
3. 读取 `{current_path}/.novel/state.yaml`

## 输入参数

- `$0` (field): 要修改的字段
- `$1+` (value): 新值

支持的修改格式：
- `/novel-edit 书名 新书名`
- `/novel-edit 类型 玄幻`
- `/novel-edit 视角 第三人称限制`
- `/novel-edit 目标字数 500000`
- `/novel-edit 更新频率 每日一章`
- `/novel-edit 风格模板 冷叙述`
- `/novel-edit 状态 revising`

## 字段映射

| 用户关键词 | meta.yaml 字段 | state.yaml 字段 |
|-----------|---------------|-----------------|
| 书名/名称 | `name` | `project.name` |
| 类型/流派 | `genre` | `project.genre` |
| 子类型 | `sub_genre` | — |
| 作者 | `author` | — |
| 视角/POV | `writing.pov` | — |
| 目标字数 | `writing.target_word_count` | — |
| 更新频率 | `writing.update_frequency` | — |
| 风格模板 | `style.template` | — |
| 文笔风格 | `style.prose` | — |
| 状态 | `status` | — |

## 执行步骤

### 1. 解析修改意图

识别用户要修改的字段和目标值。

### 2. 影响分析（书名变更时必须执行）

如果修改的是**书名**，这是高影响操作，需要：

a) 列出所有受影响文件：
   - `{current_path}/.novel/meta.yaml` → `name`
   - `{current_path}/.novel/state.yaml` → `project.name`
   - `.projects.yaml` → 对应项目条目的 `name`
   - `.current.yaml` → `current_project`（若是当前项目）
   - 项目文件夹名称 `projects/{旧名}` → `projects/{新名}`

b) 向用户展示影响范围，等待确认：

```
⚠️ 书名变更影响分析

旧名：{{旧名}}
新名：{{新名}}

将修改以下文件：
  1. .novel/meta.yaml → name
  2. .novel/state.yaml → project.name
  3. .projects.yaml → 项目条目
  4. .current.yaml → current_project
  5. 文件夹重命名：projects/{{旧名}} → projects/{{新名}}

确认执行？(Y/N)
```

c) **用户确认后**才执行变更。

### 3. 执行变更

更新 `{current_path}/.novel/meta.yaml` 中的目标字段。

如果涉及 `state.yaml` 中的镜像字段（如 name、genre），同步更新。

刷新 `meta.yaml` 的 `updated` 和 `state.yaml` 的 `project.updated` 为今天日期。

### 4. 级联更新（书名变更时）

按影响分析的清单逐一更新：
- 重命名项目文件夹
- 更新 `.projects.yaml` 中的项目条目
- 更新 `.current.yaml`

### 5. 验证

重新读取修改后的文件，确认值已正确更新。

## 输出格式

```
✅ 项目信息已更新

📚 {{字段}}：{{旧值}} → {{新值}}

📄 已更新文件：
   - .novel/meta.yaml
   - .novel/state.yaml
   {{如有级联：}}
   - .projects.yaml
   - .current.yaml
```

**书名变更时额外输出：**

```
📁 项目路径：projects/{{旧名}} → projects/{{新名}}

⚠️ 请注意：如有外部引用旧路径，需手动更新。
```

## 注意事项

- 书名变更是高影响操作，必须用户确认
- 类型/视角等变更影响较小，可直接执行
- `status` 只允许 `drafting` / `revising` / `completed` / `suspended`
- 所有变更都会刷新 `updated` 时间戳
