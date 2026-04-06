---
name: inspiration-check
description: 检查章节借鉴风险并输出降风险建议
when_to_use: 用户希望在发布前评估借鉴风险，避免表达或桥段过度重合
argument-hint: "[章节ID]"
arguments: chapter_id
---

# 任务

对单章进行借鉴风险检查并写入报告。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/compliance/inspiration_log.yaml`
3. 读取 `{current_path}/chapters/$0.md`
4. 读取 `../novel-material/data/index.yaml` 获取素材元数据（若存在）

## 执行步骤

### 1. 读取本章借鉴登记

筛选 `chapter=$0` 的借鉴条目，获取来源素材ID和维度。

素材ID格式：`nm_{type}_{YYYYMMDD}_{random4}`

### 2. 获取素材信息

从 `../novel-material/data/index.yaml` 查询素材名称、摘要等信息。

若素材库不可访问，使用登记时的备注信息进行评估。

### 3. 风险评估

按维度评估以下风险：
- 表达相似风险（句式/比喻/关键词组合）
- 桥段相似风险（事件顺序与冲突结构）
- 人物关系相似风险（角色互动模板）

### 4. 生成修复建议

针对中高风险项给出降重建议：
- 改冲突触发机制
- 改叙事顺序
- 改角色动机
- 改语言表达层

### 5. 写入报告

更新 `{current_path}/compliance/risk_report.yaml`：

```yaml
reports:
  - chapter: ch003
    overall_risk: medium
    risk_items:
      - type: expression_similarity
        level: high
        evidence: 关键句式连续重合
        suggestion: 替换比喻源域并重构句法
        material_id: nm_novel_20260404_a1b2
```

## 输出格式

```
🛡️ 借鉴风险检查：$0

总体风险：{{overall_risk}}

高风险项：
- {{item}}（来源：{{material_id}}）

建议优先修复：
1. {{fix1}}
2. {{fix2}}
```

## 注意事项

- 未登记借鉴来源时先提示补 `/inspiration-log`
- 结果用于创作辅助，不替代法律意见
- 素材库路径：`../novel-material/data/`