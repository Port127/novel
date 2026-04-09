# 操作日志协议（Operation Journal Protocol）

> 本协议适用于所有涉及 ≥ 2 个文件写入的 skill。

## 目的

记录多文件写入操作的开始和结束，使系统能检测上次操作中断导致的半写状态。

## 日志文件

`{current_path}/.novel/ops_log.yaml`

```yaml
ops:
  - op_id: "op_20260409_143022"
    skill: "pipeline-chapter-kickoff"
    target: "ch001"
    files_to_write:
      - chapters/ch001.md
      - chapters/index.yaml
    started_at: "2026-04-09T14:30:22"
    status: completed          # in_progress | completed | failed
    completed_at: "2026-04-09T14:30:45"
```

## 操作流程

### 写入前

在开始写入第一个文件**之前**，追加一条日志：

```yaml
- op_id: "op_{YYYYMMDD}_{HHmmss}"
  skill: "{当前 skill 名}"
  target: "{操作目标，如章节 ID}"
  files_to_write: ["{将要写的文件列表}"]
  started_at: "{ISO timestamp}"
  status: in_progress
```

### 写入后

所有文件写入完成后，更新该条日志：

```yaml
  status: completed
  completed_at: "{ISO timestamp}"
```

### 写入失败

任何文件写入失败时：

```yaml
  status: failed
  completed_at: "{ISO timestamp}"
  error: "{简要错误描述}"
```

## 启动检测

适用 skill 在前置检查阶段，读取 `ops_log.yaml`，检查是否有 `status: in_progress` 的条目：

- 有 → 输出警告：

```
⚠️ 检测到上次未完成的操作：
   {skill} → {target}（开始于 {started_at}）
   以下文件可能处于半写状态：
   {files_to_write}

   建议：
   A. 运行 /novel-doctor --quick 检查完整性
   B. 忽略并继续（我来标记为 failed）

   选择？(A/B)
```

- 无 → 继续执行

## 清理策略

- `completed` 状态的条目保留最近 20 条，超出的自动删除
- `failed` 状态的条目保留直到用户处理
- `in_progress` 状态的条目永远保留（表示异常）

## 适用 skill

以下 skill 涉及 ≥ 2 个文件写入，应遵循本协议：

- `pipeline-chapter-kickoff`（chapters/{id}.md + index.yaml + 可选 outline.md）
- `chapter-update`（index.yaml + 角色卡 current_state + state.yaml）
- `chapter-draft`（chapters/{id}.md + index.yaml）
- `character-edit --rename`（多文件重命名）
- `pipeline-outline-bootstrap`（outline.md + outline.yaml + setting 文件 + state.yaml）
- `project-reindex`（大量文件写入）

单文件写入的 skill（如 `setting-add` 只写一个 entry + 索引）可以跳过。

## 实现方式

在适用 skill 中加入：

```markdown
按 [操作日志协议](_protocols/operation-journal.md)，在多文件写入前后记录 ops_log。
```
