# 预检完整性协议（Preflight Integrity Check）

> 本协议适用于所有涉及章节读写的关键 skill，在前置检查阶段嵌入。

## 目的

在执行高影响操作前，快速验证目标章节及其依赖的引用链完整性。防止因手动删文件、git 操作或上次操作中断导致的孤儿引用级联问题。

## 适用 skill

- `pipeline-chapter-kickoff`（创建章节前）
- `chapter-draft`（生成初稿前）
- `chapter-update`（推进状态前）
- `pipeline-draft-polish`（打磨前）

## 检查范围

**仅检查当前操作涉及的章节及其近邻**，不做全量扫描。

### 1. 目标章节引用链

| 检查项 | 方法 | 分级 |
|--------|------|------|
| 章节文件存在性 | `chapters/{id}.md` 是否存在 | 🔴 阻断（kickoff 除外，kickoff 是创建动作） |
| 索引条目存在性 | `chapters/index.yaml` 中是否有 `id: {target}` | 🔴 阻断（kickoff 除外） |
| 文件↔索引一致 | 两者是否都存在或都不存在 | 🔴 阻断（部分存在 = 孤儿） |
| 版本文件完整 | 若 index 有 `versions`，检查每个 `file` 是否存在 | 🟡 警告 |
| 出场角色卡存在 | `characters_involved` 中的角色 → `characters/{name}.yaml` 存在 | 🟡 警告 |

### 2. 前序章节健康（仅 chapter-draft 和 pipeline-draft-polish 需要）

| 检查项 | 方法 | 分级 |
|--------|------|------|
| 前一章有 summary | 前一章状态 ≥ draft 时，`summary` 字段非空 | 🟡 警告 |
| 前一章角色状态 | `characters_involved` 对应的角色卡有 `current_state.as_of_chapter` | 🟡 警告 |

### 3. 近邻孤儿检测（当前章 ± 2 章范围）

| 检查项 | 方法 | 分级 |
|--------|------|------|
| 孤儿索引 | index.yaml 有条目但 `chapters/{id}.md` 不存在 | 🔴 阻断 |
| 孤儿文件 | `chapters/` 下有 `ch*.md` 但 index.yaml 无对应条目 | 🟡 警告 |

## 检测结果处理

### 🟢 全部通过

```
✅ 预检通过，继续执行
```

不输出任何内容，直接进入 skill 正常流程。

### 🟡 有警告

```
⚠️ 预检发现以下问题（不阻断当前操作）：
- ch004 缺少 summary（前一章未生成摘要）
  💡 写完本章后建议 /chapter-update ch004 --status draft 补生成
- characters/王妮.yaml 不存在（ch005 标记了该角色出场）
  💡 /character-add 王妮

继续执行当前操作...
```

输出警告后继续执行。

### 🔴 有阻断

```
🚫 预检发现完整性问题，操作已暂停：

  孤儿索引：index.yaml 中有 ch003 条目，但 chapters/ch003.md 不存在
  
  可能原因：文件被手动删除、git 操作导致

  建议操作：
  A. 清理孤儿索引条目后重试 → 我来帮你清理（需确认）
  B. 手动恢复文件 → git checkout chapters/ch003.md
  C. 运行完整诊断 → /novel-doctor
  D. 跳过预检强制执行（不推荐）

  选择？(A/B/C/D)
```

**选 A**：清理 index.yaml 中的孤儿条目，然后继续。
**选 D**：跳过预检，skill 按正常流程执行（用户自行承担风险）。

## 实现方式

在适用 skill 的「前置检查」步骤末尾加一行：

```markdown
N. 按 [预检完整性协议](_protocols/preflight-integrity.md) 检查目标章节引用链完整性
```

## 性能约束

- 只检查目标章节 ± 2 章的范围，不全量扫描
- 只读操作，不修改任何文件（除非用户选择 A 清理孤儿）
- 目标耗时 < 3 秒（约等于读 5-10 个文件的时间）

## 与 novel-doctor 的关系

- 预检协议：**窄范围、自动嵌入、快速**——每次关键操作前自动跑
- novel-doctor：**全量、手动触发、详尽**——定期或出问题时手动跑
- novel-doctor `--quick`：介于两者之间——只做索引一致性（§4），跳过目录和格式检查
