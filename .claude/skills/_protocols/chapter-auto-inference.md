# 章节自动推断协议

当章节类 skill 的 `$0`（chapter_id）未提供时，按以下顺序推断：

## 推断步骤

1. **当前文件推断**：检查用户当前打开/引用的文件是否匹配 `chapters/*.md`，若是则提取章节 ID
2. **最近 draft 推断**：从 `chapters/index.yaml` 中找 `status: draft` 且 `updated` 最近的章节
3. **兜底**：若仍无法确定，提示用户指定章节 ID

## 引用方式

在 skill 的「前置检查」中写：

```
按 [章节自动推断协议](_protocols/chapter-auto-inference.md) 确定目标章节。
```

## 引用此协议的 skill

- `chapter-review`
- `chapter-update`
- `anti-ai-check`
- `anti-ai-rewrite`
- `voice-check`
