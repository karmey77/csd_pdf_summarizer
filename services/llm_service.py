"""
services/llm_service.py
封裝與 LLM 的互動邏輯。
"""

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import ChatMessage as LangchainChatMessage
from langchain.callbacks.base import BaseCallbackHandler
import streamlit as st
from utils.config import settings
from utils.callbacks import StreamHandler
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class LLMService:
    """呼叫 LLM 並串流回應"""

    def __init__(self, provider: str = "local", streaming: bool = True):
        """
        provider: "local" or "gemini"
        """
        if provider == "gemini":
            self.llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.2,
                convert_system_message_to_human=True,
                disable_streaming=(not streaming)
            )
        else:
            self.llm = ChatOpenAI(
                model=settings.LLM_MODEL,
                temperature=0.1,
                openai_api_key=settings.LLM_API_KEY,
                openai_api_base=settings.LLM_API_BASE,
                streaming=streaming
            )

    def chat(self, messages: list[LangchainChatMessage]) -> str:
        """
        傳送聊天訊息給 LLM 並回傳回應文字（支援 streaming）。
        """
        stream_handler = StreamHandler(st.empty())
        response = ""

        # ✨ 根據不同 provider 將 messages 轉成標準格式
        parsed_messages = []
        for msg in messages:
            if msg.role == "user":
                parsed_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                parsed_messages.append(AIMessage(content=msg.content))
            elif msg.role == "system":
                parsed_messages.append(SystemMessage(content=msg.content))

        # 使用 stream 手動 token 累積
        for chunk in self.llm.stream(parsed_messages):
            token = chunk.content or ""
            response += token
            stream_handler.on_llm_new_token(token)

        return response
