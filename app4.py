import streamlit as st
from transformers import pipeline
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.title("Gemini + Hugging Face: Dual AI Demo")

# --- Load HF model once, cached ---
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")

sentiment_model = load_sentiment_model()

# --- User input ---
text = st.text_area("Enter some text:")

if text:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🤗 Hugging Face — Sentiment")
        result = sentiment_model(text)
        label = result[0]['label']
        score = result[0]['score']
        st.write(f"**{label}** ({score:.2%} confidence)")

    with col2:
        st.subheader("✨ Gemini — Analysis")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"In 2-3 sentences, explain the tone and intent behind this text: {text}"
        )
        st.write(response.text)