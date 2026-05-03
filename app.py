import streamlit as st
from src.loader    import load_pdf
from src.embedder  import build_index
from src.retriever import retrieve
from src.generator import generate

st.set_page_config(page_title="RAG - Chat with PDF", page_icon="📄")
st.title("📄 Chat with your PDF")

# ── Upload PDF ────────────────────────────────────────────
uploaded = st.file_uploader("Upload a PDF", type="pdf")

if uploaded:
    # save uploaded file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(uploaded.read())

    # index only once per upload
    if "index" not in st.session_state:
        with st.spinner("Reading and indexing PDF..."):
            st.session_state.chunks = load_pdf("temp.pdf")
            st.session_state.index  = build_index(st.session_state.chunks)
        st.success(f"Ready! Indexed {len(st.session_state.chunks)} chunks.")

    # ── Chat ──────────────────────────────────────────────
    question = st.chat_input("Ask anything about your PDF...")

    if question:
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                relevant = retrieve(question, st.session_state.chunks, st.session_state.index)
                answer   = generate(question, relevant)
            st.write(answer)