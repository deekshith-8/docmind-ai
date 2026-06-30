<div align="center">

# DocMind AI

### Ask questions. Get answers. Straight from your documents.

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and interact with them using natural language. DocMind AI retrieves the most relevant sections from the document and generates context-aware answers powered by LLaMA 3.3 70B.

<br>

<img src="https://img.shields.io/badge/LangChain-RAG%20Pipeline-3C3C3C?style=flat-square" />
<img src="https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-F55036?style=flat-square" />
<img src="https://img.shields.io/badge/FAISS-Vector%20Search-4A90D9?style=flat-square" />
<img src="https://img.shields.io/badge/HuggingFace-Embeddings-yellow?style=flat-square" />
<img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=flat-square&logo=streamlit" />
<img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" />

<br><br>

<a href="https://docmind-ai-nbsnknbbrdlshnaxmjx3iv.streamlit.app/"><strong>Live Demo</strong></a>

</div>

---

# Overview

DocMind AI is a Retrieval-Augmented Generation (RAG) system that enables users to upload PDF documents and ask natural language questions about their contents.

Instead of relying solely on an LLM's internal knowledge, the application retrieves the most semantically relevant portions of the uploaded document using vector search and supplies them as context to the language model. This ensures responses remain grounded in the document while significantly reducing hallucinations.

The application also displays the retrieved source chunks, allowing users to verify exactly where each answer originated.

---

# Features

- Upload any PDF and start chatting instantly
- Semantic document retrieval using FAISS
- Fast inference with Groq's LLaMA 3.3 70B
- Context-aware answers grounded in uploaded documents
- Source chunk references for transparency
- Fully local embedding generation
- Modern Streamlit interface
- Low-latency RAG pipeline

---

# Tech Stack

| Layer | Technology |
|---------|------------|
| Language Model | Groq - LLaMA 3.3 70B |
| RAG Framework | LangChain |
| Vector Database | FAISS |
| Embeddings | HuggingFace all-MiniLM-L6-v2 |
| PDF Parsing | PyMuPDF |
| Frontend | Streamlit |
| Deployment | Streamlit Community Cloud |

---

# Architecture

```text
                    Upload PDF
                        │
                        ▼
               ┌────────────────┐
               │    PyMuPDF     │
               │ PDF Extraction │
               └────────────────┘
                        │
                        ▼
               ┌────────────────┐
               │ Text Chunking  │
               │ Recursive Split│
               └────────────────┘
                        │
                        ▼
               ┌────────────────┐
               │ HuggingFace    │
               │ Embeddings     │
               └────────────────┘
                        │
                        ▼
               ┌────────────────┐
               │ FAISS Index    │
               └────────────────┘
                        ▲
                        │
               User Question
                        │
                        ▼
               ┌────────────────┐
               │ Embed Question │
               └────────────────┘
                        │
                        ▼
               ┌────────────────┐
               │ Similarity     │
               │ Search (Top-K) │
               └────────────────┘
                        │
                        ▼
               ┌────────────────┐
               │ LangChain RAG  │
               │ Prompt Builder │
               └────────────────┘
                        │
                        ▼
               ┌────────────────┐
               │ Groq LLaMA     │
               │ 3.3 70B        │
               └────────────────┘
                        │
                        ▼
          Answer + Retrieved Source Chunks
```

---

# How It Works

### 1. Upload Document

Users upload any PDF through the Streamlit interface.

↓

### 2. Parse PDF

PyMuPDF extracts raw text from every page.

↓

### 3. Chunking

The extracted text is split into overlapping chunks to preserve context while keeping each chunk within the embedding model's limits.

↓

### 4. Generate Embeddings

Each chunk is converted into dense vector embeddings using HuggingFace's `all-MiniLM-L6-v2` model.

↓

### 5. Store in FAISS

The embeddings are indexed inside FAISS for efficient similarity search.

↓

### 6. Ask Questions

The user's query is embedded using the same embedding model.

↓

### 7. Retrieve Context

FAISS returns the Top-K most semantically similar chunks.

↓

### 8. Generate Answer

LangChain combines the retrieved chunks with the user's query and sends them to Groq's LLaMA 3.3 70B.

↓

### 9. Display Results

The generated answer and supporting source chunks are presented to the user.




---

# Future Improvements

- Multiple PDF support
- Conversational memory
- OCR for scanned documents
- Hybrid search (BM25 + Vector Search)
- Persistent vector databases (ChromaDB / Pinecone)
- PDF highlighting for cited passages
- Chat history
- User authentication
- Export chat conversations

---

# Performance

- Fast embedding generation
- Millisecond-scale vector retrieval using FAISS
- Low inference latency via Groq
- Optimized for real-time document question answering

---

# Screenshots

> Add screenshots of:
>
> - Home page
> - Uploading a PDF
> - Asking a question
> - Retrieved source chunks

---

# License

This project is licensed under the MIT License.

---

---

## Author

---

<div align="center">
Built by Deekshith Gowda 
</div>
