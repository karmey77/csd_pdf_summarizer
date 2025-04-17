"""
app/main.py
主程式入口，初始化應用並執行聊天控制器。
"""

import streamlit as st
from controllers.chat_controller import ChatController
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    st.set_page_config(page_title="🦜 Simple Chat", layout="wide")
    st.title("🦜 Simple Chat")

    controller = ChatController()
    controller.run()

if __name__ == "__main__":
    main()
