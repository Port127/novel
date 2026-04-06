---
name: inspiration-report
description: 汇总借鉴登记与风险结果，生成章节范围内的合规报告
when_to_use: 用户想查看某段创作周期内的借鉴分布与风险趋势
argument-hint: "[范围]"
arguments: range
---

# 任务

输出借鉴使用和风险趋势报告。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/compliance/inspiration_log.yaml`
3. 读取 `{current_path}/compliance/risk_report.yaml`
4. 读取 `../novel-material/data/index.yaml` 获取素材名称（若存在）

## 输入参数

- `$0` (range): 范围，如 `ch001-ch020` 或 `最近10章`

## 执行步骤

### 1. 汇总借鉴数据

统计维度：
- 每章借鉴次数
- 素材来源分布（素材ID格式：`nm_xxx`）
- 借鉴维度分布（设定/节奏/结构等）

### 2. 匹配素材名称

从 `../novel-material/data/index.yaml` 查询素材ID对应名称，用于报告展示。

若素材库不可访问，仅展示素材ID。

### 3. 汇总风险数据

统计维度：
- 高/中/低风险章节数
- 高频风险类型
- 风险变化趋势

### 4. 生成建议

给出"继续借鉴可保留项"和"需要控制的高风险模式"。

## 输出格式

```
📊 借鉴合规报告：$0

借鉴概览：
- 覆盖章节：{{chapter_count}}
- 借鉴总次数：{{borrow_count}}
- 主要来源：
  - {{material_name}} ({{material_id}}): {{count}}次

风险概览：
- 高风险：{{high}}
- 中风险：{{medium}}
- 低风险：{{low}}

建议：
1. ...
2. ...
```

## 注意事项

- 报告应可追溯到章节和素材ID
- 优先提示可立即执行的降风险动作
- 素材库路径：`../novel-material/data/`