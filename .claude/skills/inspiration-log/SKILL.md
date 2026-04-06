---
name: inspiration-log
description: 记录章节借鉴来源与借鉴维度，形成可追溯借鉴台账
when_to_use: 用户在章节创作中借鉴了某素材，需要登记来源与借鉴点
argument-hint: "[章节ID] [素材ID] [借鉴点]"
arguments: chapter_id material_id note
---

# 任务

将借鉴信息写入项目合规日志。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 检查 `{current_path}/compliance/inspiration_log.yaml` 是否存在
3. 读取 `../novel-material/data/index.yaml` 校验素材ID（若存在）

## 输入参数

- `$0` (chapter_id): 章节ID
- `$1` (material_id): 素材ID，格式为 `nm_{type}_{YYYYMMDD}_{random4}`，如 `nm_novel_20260404_a1b2`
- `$2+` (note): 借鉴说明
- `--dimensions`: 借鉴维度，逗号分隔（设定/节奏/冲突/结构/人物）

## 执行步骤

### 1. 校验素材ID

检查素材ID格式：
- 必须以 `nm_` 开头
- 在 `../novel-material/data/index.yaml` 中验证存在

若素材库不可访问，提示用户确认素材ID有效性。

### 2. 规范化借鉴维度

将 `--dimensions` 解析为列表，缺省则默认 `[节奏]`。

### 3. 写入借鉴日志

在 `{current_path}/compliance/inspiration_log.yaml` 追加：

```yaml
entries:
  - chapter: ch003
    material_id: nm_novel_20260404_a1b2
    dimensions: [节奏, 结构]
    note: 借鉴冲突升级节奏，不复用具体表达
    date: 2026-04-04
```

## 输出格式

```
✅ 借鉴记录已登记

📖 章节：{{chapter}}
📚 素材：{{material_id}}
🏷️ 维度：{{dimensions}}
📝 说明：{{note}}
```

## 注意事项

- 只记录"借鉴了什么方法"，避免记录"照搬了什么表达"
- 建议每章写完后立即登记
- 素材ID需使用 novel-material 项目的规范格式