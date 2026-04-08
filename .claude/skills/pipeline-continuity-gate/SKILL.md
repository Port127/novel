---
name: pipeline-continuity-gate
description: 汇总关系、时间线和跨模块一致性检查结果，生成按优先级排序的连续性修复清单。用于用户准备阶段性收束、发文前排雷，或怀疑设定与剧情出现断裂时。
when_to_use: 用户想做阶段性一致性闸口，得到一份可以直接执行的修复清单
argument-hint: "[检查范围]"
arguments: range
---

# 任务

把连续性风险收束成 `可执行修复清单`。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/timeline/main.yaml`
3. 读取 `{current_path}/plot/outline.md`
4. 读取 `{current_path}/chapters/index.yaml`
5. 若存在，读取关系与世界观相关文件

## 输入参数

- `$0` (range): 可选检查范围，如 `ch001-ch020`、`最近10章`

## 执行步骤

### 1. 关系演进检查

调用 `/relationship-check`，将结果中的关系跳变、缺桥接事件、关系类型冲突纳入修复清单。

### 2. 时间线检查

调用 `/timeline-check`，将结果中的时间顺序冲突、角色位置冲突、年龄/因果关系问题纳入修复清单。

### 3. 设定依赖检查

参照 `/worldbuilding-review`（设定依赖与生命周期审查部分），识别：

- `confirmed` 设定是否引用了已 `deprecated` 的设定
- `setting_links` 中引用的目标是否存在
- 大量 `tentative` 堆积未提升——提示用户先做 `/pipeline-setting-consolidate`
- 孤立设定（无剧情/角色/设定关联）

### 4. 跨模块一致性检查

参照 `/consistency-check`（交叉检查维度），识别：

- 世界规则与剧情矛盾
- 章节状态与目标脱节
- 风险章节是否缺修复动作

### 5. 汇总成修复清单

按优先级输出：

- 先修会导致剧情硬伤的问题
- 再修会造成理解负担的问题
- 最后修体验型问题

## 输出格式

```markdown
## CurrentState
- 阶段：可执行修复清单
- 范围：{{range}}
- 已完成关系、时间线、设定依赖与总一致性检查

## Risks
- {{risk_1}}
- {{risk_2}}
- {{risk_3}}

## NextTasks
1. 先修硬冲突：时间线/地点/因果错误
2. 再补桥接事件：关系变化与关键转折
3. 最后回填章节元数据或设定缺口

## RecommendedCommands
- /relationship-log {{role1}} {{role2}} {{change}} --chapter {{chapter}}
- /timeline-add {{time}} {{event}}
- /setting-edit {{name}} --status confirmed
- /chapter-update {{chapter_id}} --status revise
- /pipeline-setting-consolidate
```

## 注意事项

- 这是“闸口型”流程，默认不直接批量改正文
- 同一问题链尽量指出先后修复顺序
- 若某一类问题明显过多，优先建议用户聚焦一个子域修完再回总检
