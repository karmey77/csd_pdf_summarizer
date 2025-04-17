"""
app/main.py
主程式入口，初始化應用並執行聊天控制器。
"""

import streamlit as st
from controllers.chat_controller import ChatController
from controllers.doc_chat_controller import DocChatController

def main():
    st.set_page_config(page_title="CSD PDF Summarizer", layout="wide")

    PAGES = {
        "🗣️ 一般聊天": ChatController,
        "📄 文件對話": DocChatController,
    }

    choice = st.sidebar.radio("選擇功能頁面", list(PAGES.keys()))
    controller = PAGES[choice]()
    controller.run()

if __name__ == "__main__":
    main()
