---
name: relationship-add
description: 建立角色之间的关系，并记录关系机制与张力来源。用于用户想定义镜像、救赎、共生、守护等更有戏剧张力的关系时。
when_to_use: 用户想要定义两个角色之间的关系，尤其是需要更复杂的张力结构时
argument-hint: "[角色1] [角色2] [关系] [描述]"
arguments: char1 char2 relation description
---

# 任务

建立两个角色之间的关系，更新双方的角色卡片。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 检查两个角色是否都存在

## 输入参数

- `$0` (char1): 角色1姓名（必需）
- `$1` (char2): 角色2姓名（必需）
- `$2` (relation): 关系类型（师徒/师兄弟/仇敌/恋人/父子等）
- `$3+` (description): 关系描述（可选）

复杂关系可优先考虑这些机制：
- 救赎与被救赎
- 镜像与对立
- 共生与寄生
- 守护与诅咒

## 执行步骤

### 1. 验证角色存在

读取两个角色的档案文件（优先 `.yaml`，兼容 `.md`）。

如果不存在，提示：
`角色 $0 不存在，请先使用 /character-add 创建`

### 2. 更新双方角色档案中的关系字段

在 `{current_path}/characters/$0.yaml` 和 `$1.yaml` 的 `relations` 字段中追加：

**角色1的档案（$0.yaml）：**
```yaml
relations:
  - character: "$1"
    type: "$2"
    description: "$3"
    dynamic: ""
    tension_source: ""
```

**角色2的档案（$1.yaml）：**
```yaml
relations:
  - character: "$0"
    type: "$2"
    description: "$3"
    dynamic: ""
    tension_source: ""
```

如果关系明显带有“救赎 / 镜像 / 共生 / 守护”机制，优先在 `dynamic` 中写明；
在 `tension_source` 中写清楚这段关系靠什么产生持续张力，如权力不对等、误判、依赖、立场冲突。

### 3. 更新关系快照

在 `{current_path}/characters/relations.yaml` 追加或更新条目：

```yaml
relations:
  - pair: [$0, $1]
    type: "$2"
    dynamic: ""
    tension_source: ""
    strength: 1       # 初始强度，1-5
    last_updated: {{今天日期}}
```

### 4. 更新项目状态

更新 `project.updated`。

**成功标准**: 双方 `.yaml` 档案已更新，`relations.yaml` 已追加

## 输出格式

```
✅ 关系已建立

👤 $0 ←→ 👤 $1
🔗 关系：$2
📝 描述：$3

已更新：
   - characters/$0.yaml
   - characters/$1.yaml

查看关系图：/relationship-map
```

## 注意事项

- 关系是双向的，自动更新双方档案
- 方向性关系（如师徒）需在描述中说明主次
- 已存在的关系（同 pair）会更新而非重复添加
- `relations.yaml` 记录当前关系快照；详细演进用 /relationship-log 写入 `relation_events.yaml`
- 好关系不等于稳关系，优先写清关系机制和张力来源