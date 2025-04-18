"""
app/main.py
主程式入口，初始化應用並執行聊天控制器。
"""

import streamlit as st
from controllers.chat_controller import ChatController
from controllers.doc_chat_controller import DocChatController
from controllers.summarize_controller import SummarizeController

def inject_global_css():
    st.markdown("""
    <style>
    html, body {
        font-family: "Noto Sans TC", sans-serif;
        background-color: #f7f9fb;
    }

    section[data-testid="stSidebar"] {
        background-color: #f1f5f9;
        border-right: 1px solid #e2e8f0;
    }

    /* Sidebar radio 樣式優化 */
    .stRadio label {
        font-size: 16px; 
        color: #1e293b;
        padding: 6px 10px;
        display: flex;
        align-items: center;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
                
    .stRadio p {
        font-size: 2rem; 
        color: #1e293b;
        padding: 6px 10px;
        display: flex;
        align-items: center;
        border-radius: 8px;
        transition: all 0.2s ease;
    }

    .stRadio label:hover {
        background-color: #e2e8f0;
    }

    .stRadio label span {
        margin-left: 6px;
    }

    .stRadio {
        padding-bottom: 2px;
        margin-top: -2rem;
    }

    .stRadio > div {
        gap: 2px;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .dev-card {
        background: #ffffff;
        padding: 12px 16px;
        border-radius: 12px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        font-size: 13.8px;
        line-height: 1.6;
        color: #334155;
        margin-top: 20px;
        border-left: 4px solid #cbd5e1;
    }

    .stButton > button {
        background: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: 500;
        border: none;
    }

    .stButton > button:hover {
        background: #1e40af;
    }
    </style>
    """, unsafe_allow_html=True)


# 調用
inject_global_css()

def main():
    if "llm_provider" not in st.session_state:
        st.session_state["llm_provider"] = "local"

    st.sidebar.markdown("# 🔧 模型選擇")
    st.session_state["llm_provider"] = st.sidebar.radio(" ", ["local", "gemini"], label_visibility='hidden')

    PAGES = {
        "🗣️ 一般聊天": ChatController,
        "📄 文件對話": DocChatController,
        "🧠 摘要分析": SummarizeController,
    }

    st.sidebar.markdown("# 🧭 功能頁面")
    choice = st.sidebar.radio(" ", list(PAGES.keys()), label_visibility='hidden')

    # ✨ 傳 provider 進 controller
    controller = PAGES[choice](provider=st.session_state["llm_provider"])
    controller.run()

    with st.sidebar:
        st.markdown('---')
        st.caption("""
        <div class="dev-card">
            👨‍💻 技術研發中心 <br><br>
            開發：李易修 副研究員<br>
            指導：葉神丑 研發長
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
