"""
app/main.py
主程式入口，初始化應用並執行聊天控制器。
"""

import streamlit as st
from controllers.chat_controller import ChatController
from controllers.doc_chat_controller import DocChatController
from controllers.summarize_controller import SummarizeController

def main():
    if "llm_provider" not in st.session_state:
        st.session_state["llm_provider"] = "local"
    st.session_state["llm_provider"] = st.sidebar.radio("選擇 LLM 模型", ["local", "gemini"])

    PAGES = {
        "🗣️ 一般聊天": ChatController,
        "📄 文件對話": DocChatController,
        "🧠 摘要分析": SummarizeController,
    }

    choice = st.sidebar.radio("功能頁面", list(PAGES.keys()))

    # ✨ 傳 provider 進 controller
    controller = PAGES[choice](provider=st.session_state["llm_provider"])
    controller.run()

if __name__ == "__main__":
    main()
