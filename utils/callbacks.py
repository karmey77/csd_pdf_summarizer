"""
utils/callbacks.py
共用的 LangChain Streaming Callback，用於 Streamlit markdown 顯示。
"""

from langchain.callbacks.base import BaseCallbackHandler
import streamlit as st

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container=None, initial_text=""):
        self.container = container or st.empty()
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)
