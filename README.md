
# 🐱🔍 RAG Multi-Source – Demo

## Descripción

RAG Multi‑Source Demo es un pequeño proyecto educativo que muestra cómo combinar Retrieval‑Augmented Generation con un stack Python moderno. Permite indexar documentos locales y páginas web, recuperar los fragmentos más relevantes con FAISS y generar respuestas contextuales usando un LLM ligero (TinyLlama‑1.1B‑Chat).

Ideal para:

Probar arquitecturas RAG sin depender de servicios externos.
Aprender a integrar FAISS, LangChain y FastAPI.
Desplegar una demo completa (API + UI) en minutos.



| Componente | Descripción | Tecnologías |
|------------|-------------|-------------|
| **`build_index.py`** | Lee todos los ficheros de `data/`, descarga opcionalmente URLs, fragmenta los textos y genera un índice **FAISS** | LangChain 0.2 · sentence-transformers |
| **`rag_server.py`** | API REST  – `GET /` (estado) · `GET /ask` (respuesta + fuentes) | FastAPI · Uvicorn |
| **`client.py`** | Interfaz Streamlit para chatear con el RAG | Streamlit 1.35 |
| **`models.py`** | Carga el LLM (`TinyLlama-1.1B-Chat`) y prepara el prompt | HuggingFace Transformers |
| **`vector_store/`** | Índice FAISS persistente generado por el script | FAISS-CPU |

---
##⚡ Prerrequisitos

Python ≥ 3.11

Ollama ≥ 0.1.30 para descargar y ejecutar el LLM localmente

Instala Ollama
Windows: descarga OllamaSetup.exe desde la página oficial e instala.

(macOS/Linux/WSL): curl -fsSL https://ollama.com/install.sh | sh

(Opcional) GPU con CUDA 11+ para acelerar TinyLlama

2‑3 GB de RAM libres para el índice y el modelo cuantizado


---
## 🚀 Instalación rápida

```bash
git clone https://github.com/Juanjojr9/rag-multi-source-demo.git
cd  rag-multi-source-demo
python -m venv .venv
```
 Windows:
.\.venv\Scripts\activate
macOS / Linux:
source .venv/bin/activate
```bash
pip install -r requirements.txt
```
Después abre PowerShell o CMD y ejecuta
```bash
ollama pull tinyllama:chat     # LLM
ollama pull all-minilm         # Embeddings
```

### 🔧 Construir el índice (solo la primera vez)


Copia tus PDFs, TXT, MD… en ./data o usa una URL

```bash
python build_index.py --data_dir ./data \
                      --urls "https://es.wikipedia.org/wiki/Gato"
```
El script crea data/ si no existe y genera vector_store/ con los vectores.


Ejecución
### 1) Servidor RAG
```bash
uvicorn rag_server:app --reload         # Swagger: http://localhost:8000/docs
```
### 2) Cliente Streamlit (en otra terminal)
```bash
streamlit run client.py                 # UI:     http://localhost:8501
```

## ✨ Opciones de ampliación
Cambiar el modelo de embeddings (EMB_MODEL).

Sustituir TinyLlama por otro LLM en models.py.

Añadir más ficheros o URLs y volver a ejecutar build_index.py.

Contenerizar con Docker para despliegue sencillo (no incluido).


## 🗂️ Estructura
```bash
├── build_index.py      # Indexación + ingesta web
├── rag_server.py       # API FastAPI
├── client.py           # Front Streamlit
├── models.py           # Carga LLM + generación
├── requirements.txt
└── data/ | vector_store/
```

## ⚙️ Ajustes rápidos
Variable	Dónde	Descripción
EMB_MODEL	build_index.py, rag_server.py	Cambia modelo de embeddings
INDEX_PATH	rag_server.py	Ruta al índice FAISS
API_URL	client.py	End-point del servidor en producción


## 🤝 Contribuir
¡Se aceptan PRs! Abre una issue primero para discutir cambios mayores.
Asegúrate de ejecutar pre-commit y añadir tests cuando corresponda.

