# 🧠 DocMind AI — RAG Document Q&A

An AI-powered document question-answering app built with Retrieval-Augmented Generation (RAG).

Upload any PDF and ask natural language questions — the app finds the most relevant sections and answers using LLaMA 3.3.

## 🚀 Live Demo
👉 [Try it here](https://rag-doc-app-npgrcgrsgye3ugbbwdyuep.streamlit.app/)

## 🛠️ Tech Stack
- **LangChain** — RAG pipeline orchestration
- **FAISS** — Vector database for semantic search
- **Groq (LLaMA 3.3 70B)** — LLM for answer generation
- **HuggingFace Embeddings** — Local text embeddings (all-MiniLM-L6-v2)
- **Streamlit** — Frontend UI
- **PyMuPDF** — PDF text extraction

## ⚙️ How It Works
1. Upload a PDF → text is extracted using PyMuPDF
2. Text is split into 300-character chunks with 80-character overlap
3. Chunks are embedded and stored in a FAISS vector index
4. User asks a question → top 6 relevant chunks are retrieved
5. Chunks + question are sent to LLaMA 3.3 via Groq API
6. Answer is displayed with source chunks for transparency

## 🔧 Run Locally

```bash
git clone https://github.com/deekshith-8/rag-doc-qa.git
cd rag-doc-qa
pip install -r requirements.txt
```

Create a `.env` file:
Run the app:
```bash
streamlit run app.py
```

## 👤 Built by
**Deekshith Gowda** — [LinkedIn](https://linkedin.com/in/deekshithg1206) · [GitHub](https://github.com/deekshith-8)