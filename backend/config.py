"""配置管理：从 .env 文件读取环境变量"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # 硅基流动（仅用于 Embedding，LLM 已切换至 DeepSeek）
    SILICONFLOW_API_KEY: str = os.getenv("SILICONFLOW_API_KEY", "")
    SILICONFLOW_BASE_URL: str = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
    # SILICONFLOW_MODEL: str = os.getenv("SILICONFLOW_MODEL", "Qwen/Qwen3.5-397B-A17B")
    # SILICONFLOW_MODEL_LITE: str = os.getenv("SILICONFLOW_MODEL_LITE", "Qwen/Qwen3.5-122B-A10B")

    # DeepSeek
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # SerpAPI
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")

    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "edu-assistant-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))

    # 数据库
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./edu_assistant.db")


settings = Settings()
