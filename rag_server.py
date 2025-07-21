from fastapi import FastAPI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from models import load_llm, generate_answer

EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "./vector_store"
TOP_K = 4

app = FastAPI(title="RAG demo multi-directorio")

@app.get("/")  # ← ruta raíz para evitar 404 en /
def read_root():
    return {
        "msg": "RAG demo activo. Usa /docs para la UI interactiva o /ask?question=..."
    }

# ────────────── carga de recursos ──────────────
embeddings = HuggingFaceEmbeddings(model_name=EMB_MODEL)
vectordb = FAISS.load_local(INDEX_PATH, embeddings,
                            allow_dangerous_deserialization=True)
llm_pipe = load_llm()

# ────────────── endpoint principal ─────────────
@app.get("/ask")
def ask(question: str):
    docs = vectordb.similarity_search(question, k=TOP_K)
    context = "\n\n".join(d.page_content for d in docs)
    answer = generate_answer(llm_pipe, question, context)
    return {
        "answer": answer,
        "sources": [d.metadata.get("source", "") for d in docs],
    }
