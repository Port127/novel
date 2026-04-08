---
name: pipeline-setting-consolidate
description: 审查、补强并确认世界观设定集，清理 tentative 堆积和依赖问题，产出可支撑写作的稳定设定基础。用于 outline-bootstrap 之后、正式开写之前的设定整固。
when_to_use: 用户在大纲建立后想整固设定、清理 tentative 堆积，或在写到中期发现设定支撑不足时
argument-hint: "[整固重点]"
arguments: focus
---

# 任务

把散落的 tentative 设定收束为 `可支撑写作的稳定设定集`。

核心原则：**确认的设定要少而准，不追求数量。每条 confirmed 设定都必须能回答"它约束了什么、支撑了什么"。**

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/worldbuilding/worldbuilding.yaml`
3. 读取 `{current_path}/worldbuilding/setting.md`
4. 读取 `{current_path}/worldbuilding/entries/*.yaml`（所有条目）
5. 读取 `{current_path}/plot/outline.md`（用于检查设定与剧情咬合）
6. 若存在，读取 `{current_path}/ingestion_brief.md`（对照规则缺口）
7. 若存在，读取 `{current_path}/.novel/state.yaml`（获取当前计数）

## 输入参数

- `$0+` (focus): 可选整固重点，如"力量体系""势力关系""地理设定"

## 执行步骤

---

### 阶段一：设定盘点

**目标：** 搞清楚当前有什么、缺什么、什么该确认。

1. 汇总所有 entries 的状态分布：

   ```
   📊 设定集盘点
   
   总条目：{{total}}
   ✅ confirmed：{{confirmed}}
   🔶 tentative：{{tentative}}
   ⛔ deprecated：{{deprecated}}
   
   按类别：
   - world_rule: {{count}}（confirmed: {{n}}）
   - power_system: {{count}}（confirmed: {{n}}）
   - faction: {{count}}（confirmed: {{n}}）
   - geography: {{count}}（confirmed: {{n}}）
   - lore / terminology / species / artifact: {{count}}
   ```

2. 识别问题：
   - **孤立设定**：没有 `plot_links`、`character_links` 或 `setting_links` 的条目
   - **依赖断裂**：`setting_links` 引用了不存在或已废弃的条目
   - **规则缺口**：大纲关键事件依赖的规则尚未定义（对照 ingestion_brief 的"规则缺口"部分）

**阶段一止点：** 向用户展示盘点结果，确认整固方向。

---

### 阶段二：逐条审查与确认

**目标：** 把值得确认的 tentative 提升为 confirmed，清理无用条目。

按优先级排序处理 tentative 条目：

1. **剧情强相关**的规则优先（有 `plot_links` 且关联 confirmed 大纲节点）
2. **被其他设定依赖**的规则次之（有 `setting_links` 指向它）
3. **孤立设定**最后处理

对每条 tentative 设定，向用户展示：

```
🔶 tentative 设定：{{name}}（{{id}}）

📝 内容：{{summary}}
🔗 剧情关联：{{plot_links 或 "无"}}
🔗 设定依赖：{{setting_links 或 "无"}}
❓ 开放问题：{{open_questions 或 "无"}}

建议操作：
  [C] 确认（→ confirmed）
  [E] 编辑后确认（修改内容再确认）
  [D] 废弃（→ deprecated）
  [S] 跳过（保持 tentative）
```

用户选择后：
- `C`：调用 `/setting-edit`，将 status → confirmed，记录 lifecycle
- `E`：先修改内容，再调用 `/setting-edit` 确认
- `D`：调用 `/setting-edit` 标记 deprecated，检查是否有其他设定依赖它
- `S`：跳过，进入下一条

**阶段二止点：** 所有高优先级 tentative 处理完毕。

---

### 阶段三：补缺与依赖修复

**目标：** 填补规则缺口，修复依赖问题。

1. 对照大纲关键事件，检查是否仍有未覆盖的设定需求
2. 若发现缺口，引导用户确认后调用 `/setting-add` 创建新条目
3. 修复 `setting_links` 中的断裂引用
4. 更新 `worldbuilding/worldbuilding.yaml` 索引的 `core_concepts` 和 `factions_summary`
5. 同步更新 `worldbuilding/setting.md`（叙述版）

---

### 阶段四：状态同步与下一步

更新 `{current_path}/.novel/state.yaml`：
- `project.updated`：今天日期

## 输出格式

```markdown
## 当前状态
- 阶段：设定整固完成
- confirmed：{{confirmed_count}} 条
- tentative：{{remaining_tentative}} 条（已从 {{original_tentative}} 条减少）
- deprecated：{{deprecated_count}} 条

## 本次操作
- 确认了 {{n}} 条设定
- 废弃了 {{n}} 条设定
- 新增了 {{n}} 条设定
- 修复了 {{n}} 处依赖断裂

## 仍待处理
- {{remaining_issues}}

## 下一步
1. {{next_task_1}}
2. {{next_task_2}}

## 推荐命令
- /setting-add {{name}}                 补充缺口设定
- /setting-edit {{id}} {{changes}}      继续编辑
- /worldbuilding-review                 做一次完整审查
- /pipeline-chapter-kickoff             设定稳固后开始写章节
```

## 注意事项

- **不要一次确认所有 tentative。** 只确认有剧情支撑的、写作时确实要用的设定。
- 保持 tentative 状态不丢人——未展开的设定保留 tentative 是正确的。
- 废弃设定不删除文件，保留历史记录。
- 整固过程中如发现大纲需要调整，记录但不在此 pipeline 中执行，建议用 `/plot-edit` 单独处理。
- 逐条确认，不批量操作，避免误确认。
