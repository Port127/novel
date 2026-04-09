---
name: chapter-draft
description: 基于大纲和角色设定，辅助生成章节初稿。将 outline 阶段的章节推进到可打磨的 draft。
when_to_use: 用户准备从大纲开始写正文，想要 AI 辅助生成初稿，或需要一个可编辑的起点
argument-hint: "[章节ID] [--style 风格] [--focus 重点]"
arguments: chapter_id
---

# 任务

基于大纲、角色设定和世界观，为目标章节生成一份结构化初稿。

核心原则：**初稿是起点，不是终稿。优先保证剧情骨架和人物行为正确，文笔留给用户打磨。**

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 按 [章节自动推断协议](_protocols/chapter-auto-inference.md) 确定目标章节
3. 读取 `{current_path}/chapters/$0.md` 确认章节存在
4. 读取 `{current_path}/chapters/index.yaml` 获取章节元数据
5. 确认章节状态为 `outline`（若为 `idea`，提示先用 `/chapter-update` 推进到 `outline` 并补充场景大纲）
6. 按 [预检完整性协议](_protocols/preflight-integrity.md) 检查目标章节引用链完整性（含前序章节 summary 和角色状态）

## 输入参数

- `$0` (chapter_id): 章节 ID
- `--style`: 可选风格模板名称（从 `shared/styles/templates.yaml` 读取）
- `--focus`: 可选写作重点，如"开场悬念""情感冲击""打斗节奏"
- `--pov-deep`: 深度 POV 模式——叙述紧贴视角角色的感知、思维和盲区，不透露其他角色内心
- `--alt [备注]`: 生成备选版本而非覆盖主稿（见步骤 6b）

## 执行步骤

### 1. 收集写作上下文

读取以下文件构建完整上下文：

**前情积累（最重要——让 AI 知道"到目前为止发生了什么"）：**
- `{current_path}/chapters/index.yaml` — 提取本章之前**所有已写章节的 `summary`**，拼接为前情摘要链
- 本章出场角色的 `current_state` — 每个角色"此刻是什么状态"（位置、情绪、已知信息、行动目标、未解悬念）
- 若存在前一章节文件，读取其结尾段落（确保开场衔接）

**大纲与设定：**
- `{current_path}/plot/outline.md` — 本章对应的大纲节点（目标、事件、冲突、钩子）
- `{current_path}/plot/outline.yaml` — 伏笔和节奏标记
- `{current_path}/characters/*.yaml` — 本章出场角色的完整档案（重点：`traits`、`fatal_flaw`、`obsession`、`soft_spot`、`misbelief`、`contrast_habit`、`speech_pattern`）
- `{current_path}/characters/relations.yaml` — 出场角色之间的当前关系状态
- `{current_path}/characters/relation_events.yaml` — 最近的关系变化事件
- `{current_path}/worldbuilding/setting.md` — 本章涉及的世界观背景
- `{current_path}/worldbuilding/entries/*.yaml` — 本章依赖的具体设定条目（**注意有效期筛选，见下方**）
- `{current_path}/timeline/main.yaml` — 本章的时间位置

**设定有效期筛选**：读取设定条目时，检查 `valid_until`、`superseded_by` 和 `expiry_trigger`：
- 已被取代的条目（`superseded_by` 非空）→ 跳过，改用新版条目
- 已过有效期的条目（`valid_until` 对应的章节/事件已发生）→ 跳过，并检查是否有后继条目
- 即将过期的条目（本章接近 `valid_until`）→ 标记警告，写作时考虑体现设定变化的过渡
- 如果一条过期设定没有后继条目，在步骤 4 的生成前检查中报错

构建上下文的优先级：**前情摘要链 > 角色当前状态 > 前章结尾 > 本章大纲 > 角色档案 > 设定**。如果上下文过长需要裁剪，从底部开始砍。

### 2. 素材库参考检索（可选）

如果 `../novel-material/data/material.db` 存在，根据本章大纲自动检索参考场景：

```bash
python ../novel-material/scripts/search.py scene \
  --scene-type {本章主要场景类型} \
  --emotion {本章主要情感基调} \
  --limit 5
```

将 Top-3 结果摘要附入写作上下文，标注「参考场景」。不直接复用原文，仅作结构和技法参考。

如果素材库不可用，跳过此步骤，不影响后续流程。

### 3. 章节容量检查

按 [章节容量守卫协议](_protocols/chapter-scope-guard.md) 检测场景大纲是否超出单章承载量。

**检测信号**：场景数 ≥ 4、重大转折 ≥ 2、情绪跨度过大、预估字数超目标 1.5 倍、多线并行 ≥ 3、时间跨度 > 3 天。

**任一信号触发时**：停止生成，输出拆章建议，等待用户选择（拆分方案 / 不拆）。用户确认后才继续。

### 4. 生成前检查

在生成前验证：

- 本章依赖的设定是否为 `confirmed`？若有 `tentative` 设定，标记警告
- 本章出场角色是否都已创建？缺失则提示
- 前一章的章尾钩子是否在本章有回应？
- 大纲中标记的伏笔是否已安排埋设/回收位置？

**大纲仅作参考，不是约束：**

若用户提供的场景大纲（章节文件中的 `## 场景大纲`）与 `outline.md` 中的对应节点存在差异，**以章节文件中的场景大纲为准**。差异部分在输出末尾标注，不阻止生成：

```
⚡ 检测到场景大纲与主大纲存在差异：
- [差异描述]
草稿将按章节场景大纲生成。如需同步主大纲，写完后运行 /plot-edit。
```

### 5. 构建写作指令

基于收集的上下文，构造以下写作约束：

**结构约束：**
- 开场：从异常、悬念或未解释信息起手，不要日常流水
- 中段：至少一个冲突升级点，角色必须做出选择或付出代价
- 结尾：留下钩子——可以是谎言、口误、异常意象或未解答的问题

**人物约束：**
- POV 角色的内心独白必须反映其 `misbelief` 或 `obsession`
- 关键对白必须体现角色 `traits` 和身份差异，不同质化
- 至少一个角色在本章展现 `fatal_flaw` 或 `contrast_habit`
- 关系互动必须与 `relations.yaml` 的当前状态一致

**称呼约束（基于 [名字解析协议](_protocols/name-resolution.md) §1b）：**
- 叙述中对角色的称呼由 POV 角色与该角色的关系亲疏决定，不默认使用正式全名
- 对白中的称呼由说话者决定（见协议 §1c）
- 如果角色 aliases 为空，用全名，不编造昵称

**对白约束（基于 speech_pattern）：**
- 每个出场角色写对白前，先读取其 `speech_pattern`
- 按 `tone` 设定语气基调（嘲讽的角色不会正经说话，粗犷的角色不会用敬语）
- 按 `profanity_level` 控制粗话频率（"满嘴脏话"的角色每段对白都应有脏字，"无"的角色绝对不出现）
- 按 `sentence_style` 控制句式（"短句多"的角色不写超过 15 字的对白）
- 插入 `catchphrase` 和 `verbal_tics`（不是每句都插，自然分布即可）
- 检查 `taboo_words`，确保角色不说不该说的话
- 按 `education_voice` 调整用词层次（文盲不用成语，学究不说大白话）
- 如果角色没有 `speech_pattern`，用 `traits` + `profile` 推断一个临时画像，并在写作备忘中标记"建议补充 speech_pattern"

**文风约束：**
- 若指定了 `--style`，按风格模板的句式、修辞、节奏特征写
- 若项目 `meta.yaml` 中有 `style.prose` 或 `style.notes`，作为基础文风参考
- 默认不使用典型 AI 文风（避免并列排比、空泛抒情、机械转折）
- 比喻每千字不超过 3 个，且必须贴合 POV 角色的认知范围
- 场景描写不连续超过 2 段，每段描写需绑定角色反应或叙事推进

### 6. 生成初稿

**创作态度——大纲是骨架，你要写活它：**
- 大纲里"张三发现真相"是一句话，正文里是一整个从困惑到震惊到否认的过程——写那个过程
- 细节要具体到能拍电影：不写"他紧张了"，写"他把筷子夹断了"
- 感官优先于评价：不写"这个地方很危险"，写"空气里有铁锈味，脚下的台阶缺了一角"
- 留白比解释更有力：角色不说的话、不做的动作，有时比说了做了更有信息量
- 每个场景找一个"只有这个故事才会有的细节"——不要通用意象，要属于你的世界的独特画面
- 叙述节奏要有呼吸感：紧张处用短句推进，沉静处让长句铺开，不要匀速

按场景大纲的顺序逐场景生成，每个场景包含：

- 场景起始的环境/情绪锚点（1-2 句）
- 核心动作/对白/冲突
- 场景结束的推进或悬念

**标准模式**：初稿写入 `{current_path}/chapters/$0.md` 的「正文草稿」部分。

**备选版本模式（--alt）**：见步骤 6b。

### 6b. 备选版本写入（--alt）

当指定 `--alt` 时，不覆盖主稿：

1. **确定版本号**：扫描 `chapters/` 目录中的 `{chapter_id}_v*.md` 文件，取最大版本号 +1。若无备选文件，新版本为 `v2`（主稿隐含为 `v1`）。

2. **写入备选文件**：创建 `{current_path}/chapters/{chapter_id}_v{N}.md`，格式与主稿相同（含元数据头部、场景大纲、正文草稿、伏笔区）。

3. **更新 index.yaml**：
   - 若该章节尚无 `versions` 字段，先为主稿补建：`{ tag: v1, file: {chapter_id}.md, word_actual: ..., note: "主稿", created: ... }`
   - 追加新版本：`{ tag: v{N}, file: {chapter_id}_v{N}.md, word_actual: ..., note: "{用户备注}", created: 今天 }`
   - `active_version` 保持不变（仍指向主稿）

4. **输出提示**：
   ```
   ✅ 备选版本已生成

   🧩 章节：$0（版本 v{N}）
   📝 字数：{{word_count}}
   📝 备注：{{用户备注}}
   📄 文件：chapters/{chapter_id}_v{N}.md

   当前版本数：{{total_versions}}
   💡 对比版本：/chapter-compare $0
   💡 切换主稿：/chapter-update $0 --promote v{N}
   ```

### 7. 生成附带信息

在正文之后追加本章写作备忘和来源水印：

```markdown
## 写作备忘（AI 生成，可删除）

- 本章伏笔：{{planted_hooks}}
- 待回收伏笔：{{pending_hooks}}
- 角色状态变化：{{character_changes}}
- 下一章衔接点：{{next_chapter_hook}}

## 内容来源追溯（AI 生成，可删除）

| 段落/场景 | 来源 | 置信度 |
|-----------|------|--------|
| {{场景1描述}} | 场景大纲 / 草稿 L{N} | ✅ 原文 |
| {{场景2描述}} | 大纲 + 角色卡推断 | 🔶 推断 |
| {{场景3描述}} | 无明确来源 | ❌ AI 补充 |
```

**来源水印规则**：
- 对每个生成的场景/段落，追溯其内容依据
- `✅ 原文`：该场景的核心事件在场景大纲或用户草稿中有明确对应
- `🔶 推断`：事件框架来自大纲，但细节（对白、动作、环境描写）是 AI 基于角色卡/设定推断
- `❌ AI 补充`：事件本身在任何输入材料中都没有对应，是 AI 为连贯性/节奏需要补充的
- 让用户一眼看出哪些忠于原始材料，哪些是 AI 自由发挥

### 8. 操作日志

按 [操作日志协议](_protocols/operation-journal.md)，更新 `.novel/ops_log.yaml` 为 completed。

### 9. 更新状态

通过 `/chapter-update` 将章节状态推进到 `draft`。

更新 `{current_path}/chapters/index.yaml` 的 `word_actual`。

## 输出格式

```
✅ 初稿生成完成

🧩 章节：$0
📝 字数：{{word_count}}
👁️ 视角：{{pov}}
🎯 完成目标：{{goal}}

⚠️ 注意事项：
{{#if tentative_settings}}
- 本章依赖未确认设定：{{tentative_settings}}
{{/if}}
{{#if missing_hooks}}
- 前章钩子未在本章回应：{{missing_hooks}}
{{/if}}

下一步：
   直接编辑 chapters/$0.md 修改初稿
   /chapter-review $0              审查结构和节奏
   /pipeline-draft-polish $0       一键打磨
   /voice-check [角色名] $0        检查对白区分度
```

## 注意事项

- 初稿是**可编辑的起点**，不是成品。优先保证骨架正确，风格和细节留给用户
- 不要过度描写——宁可留白让用户补充，也不要填充空泛抒情
- 对白要体现人物差异，不要所有角色说话一个味
- 如果大纲信息不足以支撑完整初稿，在稀薄处用 `<!-- TODO: 此处需要补充... -->` 标记，不要编造
- 生成后建议运行 `/anti-ai-check` 评估 AI 痕迹
- 如果用户只想要某个场景的初稿而非整章，可以指定 `--focus` 聚焦
- **草稿优先**：草稿写完后不自动更新大纲、人物卡或设定；差异在报告中标注，由用户决策是否触发更新（见 `_protocols/draft-primacy.md`）
