# PDF Summarization and Retrieval Chat

A modular Streamlit application for working with PDF documents through multi-strategy summarization and retrieval-augmented conversation.

The project demonstrates an end-to-end applied-AI workflow: accept uploaded documents, extract and split their contents, create vector embeddings, retrieve relevant context, maintain conversation history, and stream model responses through a user-facing interface.

## What it does

- Upload and process one or more PDF documents.
- Generate Traditional Chinese summaries with three strategies:
  - **Stuff** for shorter documents that fit into a single prompt.
  - **MapReduce** for chunk-level summaries followed by aggregation.
  - **Refine** for iterative summary improvement across chunks.
- Ask questions about uploaded documents through FAISS-based semantic retrieval.
- Maintain multi-turn document-chat history in Streamlit sessions.
- Use Google Gemini or an OpenAI-compatible endpoint, including a separately configured local endpoint.
- Stream generated responses in the interface.

## Architecture

```text
Streamlit UI
  ├─ controllers/   coordinates chat, document Q&A, and summarization flows
  ├─ services/      model access, PDF processing, vector retrieval, and summarization
  ├─ views/         Streamlit input and output components
  ├─ models/        application message model
  └─ utils/         settings, logging, and streaming callbacks

PDF upload
  → PyPDFLoader
  → RecursiveCharacterTextSplitter
  → OpenAI-compatible embeddings
  → FAISS retriever
  → conversational retrieval or Gemini context prompt
  → streamed response
```

## Technology

- Python and Streamlit
- LangChain
- FAISS vector search
- OpenAI-compatible chat and embedding endpoints
- Google Gemini
- PyPDF
- Pydantic settings and `.env` configuration

## Run locally

1. Clone the repository.

   ```bash
   git clone https://github.com/karmey77/csd_pdf_summarizer.git
   cd csd_pdf_summarizer
   ```

2. Create and activate a virtual environment.

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows, activate it with `.venv\\Scripts\\activate`.

3. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Copy the environment template and configure the model and embedding endpoints you intend to use.

   ```bash
   cp .env.example .env
   ```

5. Start the application.

   ```bash
   streamlit run main.py
   ```

## Configuration

| Variable | Purpose |
| --- | --- |
| `LLM_MODEL` | Model name for the OpenAI-compatible chat endpoint. |
| `LLM_API_KEY` | API key for that endpoint. |
| `LLM_API_BASE` | Base URL for the endpoint. |
| `GOOGLE_API_KEY` | Google Gemini API key. |
| `GEMINI_MODEL` | Gemini model name. |
| `EMBEDDING_MODEL` | Embedding model name. |
| `EMBEDDING_API_KEY` | Embedding endpoint API key. |
| `EMBEDDING_API_BASE` | Embedding endpoint base URL. |

Never commit a populated `.env` file or real API credentials.

## Project status and limitations

This repository is an applied-AI prototype, not a production service. It does not publish comparative model-quality, latency, cost, or scale claims.

Current engineering follow-ups include:

- add meaningful unit and integration tests; the current test placeholder is empty;
- validate the complete dependency set in a clean environment;
- add document-size limits, upload validation, and more granular error handling;
- add retrieval and summarization evaluation cases;
- document a production deployment and observability path.

## Attribution

Developed by Yi-Hsiu Lee during his work at the Corporate Synergy Development Center (CSDC／財團法人中衛發展中心).

## License

No open-source license is currently granted. The source is public for inspection and portfolio reference; reuse requires permission from the repository owner and any applicable rights holder.
