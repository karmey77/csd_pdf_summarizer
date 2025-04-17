"""
controllers/summarize_controller.py
控制 PDF 檔案上傳與摘要模式邏輯。
"""

import streamlit as st
from services.vector_service import RetrieverService
from services.llm_service import LLMService
from services.summarizer_service import SummarizerService
from views.summarize_view import SummarizeView
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

class SummarizeController:
    def __init__(self):
        self.view = SummarizeView()
        self.retriever_service = RetrieverService()
        self.llm = LLMService().llm
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            chat_memory=StreamlitChatMessageHistory(),
            return_messages=True,
        )

    def run(self):
        uploaded_files = self.view.upload_file_input()
        if not uploaded_files:
            return

        docs, splits, retriever = self.retriever_service.configure_with_docs(uploaded_files)

        if len(self.memory.chat_memory.messages) == 0 or st.sidebar.button("Clear message history"):
            self.memory.chat_memory.clear()
            self.memory.chat_memory.add_ai_message("以繁體中文對話。我可以怎麼幫你呢?")

        self.view.display_history(self.memory.chat_memory.messages)

        mode = self.view.select_summary_mode()
        summarize_button = self.view.display_summarize_button()

        if summarize_button:
            with self.view.create_response_container():
                response = SummarizerService(self.llm, splits).summarize(mode)
                self.memory.chat_memory.add_ai_message(response)
