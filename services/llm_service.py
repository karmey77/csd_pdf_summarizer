"""
services/llm_service.py
封裝與 LLM 的互動邏輯。
"""

from langchain_openai import ChatOpenAI
from langchain.schema import ChatMessage as LangchainChatMessage
from langchain.callbacks.base import BaseCallbackHandler
import streamlit as st
from utils.config import settings
from utils.callbacks import StreamHandler

class LLMService:
    """呼叫 LLM 並串流回應"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=0.1,
            openai_api_key=settings.LLM_API_KEY,
            openai_api_base=settings.LLM_API_BASE,
            streaming=True
        )

    def chat(self, messages: list[LangchainChatMessage]) -> str:
        """
        傳送聊天訊息給 LLM 並回傳回應文字（支援 streaming）。
        """
        stream_handler = StreamHandler(st.empty())
        response = ""

        # stream() 不支援 callbacks，只能手動串流處理
        for chunk in self.llm.stream(messages):
            token = chunk.content or ""
            response += token
            stream_handler.on_llm_new_token(token)

        return response
