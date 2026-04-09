# 编辑后影响扫描协议（Post-Edit Impact Scan）

> 适用于 `setting-edit`、`character-edit`、`setting-add`（--status confirmed 时）等会修改已有设定或角色的 skill。

## 触发条件

以下任一操作完成后，自动执行影响扫描：

| 操作 | 条件 |
|---|---|
| `setting-edit` | 修改了 `description`、`rules`、`constraints` 等核心内容字段 |
| `character-edit` | 修改了 `traits`、`abilities`、`fatal_flaw`、`obsession`、`speech_pattern`、`backstory` 等影响行为的字段 |
| `setting-add --status confirmed` | 新增一条 confirmed 设定 |

纯元数据修改（`updated` 日期、`status` 流转、`source`、`open_questions`）不触发扫描。

## 扫描范围

**只扫描与本次变更直接相关的文件，不做全量一致性检查。**

### 设定修改后

1. 从修改的设定条目中读取 `plot_links` 和 `character_links`
2. 扫描 `chapters/index.yaml`，找出涉及关联角色或关联剧情节点的已写章节（status 为 `draft` / `revise` / `done`）
3. 对命中的章节，读取其正文/摘要，检查是否存在与**修改后设定**矛盾的描述

### 角色修改后

1. 在已写章节中搜索该角色名（含 `aliases`）
2. 对命中的章节，检查：
   - 修改了 `abilities` → 正文中是否有该角色使用了已删除/已修改能力的描写
   - 修改了 `traits` / `fatal_flaw` → 正文中该角色行为是否与新设定明显矛盾
   - 修改了 `speech_pattern` → 正文对白是否与新语言画像冲突
   - 修改了 `backstory` → 正文中是否有与新背景矛盾的信息

## 输出格式

### 未发现冲突

```
✅ 影响扫描完成：未发现与已写内容的冲突

扫描范围：{{N}} 个已写章节（{{章节列表}}）
```

### 发现潜在冲突

```
⚠️ 影响扫描：发现 {{N}} 处潜在冲突

本次修改：{{字段}}：{{旧值}} → {{新值}}

### 冲突 1
📖 章节：{{chapter_id}}，第 {{N}} 段
📝 原文：「{{引用冲突段落}}」
❗ 问题：{{冲突描述}}
💡 建议：{{修复方向}}

### 冲突 2
...

---

🔧 修复命令：
   直接编辑 chapters/{{chapter_id}}.md    手动修正
   /rewrite {{chapter_id}} --focus {{段落}}  定向改写
   /consistency-check                      全面检查
```

## 行为约束

- **只报告，不修改。** 扫描结果是提醒，不自动改任何章节。
- **宁可多报，不要漏报。** 判断不确定时归入"潜在冲突"。
- **尊重草稿优先。** 冲突方向默认是"章节可能需要更新"，但用户可能选择"撤回本次设定修改"。两个方向都要在建议中提及。
- **效率优先。** 如果已写章节超过 20 章，只扫描最近 10 章 + `plot_links` / `character_links` 直接关联的章节，避免扫描时间过长。超出范围的章节在输出末尾提示"更早的章节未扫描，如需全量检查请运行 `/consistency-check`"。
