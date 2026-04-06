---
name: chapter-board
description: 按状态展示章节看板，快速识别积压与风险章节
when_to_use: 用户想查看章节整体进度，或按状态筛选章节
argument-hint: "[--status 状态]"
---

# 任务

展示当前项目章节看板。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/chapters/index.yaml`

## 执行步骤

### 1. 读取章节索引

获取全部章节的 `id/title/status/pov/word_actual/word_target/updated`。

### 2. 分组统计

按状态分组统计：`idea`、`outline`、`draft`、`revise`、`final`、`published`。

### 3. 风险提示

标记以下风险项：
- 长期停留在 `draft` 的章节
- 实际字数显著低于目标字数
- 缺少 `pov` 的章节

## 输出格式

```
📚 章节看板

idea: {{n1}} | outline: {{n2}} | draft: {{n3}}
revise: {{n4}} | final: {{n5}} | published: {{n6}}

---

ch001  山村惊变    draft     张三    2780/3000
ch002  初入宗门    outline   李四    0/3200

⚠️ 风险章节：
- ch002 缺少 POV
- ch001 停留 draft 超过 7 天
```

## 注意事项

- 支持 `--status` 仅展示某一状态
- 默认按章节ID升序展示
