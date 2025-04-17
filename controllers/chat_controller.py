"""
controllers/chat_controller.py
負責聊天訊息流程與 LLM 回應控制。
"""

import streamlit as st
from services.llm_service import LLMService
from views.chat_view import ChatView
from models.chat_message import ChatMessage
from utils.logger import logger

class ChatController:
    """控制聊天訊息輸入、記憶、回覆流程"""

    def __init__(self):
        self.llm = LLMService()
        self.view = ChatView()

        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                ChatMessage(role="system", content="以繁體中文對話。我可以怎麼幫你呢?")
            ]

    def run(self):
        """主執行流程"""
        self.view.display_history(st.session_state["messages"])
        user_input = self.view.get_user_input()

        if user_input:
            st.session_state["messages"].append(ChatMessage(role="user", content=user_input))
            self.view.display_user_message(user_input)

            with self.view.create_response_container():
                response = self.llm.chat(st.session_state["messages"])
                st.session_state["messages"].append(ChatMessage(role="assistant", content=response))
