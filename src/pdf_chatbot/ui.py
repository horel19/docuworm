"""Streamlit UI for the PDF chatbot."""

from __future__ import annotations

import streamlit as st

from pdf_chatbot.chat import ask
from pdf_chatbot.ingestor import extract_text
from pdf_chatbot.validators import ChatSession

st.set_page_config(page_title="PDF Chatbot", page_icon="📄", layout="wide")

st.title("PDF Chatbot")
st.caption("Upload a PDF and ask questions about its content — powered by Gemini")

# ---- Initialise session state ----
if "session" not in st.session_state:
    st.session_state.session: ChatSession | None = None

# ---- Sidebar: upload ----
with st.sidebar:
    uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded and (
        st.session_state.session is None
        or st.session_state.session.pdf_name != uploaded.name
    ):
        pdf_text = extract_text(uploaded.read())
        st.session_state.session = ChatSession(
            pdf_name=uploaded.name, pdf_text=pdf_text
        )
        st.success(f"Loaded **{uploaded.name}**")

# ---- Chat interface ----
if st.session_state.session is None:
    st.info("Upload a PDF from the sidebar to get started.")
    st.stop()

session = st.session_state.session

for msg in session.messages:
    with st.chat_message(msg.role):
        st.markdown(msg.content)

if prompt := st.chat_input("Ask a question about the document…"):
    session.add_message("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            answer = ask(session.pdf_text, prompt)
        st.markdown(answer)

    session.add_message("assistant", answer)
