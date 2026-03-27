# 开发计划文档（Implementation Plan）

> 本文档为项目开发前的执行计划基准文档，与 PRD.md 配套使用。
> 开发过程中若发现计划需要调整或存在更优方案，须直接提出，经用户确认后方可修改。

---

## 一、项目概况

* **项目名称**：EduAssistant 教育助手 AI Agent
* **开发周期**：2026-03-24 ～ 无硬性截止
* **当前阶段**：文档规划完成，准备进入阶段一开发

---

## 二、技术架构概览

```
┌────────────────────────────────────────────────────────┐
│                    前端（Vue 3 + Naive UI）              │
│  LoginView / ChatView / UserProfileView                │
│  WebSocket 通信 ←→ Agent 步骤实时展示                    │
└───────────────────────┬────────────────────────────────┘
                        │ HTTP REST + WebSocket
┌───────────────────────▼────────────────────────────────┐
│                   后端（FastAPI）                        │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ 认证模块  │  │  对话管理模块  │  │   知识库管理模块  │  │
│  └──────────┘  └──────┬───────┘  └────────┬─────────┘  │
│                       │                   │             │
│  ┌────────────────────▼───────────────────▼──────────┐  │
│  │              LangChain Agent 层                    │  │
│  │  ┌──────────────┐     ┌──────────────────┐        │  │
│  │  │ 教育助手Agent │     │  保研信息Agent    │        │  │
│  │  │ - 文本总结    │     │  - 院校信息查询   │        │  │
│  │  │ - 习题生成    │     │  - 保研时间线     │        │  │
│  │  │ - 知识点提取  │     │  - 条件匹配推荐   │        │  │
│  │  │ - 学习计划    │     │                  │        │  │
│  │  │ - 联网搜索    │     │  - 联网搜索       │        │  │
│  │  │ - 知识库检索  │     │  - 知识库检索     │        │  │
│  │  └──────────────┘     └──────────────────┘        │  │
│  └───────────────────────────────────────────────────┘  │
│                       │                                 │
│  ┌────────────────────▼──────────────────────────────┐  │
│  │                  数据层                             │  │
│  │  SQLite（用户/对话/消息）  ChromaDB（向量知识库）     │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
   硅基流动 LLM    SerpAPI 搜索    硅基流动 Embedding
```

### 预期目录结构（粗粒度，开发中按需调整）

```
EduAssistant/
├── backend/                  # FastAPI 后端
│   ├── main.py               # 应用入口
│   ├── config.py             # 配置管理
│   ├── database.py           # 数据库初始化
│   ├── models/               # ORM 模型
│   ├── schemas/              # Pydantic 请求/响应模型
│   ├── routers/              # API 路由
│   ├── services/             # 业务逻辑
│   ├── agents/               # LangChain Agent + 工具定义
│   ├── rag/                  # RAG 知识库（文档处理、向量存储、检索）
│   ├── knowledge_data/       # 预置保研数据
│   └── uploads/              # 用户上传文件
│
└── frontend/                 # Vue 3 前端
    └── src/
        ├── api/              # API 请求封装
        ├── stores/           # Pinia 状态管理
        ├── router/           # 路由配置
        ├── views/            # 页面级组件
        ├── components/       # 可复用组件
        ├── composables/      # 组合式函数
        └── types/            # TypeScript 类型定义
```

---

## 三、开发阶段规划

### 阶段一：项目骨架与基础设施

* **目标**：前后端项目初始化，登录流程跑通
* **任务清单**：
  * [ ] 1.1 初始化后端 FastAPI 项目 
    * 创建目录结构、requirements.txt、.env.example
    * 配置 CORS、静态文件、日志
  * [ ] 1.2 初始化前端 Vue 3 项目 
    * Vite + TS 脚手架、安装 Naive UI / Pinia / Vue Router
    * 配置 Vite 代理（HTTP + WebSocket → 后端 8000 端口）
  * [ ] 1.3 数据库建模 
    * SQLAlchemy ORM 模型：users, conversations, messages, documents
    * 数据库初始化脚本（自动建表）
  * [ ] 1.4 用户认证 API 
    * POST `/api/auth/register`、POST `/api/auth/login`、GET `/api/auth/me`
    * JWT 生成与验证、密码 bcrypt 加密
  * [ ] 1.5 前端登录/注册页面 
    * LoginView.vue、RegisterView.vue
    * Pinia auth store、路由守卫
  * [ ] 1.6 前端主布局骨架 
    * AppLayout.vue（Header + Sidebar + 主内容区）
    * ChatView.vue 页面框架（空壳）
  * [ ] 1.7 前后端联调验证 
    * 注册 → 登录 → 跳转主界面 → 获取用户信息
* **交付物**：可登录的前后端骨架应用

---

### 阶段二：核心聊天 + 通用教育 Agent

* **目标**：聊天系统跑通，教育 Agent 可用，工具调用过程可视化
* **任务清单**：
  * [ ] 2.1 后端 WebSocket 聊天接口 
    * `ws://host/api/chat/ws/{conversation_id}?token=xxx`
    * 消息协议：thinking_start / step / tool_call / tool_result / token / done / error
  * [ ] 2.2 配置硅基流动 LLM 
    * 通过 `ChatOpenAI` 兼容接口接入
    * 验证 function calling 功能
  * [ ] 2.3 Agent 基类 + 自定义 Callback 
    * BaseAgent：封装 LLM、工具注册、prompt 模板、AgentExecutor
    * AsyncCallbackHandler：在 on_agent_action / on_tool_end / on_llm_new_token 时推送 WebSocket 消息
  * [ ] 2.4 通用教育 Agent + 工具 
    * edu_agent.py：System Prompt + 工具集
    * 工具实现：summarize、quiz_generator、knowledge_extractor、study_plan
    * 每个工具核心逻辑 = LLM 二次调用 + 格式化 prompt
  * [ ] 2.5 联网搜索工具 
    * 基于 SerpAPI 的 web_search 工具
    * 两个 Agent 共享使用
  * [ ] 2.6 对话历史 CRUD API 
    * GET/POST/DELETE `/api/conversations`
    * GET `/api/conversations/{id}`（含消息列表）
  * [ ] 2.7 前端聊天组件 `
    * ChatWindow.vue、MessageBubble.vue、MessageInput.vue
    * useWebSocket.ts composable
    * 流式文本逐字显示
  * [ ] 2.8 前端 Agent 步骤展示 
    * AgentSteps.vue（可折叠步骤列表）
    * ToolCallCard.vue（工具调用卡片：工具名、输入、状态、输出）
  * [ ] 2.9 前端对话管理 
    * ChatSidebar.vue（对话列表 + 新建对话）
    * 顶部 Tab 模式切换（教育助手 / 保研助手）
  * [ ] 2.10 Markdown 渲染 
    * MarkdownRenderer.vue（markdown-it + highlight.js）
* **交付物**：可与教育 Agent 对话、能看到工具调用过程的聊天应用

---

### 阶段三：RAG 知识库

* **目标**：文档上传和基于文档的问答功能可用
* **任务清单**：
  * [ ] 3.1 配置 ChromaDB + Embedding 
    * 硅基流动 Embedding 模型接入
    * ChromaDB 本地持久化（`backend/chroma_db/`）
  * [ ] 3.2 文档处理流程 
    * document_loader.py：支持 PDF / TXT / DOCX / MD
    * RecursiveCharacterTextSplitter(chunk_size=800, overlap=200)
    * 向量化写入 ChromaDB
  * [ ] 3.3 文档管理 API 
    * POST `/api/knowledge/upload`（上传并向量化）
    * GET `/api/knowledge/documents`（文档列表）
    * DELETE `/api/knowledge/documents/{id}`（删除文档及向量）
  * [ ] 3.4 RAG 检索工具接入 Agent 
    * search_knowledge_base 工具：检索用户上传的文档
    * similarity search top-4
  * [ ] 3.5 前端文件上传组件 
    * FileUpload.vue：上传按钮 + 已上传文档列表
  * [ ] 3.6 端到端 RAG 测试 
* **交付物**：用户可上传文档并基于文档内容提问

---

### 阶段四：CS 保研信息助手

* **目标**：保研模式完整可用
* **任务清单**：
  * [ ] 4.1 整理 CS 保研预置数据 
    * 10-15 所高校 CS 保研信息（JSON + Markdown 经验帖）
    * 数据结构：院校名、院系、项目类型、申请条件、时间线、联系方式
  * [ ] 4.2 数据初始化脚本 
    * 启动时自动加载预置数据到 `admission_knowledge` Collection
  * [ ] 4.3 保研 Agent + 工具 
    * admission_agent.py：System Prompt + 工具集
    * 工具：school_info（院校查询）、timeline（时间线）、condition_match（条件匹配）
    * 共享工具：web_search、search_knowledge_base
  * [ ] 4.4 后端 Agent 路由 
    * 根据对话 mode 字段路由到 edu_agent 或 admission_agent
  * [ ] 4.5 测试保研问答场景 
* **交付物**：可切换到保研模式并查询 CS 保研信息

---

### 阶段五：用户中心 + 打磨

* **目标**：功能完善，准备交付
* **任务清单**：
  * [ ] 5.1 用户中心页面 
    * UserProfileView.vue：编辑年级、专业、学科、GPA
    * PUT `/api/user/profile` API
  * [ ] 5.2 用户画像注入 Agent 
    * 将用户个人信息动态插入 Agent 的 system prompt
  * [ ] 5.3 UI 打磨 
    * 加载状态、错误提示、空状态处理
    * 对话标题自动生成
  * [ ] 5.4 项目文档更新 
    * 更新 PRD.md、progress.md、CLAUDE.md 中的文件结构
* **交付物**：完整可交付的课程项目

---

## 四、模块依赖关系

| 模块 | 依赖模块 | 备注 |
|-|-|-|
| 阶段一：项目骨架 | 无 | 优先开发 |
| 阶段二：聊天 + Agent | 阶段一 | 依赖认证和数据库 |
| 阶段三：RAG 知识库 | 阶段二 | 依赖 Agent 基础设施 |
| 阶段四：保研助手 | 阶段二、阶段三 | 依赖 Agent + RAG |
| 阶段五：打磨 | 阶段一~四 | 最后执行 |

---

## 五、关键风险与应对

| 风险描述 | 可能影响 | 应对方案 |
|-|-|-|
| 硅基流动 Qwen3.5 function calling 不稳定 | Agent 无法正确调用工具 | 降级到 ReAct prompt 解析模式，或换用其他模型 |
| WebSocket 长连接在 Agent 执行耗时较长时断开 | 前端收不到完整结果 | 增加心跳机制，设置合理超时 |
| ChromaDB Windows 兼容性问题 | RAG 功能不可用 | 备选方案：FAISS（纯 Python） |
| SerpAPI 免费额度耗尽 | 联网搜索不可用 | 做好降级处理，搜索失败时返回提示而非报错 |

---

## 六、变更记录

| 日期 | 修改内容 | 修改原因 |
|-|-|-|
| 2026-03-24 | 初始版本创建 | — |
