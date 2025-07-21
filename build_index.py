# build_index.py (fragmento modificado)  ─────────────────────────────────────
import argparse, os, hashlib
from pathlib import Path
from datetime import datetime

from langchain_community.document_loaders import DirectoryLoader, WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_local_docs(dir_path: str):
    path = Path(dir_path)
    if not path.exists():
        print(f"Directorio «{dir_path}» creado.")
        path.mkdir(parents=True, exist_ok=True)
    if not path.is_dir():
        raise NotADirectoryError(f"«{dir_path}» existe pero no es un directorio.")
    return DirectoryLoader(str(path), show_progress=True).load()

def save_web_page(content: str, url: str, data_dir: Path) -> Path:
    """Guarda el contenido en un .txt usando hash de la URL para evitar duplicados."""
    uid = hashlib.sha256(url.encode()).hexdigest()[:10]
    fname = f"web_{uid}.txt"
    fpath = data_dir / fname
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(f"# URL: {url}\n# Fecha: {datetime.utcnow()} UTC\n\n{content}")
    return fpath

def add_web_docs(urls: list[str], docs: list, data_dir: str):
    if not urls:
        return
    os.environ.setdefault("USER_AGENT", "rag-demo/0.1")
    loader = WebBaseLoader(urls)
    web_docs = loader.load()
    docs.extend(web_docs)
    # guardar en disco
    for d in web_docs:
        save_web_page(d.page_content, d.metadata.get("source", ""), Path(data_dir))

def build_faiss(docs, out_dir: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name=EMB_MODEL)
    FAISS.from_documents(chunks, embeddings).save_local(out_dir)
    print(f"Índice guardado en «{out_dir}» con {len(chunks)} fragmentos")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", required=True, help="Carpeta con documentos")
    ap.add_argument("--out_dir", default="vector_store", help="Destino del índice")
    ap.add_argument("--urls", nargs="*", help="URLs opcionales")
    args = ap.parse_args()

    docs = load_local_docs(args.data_dir)
    add_web_docs(args.urls, docs, args.data_dir)
    build_faiss(docs, args.out_dir)

if __name__ == "__main__":
    main()
