---
name: style-create
description: 创建写作风格模板
when_to_use: 用户想要定义新的写作风格
argument-hint: "[名称] [特征描述]"
arguments: name features
---

# 任务

创建新的写作风格模板。

## 输入参数

- `$0` (name): 风格名称
- `$1+` (features): 风格特征描述

可选：
- `--from 素材名` 从素材提取
- `--sample "文本"` 从样本提取

## 执行步骤

### 1. 解析风格定义

从用户描述或素材中提取风格特征。

### 2. 生成风格模板

```yaml
- name: $0
  tags: [{{标签}}]
  features:
    sentence:
      - {{句式特点1}}
      - {{句式特点2}}
    rhetoric:
      - {{修辞特点}}
    dialogue:
      - {{对话特点}}
    rhythm:
      - {{节奏特点}}
  examples:
    - "{{示例1}}"
    - "{{示例2}}"
  use_cases:
    - {{适用场景1}}
```

### 3. 保存到风格库

追加写入 `shared/styles/templates.yaml`。

## 输出格式

```
✅ 风格模板已创建

🎨 名称：$0
🏷️ 标签：{{tags}}

## 特征摘要
- 句式：{{sentence_feature}}
- 对话：{{dialogue_feature}}
- 节奏：{{rhythm_feature}}

## 示例
> {{example}}

📁 已保存：shared/styles/templates.yaml

💡 应用风格：/rewrite --style $0 [内容]
```

## 注意事项

- 风格名称唯一
- 特征要具体可操作
- 提供示例