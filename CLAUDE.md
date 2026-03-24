# 项目：EduAssistant 教育助手 AI Agent

## 🔴 关键上下文（首先阅读）

* **操作系统**：Windows 11 / Git 2.49.0.windows.1
* **开发工具**：Cursor + Claude Code
* **网络代理**：Clash 规则模式，端口 7890
* **LLM 平台**：硅基流动（SiliconFlow），API 基地址 `https://api.siliconflow.cn/v1`
* **模型**：`Qwen/Qwen3.5-397B-A17B`（主力）/ `Qwen/Qwen3.5-122B-A10B`（备用）
* **前端**：Vue 3 + Vite + TypeScript + Naive UI + Pinia
* **后端**：FastAPI + LangChain + SQLite + ChromaDB

---

## ✅ 核心开发原则

1. **先读后写** — 编写任何代码前，先通读现有结构与逻辑，确保改动风格一致、可维护
2. **拆分复杂性** — 大型任务拆解为小步骤，逐步推进，避免一次性大改
3. **需求确认优先** — 每次交互先简明复述需求；信息不完整或存在多种实现路径时，先提问再动手
4. **保持简洁** — 代码简洁完整，去除冗余逻辑；所有注释统一使用**中文**
5. **路径统一** — 一律使用相对路径，禁止硬编码绝对路径

---

## 📁 当前文件结构

```
EduAssistant/
├── CLAUDE.md / PRD.md / implementation-plan.md / progress.md
├── backend/
│   ├── main.py, config.py, database.py
│   ├── models/          (user.py, conversation.py)
│   ├── schemas/          (user.py, conversation.py, chat.py)
│   ├── routers/          (auth.py, user.py, conversation.py, chat.py)
│   ├── services/         (auth_service.py)
│   ├── agents/           (llm.py, base_agent.py, edu_agent.py, admission_agent.py, callbacks.py)
│   │   └── tools/        (summarize, quiz_generator, knowledge_extractor, study_plan, web_search, knowledge_search, school_info, admission_timeline, condition_match)
│   ├── rag/              (embeddings.py, vector_store.py, document_loader.py, retriever.py)
│   ├── knowledge_data/admission/ (schools.json, timeline.json, experience_tips.md, init_admission_kb.py)
│   └── uploads/
└── frontend/
    └── src/
        ├── api/          (index.ts, auth.ts, conversation.ts, knowledge.ts)
        ├── stores/       (auth.ts, conversation.ts)
        ├── router/       (index.ts)
        ├── views/        (LoginView, RegisterView, ChatView, UserProfileView)
        ├── components/chat/      (ChatWindow, MessageBubble, MessageInput, AgentSteps)
        ├── components/knowledge/ (FileUpload)
        ├── composables/  (useWebSocket.ts)
        └── types/        (index.ts)
```

> 预期完整目录结构见 `implementation-plan.md` 第二节「技术架构概览」。

---

## 🖥️ 可用命令

```bash
# 后端
cd backend
pip install -r requirements.txt       # 安装依赖
uvicorn main:app --reload --port 8000 # 启动开发服务器

# 前端
cd frontend
npm install                           # 安装依赖
npm run dev                           # 启动开发服务器（默认 5173 端口）
npm run build                         # 构建生产版本
```

---

## ⚠️ 注意事项

> 如错误或问题反复出现时，在此处简要记录，避免重蹈覆辙。

* [ ] 硅基流动 API Key 仅放在 `backend/.env`，禁止提交到版本控制
* [ ] SerpAPI Key 同上，放在 `.env` 中
* [ ] 通义千问 function calling 需使用较大模型（397B），小模型可能不稳定
* [ ] Vite 代理需在 `/api` 规则上加 `ws: true`，WebSocket 才能走代理（不能单独配 `/ws`）
* [ ] **禁止用 `taskkill node.exe` 杀进程**——会连带杀掉 Playwright MCP Server；应用端口号精确杀（`netstat -ano | findstr :<port>` 找 PID 再 `taskkill //F //PID <PID>`）
* [ ] Clash 规则模式会拦截 localhost 请求，curl 测试本地服务需加 `--noproxy localhost`；浏览器直接访问不受影响

---

## 📄 开发文档说明

|文件|用途|写入时机|
|-|-|-|
|`progress.md`|开发过程日志，含计划完成情况、当前文件结构与每次开发记录|仅当用户明确指示时才写入|
|`PRD.md`|项目需求与设计文档（开发前制定）|开发过程中发现项目有设计问题时，须直接指出，用户确认后方可修改|
|`implementation-plan.md`|开发计划文档（开发前制定）|开发过程中发现计划需调整时，须直接指出，用户确认后方可修改|



