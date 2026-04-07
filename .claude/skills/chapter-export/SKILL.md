---
name: chapter-export
description: 将章节导出为连续文档，支持范围选择和格式配置，用于预览、投稿或发布
when_to_use: 用户想将写好的章节合并为一个完整文档，用于预览全文、投稿平台或分享
argument-hint: "[范围] [--format md|txt] [--clean]"
arguments: range
---

# 任务

将指定范围的章节合并导出为连续文档。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/chapters/index.yaml`
3. 确认目标范围内的章节存在且有正文内容

## 输入参数

- `$0` (range): 导出范围，如 `ch001-ch010`、`全部`、`已发布`
- `--format`: 输出格式，默认 `md`
  - `md`：Markdown 格式，保留章节标题
  - `txt`：纯文本，适合投稿平台
- `--clean`: 清洁模式——去除元数据头、写作备忘、TODO 标记、HTML 注释
- `--status`: 只导出特定状态的章节，如 `--status final,published`
- `--output`: 输出文件路径，默认 `{current_path}/export/{{project_name}}_{{range}}.{{format}}`

## 执行步骤

### 1. 确定导出章节

根据范围和状态筛选章节列表：

- `ch001-ch010`：按 ID 范围
- `全部` / `all`：所有有正文的章节
- `已发布` / `published`：只导出 `status: published` 的章节
- `--status final,published`：导出 `final` 或 `published` 状态

### 2. 检查导出就绪度

对每个目标章节检查：

- 正文部分是否为空（跳过空章节并警告）
- 是否有未填充的 `<!-- TODO -->` 标记（警告但不阻塞）

### 3. 提取正文

从每个 `chapters/$id.md` 中提取正文内容：

- 跳过元数据头（`> 状态：...` 等行）
- 跳过「场景大纲」部分
- 跳过「伏笔」部分
- 跳过「写作备忘」部分
- 保留「正文草稿」部分的实际内容

若 `--clean` 模式：
- 额外去除所有 HTML 注释 `<!-- ... -->`
- 去除所有 `TODO` 标记
- 去除空的章节模板占位符

### 4. 合并输出

按章节顺序拼接，章节之间插入分隔：

**md 格式：**
```markdown
# 第1章 {{title}}

{{正文}}

---

# 第2章 {{title}}

{{正文}}
```

**txt 格式：**
```
第1章 {{title}}

{{正文}}


========================================


第2章 {{title}}

{{正文}}
```

### 5. 写入文件

确保 `{current_path}/export/` 目录存在。

写入目标文件。

### 6. 统计信息

计算导出内容的总字数、章节数。

## 输出格式

```
✅ 导出完成

📄 文件：export/{{filename}}
📊 统计：
   章节数：{{chapter_count}}
   总字数：{{word_count}}
   格式：{{format}}

⚠️ 注意事项：
{{#if empty_chapters}}
- 跳过了空章节：{{empty_chapters}}
{{/if}}
{{#if todo_chapters}}
- 以下章节含 TODO 标记：{{todo_chapters}}
{{/if}}
```

## 注意事项

- 导出不修改原始章节文件
- 空章节自动跳过，不中断导出
- `--clean` 模式适合投稿和分享，会去掉所有内部标记
- 大范围导出时建议先用 `--status final,published` 筛选，避免导出半成品
- 导出文件放在 `export/` 目录下，该目录建议加入 `.gitignore`
