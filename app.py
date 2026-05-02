import os
import streamlit as st
from dotenv import load_dotenv

import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ── Page config ──────────────────────────────────────────
st.set_page_config(page_title="DocMind AI", page_icon="🧠", layout="wide")

# ── Custom CSS ───────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #0f1117; }
    
    .hero {
        background: linear-gradient(135deg, #1a1f2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 24px;
        border: 1px solid #ffffff15;
        text-align: center;
    }
    .hero h1 {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6ee7f7, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .hero p {
        color: #94a3b8;
        font-size: 1.05rem;
        margin: 0;
    }
    .badge {
        display: inline-block;
        background: #ffffff10;
        border: 1px solid #ffffff20;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 14px;
    }

    .stat-card {
        background: #1e2330;
        border: 1px solid #ffffff10;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .stat-card .value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #6ee7f7;
    }
    .stat-card .label {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 4px;
    }

    .answer-box {
        background: linear-gradient(135deg, #1e2330, #1a2540);
        border: 1px solid #6ee7f720;
        border-left: 4px solid #6ee7f7;
        border-radius: 12px;
        padding: 24px;
        margin-top: 16px;
        color: #e2e8f0;
        font-size: 1rem;
        line-height: 1.7;
    }

    .chunk-card {
        background: #1e2330;
        border: 1px solid #ffffff10;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 10px;
        font-size: 0.85rem;
        color: #94a3b8;
        line-height: 1.6;
    }
    .chunk-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #a78bfa;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .footer {
        text-align: center;
        padding: 24px 0 8px 0;
        color: #334155;
        font-size: 0.82rem;
    }
    .footer span {
        color: #6ee7f7;
        font-weight: 600;
    }

    div[data-testid="stFileUploader"] {
        background: #1e2330;
        border: 2px dashed #ffffff15;
        border-radius: 12px;
        padding: 12px;
    }
    div[data-testid="stTextInput"] input {
        background: #1e2330 !important;
        border: 1px solid #ffffff15 !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        padding: 12px 16px !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #6ee7f750 !important;
        box-shadow: 0 0 0 3px #6ee7f715 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Hero section ─────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🧠 DocMind AI</h1>
    <p>Upload any PDF and get instant AI-powered answers from your document</p>
    <div class="badge">Powered by RAG · LLaMA 3 · FAISS</div>
</div>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────
def extract_text(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

@st.cache_resource(show_spinner="🔍 Building knowledge base...")
def build_vectorstore(text):
    splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=80
    )
    chunks = splitter.split_text(text)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore, len(chunks)

def build_chain(vectorstore):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        api_key=os.getenv("GROQ_API_KEY")
    )
    prompt = PromptTemplate.from_template("""
You are a helpful assistant. Use the context below to answer the question accurately.
If the answer isn't in the context, say "I couldn't find that in the document."

Context:
{context}

Question: {question}

Answer:""")

    retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 6, "fetch_k": 20}
)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever

# ── Layout ────────────────────────────────────────────────
col1, col2 = st.columns([1, 1.6], gap="large")

with col1:
    st.markdown("### 📂 Upload Document")
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

    if uploaded_file:
        text = extract_text(uploaded_file)
        vectorstore, num_chunks = build_vectorstore(text)
        chain, retriever = build_chain(vectorstore)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📊 Document Stats")

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="value">{len(text)//1000}K</div>
                <div class="label">Characters</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="value">{num_chunks}</div>
                <div class="label">Chunks</div>
            </div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="value">{uploaded_file.name[:6]}..</div>
                <div class="label">File</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📄 Preview extracted text"):
            st.caption(text[:1000])

with col2:
    if uploaded_file:
        st.markdown("### 💬 Ask a Question")
        question = st.text_input("", placeholder="e.g. What are the main projects listed?", label_visibility="collapsed")

        if question:
            with st.spinner("Thinking..."):
                answer = chain.invoke(question)
                source_docs = retriever.invoke(question)

            st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📚 Source chunks used by AI"):
                for i, doc in enumerate(source_docs):
                    st.markdown(f"""
                    <div class="chunk-card">
                        <div class="chunk-label">Chunk {i+1}</div>
                        {doc.page_content}
                    </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("👈 Upload a PDF on the left to get started")

# ── Footer ────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with ❤️ by <span>Deekshith Gowda</span> · RAG · LangChain · Groq · Streamlit
</div>
""", unsafe_allow_html=True)