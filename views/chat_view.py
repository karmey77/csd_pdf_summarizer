"""
views/chat_view.py
處理聊天視覺呈現。
"""

import streamlit as st
from models.chat_message import ChatMessage

class ChatView:
    """負責呈現聊天輸入與訊息內容"""

    def get_user_input(self) -> str:
        return st.chat_input("請輸入訊息：")

    def display_user_message(self, message: str):
        st.chat_message("user").write(message)

    def create_response_container(self):
        return st.chat_message("assistant")

    def display_history(self, messages: list[ChatMessage]):
        for msg in messages:
            st.chat_message(msg.role).write(msg.content)
