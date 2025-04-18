"""
services/summarizer_service.py
根據模式執行 Stuff / MapReduce / Refine 三種摘要策略。
"""

from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import LLMChain, MapReduceDocumentsChain, ReduceDocumentsChain, RefineDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import tempfile

class SummarizerService:
    def __init__(self):
        pass

    def summarize(self, uploaded_files, mode: str, llm) -> str:
        docs = self.extract_docs(uploaded_files)
        splits = self.split_docs(docs)
        self.llm = llm
        self.splits = splits

        if mode == "stuff_chain":
            return self._stuff_chain()
        elif mode == "map_reduce":
            return self._map_reduce()
        elif mode == "refine":
            return self._refine()
        else:
            return "請選擇有效的摘要模式"

    def extract_docs(self, uploaded_files):
        docs = []
        temp_dir = tempfile.TemporaryDirectory()
        for file in uploaded_files:
            temp_path = os.path.join(temp_dir.name, file.name)
            with open(temp_path, "wb") as f:
                f.write(file.getvalue())
            docs.extend(PyPDFLoader(temp_path).load())
        return docs

    def extract_text(self, uploaded_files):
        docs = self.extract_docs(uploaded_files)
        return "\n\n".join([doc.page_content for doc in docs])

    def split_docs(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        return text_splitter.split_documents(docs)

    def _stuff_chain(self):
        prompt = PromptTemplate(template="""寫出以下文字內容的詳細摘要，用繁體中文回答，若有簡體字請轉換成繁體字。
```{text}```
摘要:""", input_variables=["text"])
        chain = load_summarize_chain(self.llm, chain_type="stuff", prompt=prompt, verbose=True)
        return chain.run(self.splits)

    def _map_reduce(self):
        doc_prompt = PromptTemplate(input_variables=["page_content"], template="{page_content}")
        doc_var = "context"
        summary_prompt = PromptTemplate.from_template("總結以下內容，用繁體中文回答: {context}")
        reduce_prompt = PromptTemplate.from_template("結合這些總結，用繁體中文回答: {context}")
        collapse_prompt = PromptTemplate.from_template("將這些內容提煉為主要主題的最終綜合摘要。用繁體中文回答: {context}")

        llm_chain = LLMChain(llm=self.llm, prompt=summary_prompt)
        reduce_chain = LLMChain(llm=self.llm, prompt=reduce_prompt)
        collapse_chain = LLMChain(llm=self.llm, prompt=collapse_prompt)

        combine_chain = StuffDocumentsChain(llm_chain=reduce_chain, document_prompt=doc_prompt, document_variable_name=doc_var)
        reduce_documents_chain = ReduceDocumentsChain(
            combine_documents_chain=combine_chain,
            collapse_documents_chain=StuffDocumentsChain(llm_chain=collapse_chain, document_prompt=doc_prompt, document_variable_name=doc_var)
        )

        chain = MapReduceDocumentsChain(
            llm_chain=llm_chain,
            reduce_documents_chain=reduce_documents_chain,
            return_intermediate_steps=False
        )
        return chain.run(self.splits)

    def _refine(self):
        doc_prompt = PromptTemplate(input_variables=["page_content"], template="{page_content}")
        doc_var = "context"
        initial_prompt = PromptTemplate.from_template("總結以下內容，用繁體中文回答: {context}\n")
        refine_prompt = PromptTemplate.from_template(
            "這是你的第一次總結: {prev_response}.\n現在基於以下內容增加上去: {context}\n"
        )

        initial_chain = LLMChain(llm=self.llm, prompt=initial_prompt)
        refine_chain = LLMChain(llm=self.llm, prompt=refine_prompt)

        chain = RefineDocumentsChain(
            initial_llm_chain=initial_chain,
            refine_llm_chain=refine_chain,
            document_prompt=doc_prompt,
            document_variable_name=doc_var,
            initial_response_name="prev_response"
        )
        return chain.run(self.splits)
