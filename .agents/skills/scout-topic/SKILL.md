---
name: scout-topic
description: 品类选择 + 选题分析。开新书或找题材时使用。
---

# scout-topic（选题侦察）

> **用途**：帮助用户选择品类、分析目标平台、制定选题策略。
> **前置条件**：项目已创建（`novel new` 或已有项目目录）。
> **输出文件**：`settings/scout_report.yaml`

---

## 核心原则

1. **数据驱动**：基于平台榜单数据和品类分析，不凭感觉选。
2. **品类先行**：先定品类，再定题材，最后定标签。
3. **差异化**：同质化方向不选，必须有差异化定位。
4. **可行性**：样本不足给"中"，不给"高"。内置知识模式一律"中"。

---

## Phase 定义

### Phase 1：品类定位

**入口条件**：项目已创建
**目标**：确定品类（玄幻/都市/系统/言情/其他）

**步骤**：
1. 读取 `references/genre-catalog.md`，向用户展示品类路由表
2. 询问用户倾向的品类方向
3. 根据用户回答，展示该品类的核心机制、结构节点、关键维度
4. 确认品类选择，记录到 `scout_report.yaml` 的 `genre` 字段

**出口条件**：`genre` 字段已填写
**加载 References**：`genre-catalog.md`

---

### Phase 2：平台分析

**入口条件**：品类已确定
**目标**：确定目标平台 + 了解平台调性

**步骤**：
1. 读取 `references/platform-profiles.md`，展示各平台特点
2. 询问用户目标平台（番茄/起点/晋江/其他）
3. 展示该平台的目标读者画像、内容调性、付费模式
4. 确认平台选择，记录到 `scout_report.yaml` 的 `platform` 和 `target_audience` 字段

**出口条件**：`platform` 和 `target_audience` 字段已填写
**加载 References**：`platform-profiles.md`

---

### Phase 3：选题决策

**入口条件**：平台已确定
**目标**：基于品类+平台，产出具体的选题方向

**步骤**：
1. 读取 `references/topic-decision.md`
2. 按"选题四步"引导用户：
   - 能爆的原因（先当假设）
   - 市场验证（榜单样本）
   - 差异化定位
   - 可行性 + 风险 + 验证动作
3. 产出 2-3 个选题方向，写入 `scout_report.yaml` 的 `premise` 和 `core_hooks`

**出口条件**：`premise` 和 `core_hooks` 已填写
**加载 References**：`topic-decision.md`

---

### Phase 4：标签策略

**入口条件**：选题方向已确定
**目标**：制定标签组合策略

**步骤**：
1. 读取 `references/tag-strategy.md`
2. 分析目标品类的热门标签 + 竞争度
3. 设计标签组合（3-6 个主要标签 + 次要标签）
4. 运行 `scripts/check-tags.js` 验证标签组合
5. 确认标签，记录到 `scout_report.yaml` 的 `recommended_tags` 和 `tag_analysis`

**出口条件**：标签组合已通过 check-tags.js 验证
**加载 References**：`tag-strategy.md`

---

### Phase 5：品类感知配置

**入口条件**：标签已确定
**目标**：引导用户填写 `required_elements`，供后续 skill 做质量门禁

**步骤**：
1. 根据已选品类，展示该品类的默认 `required_elements`（见下表）
2. 询问用户是否需要调整（增删必需/可选元素）
3. 确认并写入 `scout_report.yaml` 的 `required_elements` 字段

**出口条件**：`required_elements` 已填写
**加载 References**：无（使用内置品类默认值）

**品类默认值参考**：

| 品类 | worldbuilding.required | characters | opening_hook.type | structure.type |
|------|------------------------|------------|-------------------|----------------|
| xuanhuan | power_system, factions, locations | protagonist+mentor+villain | golden_finger | 三幕式 |
| urban | era_details, locations, social_rules | protagonist+supporting_cast | conflict | 起承转合 |
| system | system_rules, quest_mechanics | protagonist+system_entity | golden_finger | 三幕式 |
| romance | locations, relationship_context | protagonist+love_interest | meet_cute | 起承转合 |
| suspense | crime_rules, investigation_procedures | protagonist+suspect_pool | mystery_hook | 三幕式 |

---

### Phase 6：报告定稿

**入口条件**：所有字段已填写
**目标**：生成完整的 scout_report.yaml

**步骤**：
1. 汇总所有字段，展示给用户确认
2. 如有遗漏，提示补充
3. 写入 `settings/scout_report.yaml`
4. 清理 `_progress.md`（如存在）

**出口条件**：scout_report.yaml 已生成
**加载 References**：无

---

## 质量门禁

本 skill 无自动化脚本门禁，但有以下检查：

- Phase 4 使用 `check-tags.js` 验证标签组合无冲突
- Phase 5 确保 `required_elements` 至少声明了 worldbuilding、characters、opening_hook、structure

---

## 断点恢复

**状态文件**：`_progress.md`（位于小说项目根目录）

**格式**：
```markdown
# scout-topic Progress
- current_phase: <1-6>
- status: in_progress | completed
- last_updated: <timestamp>
```

**恢复逻辑**：
- 启动时检查 `_progress.md`
- 若存在且 status != completed，提示用户是否继续上次进度
- 跳到对应 Phase 继续执行

---

## 输出文件

- `settings/scout_report.yaml`：选题侦察报告（完整格式见 data/schemas/scout_report.schema.yaml）

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | genre-catalog.md | 品类框架速查，选择品类 |
| 2 | platform-profiles.md | 平台画像，选择平台 |
| 3 | topic-decision.md | 选题决策方法论 |
| 4 | tag-strategy.md | 标签组合策略 |
| 5 | （内置默认值） | 品类感知配置 |
| 6 | — | 报告定稿 |

---

## 下一步

scout_report.yaml 生成后，可进入：
- `/worldbuilding`：世界观设计
- `/design-character`：人设设计
