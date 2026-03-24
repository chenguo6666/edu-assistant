# EduAssistant 教育助手

基于大语言模型的教育 AI Agent，支持通用学习辅助（总结/出题/知识点提取/学习计划）和 CS 保研信息查询，结合 RAG 个人知识库与联网搜索，提供实时流式对话体验。

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue 3 + Vite + TypeScript + Naive UI + Pinia |
| 后端 | FastAPI + LangChain + SQLite + ChromaDB |
| LLM | 硅基流动（SiliconFlow）Qwen3.5-397B |
| 搜索 | SerpAPI 联网搜索 |
| 通信 | WebSocket 流式推送 |

---

## 前置条件

在开始前，确保本机已安装：

- **Python 3.10+**（建议 3.11）：[下载](https://www.python.org/downloads/)，安装时勾选 "Add Python to PATH"
- **Node.js 18+**：[下载](https://nodejs.org/)
- **Git**：[下载](https://git-scm.com/)

需要准备的 API Key：

| Key | 用途 | 获取方式 |
|---|---|---|
| `SILICONFLOW_API_KEY` | LLM 调用（必填） | [硅基流动控制台](https://cloud.siliconflow.cn/) 注册后创建 |
| `SERPAPI_API_KEY` | 联网搜索（必填） | [SerpAPI](https://serpapi.com/) 注册，有免费额度 |

---

## 快速启动（Windows）

### 1. 克隆仓库

```cmd
git clone https://github.com/chenguo6666/edu-assistant.git
cd edu-assistant
```

### 2. 配置后端

**2.1 创建并激活虚拟环境**

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
```

激活成功后，命令行前缀会显示 `(venv)`。

**2.2 安装依赖**

```cmd
pip install -r requirements.txt
```

> 国内网络建议使用镜像加速：
> ```cmd
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

**2.3 配置环境变量**

将 `.env.example` 复制为 `.env`，然后填入你的 API Key：

```cmd
copy .env.example .env
```

用文本编辑器打开 `backend\.env`，修改以下两项（其余保持默认即可）：

```env
SILICONFLOW_API_KEY=你的硅基流动APIKey
SERPAPI_API_KEY=你的SerpAPIKey
```

**2.4 启动后端**

```cmd
uvicorn main:app --reload --port 8000
```

看到如下输出即表示启动成功：

```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

> 首次启动会自动初始化数据库和保研知识库，约需 10–30 秒，请等待 `startup complete` 出现。

### 3. 配置前端

**新开一个命令行窗口**（保持后端运行），执行：

```cmd
cd edu-assistant\frontend
npm install
npm run dev
```

看到如下输出即表示前端启动成功：

```
  VITE v5.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

### 4. 访问应用

打开浏览器访问 **http://localhost:5173**，注册账号后即可使用。

---

## 环境变量说明

位置：`backend/.env`（不提交到 Git，请勿泄露）

| 变量 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `SILICONFLOW_API_KEY` | ✅ | 无 | 硅基流动 API Key |
| `SILICONFLOW_BASE_URL` | 否 | `https://api.siliconflow.cn/v1` | API 地址 |
| `SILICONFLOW_MODEL` | 否 | `Qwen/Qwen3.5-397B-A17B` | 主力模型（function calling） |
| `SILICONFLOW_MODEL_LITE` | 否 | `Qwen/Qwen3.5-122B-A10B` | 备用模型 |
| `SERPAPI_API_KEY` | ✅ | 无 | SerpAPI 联网搜索 Key |
| `JWT_SECRET_KEY` | 否 | 内置默认值 | 生产环境请务必更换 |
| `DATABASE_URL` | 否 | `sqlite:///./edu_assistant.db` | 数据库路径 |

---

## 主要功能

### 教育助手模式
- 📝 **总结课文** — 提取核心知识点
- ❓ **生成练习题** — 自动出题并附答案解析
- 💡 **概念解释** — 简明易懂的知识讲解
- 📅 **学习计划** — 个性化学习安排
- 📁 **个人知识库** — 上传 PDF/TXT/MD/DOCX，AI 基于文档回答

### 保研助手模式
- 🏫 查询 12 所高校 CS 保研条件
- 📅 预推免时间线一览
- 📊 院校横向对比
- ✅ 个人条件自测匹配
- 🌐 结合联网搜索获取最新信息

---

## 项目结构

```
edu-assistant/
├── backend/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置读取
│   ├── database.py          # SQLite 初始化
│   ├── .env.example         # 环境变量模板
│   ├── requirements.txt     # Python 依赖
│   ├── models/              # 数据模型
│   ├── schemas/             # Pydantic Schema
│   ├── routers/             # API 路由
│   ├── agents/              # LangChain Agent + 工具
│   │   └── tools/           # 9 个 Agent 工具
│   ├── rag/                 # RAG 知识库（ChromaDB）
│   ├── knowledge_data/      # 保研预置数据
│   └── uploads/             # 用户上传文件
└── frontend/
    └── src/
        ├── views/           # 页面（登录/注册/聊天/用户中心）
        ├── components/      # 组件（聊天/知识库上传）
        ├── stores/          # Pinia 状态管理
        ├── api/             # HTTP/WS 接口封装
        └── composables/     # useWebSocket
```

---

## 常见问题

**Q: `pip install` 时报 SSL 错误或超时**
> 使用国内镜像：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

**Q: 后端启动报 `ModuleNotFoundError`**
> 确认虚拟环境已激活（命令行前缀显示 `(venv)`），再重新执行 `pip install -r requirements.txt`

**Q: 前端访问后登录/发消息没有响应**
> 检查后端是否正常运行（浏览器访问 http://localhost:8000/api/health 应返回 `{"status":"ok"}`）

**Q: Agent 回答不调用工具，只返回纯文本**
> 确认使用的是 397B 主力模型，小模型 function calling 能力较弱

**Q: 联网搜索不生效**
> 检查 `SERPAPI_API_KEY` 是否正确填写；SerpAPI 免费额度为每月 100 次搜索

**Q: `venv\Scripts\activate` 报错"无法加载文件，因为在此系统上禁止运行脚本"**
> 以管理员身份打开 PowerShell，执行：`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## API 文档

后端启动后访问 **http://localhost:8000/docs** 查看自动生成的 Swagger API 文档。
