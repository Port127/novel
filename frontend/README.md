# 小说工作台 — 前端

AI 小说写作系统的 Web 前端，基于 React + FastAPI。

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | React 18 + TypeScript + Vite |
| UI | TailwindCSS v4 + shadcn/ui |
| 状态 | Zustand |
| 路由 | React Router v7 |
| 图表 | Recharts |
| 后端 | Python FastAPI |
| YAML | ruamel.yaml (保留注释) |
| LLM | httpx + SSE streaming |

## 快速启动

```bash
# 1. 安装前端依赖
npm install

# 2. 安装后端依赖
pip install -r server/requirements.txt

# 3. 一键启动（前后端同时运行）
./start.sh

# 或者分别启动：
# 终端 1 - 后端
cd .. && python -m uvicorn server.main:app --reload --app-dir frontend --port 4273
# 终端 2 - 前端
npm run dev
```

打开 http://localhost:4173 即可使用。

## 配置 LLM

进入 **设置** 页面，填写：
- **API URL**: 第三方大模型的 API 地址（兼容 OpenAI 格式）
- **API Token**: 你的 API 密钥
- **模型名称**: 如 `gpt-4o`, `deepseek-chat`, `claude-3-opus` 等

## 页面概览

| 页面 | 功能 |
|---|---|
| 仪表板 | 项目 KPI、章节状态分布、最近更新 |
| 角色 | 角色卡片列表、详情五件套、关系、弧光 |
| 世界观 | 设定条目管理、分类筛选、状态追踪 |
| 大纲 | Markdown 大纲、伏笔追踪、紧张度曲线 |
| 章节 | Kanban 看板、Markdown 编辑器、字数统计 |
| 时间线 | 时间轴视图、事件管理 |
| 关系 | 关系图谱、强度可视化、事件日志 |
| 写作质量 | AI 痕迹七维雷达图、检测历史 |
| 合规检查 | 借鉴登记、风险报告 |
| 流水线 | 8 个预置 Pipeline 工作流 |
| AI 助手 | 通用对话 + 55 个 Skill 选择执行 |
| 设置 | LLM 配置、主题切换 |

## 目录结构

```
frontend/
├── src/                  # React 前端
│   ├── components/       # 共享组件 + shadcn/ui
│   ├── pages/            # 页面组件
│   ├── stores/           # Zustand 状态
│   ├── services/         # API 调用层
│   ├── hooks/            # 自定义 Hooks
│   ├── types/            # TypeScript 类型
│   └── layouts/          # 布局组件
├── server/               # Python FastAPI 后端
│   ├── main.py           # 入口
│   ├── config.py         # 配置
│   ├── routers/          # API 路由
│   └── services/         # 文件/LLM 服务
└── start.sh              # 一键启动脚本
```
