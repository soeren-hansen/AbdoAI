import streamlit as st
from pathlib import Path

st.set_page_config(page_title="AbdoAI", page_icon="🩺")

st.title("🩺 AbdoAI")
st.write("Første prototype: chatbot baseret på én markdown-fil.")

knowledge_path = Path("knowledge/brok_kikkertoperation.md")

if knowledge_path.exists():
    content = knowledge_path.read_text(encoding="utf-8")
    st.success("Vidensfil fundet.")
else:
    content = ""
    st.error("Vidensfil mangler.")

question = st.text_input("Stil et spørgsmål om brokoperation med kikkert:")

if question:
    st.subheader("Spørgsmål")
    st.write(question)

    st.subheader("Foreløbigt svar")
    st.write("Næste trin er at koble GPT på, så svaret dannes ud fra markdown-filen.")

    with st.expander("Se markdown-indhold"):
        st.markdown(content)