import streamlit as st
from transformers import pipeline

st.title("Sentiment Checker")

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")

classifier = load_model()

text = st.text_input("Enter some text:")
if text:
    result = classifier(text)
    st.write(result)