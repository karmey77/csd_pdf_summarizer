"""
services/vector_service.py
處理 PDF → chunk → 向量化檢索。
"""

import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from utils.config import settings

class RetrieverService:
    def _process_files(self, uploaded_files):
        """處理檔案，回傳原始 doc、chunk、向量 retriever"""
        docs = []
        temp_dir = tempfile.TemporaryDirectory()

        for file in uploaded_files:
            temp_path = os.path.join(temp_dir.name, file.name)
            with open(temp_path, "wb") as f:
                f.write(file.getvalue())
            docs.extend(PyPDFLoader(temp_path).load())

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        splits = text_splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.EMBEDDING_API_KEY,
            openai_api_base=settings.EMBEDDING_API_BASE,
            check_embedding_ctx_length=False
        )

        vectordb = FAISS.from_documents(splits, embeddings)
        retriever = vectordb.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 8, "fetch_k": 16, "score_threshold": 0.85}
        )

        return docs, splits, retriever

    def configure(self, uploaded_files):
        """只回傳 retriever 給對話用"""
        _, _, retriever = self._process_files(uploaded_files)
        return retriever

    def configure_with_docs(self, uploaded_files):
        """回傳 docs + splits + retriever 給摘要用"""
        return self._process_files(uploaded_files)
