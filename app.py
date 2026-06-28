import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

from src.retriever import retrieve

load_dotenv()

client = OpenAI()

st.set_page_config(page_title="AbdoAI", page_icon="🏥")
st.title("🏥 AbdoAI")
st.caption("Spørgsmål besvares på baggrund af afdelingens egne dokumenter.")

question = st.chat_input("Stil et spørgsmål...")

if question:
    st.chat_message("user").write(question)

    with st.spinner("Finder relevante dokumenter..."):
        results = retrieve(question)

    context = "\n\n".join(
        [f"KILDE {i+1}:\n{doc}" for i, doc in enumerate(results)]
    )

    prompt = f"""
Du er AbdoAI, en hjælpsom klinisk assistent for Abdominalcenter K.

Svar kun ud fra nedenstående kontekst.
Hvis svaret ikke findes i konteksten, så sig:
"Det kan jeg ikke besvare ud fra de tilgængelige dokumenter."

KONTEKST:
{context}

SPØRGSMÅL:
{question}
"""

    with st.spinner("Skriver svar..."):
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Du svarer klart, sikkert og på dansk."},
                {"role": "user", "content": prompt},
            ],
        )

    answer = response.choices[0].message.content
    st.chat_message("assistant").write(answer)