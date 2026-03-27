# 开发进度日志

> 记录语言须简练概括，每次写入须同步更新「开发计划」与「文件结构」两个模块。

---

## 📋 开发计划

> 每条任务后标注当前状态：`未完成` / `处理中` / `已完成`

### 阶段一：项目骨架与基础设施
- [x] 1.1 初始化后端 FastAPI 项目 — `已完成`
- [x] 1.2 初始化前端 Vue 3 项目 — `已完成`
- [x] 1.3 数据库建模（users, conversations, messages, documents） — `已完成`
- [x] 1.4 用户认证 API（注册/登录/JWT） — `已完成`
- [x] 1.5 前端登录/注册页面 — `已完成`
- [x] 1.6 前端主布局骨架 — `已完成`
- [x] 1.7 前后端联调验证 — `已完成`

### 阶段二：核心聊天 + 通用教育 Agent
- [x] 2.1 后端 WebSocket 聊天接口 — `已完成`
- [x] 2.2 配置硅基流动 LLM — `已完成`
- [x] 2.3 Agent 基类 + 自定义 Callback — `已完成`
- [x] 2.4 通用教育 Agent + 4 个工具 — `已完成`
- [x] 2.5 联网搜索工具（SerpAPI） — `已完成`
- [x] 2.6 对话历史 CRUD API — `已完成`
- [x] 2.7 前端聊天组件 — `已完成`
- [x] 2.8 前端 Agent 步骤展示 — `已完成`
- [x] 2.9 前端对话管理 + 模式切换 — `已完成`
- [x] 2.10 Markdown 渲染 — `已完成`

### 阶段三：RAG 知识库
- [x] 3.1 配置 ChromaDB + Embedding — `已完成`
- [x] 3.2 文档处理流程 — `已完成`
- [x] 3.3 文档管理 API — `已完成`
- [x] 3.4 RAG 检索工具接入 Agent — `已完成`
- [x] 3.5 前端文件上传组件 — `已完成`
- [x] 3.6 端到端 RAG 测试 — `已完成`

### 阶段四：CS 保研信息助手
- [x] 4.1 整理 CS 保研预置数据 — `已完成`
- [x] 4.2 数据初始化脚本 — `已完成`
- [x] 4.3 保研 Agent + 3 个工具 — `已完成`
- [x] 4.4 后端 Agent 路由（mode 切换） — `已完成`
- [x] 4.5 测试保研问答场景 — `已完成`

### 阶段五：用户中心 + 打磨
- [x] 5.1 用户中心页面 — `已完成`
- [x] 5.2 用户画像注入 Agent prompt — `已完成`
- [x] 5.3 UI 打磨 — `已完成`
- [x] 5.4 项目文档更新 — `已完成`


### 阶段六：Bug 修复 + 功能增强 + 上线
- [x] 6.1 修复 WebSocket 双重回答 bug — `已完成`
- [x] 6.2 修复界面未占满浏览器 / 输入框位置异常 — `已完成`
- [x] 6.3 预设问题卡片功能 — `已完成`
- [x] 6.4 撰写 README 团队启动文档 — `已完成`
- [x] 6.5 推送项目到 GitHub — `已完成`

### 阶段七：Bug 修复 + 用户体验增强
- [x] 7.1 修复切换账号后"对话不存在" bug — `已完成`
- [x] 7.2 修复 langchain/chromadb 依赖版本冲突 — `已完成`
- [x] 7.3 预设卡片常驻（输入框上方两行迷你网格） — `已完成`
- [x] 7.4 消息操作栏（复制/朗读/重新回答） — `已完成`
- [x] 7.5 导出功能（Markdown + PDF） — `已完成`
- [x] 7.6 答题交互组件初版（内嵌表单，存在解析 bug） — `已完成`

### 阶段八：答题系统重构与 Agent 工具调用修复
- [x] 8.1 答题弹窗模式（替换内嵌表单） — `已完成`
- [x] 8.2 修复题目数据源（用工具 output 替代完整 AI 回复） — `已完成`
- [x] 8.3 修复 agent_steps 500 字符截断问题 — `已完成`
- [x] 8.4 修复多次 generate_quiz 调用时只取第一次输出的问题 — `已完成`
- [x] 8.5 重写解析器（两层分割：段落→题号，兼容 Markdown/emoji） — `已完成`
- [x] 8.6 增加内容兜底检测（Agent 未调用工具时也能识别出题消息） — `已完成`
- [x] 8.7 约束出题：统一只生成选择题，每题立即附答案和解析 — `已完成`
- [x] 8.8 edu_agent 强制工具调用规则（出题/总结/知识点/学习计划均必须调工具） — `已完成`

### 阶段九：功能精进
- [x] 9.1 重构登录/注册页面 UI — `已完成`
- [x] 9.2 工具 LLM 性能优化（122B → 397B）— `已完成`
- [x] 9.3 修复 WebSocketCallbackHandler `on_chat_model_start` 报错 — `已完成`

### 阶段十：API 迁移 + Bug 修复
- [x] 10.1 LLM 从硅基流动迁移至 DeepSeek API — `已完成`
- [x] 10.2 修复保研知识库初始化报错（Embedding 保留硅基流动）— `已完成`
- [x] 10.3 修复文档删除功能无效（DELETE 请求被 n-upload 事件捕获）— `已完成`

### 阶段十一：Cloudflare 隧道部署 + 功能微调
- [x] 11.1 FastAPI 托管前端静态文件（构建后单端口访问）— `已完成`
- [x] 11.2 Cloudflare 临时隧道公网暴露本地服务 — `已完成`
- [x] 11.3 精简学习计划工具输出（300字以内）— `已完成`
- [x] 11.4 edu_agent 补充输出规则（禁止二次压缩工具结果）— `已完成`
- [x] 11.5 修复保研 Agent 工具反复调用（补充查询策略 + max_iterations 调整为 10）— `已完成`

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
│   ├── agents/           (llm.py, base_agent.py, edu_agent.py, callbacks.py)
│   │   └── tools/        (summarize, quiz_generator, knowledge_extractor, study_plan, web_search, knowledge_search)
│   ├── rag/              (embeddings.py, vector_store.py, document_loader.py, retriever.py)
│   ├── knowledge_data/admission/ (schools.json, timeline.json, experience_tips.md, init_admission_kb.py)
│   └── uploads/
└── frontend/
    └── src/
        ├── api/          (index.ts, auth.ts, conversation.ts, knowledge.ts)
        ├── stores/       (auth.ts, conversation.ts)
        ├── router/       (index.ts)
        ├── views/        (LoginView, RegisterView, ChatView, UserProfileView)
        ├── components/chat/      (ChatWindow, MessageBubble, MessageInput, AgentSteps, QuizInteractive)
        ├── components/knowledge/ (FileUpload)
        ├── composables/  (useWebSocket.ts)
        └── types/        (index.ts)
```

---

## 📒 开发记录

<!-- 每次开发结束后，在此处新增一条记录，最新记录置顶 -->

---

### 🗓️ 第 14 次｜2026-03-27

#### 📝 功能点 / 修改点
阶段十一 11.5：修复保研 Agent 工具反复调用至上限

#### 📦 涉及文件 / 模块
`backend/agents/admission_agent.py`、`backend/agents/base_agent.py`

#### 🛠️ 实施内容摘要
- **根因**：`query_school_info` 每次返回 k=3 个片段不区分学校，比较多校时 LLM 反复调用同一工具试图补全信息，直到触发 `max_iterations` 上限（6次）停止并输出 "Agent stopped due to max iterations"
- **修复 1**：`admission_agent.py` system prompt 补充【查询策略】：比较多所学校时每所学校单独调用一次、同一学校不重复查询、收集完毕即汇总
- **修复 2**：`base_agent.py` 将 `max_iterations` 从 6 调整为 10，防止复杂任务误触上限

#### ⚠️ 遗留问题
- 无

---

### 🗓️ 第 13 次｜2026-03-27

#### 📝 功能点 / 修改点
阶段十一：Cloudflare 隧道部署 + 学习计划工具精简 + Agent 输出规则

#### 📦 涉及文件 / 模块
`backend/main.py`、`backend/agents/edu_agent.py`、`backend/agents/tools/study_plan.py`

#### 🛠️ 实施内容摘要
- **FastAPI 托管前端静态文件**：`main.py` 挂载 `frontend/dist/assets` 静态目录，并添加 SPA 兜底路由（`/{full_path:path}` → `index.html`），前后端合并为单端口（8000）访问
- **Cloudflare 临时隧道**：通过 `cloudflared tunnel --url http://localhost:8000` 将本地服务暴露为公网链接，无需服务器；`cloudflared` 通过 winget 安装
- **精简学习计划输出**：`study_plan.py` prompt 改为每天不超过 2 行、不展开细节、总字数 300 字以内，减少工具执行时间和 LLM 回复长度
- **Agent 输出规则**：`edu_agent.py` 补充【输出规则】，要求工具结果完整呈现，禁止二次压缩
- **性能分析（未修改）**：分析了复合任务慢的三个根因——ChromaDB + 硅基流动 Embedding 冷启动（5s）、AgentExecutor 串行工具调用、三工具各自独立 LLM 调用；结论为架构改动成本高，暂不优化

#### ⚠️ 遗留问题
- 无

---

### 🗓️ 第 12 次｜2026-03-27

#### 📝 功能点 / 修改点
阶段十 10.1-10.3：LLM 迁移至 DeepSeek + 两处 Bug 修复

#### 📦 涉及文件 / 模块
`backend/agents/llm.py`、`backend/config.py`、`backend/routers/knowledge.py`、`backend/.env`、`frontend/src/components/knowledge/FileUpload.vue`

#### 🛠️ 实施内容摘要
- **LLM 迁移至 DeepSeek**：硅基流动延迟高（25-90s/次）且波动大，切换至 DeepSeek API（deepseek-chat 即 DeepSeek-V3）；`llm.py` 改用 `DEEPSEEK_API_KEY/BASE_URL/MODEL`，旧硅基流动调用注释保留；`config.py` 新增 DeepSeek 三字段
- **Embedding 保留硅基流动**：DeepSeek 无 Embedding API，`BAAI/bge-m3` 仍由硅基流动提供；`SILICONFLOW_API_KEY` / `SILICONFLOW_BASE_URL` 保留，仅注释掉模型字段
- **修复保研知识库初始化报错**：`rag/embeddings.py` 引用 `settings.SILICONFLOW_API_KEY`，迁移时误将该字段注释导致 `AttributeError`；恢复两个 Embedding 相关字段后解决
- **修复文档删除无效 bug**：`FileUpload.vue` 中删除按钮缺少 `@click.stop`，点击事件冒泡至父级 `n-upload` 组件被捕获为文件选择，导致 DELETE 请求从未发出；加 `.stop` 修饰符后请求正常触发；同步加强后端 `delete_document` 鲁棒性（vector store 删除失败不阻断 DB 删除）

#### ⚠️ 遗留问题
- 无

---

### 🗓️ 第 11 次｜2026-03-26

#### 📝 功能点 / 修改点
阶段九 9.2-9.3：回复速度分析 + 工具 LLM 优化 + Callback 修复

#### 📦 涉及文件 / 模块
backend/（agents/tools/summarize.py, knowledge_extractor.py, quiz_generator.py, study_plan.py, agents/callbacks.py）

#### 🛠️ 实施内容摘要
- **性能基准测试**：编写 `benchmark.py` 逐层测量 LLM 原始延迟、工具耗时、完整 Agent 耗时；发现 122B（轻量模型）在硅基流动上实际比 397B **更慢**（extract_knowledge：134s vs 72s，study_plan：138s vs 87s），原因是 122B 在硅基流动排队更繁忙
- **工具 LLM 换回 397B**：将 summarize / extract_knowledge / generate_quiz / generate_study_plan 4 个工具的 `get_llm(lite=True)` 改为 `get_llm(lite=False)`，实测 extract_knowledge 提速 47%、study_plan 提速 37%；根本瓶颈为硅基流动服务端延迟（25-90s/次），代码层已无更大优化空间
- **修复 Callback 报错**：LangChain 新版要求 `AsyncCallbackHandler` 子类实现 `on_chat_model_start`，否则抛 `NotImplementedError`（不影响功能但有错误日志）；在 `WebSocketCallbackHandler` 中补充空实现

#### ⚠️ 遗留问题
- 硅基流动 API 延迟高且波动大（同一请求 25-90s 不等），计划下一阶段更换 API 服务商

---

### 🗓️ 第 10 次｜2026-03-26

#### 📝 功能点 / 修改点
阶段九 9.1：重构登录 / 注册页面 UI

#### 📦 涉及文件 / 模块
frontend/（views/LoginView.vue, views/RegisterView.vue）

#### 🛠️ 实施内容摘要
- **修复空白 bug**：将 `.login-page` / `.register-page` 的 `height: 100%`（依赖链式继承，在 Naive UI 包裹组件处断裂）改为 `min-height: 100vh`，确保全屏覆盖
- **整体重构为分栏布局**：参考 CareerCompass 设计，采用左 56% 插图区 + 右 44% 表单区的双栏全屏布局
- **左侧插图区**：深林绿渐变背景（`#0b3d2e → #1a7a5e`），内嵌纯 SVG 教育主题插图（登录页：戴学士帽猫头鹰 + 书堆；注册页：翻开的大书 + 铅笔），附浮动动画（书本漂浮、星星闪烁）
- **右侧表单区**：白底，"欢迎回来！" / "创建账号"大标题，自定义原生 `<input>` 字段（脱离 Naive UI 组件以实现精细样式控制），含密码显示/隐藏切换、实时校验、加载态动画
- **去除 Naive UI 表单组件依赖**：form/form-item/input 改为原生 HTML，仅保留 `useMessage` 用于 toast 通知
- **响应式适配**：768px 以下切换为垂直堆叠布局

---

### 🗓️ 第 9 次｜2026-03-26

#### 📝 功能点 / 修改点
阶段八全部完成：答题系统重构 + Agent 工具调用修复

#### 📦 涉及文件 / 模块
backend/（routers/chat.py, agents/edu_agent.py, agents/tools/quiz_generator.py）
frontend/（components/chat/QuizInteractive.vue, components/chat/MessageBubble.vue, components/chat/ChatWindow.vue）

#### 🛠️ 实施内容摘要
- **答题弹窗重构**：QuizInteractive.vue 改为 Teleport 居中弹窗，MessageBubble 改为"去答题"按钮触发；弹窗宽 640px、高 82vh 可滚动，支持点击遮罩关闭
- **修复题目数据源**：原实现把整条 AI 回复（含总结/知识点/题目）传给解析器，导致非题目内容被误识别；改为从 `agent_steps` 中取 `generate_quiz` 工具的 `output` 字段（纯题目文本）
- **修复 agent_steps 截断**：`chat.py` 中 `generate_quiz` 工具输出被硬截断为 500 字符，完整题目通常超 1000 字符；改为 `generate_quiz` 不截断，其余工具保留 5000 字符上限
- **修复多次调用合并**：用户要求"N道选择题+M道简答题"时 Agent 分两次调用 `generate_quiz`，原 `find` 只取第一次；改为 `filter` 收集全部并拼接
- **重写解析器**：改为两层分割策略——先按段落标题（选择题/简答题等，兼容 emoji 前缀、中文序号）分组，再在每组内按题号独立分割；解决简答题编号从 1 重置导致的题目混乱
- **内容兜底检测**：`hasQuizContent` 在 Agent 未调用工具时，通过检测消息内容中的选项行模式识别出题消息并触发答题按钮
- **约束出题格式**：`quiz_generator.py` 提示词要求每道题生成后立即附答案和解析（不先列完所有题目再统一给答案）；`edu_agent.py` 强制 `quiz_type="choice"`，不再支持其他题型
- **edu_agent 强制规则扩展**：出题/总结/知识点提取/学习计划四个场景全部强制调用对应工具，无论是否涉及上传文档

#### ✅ 目标 / 作用
彻底修复答题系统的数据链路（数据源→截断→解析→多调用合并），统一选择题模式，提供流畅的弹窗答题体验

---

### 🗓️ 第 8 次｜2026-03-25

#### 📝 功能点 / 修改点
阶段七全部完成：Bug 修复 + 用户体验增强（4 项新功能）

#### 📦 涉及文件 / 模块
frontend/（stores/conversation.ts, views/ChatView.vue, components/chat/ChatWindow.vue, components/chat/MessageBubble.vue, components/chat/QuizInteractive.vue）
backend/（requirements.txt）

#### 🛠️ 实施内容摘要
- **Bug 修复①（切换账号后"对话不存在"）**：根因是退出登录时 conversation store 未重置，旧用户的 `currentId` 残留导致新用户登录后请求旧对话。修复：conversation.ts 新增 `$reset()` 方法，ChatView 的 logout 调用 `conversationStore.$reset()`
- **Bug 修复②（依赖版本冲突）**：`langchain==0.3.14` 要求 `langsmith<0.3` 而 `langchain-core==0.3.83` 要求 `langsmith>=0.3.45`，导致队友无法安装。修复：升级 langchain/langchain-community 到 0.3.28，锁定全部关键包版本，`pip check` 验证零冲突
- **新功能①（预设卡片常驻）**：将预设卡片从空状态区移到输入框上方，改为 3×2 迷你按钮网格，对话过程中始终可见
- **新功能②（消息操作栏）**：AI 消息气泡下方添加操作按钮：复制（Clipboard API + 降级方案）、朗读（Web Speech API，zh-CN）、重新回答（重新发送最后一条用户消息）
- **新功能③（导出功能）**：支持 Markdown 文件下载 + PDF 导出（通过浏览器打印对话框），纯前端实现无需后端
- **新功能④（答题交互组件）**：新建 QuizInteractive.vue，解析 AI 出题内容自动识别选择题（A/B/C/D）、填空题（____）、简答题，渲染为可交互表单；用户提交后格式化答案发送给 AI 批改；通过检测 agent_steps 是否包含 `generate_quiz` 工具调用来触发

#### ✅ 目标 / 作用
修复核心交互 bug，大幅提升用户体验：预设卡片降低提问门槛，操作栏提供类 ChatGPT 交互，答题组件实现练习闭环，导出功能方便离线学习

---

### 🗓️ 第 7 次｜2026-03-24

#### 📝 功能点 / 修改点
阶段六全部完成：Bug 修复 + 预设问题卡片 + 项目上线

#### 📦 涉及文件 / 模块
frontend/（composables/useWebSocket.ts, components/chat/ChatWindow.vue, components/chat/MessageInput.vue, views/ChatView.vue）
根目录（README.md, .gitignore）

#### 🛠️ 实施内容摘要
- **Bug 修复①（双重回答）**：useWebSocket 新增 `resetStreamingState()`；ChatWindow 的 `watch(isDone)` 改为 async，await 历史消息加载完成后再清空流式状态，彻底避免历史消息与流式气泡同时显示
- **Bug 修复②（界面未占满浏览器）**：根因是 naive-ui 2.44 的 NConfigProvider 渲染了一个无高度的 `<div>`，导致 `height: 100%` 百分比链断裂；将 `ChatView.vue` 中 `.chat-page` 改为 `height: 100vh; overflow: hidden` 直接锚定视口，同时给 `.chat-window` 加 `flex: 1; overflow: hidden`、`.messages-area` 加 `min-height: 0`
- **新功能（预设问题卡片）**：MessageInput 通过 `defineExpose({ fill })` 暴露填入接口；ChatWindow 空状态重设计为欢迎语 + 副标题 + 3×2 卡片网格，教育/保研两套各 6 张卡片，点击直接填入输入框
- **README.md**：Windows 完整启动文档，含前置条件、4步快速启动、环境变量表格、常见问题7条
- **.gitignore**：补充排除 `.claude/`、`.playwright-mcp/`
- **GitHub 推送**：初始提交 85 个文件，推送至 https://github.com/chenguo6666/edu-assistant

#### ✅ 目标 / 作用
消除核心交互 bug，提升新用户引导体验（预设卡片降低冷启动门槛），项目正式上线到 GitHub 供团队协作

---

### 🗓️ 第 6 次｜2026-03-24

#### 📝 功能点 / 修改点
阶段五全部完成：用户中心 + UI 打磨

#### 📦 涉及文件 / 模块
frontend/（composables/useWebSocket.ts, components/chat/ChatWindow.vue, components/chat/AgentSteps.vue, views/ChatView.vue, views/UserProfileView.vue）

#### 🛠️ 实施内容摘要
- 修复 WebSocket done 信号：新增 isDone ref，done/error 事件后触发对话重载（替换原有 `oldVal===false` 的 bug）
- ChatWindow 重写：三点等待动画、表格/代码块 Markdown 样式、消息结束后自动重载历史、根据 mode 显示不同空状态提示
- ChatView 重写：对话列表按 Tab 过滤、模式徽章（学/研）、Tab 切换自动选中对应最近对话、顶部显示用户名
- UserProfileView 完善：年级下拉选择、感兴趣学科动态标签（NDynamicTags）
- AgentSteps：折叠时显示工具名预览、展开图标旋转动画、running 状态加 Spin 图标
- 用户画像注入（5.2）：base_agent._build_prompt 已实现，通过 chat.py _get_user_profile 传入

#### ✅ 目标 / 作用
修复核心流程 bug，完善用户体验细节，项目进入可交付状态

---

### 🗓️ 第 5 次｜2026-03-24

#### 📝 功能点 / 修改点
阶段四全部完成：CS 保研信息助手

#### 📦 涉及文件 / 模块
backend/（knowledge_data/admission/, agents/admission_agent.py, agents/tools/{school_info,admission_timeline,condition_match}.py）

#### 🛠️ 实施内容摘要
- 预置数据：12所高校CS保研信息（JSON）、预推免时间线（JSON）、经验帖（MD），共20条向量记录
- 启动自动初始化：main.py startup 事件触发知识库构建，已存在则跳过
- 保研 Agent：3个专用工具（院校查询/时间线/条件匹配）+ web_search，通过对话 mode 路由
- 验证：查询「浙大CS保研条件」时，Agent 正确调用 query_school_info + web_search，返回准确结果

#### ✅ 目标 / 作用
保研模式下用户可通过自然语言查询CS保研信息，Agent 结合本地知识库+联网搜索回答

---

### 🗓️ 第 4 次｜2026-03-24

#### 📝 功能点 / 修改点
阶段三全部完成：RAG 知识库

#### 📦 涉及文件 / 模块
backend/（rag/, agents/tools/knowledge_search.py, routers/knowledge.py）
frontend/（api/knowledge.ts, components/knowledge/FileUpload.vue, views/ChatView.vue）

#### 🛠️ 实施内容摘要
- 后端：硅基流动 BAAI/bge-m3 Embedding（1024维），ChromaDB 本地持久化，文档加载分块（PDF/TXT/MD/DOCX，chunk_size=800），知识库检索工具（按用户动态注入），文档上传/列表/删除 API
- 前端：knowledge.ts API 封装，FileUpload 组件（拖拽上传+文档列表），教育模式侧边栏集成
- 验证：上传 TXT 文档后 Agent 成功调用 search_knowledge_base 工具，检索到相关内容
- 依赖：新增 langchain-chroma==0.2.6，存在 langchain-core/langsmith 版本警告（不影响运行）

#### ✅ 目标 / 作用
用户可上传文档建立个人知识库，Agent 可基于文档内容回答问题

---

### 🗓️ 第 3 次｜2026-03-24

#### 📝 功能点 / 修改点
阶段二全部完成：WebSocket 聊天 + 通用教育 Agent

#### 📦 涉及文件 / 模块
backend/（routers/chat.py, agents/, agents/tools/）
frontend/（components/chat/, composables/useWebSocket.ts, views/ChatView.vue）

#### 🛠️ 实施内容摘要
- 后端：WebSocket 聊天路由，硅基流动 LLM 接入（OpenAI 兼容接口），Agent 基类 + AgentExecutor，自定义 AsyncCallbackHandler 流式推送，5 个工具（总结/出题/知识点提取/学习计划/联网搜索），对话标题自动生成
- 前端：useWebSocket composable，ChatWindow（流式渲染）、MessageBubble（Markdown）、MessageInput、AgentSteps（可折叠工具调用展示）
- 验证：WebSocket API 测试通过，Agent 成功调用 generate_study_plan 工具，流式 token 推送正常
- 踩坑记录：Vite 代理需在 `/api` 规则加 `ws:true`（不能单独配 `/ws`）；`taskkill node.exe` 会杀掉 Playwright MCP，应用端口精确杀；Clash 代理拦截 localhost，curl 测试需加 `--noproxy localhost`

#### ✅ 目标 / 作用
完成核心 Agent 对话能力，前端可实时展示工具调用过程

---

### 🗓️ 第 2 次｜2026-03-24

#### 📝 功能点 / 修改点
阶段一全部完成：前后端项目骨架搭建

#### 📦 涉及文件 / 模块
backend/（main.py, config.py, database.py, models/, schemas/, routers/, services/）
frontend/（App.vue, main.ts, api/, stores/, router/, views/, types/）

#### 🛠️ 实施内容摘要
- 后端：FastAPI 项目初始化，SQLite 4 张表建模，JWT 认证（注册/登录/me），对话 CRUD API，用户资料更新 API
- 前端：Vue 3 + Vite + TS + Naive UI 项目初始化，登录/注册页，聊天主页骨架（顶部 Tab + 左侧对话列表），用户中心页
- 联调验证：所有后端 API curl 测试通过，前端 TS 编译和 Vite 构建无错误
- 踩坑记录：bcrypt 5.0 与 passlib 不兼容（锁定 4.2.1）；requirements.txt 中文注释导致 GBK 解码失败；Node 18 需用 create-vite@5

#### ✅ 目标 / 作用
完成前后端基础设施，为阶段二的聊天和 Agent 功能提供可运行的框架

---

### 🗓️ 第 1 次｜2026-03-24

#### 📝 功能点 / 修改点
项目规划与文档编写

#### 📦 涉及文件 / 模块
CLAUDE.md、PRD.md、implementation-plan.md、progress.md

#### 🛠️ 实施内容摘要
完成项目需求讨论，确定技术选型（Vue 3 + FastAPI + LangChain + 硅基流动 Qwen3.5 + ChromaDB），编写四份项目文档。明确两大核心模块：通用教育助手和 CS 保研信息助手（作为主界面的功能模块通过顶部 Tab 切换），新增联网搜索工具（SerpAPI）。

#### ✅ 目标 / 作用
为正式开发建立完整的文档基准，明确需求、架构和开发计划。
