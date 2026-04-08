---
name: relationship-check
description: 检查角色关系演进是否存在跳变、逻辑断裂，以及事件日志是否缺少原因、代价或误判依据。用于用户担心人物关系不连贯，或定稿前做关系一致性检查。
when_to_use: 用户担心人物关系发展不连贯，或在定稿前做一致性检查
---

# 任务

检查关系数据中的逻辑问题并给出修复建议。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/characters/relations.yaml` 与 `{current_path}/characters/relation_events.yaml`
3. 读取 `{current_path}/timeline/main.yaml`（用于辅助时序判定）
4. 若存在，抽样读取涉及角色对的 `{current_path}/characters/*.yaml`，对照 `fatal_flaw`、`obsession`、`soft_spot`、`misbelief` 是否与关系变化相容

## 执行步骤

### 1. 检查项

**关系检查要有情感直觉，不只是数据比对：**
- +4 到 -4 不一定是"跳变"——如果中间有一次足够重的背叛，这反而真实
- 问自己：这两个人的关系变化，能从日常生活中找到映射吗？找不到就可能写得不够真
- 关系的戏剧性不在于变化幅度，在于变化的不可逆感——"回不去了"比"翻脸了"更有重量

- 强度跳变过大（如 `+4 -> -4` 且无关键事件）
- 关系类型冲突（同一时点既“生死仇敌”又“亲密盟友”）
- 缺失桥接事件（长期稳定后突然逆转）
- 单向关系不一致（A 视角与 B 视角严重冲突）
- 事件日志单薄：重大变化缺少 `cause` 或 `cost`（若项目已使用这些字段）
- 误判链断裂：事件写了 `misbelief`，但后续章节未安排澄清或代价兑现
- 标记为 `irreversible: true` 的变化，是否在前后文中有一致铺垫
- 快照缺少张力依据：`relations.yaml` 中重要关系对若已有 `dynamic` / `tension_source` 字段，检查是否与 `relation_events` 演进一致

### 2. 生成修复建议

给出“补事件/补对白/补动机”三类建议；若缺日志字段，可建议用 `/relationship-log` 补记 `cause`、`cost`、`misbelief`。

## 输出格式

```
🔍 关系一致性检查

✅ 通过项：{{pass}}
⚠️ 警告项：{{warn}}
❌ 错误项：{{error}}

[高] 张三-李四：ch010 关系突变缺少桥接事件
建议：在 ch009 增加误会导火索或利益冲突片段
```

## 注意事项

- 优先报告影响主线剧情的关系问题
- 建议需对应到章节位置
