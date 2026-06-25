---
name: export-novel
description: 此技能仅在用户明确调用"/export-novel"或直接提及技能名称时使用。
---

# 导出小说

导出小说为各种格式。

## 工作流程

### 1. 选择格式

TXT / Markdown / EPUB（需 pandoc）

### 2. 选择范围

全部章节 / 已完成章节 / 指定范围

### 3. 包含设定

是否包含世界观/人物/大纲简介。

### 4. 执行导出

```bash
novel export {project_id} --format {format}
```

### 5. 展示结果

文件路径、格式、章节数、总字数。

## 参考

- 注意：默认不导出 draft 状态章节；EPUB 需要 pandoc（`brew install pandoc`）