# PDF 智能摘要與對話系統

這是一個基於 Streamlit 的 PDF 文件處理系統，提供以下功能：
- 📄 PDF 文件上傳與處理
- 🧠 智能摘要生成（支援 Stuff/MapReduce/Refine 三種模式）
- 💬 文件內容對話（基於向量檢索）
- 🤖 支援 OpenAI 和 Google Gemini 模型

## 功能特點

- 多種摘要模式：
  - Stuff：直接處理全文
  - MapReduce：分塊處理後合併
  - Refine：迭代式精煉摘要
- 文件對話：
  - 基於向量檢索的語意搜尋
  - 上下文記憶對話
- 模型支援：
  - OpenAI API
  - Google Gemini API
  - 本地模型（需自行設定）

## 安裝與設定

1. 克隆專案：
```bash
git clone [repository-url]
cd csd_pdf_summarizer
```

2. 建立虛擬環境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安裝依賴：
```bash
pip install -r requirements.txt
```

4. 設定環境變數：
```bash
cp .env.example .env
```
編輯 `.env` 文件，填入必要的 API 金鑰和設定。

## 使用方式

1. 啟動應用：
```bash
streamlit run main.py
```

2. 在瀏覽器中開啟 `http://localhost:8501`

3. 選擇功能：
   - 一般聊天：直接與 AI 對話
   - 文件對話：上傳 PDF 後進行問答
   - 摘要分析：上傳 PDF 後生成摘要

## 環境變數說明

- `LLM_MODEL`：OpenAI 模型名稱
- `LLM_API_KEY`：OpenAI API 金鑰
- `LLM_API_BASE`：OpenAI API 基礎 URL（可選）
- `GOOGLE_API_KEY`：Google API 金鑰
- `GEMINI_MODEL`：Gemini 模型名稱
- `EMBEDDING_MODEL`：嵌入模型名稱
- `EMBEDDING_API_KEY`：嵌入模型 API 金鑰
- `EMBEDDING_API_BASE`：嵌入模型 API 基礎 URL（可選）

## 開發團隊

- 開發：李易修 副研究員
- 指導：葉神丑 研發長

## 授權

[授權資訊] 