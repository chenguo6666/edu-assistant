"""EduAssistant 后端应用入口"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import init_db
from routers import auth, user, conversation, chat, knowledge

# 前端构建产物目录
FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

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


# 托管前端静态文件（须在所有 API 路由之后注册）
if os.path.isdir(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        """所有非 API 路由返回 index.html，支持前端 SPA 路由"""
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
