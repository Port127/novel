---
name: chapter-create
description: 创建新章节并初始化章节元数据
when_to_use: 用户要开始写新章节，或需要为章节建立写作目标和状态
argument-hint: "[章节ID] [一句话目标]"
arguments: chapter_id goal
---

# 任务

创建章节文件并登记到章节索引。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 如果为空，提示用户先执行 `/novel-init` 或 `/novel-switch`
3. 检查 `$0` 是否提供（如 `ch001`）

## 输入参数

- `$0` (chapter_id): 章节ID，建议格式 `ch001`
- `$1+` (goal): 一句话章节目标

## 执行步骤

### 1. 初始化章节索引

检查 `{current_path}/chapters/index.yaml` 是否存在，不存在则创建。

### 2. 创建章节正文文件

写入 `{current_path}/chapters/$0.md`：

```markdown
# 第{{序号}}章 {{可选标题}}

> 状态：idea
> 视角：待定
> 目标：$1
> 目标字数：3000
> 实际字数：0
> 更新时间：{{今天日期}}

---

## 场景大纲

<!-- 待补充 -->

## 正文草稿

<!-- 从这里开始写正文 -->

## 伏笔

<!-- 埋设与回收记录 -->
```

### 3. 更新章节索引

在 `{current_path}/chapters/index.yaml` 增加条目：

```yaml
chapters:
  - id: $0
    title: ""
    status: idea
    pov: ""
    goal: $1
    word_target: 3000
    word_actual: 0
    hooks_planted: []
    hooks_revealed: []
    updated: {{今天日期}}
```

## 输出格式

```
✅ 章节创建完成

🧩 章节ID：$0
🎯 章节目标：$1
📄 文件：chapters/$0.md

下一步：
   /chapter-update $0 --status outline
   /chapter-review $0
```

## 注意事项

- 若章节ID已存在，先询问是否覆盖
- 章节状态默认 `idea`
- 章节字数可在后续更新
