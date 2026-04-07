---
name: skill-doctor
description: 评估 skill 变更影响范围，检查跨 skill 一致性，自动同步文档。
when_to_use: 用户修改了某个 skill 想知道影响面，或想做 skill 体系的全面健康检查并自动更新文档
argument-hint: "[skill名称|sync|--full]"
arguments: target
---

# 任务

评估 skill 变更的影响范围，验证跨 skill 引用一致性，自动同步关联文档。

## 前置检查

1. 确认 `.claude/skills/` 目录存在
2. 确认 `docs/SPEC.md` 存在

## 输入参数

- `$0` (target): 操作目标，三种模式：
  - `<skill-name>`：对指定 skill 做变更影响分析（如 `consistency-check`）
  - `sync`：扫描所有 skill，自动同步文档
  - `--full`：完整健康检查 + 自动同步

使用示例：
- `/skill-doctor consistency-check` — 我改了 consistency-check，帮我看影响
- `/skill-doctor sync` — 同步所有文档
- `/skill-doctor --full` — 全面体检

---

## 模式一：变更影响分析（`$0` = skill 名称）

### 1. 读取目标 skill

读取 `.claude/skills/{target}/SKILL.md`，提取：
- 该 skill 引用的其他 skill（扫描 `/skill-name` 格式）
- 该 skill 引用的协议（扫描 `_protocols/*.md` 链接）
- 该 skill 读写的数据路径（扫描 `{current_path}/` 路径模式）
- 该 skill 的 frontmatter（name, description, arguments）

### 2. 扫描下游依赖

遍历所有 `.claude/skills/*/SKILL.md`，找出**引用了目标 skill**的 skill：
- 搜索 `/target-name` 斜杠命令引用
- 搜索 `target-name` 名称引用（在推荐命令、管道步骤中）

### 3. 扫描协议引用

检查 `_protocols/*.md` 中是否有引用目标 skill 的协议。

### 4. 分类影响等级

按以下规则判定：

| 变更类型 | 判定方式 | 影响等级 |
|---------|---------|---------|
| 内部逻辑（检查规则、措辞、提示词） | 输出格式和参数不变 | 🟢 低 — 下游行为不受影响 |
| 输出格式（报告结构、字段变化） | 下游 skill 解析其输出 | 🟡 中 — 需检查下游是否依赖旧格式 |
| 接口变更（参数、命令名、文件路径） | frontmatter 或路径改变 | 🔴 高 — 必须逐个更新下游引用 |
| 数据结构变更（yaml 字段增删） | 多 skill 共用同一数据文件 | 🔴 高 — 需全局搜索该字段 |

### 5. 输出影响报告

```
🔍 变更影响分析：{{skill-name}}

## 目标 skill 概要
- 描述：{{description}}
- 引用协议：{{protocols}}
- 读写路径：{{data_paths}}
- 上游依赖：{{upstream_skills}}

## 下游影响（谁依赖我）

| 下游 skill | 引用方式 | 影响等级 |
|-----------|---------|---------|
| {{skill}} | {{how}} | {{level}} |

共 {{count}} 个 skill 直接依赖。

## 共享数据路径（谁和我读写同一份文件）

| 数据文件 | 也在读写的 skill |
|---------|----------------|
| {{path}} | {{skills}} |

## 关联文档

需同步的文档：
- [ ] docs/SPEC.md — {{是否需要更新}}
- [ ] _protocols/{{name}}.md — {{引用列表是否需更新}}
- [ ] docs/USAGE-GUIDE.md — {{是否涉及使用示例}}

## 安全建议

{{根据影响等级给出具体操作建议}}
```

---

## 模式二：文档同步（`$0` = `sync`）

### 1. 扫描 skill 清单

遍历 `.claude/skills/*/SKILL.md`，从 frontmatter 提取每个 skill 的 `name`、`description`、`argument-hint`、`arguments`。

跳过 `_protocols/` 目录（协议不是 skill）。

### 2. 比对 SPEC.md

读取 `docs/SPEC.md`，与扫描结果比对：

- **新增 skill**：存在于文件系统但不在 SPEC.md 的 Skill清单中
- **已删除 skill**：在 SPEC.md 中但文件系统已无对应目录
- **信息过时**：description 或 arguments 与 SKILL.md 不一致

### 3. 比对协议引用

对每个 `_protocols/*.md`：
- 读取其「引用此协议的 skill」列表
- 扫描所有 skill 中实际引用该协议的 skill
- 找出漏登记或多登记的条目

### 4. 比对 ARCHITECTURE.md

检查：
- pipeline 数量描述是否与实际 `pipeline-*` skill 数量一致
- 领域列表是否覆盖所有 skill 分类

### 5. 执行同步

对每处不一致，向用户展示 diff 预览：

```
📋 文档同步预览

## SPEC.md 变更
+ 新增 skill：skill-doctor（项目管理 → Skill清单）
~ 更新描述：consistency-check（旧→新）

## _protocols/chapter-auto-inference.md 变更
+ 新增引用者：chapter-draft
- 移除引用者：voice-check（已不再引用）

## ARCHITECTURE.md 变更
~ 流程编排数量：8 → 9

确认执行同步？(Y/N)
```

用户确认后，逐个更新文件。

### 6. 输出同步报告

```
✅ 文档同步完成

📄 已更新文件：
   - docs/SPEC.md — {{n}} 处变更
   - _protocols/chapter-auto-inference.md — 引用列表更新
   - ARCHITECTURE.md — pipeline 数量更新

📊 当前 skill 体系：
   - 原子 skill：{{count}} 个
   - Pipeline 编排：{{count}} 个
   - 共享协议：{{count}} 个
```

---

## 模式三：完整健康检查（`$0` = `--full`）

先执行以下检查，再执行「模式二：文档同步」。

### 1. 孤立 skill 检查

找出没有任何其他 skill 引用、也不被任何 pipeline 编排的 skill。这些 skill 仍然有价值（用户直接调用），但如果数量过多，可能说明编排层覆盖不足。

### 2. 断裂引用检查

扫描所有 skill 中的 `/skill-name` 引用和 `_protocols/` 链接，检查目标是否实际存在。

### 3. 循环依赖检查

检测 skill 之间是否存在 A→B→C→A 的循环引用链。pipeline 之间的循环引用是设计风险。

### 4. 协议覆盖率

检查是否有"多个 skill 重复实现相同逻辑"但未抽取为 `_protocols/` 的情况：
- 扫描所有 skill 中相似的步骤描述
- 如果 3 个以上 skill 有高度相似的「前置检查」或「执行步骤」段落，建议提取为协议

### 5. 数据路径冲突

列出被 3 个以上 skill 同时读写的数据文件，标注潜在的并发写入风险。

### 6. 输出健康报告

```
🏥 Skill 体系健康报告

## 体系概览
- 原子 skill：{{count}} 个
- Pipeline 编排：{{count}} 个
- 共享协议：{{count}} 个
- 总引用关系：{{count}} 条

## 断裂引用
{{无 / 列出断裂引用}}

## 循环依赖
{{无 / 列出循环链}}

## 高扇入枢纽（改动需谨慎）
| Skill | 被引用次数 | 下游 skill |
|-------|-----------|-----------|
| {{skill}} | {{count}} | {{list}} |

## 孤立 skill（仅用户直接调用）
{{list}}

## 热点数据文件（≥3 个 skill 读写）
| 文件 | 读写 skill 数 |
|-----|-------------|
| {{path}} | {{count}} |

## 协议提取建议
{{无 / 列出可提取为协议的重复逻辑}}

---

📊 健康评分：{{score}}/100

🔧 建议：
  1. {{建议1}}
  2. {{建议2}}

📋 接下来执行文档同步...
```

然后自动进入模式二的文档同步流程。

---

## 注意事项

- 影响分析基于静态扫描（搜索文本引用），不执行 skill 本身
- 文档同步只修改文档文件（SPEC.md、协议、ARCHITECTURE.md），不修改 skill 本身
- 同步前始终展示 diff 预览，等待用户确认
- 新增 skill 时，SPEC.md 中的分类位置需根据 skill 名称前缀自动判断（`chapter-*` → 章节管理，`pipeline-*` → Pipeline 编排，等）
- 变更影响分析是建议性的，不会阻止用户修改
