"""
controllers/summarize_controller.py
文件摘要功能，支援 Stuff / MapReduce / Refine 模式，並支援 Gemini 模型。
"""

import streamlit as st
from services.summarizer_service import SummarizerService
from services.llm_service import LLMService
from views.summarize_view import SummarizeView
from langchain_core.messages import HumanMessage
from utils.callbacks import StreamHandler


class SummarizeController:
    def __init__(self, provider: str = "local"):
        self.provider = provider
        self.llm = LLMService(provider=provider)
        self.view = SummarizeView()
        self.summarizer = SummarizerService()

    def run(self):
        uploaded_files = self.view.upload_file_input()
        if not uploaded_files:
            return

        mode = self.view.select_summary_mode()

        # 先顯示使用者輸入摘要請求
        st.chat_message("user").write(f"請幫我用 {mode} 模式摘要這份文件")

        with self.view.create_response_container():
            if self.provider == "gemini":
                # Gemini 模式下手動處理 prompt injection（Stuff only）
                full_text = self.summarizer.extract_text(uploaded_files)
                prompt = f"""
你是一位專業文件總結員，請以繁體中文閱讀並摘要以下內容：

--- 文件內容 ---
{full_text}

請總結成一段摘要，注意保留關鍵數據與邏輯脈絡。
"""
                stream_handler = StreamHandler(st.empty())
                response = ""
                for chunk in self.llm.llm.stream([HumanMessage(content=prompt)]):
                    token = chunk.content or ""
                    response += token
                    stream_handler.on_llm_new_token(token)

            else:
                # OpenAI 模式下使用原有 summarizer chain
                response = self.summarizer.summarize(
                    uploaded_files=uploaded_files,
                    mode=mode,
                    llm=self.llm.llm,
                )
                st.chat_message("assistant").markdown(response)

            st.session_state["last_summary"] = response
