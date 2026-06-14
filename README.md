# 🧠 DocMind AI

> AI-powered PDF question answering using Retrieval-Augmented Generation (RAG)

Upload any PDF and ask questions in plain English. DocMind retrieves the most relevant sections from your document and generates precise answers using LLaMA 3.3 70B — no hallucinations, just grounded responses.

👉 **[Try it Live](https://docmind-ai-23cb.onrender.com)**

---

## ✨ Features

- 📄 Upload any PDF and instantly query its contents
- 🔍 Semantic search using FAISS vector index
- 🤖 Answers powered by LLaMA 3.3 70B via Groq API
- 📌 Source chunks displayed alongside every answer for transparency
- ⚡ Fast local embeddings — no external embedding API needed

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq — LLaMA 3.3 70B |
| RAG Pipeline | LangChain |
| Vector Store | FAISS |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| PDF Parsing | PyMuPDF |
| Frontend | Streamlit |
| Hosting | Render |

---

## ⚙️ How It Works

```
PDF Upload
    ↓
Text extracted via PyMuPDF
    ↓
Split into 300-char chunks (80-char overlap)
    ↓
Embedded using all-MiniLM-L6-v2 → stored in FAISS
    ↓
User asks a question
    ↓
Top 6 relevant chunks retrieved
    ↓
Chunks + question → LLaMA 3.3 via Groq API
    ↓
Answer + source chunks displayed
```

---

## 👤 Built by

**Deekshith Gowda** — [LinkedIn](https://linkedin.com/in/deekshithg1206) · [GitHub](https://github.com/deekshith-8)
