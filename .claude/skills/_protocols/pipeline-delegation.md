# Pipeline 委派协议

Pipeline skill 引用子 skill 时，使用以下两种标准措辞之一。

## 调用模式

Pipeline 要求 AI 完整执行子 skill 的流程并使用其产出。

**标准措辞：**

```
调用 `/skill-name`，将结果用于下一步。
```

适用场景：
- pipeline 让子 skill 执行完整流程并产出文件或报告（如 kickoff 中的 `/chapter-create`，note-triage 中的 `/setting-add`）
- pipeline 不需要理解子 skill 的内部逻辑，只需要其结果

## 参照模式

Pipeline 引用子 skill 的部分逻辑，但在自己的上下文中执行。

**标准措辞：**

```
参照 `/skill-name`（[具体部分]），[做什么]。
```

适用场景：
- pipeline 借用子 skill 的审查标准但自行判断（如 outline-polish 中参照 `/plot-review` 的审查维度）
- pipeline 只需要子 skill 的部分逻辑，不需要完整执行

**要求：** 必须注明参照的具体部分（如"审查维度""检查标准""输出格式"），不使用笼统引用。

## 禁止的模糊写法

以下措辞含义不明确，禁止在 pipeline 中使用：

- "按 /X 的标准"
- "按 /X 的口径"
- "按 /X 的方法"
- "按 /X 的维度"
- "按 /X 的契约"
- "结合 /X 的方法"
- "按 /X 的流程执行"

## 引用方式

在 pipeline skill 的步骤说明中直接使用上述标准措辞。

## 引用此协议的 skill

- `pipeline-outline-bootstrap`
- `pipeline-outline-polish`
- `pipeline-chapter-kickoff`
- `pipeline-draft-polish`
- `pipeline-setting-consolidate`
- `pipeline-note-triage`
- `pipeline-continuity-gate`
- `pipeline-compliance-gate`
