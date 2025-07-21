# client.py ───────────────────────────────────────────────────────────
import streamlit as st
import requests
from urllib.parse import quote

API_URL = "http://localhost:8000"

st.set_page_config(page_title="RAG demo – Cliente", layout="centered")
st.title("🔍 Pregunta al RAG")

st.markdown(
    """
Este cliente se conecta al endpoint **/ask** de la API.  
Escribe una pregunta y presiona **Enviar** para obtener la respuesta con sus fuentes.
"""
)

# --- Entrada de usuario ------------------------------------------------
question = st.text_input(
    "Pregunta",
    placeholder="¿Cuánto vive un gato doméstico?",
    label_visibility="visible",
)

col1, col2 = st.columns([1, 4])
with col1:
    send_btn = st.button("Enviar", use_container_width=True)
with col2:
    clear_btn = st.button("Limpiar historial", use_container_width=True)

# --- Área de historial -------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if clear_btn:
    st.session_state.history.clear()
    st.rerun()

for entry in st.session_state.history:
    st.chat_message("user").write(entry["q"])
    with st.chat_message("assistant"):
        st.markdown(entry["a"])
        if entry["sources"]:
            with st.expander("Fuentes"):
                for src in entry["sources"]:
                    st.markdown(f"- {src}")

# --- Petición a la API --------------------------------------------------
if send_btn:
    if not question.strip():
        st.warning("Escribe una pregunta antes de enviar.")
        st.stop()

    with st.spinner("Consultando RAG..."):
        try:
            r = requests.get(f"{API_URL}/ask", params={"question": question})
            r.raise_for_status()
            data = r.json()
        except Exception as err:
            st.error(f"Error al llamar a la API: {err}")
            st.stop()

    # Guardar en historial
    st.session_state.history.append(
        {"q": question, "a": data.get("answer", "Sin respuesta"), "sources": data.get("sources", [])}
    )
    st.rerun()
