---
name: pipeline-compliance-gate
description: 在发布前串联借鉴登记、风险检查和范围报告，形成可追溯的合规闸口。用于用户准备发布章节或阶段性检查借鉴风险时，不想手动拆分 inspiration 流程。
when_to_use: 用户想在发布前完成借鉴留痕、风险检查与合规汇总
argument-hint: "[章节ID或范围]"
arguments: target
---

# 任务

把目标章节或范围推进到 `可发前闸口`。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/compliance/inspiration_log.yaml`
3. 读取 `{current_path}/compliance/risk_report.yaml`
4. 若目标是单章，读取 `{current_path}/chapters/$0.md`

## 输入参数

- `$0` (target): 章节 ID 或范围，如 `ch012`、`ch001-ch012`

## 执行步骤

### 1. 先检查登记是否完整

参照 `/inspiration-log`（登记字段要求），检查目标范围内是否已有借鉴登记。

若缺失：

- 列出缺失章节
- 提示用户补充素材 ID、借鉴维度与说明
- 在信息缺失前，不直接声称“合规完成”

### 2. 逐章风险检查

调用 `/inspiration-check`，检查目标范围内各章的表达相似、桥段相似、人物关系相似风险。

### 3. 生成范围报告

调用 `/inspiration-report`，汇总：

- 覆盖章节数
- 风险级别分布
- 高频风险模式
- 可立即执行的降风险动作

## 输出格式

```markdown
## CurrentState
- 阶段：可发前闸口
- 范围：{{target}}
- 已完成借鉴登记校验与风险汇总

## Risks
- {{risk_1}}
- {{risk_2}}

## NextTasks
1. 补齐未登记章节的来源与维度
2. 优先处理高风险表达或桥段
3. 在复检前不要直接发布高风险章节

## RecommendedCommands
- /inspiration-log {{chapter_id}} {{material_id}} {{note}}
- /inspiration-check {{chapter_id}}
- /inspiration-report {{target}}
```

## 注意事项

- 合规闸口依赖可追溯记录，缺登记就不能算通过
- 结果仅用于创作辅助，不替代法律意见
- 若范围过大，先按高风险章节排序再逐章处理
