# 写作风格生命周期协议（Style Lifecycle Protocol）

> 本协议定义风格模板的自动提炼触发时机和漂移检测机制。

## 目的

让风格模板从"用户得记得手动跑"变成"系统在合适时机主动发起"。

## 三个阶段

### 阶段一：积累期（0-2 章 draft）

- 不触发风格提炼
- `chapter-draft` 使用 `meta.yaml` 的 `style.prose` 和 `style.notes` 作为基础文风参考
- 无风格模板是正常的

### 阶段二：提炼触发（第 3+ 章到达 draft 时）

**触发条件**（全部满足）：

1. 当前项目 `style.template` 为空（尚未建立风格模板）
2. `chapters/index.yaml` 中状态为 `draft` 及以上的章节数 **≥ 3**
3. `state.yaml` 中 `style_prompt_declined` 不为 `true`（用户没有拒绝过）

**触发行为**（由 `chapter-update` 在推进到 draft 时执行）：

不仅仅在输出末尾加一行建议——**主动启动提炼流程**：

```
📝 你已完成 {N} 章草稿，从实际写作中提炼你的风格模板吗？

这会分析你写出来的内容，提炼真实的句式、节奏和修辞偏好。
后续改写（/anti-ai-rewrite）和生成初稿（/chapter-draft）会更贴近你的写法。

(Y 开始提炼 / N 跳过)
```

- 用户选 Y → 执行 `style-create --from-chapters` 的完整流程（分析 7 维度 → 展示报告 → 确认后保存）
- 用户选 N → 在 `state.yaml` 记录 `style_prompt_declined: true`，不再触发
- 保存成功后，更新 `meta.yaml` 的 `style.extracted_at_chapter` 为当前章节号

### 阶段三：漂移检测（持续）

**触发条件**（由 `pipeline-draft-polish` 检测）：

1. `meta.yaml` 的 `style.extracted_at_chapter` 非空（已有风格模板）
2. 当前打磨的章节号 - `extracted_at_chapter` ≥ 10

**触发行为**：

```
💡 你的风格模板是在 {extracted_at_chapter} 时提炼的，已过去 {N} 章。
   写作风格可能已经演化。要更新风格模板吗？
   
   Y → /style-create --from-chapters（用最近章节重新提炼）
   N → 跳过（下次再提醒）
   永不 → 关闭漂移检测
```

- 选 Y → 重新提炼，更新 `extracted_at_chapter`
- 选 N → 本次跳过，10 章后再提醒
- 选"永不" → `state.yaml` 记录 `style_drift_check_disabled: true`

## 引用此协议的 skill

- `chapter-update`（步骤 5c 风格提炼触发）
- `pipeline-draft-polish`（风格漂移检测步骤）
