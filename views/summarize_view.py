"""
views/summarize_view.py
處理 PDF 上傳與摘要互動視覺介面。
"""

import streamlit as st
from langchain.schema import BaseMessage

class SummarizeView:
    def upload_file_input(self):
        return st.sidebar.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

    def select_summary_mode(self):
        return st.sidebar.selectbox("選擇摘要模式", options=["stuff_chain", "map_reduce", "refine"], index=0)

    def display_summarize_button(self):
        return st.sidebar.button("Summarize")

    def display_history(self, messages: list[BaseMessage]):
        avatars = {"human": "user", "ai": "assistant"}
        for msg in messages:
            st.chat_message(avatars.get(msg.type, "assistant")).write(msg.content)

    def create_response_container(self):
        return st.chat_message("assistant")
