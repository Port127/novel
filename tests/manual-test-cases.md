# 手动测试用例集（300例）

> 模拟真实用户操作路径，覆盖全部 skill、pipeline、backend API 和跨模块交互。
> 每条用例包含：前置条件、操作步骤、预期结果。
> 标记说明：🟢 基础流程 | 🟡 边界场景 | 🔴 压力/异常场景

---

## A. 项目生命周期（A001–A030）

### 创建项目

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| A001 | 🟢 首次创建项目 | 无任何项目存在 | `/novel-init 我的第一本书 都市异能` | 创建 `projects/我的第一本书/` 完整目录结构；`.projects.yaml` 新增条目；`.current.yaml` 指向该项目；`.cursor/rules/` 同步项目规则 |
| A002 | 🟢 创建第二个项目 | 已有项目 A | `/novel-init 第二本书 玄幻` | 新项目创建成功；`.current.yaml` 切换到新项目；旧项目文件不受影响 |
| A003 | 🟡 书名含特殊字符 | 无 | `/novel-init 灵气复苏？不，超凡即是污染！ 都市异能` | 目录名含问号和感叹号能正确创建；后续所有路径操作正常 |
| A004 | 🟡 书名含空格和引号 | 无 | `/novel-init "那年 那月" 言情` | 含空格的目录名正确创建和引用 |
| A005 | 🟡 重复书名创建 | 已有同名项目 | `/novel-init 我的第一本书 科幻` | 提示项目已存在，要求确认或更名 |
| A006 | 🟡 使用 `--with-examples` | 无 | `/novel-init 测试项目 都市异能 --with-examples` | 生成带示例数据的项目，示例数据格式正确 |
| A007 | 🔴 `.projects.yaml` 不存在时创建项目 | 手动删除 `.projects.yaml` | `/novel-init 恢复测试 科幻` | 自动重建 `.projects.yaml` 或给出清晰错误 |

### 切换/列表/状态

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| A008 | 🟢 切换到已有项目 | 有项目 A 和 B，当前在 A | `/novel-switch 第二本书` | `.current.yaml` 更新；`.cursor/rules/` 同步为项目 B 的规则 |
| A009 | 🟡 切换到不存在的项目 | 只有项目 A | `/novel-switch 不存在的书` | 明确报错，当前项目不变 |
| A010 | 🟢 列出所有项目 | 有多个项目 | `/novel-list` | 显示所有项目名、类型、状态；标记当前项目 |
| A011 | 🟡 无项目时列表 | 无任何项目 | `/novel-list` | 显示空列表提示，建议创建 |
| A012 | 🟢 查看项目状态 | 有活跃项目，已创建角色和章节 | `/novel-status` | 显示完整状态：角色数、章节数、设定数、进度等 |
| A013 | 🟡 新项目无任何内容时查看状态 | 刚 init 的空项目 | `/novel-status` | 显示零值状态而不是报错 |
| A014 | 🟡 `.current.yaml` 损坏 | 手动写入无效内容 | `/novel-status` | 明确报错，提示修复方法 |

### 编辑项目信息

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| A015 | 🟢 修改书名 | 已有项目 | `/novel-edit name 新书名` | 文件夹重命名；`.projects.yaml`、`.current.yaml`、`meta.yaml` 全部更新 |
| A016 | 🟢 修改类型 | 已有项目 | `/novel-edit genre 科幻` | `meta.yaml` 更新 |
| A017 | 🟡 将书名改为已存在的项目名 | 有项目 A 和 B | `/novel-edit name 第二本书` | 检测冲突并拒绝或要求确认 |
| A018 | 🟡 修改书名后，引用旧路径的规则文件 | 已有项目且 rules 已同步 | 修改书名后检查 `.cursor/rules/*.mdc` | 规则文件中的项目路径引用已更新 |

### 诊断

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| A019 | 🟢 项目健康检查 | 完整项目 | `/novel-doctor` | 显示各模块健康状态 |
| A020 | 🟡 缺少 `worldbuilding.yaml` | 手动删除该文件 | `/novel-doctor` | 报告缺失文件，建议修复 |
| A021 | 🟡 `character_index.yaml` 与实际角色文件不一致 | 手动添加角色文件但不更新索引 | `/novel-doctor` | 检测到不一致并报告 |
| A022 | 🟡 `chapters/index.yaml` 引用不存在的 `.md` 文件 | 删除某章节 `.md` 但保留索引条目 | `/novel-doctor` | 报告悬空引用 |
| A023 | 🟡 `../novel-material` 不存在 | 未配置素材库 | `/novel-doctor` | 正常完成，提示素材库不可用 |

### 索引维护

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| A024 | 🟢 重建索引 | 已有角色、设定、章节 | `/project-reindex` | 交叉引用全部重建；`PROJECT_MAP.md` 更新 |
| A025 | 🟡 dry-run 模式 | 同上 | `/project-reindex --dry-run` | 只输出变更预览，不实际写入 |
| A026 | 🟡 角色文件存在但索引中缺失 | 手动创建了 `characters/新角色.yaml` | `/project-reindex` | 将新角色补入 `character_index.yaml` |
| A027 | 🟡 设定交叉引用有残留（引用已删除的角色） | 删除角色但未清理设定的 `character_links` | `/project-reindex` | 清理无效引用 |

### KPI/周报

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| A028 | 🟢 生成周报 | 本周有写作活动 | `/project-weekly-report 本周` | 输出产能、进度、风险指标 |
| A029 | 🟡 无活动时生成周报 | 本周无任何操作 | `/project-weekly-report 本周` | 显示零产出而非报错 |
| A030 | 🟢 计算 KPI | 有多章完成 | `/novel-kpi 全部` | 显示字数、完成率、质量指标 |

---

## B. 素材消化（B001–B015）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| B001 | 🟢 首次消化草稿 | 新项目，有一份用户写的草稿 `.md` | `/draft-ingest drafts/故事构思.md` | 生成 `ingestion_brief.md`；`state.yaml` 更新 ingestion 状态 |
| B002 | 🟢 草稿中包含人物设定 | 草稿含"赵宋，20岁，大学生" | 消化后查看 `ingestion_brief.md` | 人物信息被提取并结构化记录 |
| B003 | 🟢 草稿中包含世界观描述 | 草稿含力量体系说明 | 消化后查看 | 世界观信息被正确识别和提取 |
| B004 | 🟡 草稿使用别称和口语化表述 | 草稿中角色用绰号，如"老赵"、"小宋" | 消化后查看 | 别称被保留在摘要中，不被强行替换为正式名 |
| B005 | 🟡 草稿内容不完整（写到一半截断） | 草稿以逗号结尾，明显未完 | `/draft-ingest` | 摘要标注"素材未完"，不自行补完 |
| B006 | 🟡 草稿包含矛盾信息 | "赵宋20岁"和"赵宋大三（22岁）"出现在同一草稿 | 消化后查看 | 摘要中标记矛盾，不擅自选择 |
| B007 | 🟡 重复消化同一文件 | 已消化过 A.md | 再次 `/draft-ingest drafts/A.md` | 提示已消化，询问是否覆盖/追加 |
| B008 | 🟡 消化后再消化另一份草稿 | 已有 ingestion_brief | `/draft-ingest drafts/第二份构思.md` | 追加或合并到现有摘要，不丢失首次内容 |
| B009 | 🟢 消化后确认写入 | 消化流程进行中 | AI 展示提取结果并要求确认 | 用户确认前不写入任何文件 |
| B010 | 🟡 用户拒绝确认 | 消化流程中 AI 展示了结果 | 用户说"不对，重新来" | 不写入文件，保持原状 |
| B011 | 🔴 草稿文件为空 | 空的 `.md` 文件 | `/draft-ingest drafts/empty.md` | 提示文件为空，不生成空摘要 |
| B012 | 🔴 草稿文件不存在 | 路径错误 | `/draft-ingest drafts/不存在.md` | 明确报错 |
| B013 | 🟡 草稿含大量对话 | 草稿以对话为主 | 消化后查看 | 对话被作为风格素材保留，不被丢弃 |
| B014 | 🟡 草稿是纯设定无剧情 | 整份草稿都是世界观规则 | 消化后查看 | 正确识别为设定类素材 |
| B015 | 🟡 草稿含图片引用或非文本标记 | 草稿有 `![图片](...)` 或 `<img>` | 消化后查看 | 跳过不可解析内容，不报错 |

---

## C. 角色管理（C001–C035）

### 创建角色

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| C001 | 🟢 手动创建主角 | 已有项目 | `/character-add 赵宋 --role 主角 --age 20` | 生成 `characters/赵宋.yaml`；更新 `character_index.yaml` |
| C002 | 🟢 从草稿提取角色 | 已消化草稿 | `/character-add 王妮 --from ingestion_brief.md` | 从摘要提取王妮信息，生成角色卡 |
| C003 | 🟡 创建同名角色 | 已有"赵宋" | `/character-add 赵宋 --role 配角` | 提示已存在，拒绝或要求确认 |
| C004 | 🟡 快速模式创建 | 无 | `/character-add 路人甲 --quick` | 最小化创建，五件套可以暂缺但有提示 |
| C005 | 🟢 补齐五件套 | 角色卡缺少 `fatal_flaw` 等 | 创建时手动补充或后续编辑 | 五件套（fatal_flaw/obsession/soft_spot/misbelief/contrast_habit）全部填写 |
| C006 | 🟡 角色名含生僻字 | 无 | `/character-add 鑫鑫 --role 配角` | 正常创建，文件名正确 |
| C007 | 🟡 角色名含英文/数字 | 无 | `/character-add Jack --role 外国友人` | 正常创建 |
| C008 | 🟡 不提供 role 参数 | 无 | `/character-add 无名氏` | 提示必要字段或使用默认值 |
| C009 | 🟢 创建后检查 `state.yaml` | 刚创建角色 | 读取 `state.yaml` | `project.updated` 时间已更新 |

### 编辑角色

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| C010 | 🟢 修改角色性格描述 | 已有角色"赵宋" | `/character-edit 赵宋 --traits "谨慎、多疑但善良"` | `赵宋.yaml` 的 traits 更新 |
| C011 | 🟢 修改角色名（改名） | 已有角色"赵宋" | `/character-edit 赵宋 --name 赵松` | 文件重命名为 `赵松.yaml`；所有引用更新（index、relations、chapter 中的引用）；需要确认 |
| C012 | 🟡 改名后检查关系文件 | "赵宋"与"王妮"有关系记录 | 改名后读取 `relations.yaml` | 关系中的名字已更新 |
| C013 | 🟡 改名后检查章节引用 | "赵宋"出现在已写章节的 `characters_involved` 中 | 改名后读取 `chapters/index.yaml` | `characters_involved` 中的名字已更新 |
| C014 | 🟡 改名后检查大纲引用 | "赵宋"出现在 `outline.md` | 改名后检查 | 大纲中的角色名已更新 |
| C015 | 🟢 添加别名 | 已有角色 | `/character-edit 赵宋 --aliases "老赵,小宋"` | `aliases` 字段更新 |
| C016 | 🟡 从章节回填角色信息 | 已写章节中有角色新表现 | `/character-edit 赵宋 --from-chapters` | 根据章节内容自动补充角色发展 |
| C017 | 🟡 自动补全缺失字段 | 角色卡有空字段 | `/character-edit 赵宋 --auto-fill` | AI 补全空字段，但需用户确认 |
| C018 | 🟡 编辑后触发影响扫描 | 修改了核心设定（如能力） | 编辑后观察 | 显示影响扫描结果：哪些已写章节可能受影响 |
| C019 | 🔴 编辑不存在的角色 | 无此角色 | `/character-edit 不存在 --age 25` | 明确报错 |
| C020 | 🟡 修改 `speech_pattern` | 已有角色 | `/character-edit 赵宋 --speech_pattern "简短直接，偶尔自嘲"` | 更新语音模式 |

### 查询角色

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| C021 | 🟢 查询单个角色详情 | 已有角色 | `/character-query 赵宋` | 显示完整角色信息 |
| C022 | 🟢 查询角色在某章的表现 | 角色出现在多章 | `/character-query 赵宋 --storyline` | 显示角色跨章的弧光发展 |
| C023 | 🟡 查询不存在的角色 | 无 | `/character-query 隔壁老王` | 提示不存在 |
| C024 | 🟡 按状态筛选 | 有多个角色 | `/character-query --status 主角` | 筛选结果正确 |
| C025 | 🟢 查询全部角色列表 | 多个角色 | `/character-query 全部` | 列出所有角色基本信息 |

### 角色相关的跨模块场景

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| C026 | 🟡 创建角色后立即用于章节 | 刚创建角色 | 创建角色 → 创建章节 → 在章节中引用该角色 | 章节的 `characters_involved` 正确关联 |
| C027 | 🟡 删除角色文件（手动） | 有角色文件和索引 | 用户手动删除 `characters/赵宋.yaml` | `character_index.yaml` 仍有条目（orphan）；`/novel-doctor` 应检测到 |
| C028 | 🟡 角色五件套全空创建后编辑 | `--quick` 创建的角色 | 多次编辑补齐五件套 | 每次编辑正确累积，不覆盖之前填写的字段 |
| C029 | 🟡 两个角色同姓 | 已有"赵宋" | `/character-add 赵明 --role 配角` | 两个赵姓角色共存，不混淆 |
| C030 | 🟡 角色的 `current_state` 跟踪 | 角色在多章中有发展 | 查看角色的 `current_state` | 反映最近章节中的状态（由 `chapter-update` 维护） |
| C031 | 🟡 角色首次出场记录 | 创建角色时指定 | `/character-add 林检 --first_appearance ch003` | `first_appearance` 正确记录 |
| C032 | 🟡 `cross_references` 完整性 | 角色关联了设定和章节 | `/project-reindex` 后检查角色卡 | `related_settings`、`key_chapters`、`related_plot_nodes` 正确填充 |
| C033 | 🟡 角色弧光 `arc` 记录 | 角色有多段弧光 | 编辑角色添加 arc | `arc[]` 数组正确追加 |
| C034 | 🔴 同时编辑同一角色（并发） | 两个会话 | 会话 A 编辑 traits，会话 B 编辑 age | 后写入的不覆盖先写入的不同字段（或至少有冲突提示） |
| C035 | 🟡 角色 `appearance_stats` 更新 | 角色出现在多章 | 检查 stats | 出场统计与实际章节一致 |

---

## D. 角色关系（D001–D022）

### 建立关系

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| D001 | 🟢 创建双人关系 | 两个角色已存在 | `/relationship-add 赵宋 王妮 --type 守护 --tension "信任vs隐瞒"` | `relations.yaml` 新增；两个角色卡的 `relations[]` 更新 |
| D002 | 🟡 为不存在的角色创建关系 | 只有角色 A | `/relationship-add 赵宋 不存在 --type 对手` | 报错提示角色不存在 |
| D003 | 🟡 重复创建同一对关系 | 已有赵宋-王妮关系 | 再次 `/relationship-add 赵宋 王妮 --type 对手` | 提示已有关系，询问更新还是新增 |
| D004 | 🟡 自动推导关系 | 角色在章节中有互动 | `/relationship-add 赵宋 庄怀瑾 --auto` | 从已有章节推导关系类型和张力 |
| D005 | 🟢 快速创建 | 无 | `/relationship-add 赵宋 林检 --quick` | 最小信息创建，可后续补充 |
| D006 | 🟡 从素材提取关系 | 有 ingestion_brief | `/relationship-add 赵宋 室友A --from ingestion_brief.md` | 从摘要提取关系信息 |

### 关系日志

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| D007 | 🟢 记录关系变化 | 有关系、有章节 | `/relationship-log 赵宋 王妮 --chapter ch003 --change "赵宋发现王妮隐瞒了身份" --cause "灰域事件" --cost "信任裂痕"` | `relation_events.yaml` 追加事件 |
| D008 | 🟡 记录不可逆变化 | 有关系 | `/relationship-log A B --irreversible --change "A杀死了B的师父"` | 事件标记 `irreversible: true` |
| D009 | 🟡 缺少原因字段 | 有关系 | `/relationship-log A B --change "关系恶化"` | 提示补充 cause 和 cost（不强制但建议） |
| D010 | 🟡 给关系打强度分 | 有关系 | `/relationship-log A B --strength 7` | `relations.yaml` 中 strength 更新 |

### 关系图谱与查询

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| D011 | 🟢 生成全局关系图 | 多个角色有关系 | `/relationship-map` | 输出 Mermaid 图谱，节点和边正确 |
| D012 | 🟡 只看某角色的关系 | 有多对关系 | `/relationship-map 赵宋` | 只显示赵宋相关的关系 |
| D013 | 🟢 查看关系演进 | 有多条日志 | `/relationship-evolution 赵宋 --with 王妮` | 按时间顺序显示关系变化轨迹 |
| D014 | 🟡 无日志时查看演进 | 有关系但无事件 | `/relationship-evolution 赵宋 --with 王妮` | 提示无事件记录 |

### 关系检查

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| D015 | 🟢 检查关系一致性 | 有关系和事件日志 | `/relationship-check` | 检测跳变、缺因果、缺代价的事件 |
| D016 | 🟡 关系强度突变 | 上一章 strength=8，下一章突然=2 | 检查 | 标记为可疑跳变 |
| D017 | 🟡 日志缺少 misbelief 依据 | 有标记 misbelief 的事件但缺依据 | 检查 | 报告缺失 |
| D018 | 🟡 事件时间线冲突 | 日志中事件顺序与时间线矛盾 | 检查 | 检测到时间冲突 |
| D019 | 🟡 角色改名后的关系记录 | 角色 A 改名 | 改名后查看关系 | 历史事件中的旧名是否被更新/保留标注 |
| D020 | 🟡 删除角色后关系的处理 | 手动删除角色文件 | 查看 `relations.yaml` | 存在孤立关系记录 |
| D021 | 🟡 单向关系 | A 对 B 有特殊感情，B 不知道 | 创建这种不对称关系 | 关系记录能表达不对称性 |
| D022 | 🟡 三角关系 | A-B, B-C, A-C 都有关系 | 全部创建后查看图谱 | 三角关系正确展示 |

---

## E. 世界观与设定（E001–E030）

### 添加设定

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| E001 | 🟢 添加力量体系设定 | 已有项目 | `/setting-add 五阶路径 --category power_system --status tentative` | 生成 `entries/power_001.yaml`；`worldbuilding.yaml` 索引更新 |
| E002 | 🟢 从 ingestion_brief 批量导入 | 已消化草稿 | `/setting-add --batch --from ingestion_brief.md` | 批量创建多条设定，每条需确认 |
| E003 | 🟡 默认状态为 tentative | 不指定 status | `/setting-add 灰域 --category lore` | 状态为 tentative |
| E004 | 🟡 添加与已有设定同名的条目 | 已有"五阶路径" | `/setting-add 五阶路径 --category power_system` | 提示已存在，询问操作 |
| E005 | 🟢 添加带有效期的设定 | 无 | `/setting-add 旧规则 --valid-until ch010` | 设定带有效期标记 |
| E006 | 🟡 添加替代旧设定的新设定 | 已有旧设定 | `/setting-add 新规则 --supersedes old_rule_001` | 旧设定状态变更；新设定关联旧设定 |
| E007 | 🟢 添加后的 confirmed 设定触发影响扫描 | 设定已 confirmed | `/setting-add 核心规则 --status confirmed` | 扫描已有章节是否与新设定冲突 |

### 编辑设定

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| E008 | 🟢 修改设定描述 | 已有设定 | `/setting-edit power_001 --description "新的力量描述"` | 条目更新 |
| E009 | 🟢 状态流转：tentative → confirmed | 设定为 tentative | `/setting-edit power_001 --status confirmed` | 状态更新；触发影响扫描 |
| E010 | 🟡 状态流转：confirmed → deprecated | 故事发展后设定过期 | `/setting-edit power_001 --status deprecated` | 状态更新；不自动删除 |
| E011 | 🟡 逆向状态流转：confirmed → tentative | 想撤回确认 | `/setting-edit power_001 --status tentative` | 应允许或至少给出说明 |
| E012 | 🟡 编辑 confirmed 设定的核心内容 | 设定已确认且被章节引用 | 修改 `rules`/`constraints` | 影响扫描报告哪些章节受影响 |
| E013 | 🟡 `--evolve` 设定演进 | 旧设定需要升级 | `/setting-edit power_001 --evolve` | 创建新版本设定，旧版标记 |
| E014 | 🔴 编辑不存在的设定 | 无此 ID | `/setting-edit nonexistent_001` | 明确报错 |
| E015 | 🟡 编辑设定的 `character_links` | 设定关联了角色 | 修改关联的角色列表 | 正确更新，不破坏角色侧的 `cross_references` |

### 世界观审查

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| E016 | 🟢 全面世界观审查 | 有多条设定 | `/worldbuilding-review` | 检查自洽性、代价缺失、规则缺口 |
| E017 | 🟡 聚焦力量体系审查 | 有力量设定 | `/worldbuilding-review --focus power_system` | 只审查力量相关设定 |
| E018 | 🟡 大量 tentative 设定堆积 | 10+ 条 tentative | 审查 | 报告 tentative 堆积风险 |
| E019 | 🟡 设定之间存在矛盾 | 设定 A 说"不可逆"，设定 B 说"可恢复" | 审查 | 检测到矛盾并报告 |
| E020 | 🟡 设定缺少剧情支撑 | 设定无 `plot_links` | 审查 | 报告孤立设定 |

### 设定与故事交互

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| E021 | 🟡 设定过了 `valid-until` 章节 | 设定标记 `valid-until: ch010`，已写到 ch012 | 一致性检查 | 提示该设定已过期但可能仍被引用 |
| E022 | 🟡 deprecated 设定仍在章节中被引用 | 设定已 deprecated | 一致性检查 | 标记问题 |
| E023 | 🟡 新设定与已写章节内容冲突 | ch005 的描写基于旧规则 | 添加新设定后 | 影响扫描报告冲突 |
| E024 | 🟡 设定有 `open_questions` 未解决 | 设定中标记了待确认项 | 审查 | 报告未解决问题 |
| E025 | 🟢 `setting.md` 叙事文档与 entries 一致 | 有多条设定 | 检查 `setting.md` | 内容与 entries 文件一致 |
| E026 | 🟡 手动编辑 `setting.md` 后 | 直接修改 md 而非用 skill | 审查 | 检测到与 entries 的不一致 |
| E027 | 🟡 设定的 `lifecycle` 字段 | 设定有生命周期标记 | 查看设定详情 | lifecycle 信息完整（created, confirmed, evolved 等日期） |
| E028 | 🟡 `setting_links` 依赖关系 | 设定 A depends_on 设定 B | 删除或 deprecate 设定 B | 提示设定 A 有依赖 |
| E029 | 🟡 设定 `source` 追溯 | 设定标记了来自 ingestion_brief | 查看 | source 字段正确指向原始素材 |
| E030 | 🟡 批量导入时部分拒绝 | 批量导入 5 条设定 | 用户确认 3 条，拒绝 2 条 | 只创建被确认的 3 条 |

---

## F. 剧情大纲（F001–F035）

### 初始化与结构

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| F001 | 🟢 自动推导大纲结构 | 有 ingestion_brief | `/plot-init auto` | 从素材推导结构；生成 `outline.md`、`outline.yaml`、`plot_index.yaml` |
| F002 | 🟡 手动指定模板 | 无 | `/plot-init 三幕剧` | 按三幕剧模板生成骨架 |
| F003 | 🟡 已有大纲时重新初始化 | 已有 outline | `/plot-init auto` | 提示已存在，要求确认覆盖 |
| F004 | 🟡 无 ingestion_brief 时自动推导 | 未消化草稿 | `/plot-init auto` | 提示缺少素材，建议先消化 |

### 添加情节

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| F005 | 🟢 为章节添加场景大纲 | 已有章节 ch001 | `/plot-add ch001 "赵宋在宿舍打游戏，室友突然自燃"` | 写入 `chapters/ch001.md` 的 `## 场景大纲` 区域 |
| F006 | 🟢 添加弧光级情节 | 无 | `/plot-add --arc "第一季：觉醒" "赵宋从普通人到觉醒者的转变"` | 写入 `outline.md` 的弧光区块 |
| F007 | 🟡 从素材提取情节 | 有 ingestion_brief | `/plot-add ch001 --from ingestion_brief.md` | 从摘要提取该章对应内容 |
| F008 | 🟡 为不存在的章节添加情节 | 无 ch099 | `/plot-add ch099 "内容"` | 报错提示章节不存在 |
| F009 | 🟡 给已有场景大纲的章节追加 | ch001 已有场景大纲 | `/plot-add ch001 "新增一个紧急逃离场景"` | 追加而非覆盖 |

### 编辑大纲

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| F010 | 🟢 修改某章的场景大纲 | 章节有场景大纲 | `/plot-edit ch003 --changes "将对话改为动作场景"` | 场景大纲更新 |
| F011 | 🟡 移动情节节点 | 有多章大纲 | `/plot-edit ch003 --move ch005` | 将 ch003 的情节移到 ch005 |
| F012 | 🟡 合并两章情节 | 有两章相近的情节 | `/plot-edit ch003 --merge ch004` | 合并后检查对已写章节的影响 |
| F013 | 🟡 拆分一章情节为两章 | 某章情节过多 | `/plot-edit ch003 --split` | 拆分成 ch003 和 ch003b 或提示创建新章 |
| F014 | 🟡 编辑已写完章节的大纲 | ch001 状态为 `final` | `/plot-edit ch001 --changes "..."` | 影响分析：提示该章已完稿，修改大纲不会自动修改正文 |
| F015 | 🟡 编辑涉及钩子的节点 | 节点含已埋设的钩子 | 修改该节点 | 检查钩子状态，提示钩子可能受影响 |

### 大纲审查与建议

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| F016 | 🟢 审查大纲结构 | 有完整大纲 | `/plot-review` | 检查转折分布、节奏曲线、代价感 |
| F017 | 🟡 审查发现节奏松散 | 连续几章无转折 | 审查结果 | 指出松散区段并建议 |
| F018 | 🟡 审查发现钩子堆积 | 多钩子未回收 | 审查结果 | 报告钩子管理风险 |
| F019 | 🟢 请求情节建议 | 写到某处卡住 | `/plot-suggest "ch005写到赵宋被围困，不知道怎么脱身"` | 给出多个可选方案 |
| F020 | 🟡 请求反转建议 | 想加反转 | `/plot-suggest "需要一个震撼的反转"` | 基于已有设定给出合理反转 |
| F021 | 🟡 建议使用素材库 | 有关联素材 | `/plot-suggest` 带素材检索 | 可能搜索素材库参考 |

### 大纲查询

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| F022 | 🟢 查询特定章节的大纲 | 有大纲 | `/plot-query ch005` | 显示该章大纲 |
| F023 | 🟡 按角色查询相关情节 | 有大纲含角色信息 | `/plot-query --character 赵宋` | 显示赵宋相关的所有情节节点 |
| F024 | 🟡 查询伏笔列表 | 有伏笔 | `/plot-query --hooks` | 列出所有伏笔状态 |
| F025 | 🟡 查询冲突列表 | 大纲有冲突标记 | `/plot-query --conflict` | 显示各章冲突 |

### 大纲与正文的关系

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| F026 | 🟡 正文偏离了大纲 | 写作时走了不同方向 | 一致性检查 | 报告偏离，但不自动修改大纲 |
| F027 | 🟡 大纲中有内容不在素材中 | AI 补充了大纲 | 用户质疑 | 能追溯哪些是素材来源、哪些是 AI 补充 |
| F028 | 🟡 大纲过于粗略 | 只有一句话描述 | 审查 | 建议补充细节 |
| F029 | 🟡 一个剧情跨多章 | "觉醒"剧情需要 ch001-ch003 | 在大纲中表达 | 能正确标记跨章情节 |
| F030 | 🟡 修改大纲后不自动改正文 | 修改了 ch005 大纲 | 检查 ch005.md | 正文内容不变（draft-primacy） |
| F031 | 🟡 大纲中引用的角色不存在 | 大纲提到"李四"但没有角色卡 | 一致性检查 | 报告角色缺失 |
| F032 | 🟡 大纲中引用的设定未确认 | 引用 tentative 设定 | 一致性检查 | 标注风险 |
| F033 | 🟡 `outline.md` 与 `outline.yaml` 不一致 | 手动编辑了 .md 但没改 .yaml | 审查或 reindex | 检测到不一致 |
| F034 | 🟡 大纲的 `pacing_curve` 合理性 | 有节奏标记 | 审查 | 检查节奏曲线是否单调 |
| F035 | 🟢 plot_index.yaml 与章节场景对应 | 有场景大纲 | 检查 `plot_index.yaml` | 条目与章节场景一一对应 |

---

## G. 章节生命周期（G001–G050）

### 创建章节

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| G001 | 🟢 创建第一章 | 已有项目和大纲 | `/chapter-create ch001 --goal "赵宋的日常生活"` | 生成 `chapters/ch001.md`；`index.yaml` 新增条目 |
| G002 | 🟢 创建后续章节 | 已有 ch001 | `/chapter-create ch002 --goal "灰域展开"` | ch002 创建成功，编号连续 |
| G003 | 🟡 创建时指定 POV | 无 | `/chapter-create ch001 --pov 赵宋 --goal "..."` | POV 字段正确设置 |
| G004 | 🟡 创建已存在的章节 | 已有 ch001 | `/chapter-create ch001 --goal "重新开始"` | 提示已存在，要求确认 |
| G005 | 🟡 跳号创建 | 只有 ch001 | `/chapter-create ch005 --goal "..."` | 允许跳号或提示 |
| G006 | 🟡 `index.yaml` 存在但 `.md` 不存在 | 只有索引无文件 | `/chapter-create ch001 --goal "..."` | 处理半存在状态 |
| G007 | 🟡 `.md` 存在但 `index.yaml` 无条目 | 只有文件无索引 | `/chapter-create ch001 --goal "..."` | 处理半存在状态 |
| G008 | 🟢 创建后检查文件结构 | 刚创建章节 | 读取 `chapters/ch001.md` | 包含正确的 header、`## 场景大纲`、`## 正文草稿`、`## 伏笔` 区域 |

### 写作/起草

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| G009 | 🟢 辅助生成初稿 | 章节已创建、有场景大纲 | `/chapter-draft ch001` | 在 `## 正文草稿` 区域生成初稿 |
| G010 | 🟡 指定写作风格 | 有风格模板 | `/chapter-draft ch001 --style 硬汉派` | 按指定风格生成 |
| G011 | 🟡 指定聚焦方向 | 无 | `/chapter-draft ch001 --focus "对话为主"` | 侧重对话 |
| G012 | 🟡 深度 POV | 无 | `/chapter-draft ch001 --pov-deep` | 深度沉浸视角 |
| G013 | 🟡 生成备选版本 | 已有一版草稿 | `/chapter-draft ch001 --alt` | 生成 `ch001_v2.md`，`index.yaml` 的 `versions` 更新 |
| G014 | 🟡 无场景大纲时起草 | 章节无 `## 场景大纲` 内容 | `/chapter-draft ch001` | 提示缺少大纲或自动参考 outline |
| G015 | 🟡 草稿生成时的容量控制 | 场景大纲内容很多 | 起草 | 不超出单章合理字数（scope guard），建议拆分 |
| G016 | 🟡 草稿引用前一章上下文 | ch002 的开头需要衔接 ch001 | `/chapter-draft ch002` | 读取 ch001 尾部作为上下文 |
| G017 | 🟡 草稿生成不篡改角色别称 | 草稿/大纲中用"老赵" | 查看生成结果 | 保持"老赵"不被替换为"赵宋" |
| G018 | 🔴 chapter-draft 时角色文件缺失 | 大纲引用了未创建的角色 | 起草 | 提示角色缺失或用有限信息生成 |

### 更新章节状态

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| G019 | 🟢 推进到 draft 状态 | 章节为 outline 状态 | `/chapter-update ch001 --status draft` | 状态更新；summary、characters_involved 生成 |
| G020 | 🟢 推进到 revise 状态 | 章节为 draft | `/chapter-update ch001 --status revise` | 状态更新 |
| G021 | 🟢 推进到 final 状态 | 章节为 revise | `/chapter-update ch001 --status final` | 状态更新 |
| G022 | 🟡 跳过状态（outline → final） | 无 | `/chapter-update ch001 --status final` | 禁止跳过或要求确认 |
| G023 | 🟡 回退状态（final → draft） | 已完稿 | `/chapter-update ch001 --status draft` | 应允许回退，但给出警告 |
| G024 | 🟡 更新已发布章节 | 状态为 published | `/chapter-update ch001 --title "新标题"` | published 章节有保护，需确认 |
| G025 | 🟢 更新标题 | 已有章节 | `/chapter-update ch001 --title "第一章 日常"` | 标题更新 |
| G026 | 🟡 更新字数统计 | 正文已写 | `/chapter-update ch001` | 自动计算字数 |
| G027 | 🟡 更新 POV | 写了一半决定换视角 | `/chapter-update ch001 --pov 王妮` | POV 更新 |
| G028 | 🟡 promote 版本 | 有 v1 和 v2 | `/chapter-update ch001 --promote v2` | v2 变为主版本 |
| G029 | 🟡 更新时生成 summary | 推进到 draft+ | 检查 `index.yaml` | summary 自动生成 |
| G030 | 🟡 更新时维护角色 `current_state` | 章节中角色有重大变化 | 推进状态后检查角色卡 | 角色 `current_state` 反映最新章节情况 |

### 章节审查

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| G031 | 🟢 审查结构和节奏 | 章节有正文 | `/chapter-review ch001` | 输出结构、节奏、开头吸引力、结尾悬念评估 |
| G032 | 🟡 带上下文审查 | 有前后章 | `/chapter-review ch003 --context` | 读取 ch002 尾部和 ch004 开头做衔接检查 |
| G033 | 🟡 审查发现钩子未回收 | 之前埋了钩子 | 审查结果 | 报告哪些钩子应在本章回收但未回收 |
| G034 | 🟡 审查发现正文偏离大纲 | 正文走了不同方向 | 审查结果 | 标记偏离但不自动修正（draft-primacy） |
| G035 | 🟡 审查空章节 | 章节只有 header 无正文 | `/chapter-review ch001` | 提示无内容可审查 |

### 章节对比

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| G036 | 🟢 对比同章两个版本 | ch001 有 v1 和 v2 | `/chapter-compare ch001` | 输出结构、风格、优劣势对比 |
| G037 | 🟡 对比所有版本 | 有 3 个版本 | `/chapter-compare ch001 --all` | 全部版本横向比较 |
| G038 | 🟡 无多版本时对比 | 只有一个版本 | `/chapter-compare ch001` | 提示只有一个版本 |

### 章节看板与导出

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| G039 | 🟢 查看章节看板 | 有多章不同状态 | `/chapter-board` | 按状态分类展示所有章节 |
| G040 | 🟡 筛选特定状态 | 有多章 | `/chapter-board --status draft` | 只显示 draft 状态的章节 |
| G041 | 🟢 导出章节 | 有多章已完稿 | `/chapter-export ch001-ch010 --format md` | 生成连续文档 |
| G042 | 🟡 只导出 final 状态 | 有混合状态章节 | `/chapter-export --status final` | 只包含 final 章节 |
| G043 | 🟡 导出时清理元数据 | 有 header 等 | `/chapter-export --clean` | 去除 YAML header、场景大纲等元数据 |

### 章节边界场景

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| G044 | 🟡 手动删除章节 `.md` 文件 | 有 ch001 | 用户在文件管理器中删除 `chapters/ch001.md` | `index.yaml` 仍有条目（orphan）；后续操作应检测到 |
| G045 | 🟡 删除后重新创建同编号章节 | 删除了 ch001 后 | `/chapter-create ch001 --goal "重新开始"` | 正确处理：只创建文件 or 提示索引已有条目 |
| G046 | 🟡 手动编辑章节 `.md`（不通过 skill） | 直接在编辑器中写正文 | 后续 `/chapter-update ch001` | 能识别手动写入的内容，正确更新字数 |
| G047 | 🟡 章节文件很大（5万字） | 大章节 | 各种操作 | 不超时或 crash |
| G048 | 🔴 `index.yaml` 格式损坏 | YAML 语法错误 | 尝试任何章节操作 | 明确报错，不静默失败 |
| G049 | 🟡 100+ 章节时的性能 | 大量章节 | `/chapter-board` | 合理时间内显示 |
| G050 | 🟡 章节目标 `--goal` 更新后 | 原 goal 是"觉醒"，改为"逃离" | `/chapter-update ch001 --goal "逃离灰域"` | goal 更新，不影响已有正文 |

---

## H. 伏笔/钩子系统（H001–H020）

### 埋设钩子

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| H001 | 🟢 埋设基础钩子 | 有章节 ch001 | `/hook-add "室友A的眼睛变色" --chapter ch001 --level B` | `outline.yaml` 的 `foreshadowing` 新增；`ch001.md` 的 `## 伏笔` 区域更新；`index.yaml` 的 `hooks_planted` 更新 |
| H002 | 🟡 设置回收截止 | 无 | `/hook-add "神秘声音" --chapter ch001 --deadline ch010` | 钩子带截止时间 |
| H003 | 🟡 设置回收条件 | 无 | `/hook-add "灰色石头" --chapter ch002 --condition "赵宋第二次进入灰域时"` | 钩子带回收条件 |
| H004 | 🟡 钩子分级 | 无 | `/hook-add "重大伏笔" --level S` | 级别正确设置（S/A/B/C） |
| H005 | 🟡 关联其他钩子 | 已有相关钩子 | `/hook-add "新钩子" --linked-hooks hook_001` | 钩子之间建立关联 |
| H006 | 🟡 为不存在的章节埋钩子 | 无 ch099 | `/hook-add "测试" --chapter ch099` | 报错或提示 |
| H007 | 🟡 同一章埋设多个钩子 | ch001 已有钩子 | 再埋一个 | 两个钩子共存 |

### 查询钩子

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| H008 | 🟢 查看所有钩子 | 有多个钩子 | `/hook-query` | 列出所有钩子及状态 |
| H009 | 🟡 筛选过期钩子 | 有钩子超过 deadline | `/hook-query --overdue` | 列出超期钩子 |
| H010 | 🟡 按级别筛选 | 有不同级别 | `/hook-query --level S` | 只显示 S 级 |
| H011 | 🟡 查看时间轴 | 有多钩子分布在不同章 | `/hook-query --timeline` | 按章节分布展示 |
| H012 | 🟡 查询被放弃的钩子 | 有 abandoned 钩子 | `/hook-query --status abandoned` | 显示已放弃的钩子 |

### 回收/处理钩子

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| H013 | 🟢 正常回收钩子 | 钩子 planted，当前章写到了回收点 | `/hook-resolve hook_001 --recover --chapter ch005` | 钩子状态变为 recovered；payoff 章节记录 |
| H014 | 🟡 放弃钩子 | 决定不回收某钩子 | `/hook-resolve hook_001 --abandon` | 标记 abandoned；重要钩子需确认 |
| H015 | 🟡 延期钩子 | 原本该回收但还没准备好 | `/hook-resolve hook_001 --extend --deadline ch015` | deadline 延长 |
| H016 | 🟡 回收不存在的钩子 | 无此 ID | `/hook-resolve nonexistent` | 明确报错 |
| H017 | 🟡 重复回收 | 钩子已 recovered | `/hook-resolve hook_001 --recover` | 提示已回收 |
| H018 | 🟡 放弃 S 级钩子 | S 级主线钩子 | `/hook-resolve hook_s --abandon` | 需要额外确认（主线伏笔影响大） |
| H019 | 🟡 回收时更新章节 | 回收钩子到 ch005 | 检查 ch005 | `hooks_revealed` 更新 |
| H020 | 🟡 查看钩子关联链 | 钩子之间有 linked_hooks | 查看某钩子详情 | 关联链正确展示 |

---

## I. 时间线（I001–I015）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| I001 | 🟢 添加事件 | 已有项目 | `/timeline-add "2024-03-15 赵宋宿舍自燃事件" --chapter ch001 --characters 赵宋,室友A` | `timeline/main.yaml` 新增事件 |
| I002 | 🟡 添加模糊时间事件 | 无精确日期 | `/timeline-add "融合初期 灰域首次出现" --chapter ch001` | 支持非精确时间标记 |
| I003 | 🟡 添加时间冲突的事件 | 已有事件 A 在某时间 | 添加时间上矛盾的事件 B | 添加成功但本地检查提示冲突 |
| I004 | 🟢 检查时间线一致性 | 有多事件 | `/timeline-check` | 检测时间矛盾、角色分身、设定冲突 |
| I005 | 🟡 角色同时出现在两地 | 时间线中角色位置矛盾 | 检查 | 报告角色分身问题 |
| I006 | 🟡 事件引用不存在的角色 | 事件标记了未创建的角色 | 检查 | 标记不存在的角色 |
| I007 | 🟢 查看时间线 | 有事件 | `/timeline-view` | 按时间顺序展示 |
| I008 | 🟡 多线程视图 | 有多条叙事线 | `/timeline-view --multi-thread` | 并行展示多线 |
| I009 | 🟡 筛选某角色的时间线 | 有事件 | `/timeline-view --character 赵宋` | 只显示赵宋相关事件 |
| I010 | 🟡 筛选时间范围 | 有事件 | `/timeline-view --range "2024-03~2024-06"` | 只显示范围内 |
| I011 | 🟡 事件与章节对应关系 | 有事件标记了 chapter | 查看 | 事件正确关联到章节 |
| I012 | 🔴 空时间线检查 | 无任何事件 | `/timeline-check` | 不报错，提示无事件 |
| I013 | 🟡 时间线与大纲的对应 | 大纲有时间标记 | 检查 | 时间线与大纲一致 |
| I014 | 🟡 添加事件到多个角色 | 群体事件 | `/timeline-add "灰域集体事件" --characters 赵宋,王妮,室友A,室友B` | 所有角色都关联到该事件 |
| I015 | 🟡 删除或修改事件 | 有事件 | 尝试修改 | 检查是否支持修改/删除 |

---

## J. 场景管理（J001–J008）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| J001 | 🟢 创建场景 | 已有项目 | `/scene-add 男生宿舍 --location "大学宿舍楼" --category 日常 --mood 轻松` | 生成 `scenes/{slug}.yaml` |
| J002 | 🟡 从章节提取场景 | 章节描写了某场景 | `/scene-add 灰域 --from chapters/ch001.md` | 从正文提取空间、氛围等信息 |
| J003 | 🟡 场景名称重复 | 已有"宿舍" | `/scene-add 宿舍 --location "另一个宿舍"` | 处理重复（加后缀或提示） |
| J004 | 🟡 场景的感官细节 | 创建场景时 | 检查生成的 YAML | 包含视觉、听觉、嗅觉等感官描述 |
| J005 | 🟡 场景与 `setting.md` 的关联 | 已有世界观设定 | 创建场景后 | 场景关联相关的世界观设定 |
| J006 | 🟡 场景在多章复用 | 宿舍场景出现在多章 | 查看场景信息 | 记录出现的章节列表 |
| J007 | 🟢 检查场景与 `tags.yaml` 对应 | 有场景 | 读取场景 YAML | 使用的标签在 `tags.yaml` 中定义 |
| J008 | 🟡 空参数创建场景 | 不提供任何额外参数 | `/scene-add 测试场景` | 创建最小化场景或提示补充 |

---

## K. 写作风格（K001–K012）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| K001 | 🟢 查看可用风格 | 有风格模板 | `/style-list` | 列出 `shared/styles/templates.yaml` 中的风格 |
| K002 | 🟢 手动创建风格 | 无 | `/style-create 硬汉写实 --features "短句,动作描写精准,少心理独白"` | 追加到 `templates.yaml` |
| K003 | 🟡 从已写章节提取风格 | 有多章已完稿 | `/style-create 我的风格 --from-chapters ch001-ch005` | 分析章节生成风格模板 |
| K004 | 🟡 创建同名风格 | 已有"硬汉写实" | `/style-create 硬汉写实` | 提示已存在 |
| K005 | 🟢 文风一致性审查 | 有多章 | `/style-audit ch001-ch010` | 检测风格漂移和质量波动 |
| K006 | 🟡 指定基线审查 | 有风格 | `/style-audit --baseline 硬汉写实` | 对比基线检查偏移 |
| K007 | 🟡 详细审查 | 有多章 | `/style-audit --detail` | 输出逐章详细分析 |
| K008 | 🟢 改写文本 | 有一段文字 | `/rewrite "原文..." --style 硬汉写实` | 按风格改写 |
| K009 | 🟡 改写强度控制 | 有文字 | `/rewrite --strength 3` | 最大强度改写 |
| K010 | 🟡 改写时对比 | 有文字 | `/rewrite --compare` | 输出改写前后对比 |
| K011 | 🟡 对文件进行改写 | 有章节 | `/rewrite --file chapters/ch001.md --style 简洁` | 改写文件内容（不直接写入） |
| K012 | 🟡 `templates.yaml` 为空 | 无风格模板 | `/style-list` | 提示无可用风格 |

---

## L. 质量与合规（L001–L020）

### AI 痕迹检测与改写

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| L001 | 🟢 检测章节 AI 痕迹 | 有章节正文 | `/anti-ai-check ch001` | 输出七维评分（套话/句式/比喻/描写/对白/转折/心理） |
| L002 | 🟡 自动推断章节 ID | 当前打开 ch003.md | `/anti-ai-check` | 自动识别为 ch003 |
| L003 | 🟡 检测结果写入报告 | 检测完成 | 查看 `quality/ai_trace_report.yaml` | 报告追加新记录 |
| L004 | 🟢 去 AI 感改写 | 检测到 AI 痕迹 | `/anti-ai-rewrite ch001` | 正文被改写，保留剧情信息 |
| L005 | 🟡 改写等级控制 | 有章节 | `/anti-ai-rewrite ch001 --level 1` | 轻度改写 |
| L006 | 🟡 改写等级 3（最大） | 有章节 | `/anti-ai-rewrite ch001 --level 3` | 深度改写 |
| L007 | 🟡 改写后正文字数变化 | 有字数统计 | 改写前后对比 | 字数可能变化，但不剧烈 |
| L008 | 🟡 改写不应破坏伏笔 | 正文中有埋设的伏笔 | 改写后检查 | 伏笔相关描写保留 |

### 人物声音检查

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| L009 | 🟢 检查角色对白一致性 | 有角色 `speech_pattern`、有章节 | `/voice-check 赵宋 ch001-ch005` | 检查对白是否符合角色声音 |
| L010 | 🟡 角色无 `speech_pattern` | 角色卡该字段为空 | `/voice-check 赵宋` | 提示缺少声音设定 |
| L011 | 🟡 多角色声音区分度 | 多角色在同章对话 | 检查 | 报告角色对白是否可区分 |

### 借鉴合规

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| L012 | 🟢 记录借鉴来源 | 写作参考了某作品 | `/inspiration-log ch001 "进击的巨人" --dimensions "围城意象,绝望氛围"` | `inspiration_log.yaml` 追加记录 |
| L013 | 🟢 检查借鉴风险 | 有借鉴记录 | `/inspiration-check ch001` | 生成风险评估，写入 `risk_report.yaml` |
| L014 | 🟡 无借鉴记录时检查 | 未记录任何借鉴 | `/inspiration-check ch001` | 提示无记录 |
| L015 | 🟢 生成合规报告 | 有日志和风险评估 | `/inspiration-report ch001-ch010` | 汇总报告 |
| L016 | 🟡 高风险借鉴 | 大段类似某作品 | 检查结果 | 标记高风险并给出降风险建议 |
| L017 | 🟡 素材库不存在时的借鉴检查 | 无 `../novel-material` | `/inspiration-check ch001` | 正常完成，跳过素材验证 |

### 一致性检查

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| L018 | 🟢 全面一致性检查 | 有角色、设定、章节、时间线 | `/consistency-check` | 跨模块检查，输出报告 |
| L019 | 🟡 检查发现角色设定矛盾 | 正文中角色行为与角色卡不符 | 检查结果 | 标记矛盾位置 |
| L020 | 🟡 检查发现时间线不一致 | 章节中提到的时间与 timeline 矛盾 | 检查结果 | 标记时间冲突 |

---

## M. Pipeline 编排（M001–M045）

### outline-bootstrap（大纲引导）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| M001 | 🟢 从草稿启动大纲引导 | 有用户草稿 | `/pipeline-outline-bootstrap drafts/故事构思.md` | 依次调用 draft-ingest → 用户确认 → 设定提取 → 大纲推导 |
| M002 | 🟡 从一句话启动 | 无草稿 | `/pipeline-outline-bootstrap "一个关于灵气复苏的故事"` | 从一句话开始引导 |
| M003 | 🟡 每个阶段都能中断 | 进行中 | 用户在某步说"等一下" | 暂停在当前阶段，不继续推进 |
| M004 | 🟡 已有大纲时触发 | 已有 outline | 再次 bootstrap | 提示已有大纲，确认是覆盖还是追加 |
| M005 | 🟡 素材中有矛盾 | 草稿内部有矛盾 | bootstrap 过程中 | 标出矛盾让用户决策，不自行选择 |

### outline-polish（大纲打磨）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| M006 | 🟢 打磨现有大纲 | 有大纲 | `/pipeline-outline-polish` | 调用 plot-review → worldbuilding-review → 建议 → 用户确认 → 修改 |
| M007 | 🟡 聚焦特定区域 | 有大纲 | `/pipeline-outline-polish --focus "第一季节奏"` | 只优化指定部分 |
| M008 | 🟡 打磨建议用户全部拒绝 | AI 给出建议 | 用户逐条拒绝 | 不修改任何内容 |
| M009 | 🟡 无大纲时打磨 | 未创建大纲 | `/pipeline-outline-polish` | 提示先创建大纲 |

### chapter-kickoff（章节启动）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| M010 | 🟢 启动新章节 | 有大纲 | `/pipeline-chapter-kickoff ch001 "赵宋的日常"` | 调用 chapter-create → chapter-update → plot-add（弧光） |
| M011 | 🟡 附带草稿文件启动 | 有用户手写的草稿 | `/pipeline-chapter-kickoff ch001@drafts/第一章.md` | 将草稿纳入章节 |
| M012 | 🟡 指定 POV | 无 | `/pipeline-chapter-kickoff ch001 "..." --pov 赵宋` | POV 正确传递 |
| M013 | 🟡 启动已存在的章节 | ch001 已创建 | `/pipeline-chapter-kickoff ch001` | 检测到已存在，提示而非覆盖 |
| M014 | 🟡 指定前置章节 | 有 ch001 | `/pipeline-chapter-kickoff ch002 --after ch001` | 衔接信息正确引用 |
| M015 | 🟡 大纲中无对应章节的内容 | 大纲未规划 ch005 | `/pipeline-chapter-kickoff ch005 "..."` | 正常创建，但标记大纲未覆盖 |
| M016 | 🟡 场景大纲内容过多（scope guard） | 用户给了5个场景 | kickoff 过程 | 提示内容超出单章容量，建议拆分 |
| M017 | 🔴 删除章节后重新 kickoff | 手动删除 ch001 文件和索引条目后 | `/pipeline-chapter-kickoff ch001` | 正确创建新的 ch001，不留残余状态 |
| M018 | 🔴 删除章节文件但索引条目还在 | 只删文件不删索引 | `/pipeline-chapter-kickoff ch001` | 检测到不一致状态，提示修复 |

### draft-polish（草稿打磨）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| M019 | 🟢 打磨章节草稿 | 有 draft 状态章节 | `/pipeline-draft-polish ch001` | 调用 chapter-review → voice-check → anti-ai-check → anti-ai-rewrite → chapter-update |
| M020 | 🟡 指定改写等级 | 有草稿 | `/pipeline-draft-polish ch001 --rewrite-level 2` | 按指定级别改写 |
| M021 | 🟡 打磨 outline 状态章节 | 章节还未写正文 | `/pipeline-draft-polish ch001` | 提示需先有草稿 |
| M022 | 🟡 打磨发现正文偏离大纲 | 正文与大纲不一致 | 打磨结果 | 报告偏离但不自动修改大纲或正文 |
| M023 | 🟡 打磨不应修改大纲 | 有偏离 | 打磨完成后 | 大纲文件未被修改 |

### setting-consolidate（设定整固）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| M024 | 🟢 整固世界观设定 | 有多条 tentative 设定 | `/pipeline-setting-consolidate` | 逐条审查、建议确认/修改/丢弃 |
| M025 | 🟡 聚焦某类设定 | 有多类设定 | `/pipeline-setting-consolidate --focus power_system` | 只处理力量体系 |
| M026 | 🟡 整固时发现依赖缺失 | 设定 A depends_on 未确认的 B | 整固过程 | 提示先处理依赖 |
| M027 | 🟡 所有设定已确认 | 无 tentative | 整固 | 提示无需整固 |

### note-triage（笔记分拣）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| M028 | 🟢 分拣混合笔记 | 有一份包含设定+角色+剧情的笔记 | `/pipeline-note-triage notes/脑暴.md` | 自动识别类型，分派到 setting-add、character-add、plot-add 等 |
| M029 | 🟡 dry-run 模式 | 有笔记 | `/pipeline-note-triage notes/脑暴.md --dry-run` | 只输出分拣结果，不实际创建 |
| M030 | 🟡 笔记内容模糊 | 笔记写的很随意 | 分拣 | 对模糊内容标记并询问用户 |
| M031 | 🟡 quick 模式 | 有笔记 | `/pipeline-note-triage notes/quick.md --quick` | 快速分拣，减少确认步骤 |
| M032 | 🟡 每条内容需确认 | 非 quick 模式 | 分拣过程 | 每条分拣结果都需用户确认后才落地 |

### continuity-gate（连续性检查）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| M033 | 🟢 阶段性连续性检查 | 有多章、角色、时间线 | `/pipeline-continuity-gate` | 汇总关系检查+时间线检查+一致性检查 |
| M034 | 🟡 指定范围检查 | 有多章 | `/pipeline-continuity-gate ch001-ch010` | 只检查指定范围 |
| M035 | 🟡 检查结果按优先级排序 | 有多个问题 | 查看结果 | 问题按严重性排序 |

### compliance-gate（合规闸口）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| M036 | 🟢 发布前合规检查 | 准备发布 ch001-ch005 | `/pipeline-compliance-gate ch001-ch005` | 串联 inspiration-check → inspiration-report |
| M037 | 🟡 无借鉴记录时 | 未做任何记录 | 合规检查 | 提示无借鉴记录 |

### Pipeline 通用行为

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| M038 | 🟡 Pipeline 中途用户中断 | 任何 pipeline 进行中 | 用户说"停" | 停在当前步骤，已完成的步骤不回滚 |
| M039 | 🟡 Pipeline 中某子 skill 报错 | 依赖的数据缺失 | pipeline 执行 | 报错并停止，不静默跳过 |
| M040 | 🟡 Pipeline 确认机制 | 任何需确认的 pipeline | 观察 | 每个写入步骤前都要求用户确认 |
| M041 | 🟡 Pipeline 完成后不自动触发下一个 | 完成 outline-bootstrap | 结束时 | 建议下一步但不自动执行 |
| M042 | 🟡 Pipeline 输出标准格式 | 任何 pipeline 完成 | 查看输出 | 包含 CurrentState、Risks、NextTasks、RecommendedCommands |
| M043 | 🟡 两个 pipeline 的衔接 | 先 outline-bootstrap 再 setting-consolidate | 按顺序执行 | 数据在两个 pipeline 间正确传递 |
| M044 | 🟡 重复执行 pipeline | 已执行过 | 再次执行同一 pipeline | 正确处理已有数据，不重复创建 |
| M045 | 🟡 pipeline 不自动调整大纲 | draft-polish 发现偏离 | 打磨完成 | 只报告偏离，大纲不被修改 |

---

## N. Backend API（N001–N035）

### 项目相关

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| N001 | 🟢 GET 项目列表 | 有项目 | `GET /api/projects` | 返回项目列表和元信息 |
| N002 | 🟢 GET 当前项目 | 有活跃项目 | `GET /api/projects/current` | 返回当前项目的 meta + state |
| N003 | 🟢 POST 切换项目 | 有多项目 | `POST /api/projects/switch {"name":"项目B"}` | `.current.yaml` 更新 |
| N004 | 🟡 切换到不存在的项目 | 无此项目 | `POST /api/projects/switch {"name":"ghost"}` | 返回 404 或合适错误码 |
| N005 | 🟡 无 `.projects.yaml` 时 GET 列表 | 文件不存在 | `GET /api/projects` | 尝试扫描 projects/ 或返回空列表 |

### 角色 API

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| N006 | 🟢 GET 角色列表 | 有角色 | `GET /api/characters` | 返回 `character_index.yaml` 数据 |
| N007 | 🟢 GET 单个角色 | 有角色"赵宋" | `GET /api/characters/赵宋` | 返回角色完整信息 |
| N008 | 🟢 POST 创建角色 | 有项目 | `POST /api/characters {"name":"新角色","role":"配角"}` | 创建文件和索引 |
| N009 | 🟡 POST 创建已存在角色 | 已有此角色 | 重复 POST | 返回 409 Conflict |
| N010 | 🟢 PUT 更新角色 | 有角色 | `PUT /api/characters/赵宋 {"traits":"新性格"}` | 更新角色文件 |
| N011 | 🟢 DELETE 角色 | 有角色 | `DELETE /api/characters/赵宋` | 删除文件和索引条目 |
| N012 | 🟡 DELETE 后关系文件残留 | 角色有关系记录 | DELETE 角色后检查 | 关系文件是否清理（API 层可能不处理） |
| N013 | 🟡 API 创建 vs Skill 创建差异 | 通过 API 创建的角色 | 检查角色文件 | API 可能不生成五件套提示/cross_references 等 skill 附加值 |

### 章节 API

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| N014 | 🟢 GET 章节列表 | 有章节 | `GET /api/chapters` | 返回 `index.yaml` 数据 |
| N015 | 🟢 GET 单个章节 | 有 ch001 | `GET /api/chapters/ch001` | 返回章节内容和元数据 |
| N016 | 🟢 POST 创建章节 | 有项目 | `POST /api/chapters {"id":"ch001","goal":"..."}` | 创建 `.md` 文件和索引条目 |
| N017 | 🟢 PUT 更新章节正文 | 有章节 | `PUT /api/chapters/ch001 {"body":"正文内容"}` | 正文更新 |
| N018 | 🟢 PUT 更新章节元数据 | 有章节 | `PUT /api/chapters/ch001/meta {"title":"新标题"}` | 元数据更新 |
| N019 | 🟢 DELETE 章节 | 有章节 | `DELETE /api/chapters/ch001` | 删除文件和索引条目 |
| N020 | 🟡 DELETE 后钩子引用残留 | 章节有钩子 | DELETE 后检查 outline.yaml | 钩子 plant_chapter 引用残留 |

### 世界观 API

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| N021 | 🟢 GET 世界观索引 | 有设定 | `GET /api/worldbuilding` | 返回 `worldbuilding.yaml` 数据 |
| N022 | 🟢 GET 单个设定 | 有设定 | `GET /api/worldbuilding/entries/power_001` | 返回设定详情 |
| N023 | 🟢 POST 创建设定 | 有项目 | `POST /api/worldbuilding/entries {"id":"rule_001","name":"新规则"}` | 创建条目文件和更新索引 |
| N024 | 🟡 POST 创建重复 ID | 已有此 ID | 重复 POST | 返回 409 |
| N025 | 🟢 PUT 更新设定 | 有设定 | `PUT /api/worldbuilding/entries/power_001 {"description":"..."}` | 更新条目 |
| N026 | 🟢 DELETE 设定 | 有设定 | `DELETE /api/worldbuilding/entries/power_001` | 删除条目文件和索引条目 |

### 其他 API

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| N027 | 🟢 GET 大纲 | 有大纲 | `GET /api/plot/outline` | 返回 `outline.md` 内容 + `outline.yaml` 结构 |
| N028 | 🟢 PUT 更新大纲 | 有大纲 | `PUT /api/plot/outline {"content":"..."}` | 更新 `outline.md` |
| N029 | 🟢 GET 时间线 | 有事件 | `GET /api/timeline` | 返回 `main.yaml` 数据 |
| N030 | 🟢 POST 添加时间线事件 | 有项目 | `POST /api/timeline {"time":"...","event":"..."}` | 追加到 `main.yaml` |
| N031 | 🟢 GET 关系 | 有关系 | `GET /api/relationships` | 返回 `relations.yaml` |
| N032 | 🟡 关系 API 只读 | 尝试写入 | `POST /api/relationships` | 无此端点或返回 405 |
| N033 | 🟢 GET 合规数据 | 有借鉴记录 | `GET /api/compliance/inspirations` | 返回 `inspiration_log.yaml` |
| N034 | 🟢 健康检查 | 服务运行 | `GET /api/health` | `{"status":"ok"}` |
| N035 | 🟡 CORS 限制 | 从非白名单域请求 | 非 localhost 域的请求 | CORS 拦截 |

---

## O. Skill 执行与 LLM（O001–O010）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| O001 | 🟢 GET Skill 列表 | 有 SKILL.md 文件 | `GET /api/skills` | 返回所有 skill 的 frontmatter 信息 |
| O002 | 🟡 SKILL.md 有复杂 YAML frontmatter | 某 skill 的 frontmatter 嵌套深 | GET 列表 | 正确解析或至少不崩溃 |
| O003 | 🟢 POST 执行 Skill | 选择一个 skill | `POST /api/skills/execute {"skill":"chapter-review","args":"ch001"}` | SSE 流式输出 LLM 结果 |
| O004 | 🟡 执行时附加上下文文件 | 指定额外文件 | `POST /api/skills/execute {"skill":"...","context_files":["characters/赵宋.yaml"]}` | 上下文文件内容传递给 LLM |
| O005 | 🟡 执行不存在的 Skill | 错误 skill 名 | `POST /api/skills/execute {"skill":"nonexistent"}` | 返回 404 |
| O006 | 🟢 LLM 对话 | 无 | `POST /api/llm/chat {"messages":[...]}` | SSE 流式返回 |
| O007 | 🟢 GET/PUT LLM 配置 | 无 | `GET /api/llm/config` 和 `PUT /api/llm/config` | 读写 `llm_config.json` |
| O008 | 🟡 LLM 配置无效 | 写入无效配置 | `PUT /api/llm/config {"model":"invalid"}` | 合理的错误处理 |
| O009 | 🟡 SSE 连接中断 | 流式输出中 | 客户端断开连接 | 服务端正常释放资源 |
| O010 | 🟡 并发执行多个 Skill | 同时触发多个 | 两个 `POST /api/skills/execute` 同时 | 不互相干扰 |

---

## P. 素材管理（P001–P015）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| P001 | 🟢 搜索素材 | 有 `../novel-material` | `/material-search "围城"` | 返回相关素材 |
| P002 | 🟡 素材库不存在 | 无 `../novel-material` | `/material-search "围城"` | 明确提示素材库未配置 |
| P003 | 🟢 关联素材到项目 | 有素材库 | `/material-manage link material_001` | `materials.yaml` 更新 |
| P004 | 🟡 取消关联 | 已关联且有 inspiration 引用 | `/material-manage unlink material_001` | 警告有引用存在 |
| P005 | 🟢 列出已关联素材 | 有关联 | `/material-manage list` | 显示已关联列表 |
| P006 | 🟢 查看可用素材 | 有素材库 | `/material-manage available` | 显示未关联的可用素材 |
| P007 | 🟢 应用素材到场景 | 有关联素材 | `/material-apply material_001 --mode scene --target ch001` | 素材信息融入章节 memo |
| P008 | 🟡 应用素材到大纲 | 有关联素材 | `/material-apply material_001 --mode outline` | outline.md 添加注释 |
| P009 | 🟡 应用素材到角色弧光 | 有关联素材 | `/material-apply material_001 --mode character --target 赵宋` | 角色 notes 追加 |
| P010 | 🟡 应用前需确认 | 任何应用 | 观察 | 写入前要求用户确认 |
| P011 | 🟡 应用后建议记录借鉴 | 应用完成 | 观察输出 | 提示执行 `/inspiration-log` |
| P012 | 🟡 关联不存在的素材 ID | 无此素材 | `/material-manage link nonexistent` | 报错 |
| P013 | 🟡 搜索无结果 | 有素材库但无匹配 | `/material-search "完全不相关的东西"` | 返回空结果提示 |
| P014 | 🟡 `materials.yaml` 不存在 | 手动删除 | `/material-manage list` | 提示文件缺失或自动重建 |
| P015 | 🟡 素材搜索脚本执行 | 有素材库 | 搜索时 | 正确调用 `python ../novel-material/scripts/search.py` |

---

## Q. 跨模块集成场景（Q001–Q030）

### 完整写作流程

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| Q001 | 🟢 新书完整流程 | 无 | init → ingest → bootstrap → consolidate → kickoff → draft → polish | 每步输出正确，数据一路传递 |
| Q002 | 🟡 跳过 ingest 直接 bootstrap | 无草稿 | init → bootstrap（从一句话） | 允许但信息较少 |
| Q003 | 🟡 跳过 consolidate 直接写 | 有 tentative 设定 | kickoff → draft | 提示有未确认设定 |
| Q004 | 🟡 写完不打磨直接发 | 有 draft | chapter-update → final | 允许跳过 polish |

### 草稿优先（Draft Primacy）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| Q005 | 🟡 正文与大纲冲突时 | 正文走了不同方向 | 运行 consistency-check | 报告冲突，标记双方差异，不自动修改任何一方 |
| Q006 | 🟡 正文与角色卡冲突时 | 正文中角色表现与设定不同 | consistency-check | 报告冲突，建议用户决定 |
| Q007 | 🟡 正文中出现新角色 | 正文写到了未注册的角色 | 检查 | 标记未注册角色 |
| Q008 | 🟡 正文中使用别称 | 用"老赵"而非"赵宋" | 任何处理 | 保留别称不替换 |
| Q009 | 🟡 写完后用户手动触发大纲同步 | 用户认为正文方向更好 | 用户主动修改大纲 | 大纲手动更新，不是自动的 |
| Q010 | 🟡 一致性检查不修改文件 | 检查出问题 | 检查完成 | 所有项目文件未被修改（只读操作） |

### 连锁修改场景

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| Q011 | 🟡 修改核心设定后 | 力量体系规则变了 | setting-edit → 影响扫描 | 报告哪些章节、角色受影响，不自动修改 |
| Q012 | 🟡 角色改名的连锁反应 | 改名后 | 检查所有引用 | index、relations、events、cross_references、chapters 全部更新 |
| Q013 | 🟡 删除设定后 | 废弃某设定 | 检查引用方 | 依赖此设定的条目收到通知 |
| Q014 | 🟡 新增关系后重建索引 | 添加了新关系 | `/project-reindex` | 角色的 `cross_references.related_characters` 更新 |
| Q015 | 🟡 时间线事件影响角色状态 | 重大事件发生 | 添加事件后 | 相关角色的 `current_state` 可能需要更新（手动触发） |

### AI 行为约束

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| Q016 | 🟡 AI 不擅自补充素材外内容 | 草稿只到"王妮救场，" | 任何推导 | 标记素材到此为止，后续为 AI 补充 |
| Q017 | 🟡 AI 不使用 AI 腔调 | 生成任何文本 | 检查输出 | 无"仿佛在诉说着…"、"不禁…"、"竟然…"等套话 |
| Q018 | 🟡 AI 起名自然 | 需要命名的场景 | 检查命名 | 无刻意高大上或生僻名字 |
| Q019 | 🟡 AI 不自动将全部剧情塞入单章 | 一个剧情跨 3 章 | chapter-draft | 只写当前章应有的内容 |
| Q020 | 🟡 AI 不主动调整大纲 | 写作过程中 | 检查 outline.md | 未经用户触发不修改大纲 |

### 数据完整性

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| Q021 | 🟡 `state.yaml` 精简性 | 运行多个操作后 | 检查 state.yaml | 只有不可推导的状态，无冗余数据 |
| Q022 | 🟡 `state.yaml` 的 `project.updated` | 每次写入操作后 | 检查 | 时间戳已更新 |
| Q023 | 🟡 YAML 格式一致性 | 多次编辑后 | 检查各 YAML 文件 | 格式规范，无损坏 |
| Q024 | 🟡 大文件操作原子性 | 写入过程中断 | 检查 | 文件不应处于半写入状态 |
| Q025 | 🟡 索引与实际文件一致 | 多次 CRUD 后 | `/novel-doctor` 或 `/project-reindex` | 一致性报告清洁 |

### 多项目场景

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| Q026 | 🟡 切换项目后操作 | 有项目 A 和 B | 切换到 B 后创建角色 | 角色创建在项目 B 中 |
| Q027 | 🟡 切换项目后规则同步 | 两个项目有不同约束 | 切换后检查 `.cursor/rules/` | 规则已更新为新项目的 |
| Q028 | 🟡 在错误项目中操作 | 用户忘了切换 | 在项目 A 中创建了属于 B 的角色 | 数据进入了 A（用户需自行注意） |
| Q029 | 🔴 两个项目同名角色 | A 和 B 都有"赵宋" | 切换项目后查询 | 显示当前项目的赵宋，不混淆 |
| Q030 | 🟡 删除当前项目后 | 手动删除项目文件夹 | 任何操作 | 明确报错当前项目不存在 |

---

## R. 协议行为验证（R001–R020）

### draft-primacy 协议

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| R001 | 🟡 chapter-draft 遵循 draft-primacy | 有大纲和草稿冲突 | 起草时 | 以草稿为准，标记偏离 |
| R002 | 🟡 pipeline-draft-polish 遵循 | 打磨时发现偏离 | 打磨过程 | 只报告不修复大纲 |
| R003 | 🟡 consistency-check 遵循 | 一致性检查时 | 检查结果 | 标记偏离方向是"正文→大纲"还是"大纲→正文"，不自动选择 |
| R004 | 🟡 chapter-review 遵循 | 审查时 | 审查结果 | flag drift，不 fix |
| R005 | 🟡 project-reindex 遵循 | 重建索引时 | reindex | 不从正文自动回写大纲 |

### chapter-scope-guard 协议

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| R006 | 🟡 chapter-draft 容量超限 | 场景大纲含 8 个场景 | 起草 | 提示超出单章容量，建议拆分 |
| R007 | 🟡 pipeline-chapter-kickoff 容量检查 | kickoff 时目标过多 | kickoff | 同上 |
| R008 | 🟡 用户坚持不拆分 | scope guard 触发后 | 用户说"不拆，就写这一章" | 尊重用户决定 |

### from-extraction 协议

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| R009 | 🟡 从 ingestion_brief 提取角色 | 有摘要 | `/character-add 赵宋 --from ingestion_brief.md` | 按 from-extraction 协议提取，保留源行标记 |
| R010 | 🟡 从 ingestion_brief 提取设定 | 有摘要 | `/setting-add --from ingestion_brief.md` | 同上 |
| R011 | 🟡 从章节提取关系 | 有章节 | `/relationship-add A B --from chapters/ch001.md` | 同上 |
| R012 | 🟡 提取边界标记 | 摘要中某信息只有一行 | 提取 | 正确标记边界 |

### post-edit-impact-scan 协议

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| R013 | 🟡 setting-edit 核心修改后扫描 | 修改 confirmed 设定 | 编辑后 | 自动扫描已写章节，输出影响报告 |
| R014 | 🟡 character-edit 核心修改后扫描 | 修改角色能力 | 编辑后 | 自动扫描，输出报告 |
| R015 | 🟡 setting-add confirmed 后扫描 | 新增 confirmed 设定 | 添加后 | 扫描已有章节 |
| R016 | 🟡 扫描只报告不修改 | 有影响 | 扫描结果 | 章节文件未被修改 |

### pipeline-delegation 协议

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| R017 | 🟡 pipeline 使用"调用"措辞 | 任何 pipeline | 观察 pipeline 输出 | 提到子 skill 时用"调用"而非模糊写法 |
| R018 | 🟡 pipeline 调用子 skill 的完整性 | 子 skill 有前置检查 | pipeline 中执行 | 子 skill 的前置检查仍然生效 |

### chapter-auto-inference 协议

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| R019 | 🟡 自动推断当前章节 | 打开了 ch003.md | `/chapter-review`（不带参数） | 自动识别为 ch003 |
| R020 | 🟡 无法推断时 | 未打开任何章节文件 | `/chapter-review`（不带参数） | 提示指定章节 ID |

---

## S. 前端集成（S001–S010）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| S001 | 🟢 前端启动 | 后端运行 | 访问前端页面 | 正常加载 |
| S002 | 🟢 前端显示章节列表 | 有章节 | 打开章节页面 | 正确显示所有章节 |
| S003 | 🟢 前端编辑章节 | 有章节 | 在编辑器中修改正文 | 保存后调用 PUT API |
| S004 | 🟢 前端显示角色列表 | 有角色 | 打开角色页面 | 正确显示 |
| S005 | 🟢 前端显示大纲 | 有大纲 | 打开大纲页面 | 正确显示 |
| S006 | 🟡 后端未启动 | 前端单独运行 | 访问前端 | 合理的错误提示 |
| S007 | 🟡 前端创建角色 | 有项目 | 通过前端表单创建 | 调用 POST API 成功 |
| S008 | 🟡 前端运行 Skill | 有 skill 列表 | 通过前端 skill runner | SSE 流式显示结果 |
| S009 | 🟡 前端 SSE 断开重连 | 流式输出中 | 网络短暂中断 | 优雅处理 |
| S010 | 🟡 前端与后端 CORS | 不同端口 | 前端 4173 → 后端 4273 | CORS 允许 |

---

## T. 边界与异常（T001–T015）

| ID | 场景 | 前置条件 | 操作步骤 | 预期结果 |
|----|------|----------|----------|----------|
| T001 | 🔴 YAML 文件手动编辑后格式错误 | 用户直接编辑 YAML 引入语法错误 | 触发依赖该文件的操作 | 明确报错，指向问题文件 |
| T002 | 🔴 `.md` 文件 header 格式损坏 | 章节文件 header 被弄乱 | `/chapter-update ch001` | 报错或尝试修复 |
| T003 | 🔴 极长内容（10万字章节） | 超大文件 | 各种操作 | 不崩溃，可能慢但不丢数据 |
| T004 | 🟡 Unicode 特殊字符 | 角色名/设定含 emoji 或特殊符号 | CRUD 操作 | 正确处理 |
| T005 | 🟡 空 YAML 数组 | `chapters: []` 或 `entries: []` | 依赖操作 | 正常处理空列表 |
| T006 | 🔴 磁盘空间不足 | 模拟 | 写入操作 | 合理的错误信息 |
| T007 | 🟡 路径含中文和特殊字符 | 项目名含问号、感叹号 | 所有文件操作 | 路径正确处理 |
| T008 | 🟡 并发写入同一文件 | 两个操作同时写 `index.yaml` | 观察 | 不丢数据（或至少有一方报错） |
| T009 | 🟡 文件权限问题 | 某文件只读 | 写入操作 | 明确报错 |
| T010 | 🟡 `.novel/` 目录缺失 | 手动删除 | 操作 | 报错而非创建在错误位置 |
| T011 | 🟡 `templates/project/` 被修改 | 模板文件被改 | `/novel-init` | 使用修改后的模板（正确行为 or 有校验？） |
| T012 | 🟡 超深嵌套 YAML | 非常复杂的 YAML 结构 | 读写 | 正常处理 |
| T013 | 🟡 空字符串字段 | `name: ""` 等 | 依赖操作 | 视为未填写 |
| T014 | 🟡 相对路径与绝对路径 | 不同方式引用文件 | `/draft-ingest ./drafts/a.md` vs 绝对路径 | 都能正确定位 |
| T015 | 🟡 `shared/styles/` 文件缺失 | 删除 anti_ai_rules.yaml | `/anti-ai-check` | 报错或使用默认规则 |

---

## 统计

| 分类 | 数量 |
|------|------|
| A. 项目生命周期 | 30 |
| B. 素材消化 | 15 |
| C. 角色管理 | 35 |
| D. 角色关系 | 22 |
| E. 世界观与设定 | 30 |
| F. 剧情大纲 | 35 |
| G. 章节生命周期 | 50 |
| H. 伏笔/钩子系统 | 20 |
| I. 时间线 | 15 |
| J. 场景管理 | 8 |
| K. 写作风格 | 12 |
| L. 质量与合规 | 20 |
| M. Pipeline 编排 | 45 |
| N. Backend API | 35 |
| O. Skill 执行与 LLM | 10 |
| P. 素材管理 | 15 |
| Q. 跨模块集成 | 30 |
| R. 协议行为验证 | 20 |
| S. 前端集成 | 10 |
| T. 边界与异常 | 15 |
| **合计** | **442** |

> 注：实际设计了 442 例以确保覆盖度。若需精简到 300 例，建议优先保留 🟢 和 🟡 标记的用例，按实际使用频率削减 🔴 和重复度高的边界场景。
