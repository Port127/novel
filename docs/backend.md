# 后端技术文档

> FastAPI 后端 — 为小说工作台提供数据 API 和 LLM 代理服务。

---

## 1. 架构

```
backend/
├── main.py                 # FastAPI 应用入口
├── config.py               # 路径解析 + LLM 配置读写
├── requirements.txt        # Python 依赖
├── routers/                # 11 个 API 路由模块
│   ├── projects.py         # 项目列表 / 当前项目 / 切换
│   ├── characters.py       # 角色 CRUD + 索引同步
│   ├── worldbuilding.py    # 世界观 CRUD + 索引同步
│   ├── chapters.py         # 章节 CRUD + 正文读写
│   ├── plot.py             # 大纲 Markdown + YAML
│   ├── timeline.py         # 时间线事件
│   ├── relationships.py    # 关系图谱 + 演进事件
│   ├── compliance.py       # 借鉴登记 + 风险报告
│   ├── quality.py          # AI 痕迹报告
│   ├── llm.py              # LLM 配置 + SSE 流式对话
│   └── skills.py           # Skill 扫描 + 执行（SSE）
└── services/
    ├── yaml_service.py     # ruamel.yaml 读写（保留注释）
    └── llm_service.py      # httpx 流式调用 OpenAI 兼容 API
```

### 数据流

```
前端请求 → FastAPI Router → YAML/MD 文件 I/O → JSON 响应
前端请求 → FastAPI Router → LLM Service → SSE 流式响应
```

后端不使用数据库，所有数据来自项目目录下的 YAML 和 Markdown 文件。使用 `ruamel.yaml` 而非 PyYAML，以保留注释和缩进格式，确保人工编辑和 AI agent 直接操作文件时不会丢失信息。

---

## 2. 技术栈

| 依赖 | 版本 | 用途 |
|------|------|------|
| FastAPI | ≥0.115 | Web 框架，自动生成 OpenAPI 文档 |
| uvicorn | ≥0.30 | ASGI 服务器，支持热重载 |
| ruamel.yaml | ≥0.18 | YAML 读写，保留注释和格式 |
| httpx | ≥0.27 | 异步 HTTP 客户端，用于调用 LLM API |
| Pydantic | ≥2.0 | 请求体校验和序列化 |
| sse-starlette | ≥2.0 | Server-Sent Events 流式响应 |
| python-multipart | ≥0.0.9 | 表单解析 |

---

## 3. 核心模块

### 3.1 config.py — 配置中心

- `WORKSPACE_ROOT`：项目仓库根目录（`backend/` 的父目录）
- `get_current_project()`：读取 `.current.yaml`，返回当前项目名称和相对路径
- `get_project_root()`：返回当前项目的绝对路径
- `get_llm_config()` / `save_llm_config()`：读写 `backend/llm_config.json`

### 3.2 yaml_service.py — 文件读写

| 函数 | 说明 |
|------|------|
| `read_yaml(path)` | 读取 YAML 文件，文件不存在返回 `{}` |
| `write_yaml(path, data)` | 写入 YAML，自动创建父目录 |
| `read_markdown(path)` | 读取 Markdown，文件不存在返回 `""` |
| `write_markdown(path, content)` | 写入 Markdown，自动创建父目录 |

### 3.3 llm_service.py — LLM 流式调用

`chat_stream(messages)` 异步生成器：
1. 从 `llm_config.json` 读取配置
2. 构建 OpenAI 兼容的请求体（`stream: true`）
3. 通过 `httpx.AsyncClient.stream()` 发送请求
4. 逐行解析 SSE `data:` 行，提取 `choices[0].delta.content`
5. `yield` 文本片段，错误时 yield `[Error] ...` 消息

超时 120 秒，支持 OpenAI / DeepSeek / 其他兼容 API。

---

## 4. API 规格

所有端点以 `/api` 为前缀。

### 4.1 健康检查

```
GET /api/health → {status: "ok"}
```

### 4.2 项目管理 (`/api/projects`)

| 方法 | 路径 | 说明 | 响应 |
|------|------|------|------|
| GET | `/api/projects` | 列出所有项目 | `[{name, path, meta, state}]` |
| GET | `/api/projects/current` | 当前项目详情 | `{current, meta, state}` |
| POST | `/api/projects/switch` | 切换项目 | `{ok, current_project}` |

```json
// POST /api/projects/switch
{"project_name": "末世：我开了GM权限", "project_path": "projects/末世：我开了GM权限"}
```

项目发现逻辑：优先读取 `.projects.yaml`，如不存在则扫描 `projects/` 目录下含 `.novel/` 的子目录。

### 4.3 角色 (`/api/characters`)

| 方法 | 路径 | 说明 | 响应 |
|------|------|------|------|
| GET | ` ` | 角色索引 | `{entries: [{name, role, archetype, ...}], total}` |
| GET | `/{name}` | 角色完整 YAML | Character 对象 |
| POST | ` ` | 创建角色 | `{ok, name}` |
| PUT | `/{name}` | 更新角色 | `{ok, name}` |
| DELETE | `/{name}` | 删除角色 | `{ok, name}` |

```json
// POST 创建
{"name": "陈默", "role": "protagonist", "archetype": "反英雄", "data": {"fatal_flaw": "..."}}

// PUT 更新 — data 字段 merge 到已有 YAML
{"role": "protagonist", "data": {"appearance": {"height": "178cm"}}}
```

文件映射：`characters/character_index.yaml`（索引）+ `characters/{name}.yaml`（详情）

### 4.4 世界观 (`/api/worldbuilding`)

| 方法 | 路径 | 说明 | 响应 |
|------|------|------|------|
| GET | ` ` | 世界观索引 | WorldbuildingIndex |
| GET | `/entries/{id}` | 设定详情 | Setting |
| POST | `/entries` | 创建条目 | `{ok, id}` |
| PUT | `/entries/{id}` | 更新条目 | `{ok, id}` |
| DELETE | `/entries/{id}` | 删除条目 | `{ok, id}` |

```json
// POST 创建
{"id": "rule_灰盒调试器", "name": "灰盒调试器", "category": "world_rule", "status": "confirmed", "data": {...}}
```

文件映射：`worldbuilding/worldbuilding.yaml`（索引）+ `worldbuilding/entries/{id}.yaml`（详情）

### 4.5 章节 (`/api/chapters`)

| 方法 | 路径 | 说明 | 响应 |
|------|------|------|------|
| GET | ` ` | 章节索引 | `{chapters: ChapterMeta[]}` |
| GET | `/{id}` | 元数据 + 正文 | `{meta, content}` |
| POST | ` ` | 创建章节 | `{ok, id}` |
| PUT | `/{id}` | 更新正文 | `{ok, id}` |
| PUT | `/{id}/meta` | 更新元数据 | `{ok, id}` |
| DELETE | `/{id}` | 删除章节 | `{ok, id}` |

```json
// POST 创建
{"id": "ch01", "title": "崩溃之夜", "pov": "陈默", "goal": "建立主角形象", "word_target": 3000, "content": "# 第一章..."}

// PUT 更新正文
{"content": "# 第一章\n\n凌晨两点..."}

// PUT 更新元数据
{"status": "draft", "summary": "...", "characters_involved": ["陈默", "苏婉"]}
```

文件映射：`chapters/index.yaml`（索引）+ `chapters/{id}.md`（正文）

### 4.6 大纲 (`/api/plot`)

| 方法 | 路径 | 说明 | 响应 |
|------|------|------|------|
| GET | `/outline` | 读取大纲 | `{markdown, structured}` |
| PUT | `/outline` | 更新大纲 | `{ok}` |

同时读取 `plot/outline.md`（Markdown 全文）和 `plot/outline.yaml`（结构化数据）。写入仅更新 Markdown 部分。

### 4.7 时间线 (`/api/timeline`)

| 方法 | 路径 | 说明 | 响应 |
|------|------|------|------|
| GET | ` ` | 事件列表 | `{events, threads}` |
| POST | ` ` | 添加事件 | `{ok, count}` |

```json
// POST
{"time": "Day1 02:00", "event": "天空出现裂缝", "chapter": "ch01", "characters": ["陈默"]}
```

文件映射：`timeline/main.yaml`

### 4.8 关系 (`/api/relationships`)

| 方法 | 路径 | 说明 | 响应 |
|------|------|------|------|
| GET | ` ` | 关系图谱 | `{relations, total}` |
| GET | `/events` | 演进事件 | `{events}` |

只读接口。文件映射：`characters/relations.yaml` + `characters/relation_events.yaml`

### 4.9 合规 (`/api/compliance`)

| 方法 | 路径 | 说明 | 响应 |
|------|------|------|------|
| GET | `/inspirations` | 借鉴登记 | `{entries}` |
| GET | `/risks` | 风险报告 | `{entries}` |

文件映射：`compliance/inspiration_log.yaml` + `compliance/risk_report.yaml`

### 4.10 质量 (`/api/quality`)

| 方法 | 路径 | 说明 | 响应 |
|------|------|------|------|
| GET | `/ai-trace` | AI 痕迹报告 | `{reports}` |

文件映射：`quality/ai_trace_report.yaml`

### 4.11 LLM (`/api/llm`)

| 方法 | 路径 | 说明 | 响应 |
|------|------|------|------|
| GET | `/config` | 读取配置（key 脱敏） | LLMConfig |
| PUT | `/config` | 更新配置 | `{ok}` |
| POST | `/chat` | SSE 流式对话 | EventStream |

SSE 事件格式：

```
event: message
data: <文本片段>

event: done
data: [DONE]
```

配置存储在 `backend/llm_config.json`，不随项目切换。API Key 通过 GET 接口返回时自动脱敏。

### 4.12 技能 (`/api/skills`)

| 方法 | 路径 | 说明 | 响应 |
|------|------|------|------|
| GET | ` ` | 可用 Skill 列表 | `{skills: [{name, description, category}]}` |
| POST | `/execute` | 执行 Skill（SSE） | EventStream |

```json
// POST 执行
{"skill_name": "chapter-review", "arguments": "审查 ch01", "context_files": ["chapters/ch01.md"]}
```

Skill 执行流程：
1. 读取 `.claude/skills/{skill_name}/SKILL.md` 作为系统指令
2. 自动注入 `.novel/meta.yaml` + `.novel/state.yaml` 作为上下文
3. 可选加载 `context_files` 中的额外文件
4. 构建 system + user prompt 发送给 LLM
5. SSE 流式返回结果

Skill 分类由名称前缀自动推断（`chapter-` → chapters, `character-` → characters 等）。

---

## 5. 开发指南

### 5.1 环境要求

- Python ≥ 3.11
- pip

### 5.2 安装

```bash
pip install -r backend/requirements.txt
```

### 5.3 启动

```bash
# 必须从项目根目录（novel/）运行
python -m uvicorn backend.main:app --port 4273 --reload --reload-dir backend
```

> `--reload-dir backend` 限制只监视 Python 文件变更，避免前端文件改动导致后端重启。

### 5.4 访问

| 地址 | 说明 |
|------|------|
| http://localhost:4273/docs | Swagger UI（交互式 API 文档） |
| http://localhost:4273/redoc | ReDoc（API 文档阅读模式） |
| http://localhost:4273/api/health | 健康检查 |

### 5.5 添加新路由模块

1. 在 `backend/routers/` 新建 `xxx.py`
2. 定义 `router = APIRouter(prefix="/api/xxx", tags=["xxx"])`
3. 在 `backend/main.py` 中导入并 `app.include_router(xxx.router)`
4. 重启后自动出现在 Swagger 文档中

### 5.6 CORS 配置

`main.py` 中配置了允许的前端来源：

```python
allow_origins = [
    "http://localhost:4173",   # Vite dev server
    "http://127.0.0.1:4173",
    "http://localhost:3000",
]
```

生产部署时需更新为实际域名。

---

## 6. 设计决策

### 文件即数据库

所有 CRUD 操作直接读写 YAML/MD 文件。优点：
- 与 AI agent（Cursor / Claude）直接兼容——它们直接操作同一批文件
- 全量 git 版本管理
- 人类可用任何编辑器直接修改

### LLM 代理而非直连

前端不直接调用 LLM API，统一通过后端代理：
- API Key 不暴露给浏览器
- 后端可自动注入项目文件作为上下文
- Skill 执行需要读取本地文件，只有后端能做

### 索引 + 详情分离

角色、世界观、章节都采用"索引文件 + 独立详情文件"模式：
- 列表请求只读索引文件，响应快
- 详情请求按需读取单个文件
- 写入时双写索引和详情，保持一致性
