import streamlit as st
st.title("THE MULTIVERSE OF CHATBOTS")
personality=st.selectbox("who do u want to talk to ",[
    "ms dhoni fan","virat kohli fan ","rohit sharma fan",])

from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_message=st.text_input("say something:")

if st.button("SEND"):
    if user_message:
        ai_instructions=f"you are acting as {personality}.Respond to the message sent by user staying completely in character:{user_message}"
        with st.spinner("connecting to the multiverse!........."):
            response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=ai_instructions
            )
            st.success("mesaage received!")
            st.write(response.text)
    else:
        st.warning("please type a message first")