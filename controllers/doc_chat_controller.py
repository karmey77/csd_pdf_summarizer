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
from langchain_core.messages import HumanMessage

class DocChatController:
    def __init__(self, provider: str = "local"):
        self.provider = provider
        self.llm = LLMService(provider=provider)
        self.view = DocChatView()
        self.retriever_service = RetrieverService()
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

        # 建立 QA Chain（OpenAI 使用 retriever chain，Gemini 用手動 prompt）
        if self.provider == "gemini":
            qa_chain = None
        else:
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm.llm,
                retriever=retriever,
                memory=self.memory,
                response_if_no_docs_found="I don't know!",
                verbose=False,
            )
            qa_chain.combine_docs_chain.llm_chain.prompt.messages[0] = SystemMessagePromptTemplate.from_template(
                "你是個熱情、專業的客服人員，用繁體中文回答。如果從資料得不到答案，請回答不知道。"
            )

        # ✅ 只在首次載入時初始化對話，避免每次 run() 都重置
        if "docchat_initialized" not in st.session_state:
            self.memory.chat_memory.clear()
            self.memory.chat_memory.add_ai_message("以繁體中文對話。我可以怎麼幫你呢?")
            st.session_state["docchat_initialized"] = True

        # ✅ 手動清除對話紀錄
        if st.sidebar.button("Clear message history"):
            self.memory.chat_memory.clear()
            self.memory.chat_memory.add_ai_message("以繁體中文對話。我可以怎麼幫你呢?")
            st.session_state["last_response"] = None
            st.session_state["docchat_initialized"] = True
            st.rerun()

        # 顯示歷史紀錄
        self.view.display_chat_history(self.memory.chat_memory.messages)

        # 使用者提問
        user_query = self.view.get_user_input()
        if user_query:
            self.view.display_user_message(user_query)
            self.memory.chat_memory.add_user_message(user_query)

            with self.view.create_response_container():
                if self.provider == "gemini":
                    # Gemini 模式：手動拼接 context + prompt
                    context_docs = retriever.invoke(user_query)[:3]
                    context = "\n\n".join([doc.page_content for doc in context_docs])
                    prompt = f"""
你是一位專業的資料解說員，請依據以下文件內容，以繁體中文回答用戶的問題。

--- 文件內容 ---
{context}

--- 用戶問題 ---
{user_query}
"""
                    response = self.llm.llm.invoke([HumanMessage(content=prompt)]).content
                else:
                    response = qa_chain.run(user_query)

                self.memory.chat_memory.add_ai_message(response)
                st.session_state["last_response"] = response
                st.rerun()
