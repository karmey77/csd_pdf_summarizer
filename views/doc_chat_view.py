"""
views/doc_chat_view.py
封裝 PDF 檔案上傳與對話輸入 UI。
"""

import streamlit as st
from langchain.schema import BaseMessage

class DocChatView:
    def upload_file_input(self):
        return st.sidebar.file_uploader(
            label="Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True
        )

    def get_user_input(self):
        return st.chat_input("輸入你的問題")

    def display_user_message(self, message: str):
        st.chat_message("user").write(message)

    def display_chat_history(self, messages: list[BaseMessage]):
        avatars = {"human": "user", "ai": "assistant"}
        for msg in messages:
            st.chat_message(avatars.get(msg.type, "assistant")).write(msg.content)

    def create_response_container(self):
        return st.chat_message("assistant")
