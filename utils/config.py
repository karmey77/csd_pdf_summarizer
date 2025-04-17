"""
utils/config.py
管理環境變數與應用設定。
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """集中管理應用設定"""

    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemma3:27b")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_API_BASE: str = os.getenv("LLM_API_BASE", "")

    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "")
    EMBEDDING_API_KEY: str = os.getenv("EMBEDDING_API_KEY", "")
    EMBEDDING_API_BASE: str = os.getenv("EMBEDDING_API_BASE", "")

settings = Settings()
