"""
controllers/doc_chat_controller.py
處理上傳 PDF 與語意查詢流程。
"""

import streamlit as st
from services.vector_service import RetrieverService
from services.llm_service import LLMService
from views.doc_chat_view import DocChatView
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import SystemMessagePromptTemplate
from langchain_core.prompts import PromptTemplate

class DocChatController:
    def __init__(self):
        self.view = DocChatView()
        self.retriever_service = RetrieverService()
        self.llm = LLMService()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            chat_memory=StreamlitChatMessageHistory(),
            return_messages=True,
        )

    def run(self):
        uploaded_files = self.view.upload_file_input()
        if not uploaded_files:
            return

        retriever = self.retriever_service.configure(uploaded_files)

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm.llm,
            retriever=retriever,
            memory=self.memory,
            response_if_no_docs_found="I don't know!",
        )

        # 自訂 System Prompt
        qa_chain.combine_docs_chain.llm_chain.prompt.messages[0] = SystemMessagePromptTemplate.from_template(
            "你是個熱情、專業的客服人員，用繁體中文回答。如果從資料得不到答案，請回答不知道。"
        )

        if len(self.memory.chat_memory.messages) == 0 or st.sidebar.button("Clear message history"):
            self.memory.chat_memory.clear()
            self.memory.chat_memory.add_ai_message("以繁體中文對話。我可以怎麼幫你呢?")

        self.view.display_chat_history(self.memory.chat_memory.messages)

        user_query = self.view.get_user_input()
        if user_query:
            self.view.display_user_message(user_query)

            with self.view.create_response_container():
                response = qa_chain.run(user_query)
                # response 會自動更新到 memory
