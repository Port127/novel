---
name: relationship-log
description: 记录角色关系变化事件并写入关系演进日志，强调变化原因、代价、误判与是否不可逆。用于某章节中关系发生关键变化，需要保留可追踪依据时。
when_to_use: 某章节中角色关系发生变化，需要记录变化原因、代价与影响
argument-hint: "[角色1] [角色2] [变化描述] --chapter [章节ID]"
arguments: char1 char2 change
---

# 任务

记录一条关系变化事件，并更新关系快照。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 检查角色是否在 `{current_path}/.novel/state.yaml` 中存在
3. 读取或创建 `characters/relation_events.yaml` 与 `characters/relations.yaml`

## 输入参数

- `$0` (char1): 角色1
- `$1` (char2): 角色2
- `$2+` (change): 变化描述
- `--chapter`: 章节ID
- `--type`: 关系类型（盟友/仇敌/暧昧/师徒等）
- `--strength`: 强度，建议 `-5` 到 `+5`

## 执行步骤

### 1. 写入事件日志

优先记录以下信息：
- 为什么变化
- 变化付出了什么代价
- 是否存在误判、错过或信息差
- 这次变化是否已经不可逆

在 `relation_events.yaml` 追加：

```yaml
events:
  - id: rel_evt_001
    chapter: ch001
    pair: [张三, 李四]
    type: 师兄弟
    strength: 3
    change: 共同对敌后关系升温
    cause: 共同对敌
    cost: 李四负伤
    misbelief: 张三仍误以为李四只是权宜合作
    irreversible: false
    date: 2026-04-01
```

### 2. 更新关系快照

同步更新 `relations.yaml` 中该角色对的当前状态。

若本次变化暴露出新的张力来源，也同步更新快照中的关系描述。

## 输出格式

```
✅ 关系变化已记录

👥 角色对：$0 ↔ $1
📖 章节：{{chapter}}
🔁 变化：{{change}}
💪 强度：{{strength}}
⚠️ 代价：{{cost}}
```

## 注意事项

- 关系变化应有剧情依据
- 同章节内重复变更时应合并说明
- 优先记录能改变后续选择的变化，不只记录情绪波动
- 若关系变化建立在误判、等待落空或身份错位上，要明确写出
