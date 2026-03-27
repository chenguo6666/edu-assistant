"""EduAssistant 后端应用入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import auth, user, conversation, chat, knowledge

app = FastAPI(title="EduAssistant API", version="0.1.0")

# CORS 配置（开发环境允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:5174", "http://127.0.0.1:5174",
        "http://localhost:5180", "http://127.0.0.1:5180",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(conversation.router)
app.include_router(chat.router)
app.include_router(knowledge.router)


@app.on_event("startup")
def on_startup():
    """应用启动时初始化数据库和保研知识库"""
    init_db()
    # 异步初始化保研知识库（不阻塞启动）
    try:
        import sys, os
        sys.path.insert(0, os.path.dirname(__file__))
        from knowledge_data.admission.init_admission_kb import init_admission_knowledge
        init_admission_knowledge()
    except Exception as e:
        print(f"保研知识库初始化失败（不影响其他功能）: {e}")


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
