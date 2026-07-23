import streamlit as st
st.title("🤖THE MULTIVERSE OF CHATBOTS🤖")
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
         st.write(msg["content"])
personality=st.sidebar.selectbox("who do u want to talk to ",[
    "polite friend😊","angry friend😡 ","a cool genz friend😎"," millenial friend🥸"," genalpha friend😏"])
intensity=st.sidebar.slider("SOME NAME",min_value=1,max_value=10,value=5)
if st.sidebar.button("Clear chat"):
     st.session_state.messages=[]
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
with st.chat_message("assistant"):
    st.write(f"Hi,Im' your {personality}")

if user_message:=st.chat_input("say something:"):
        with st.chat_message("user"):
             st.write(user_message)
        st.session_state.messages.append({"role": "user", "content": user_message})
        ai_instructions=f"you are acting as {personality} with an intensity level of{intensity}.Respond to the message sent by user staying completely in character:{user_message}"
        with st.spinner("connecting to the multiverse!........."):
            try:
                response=client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=ai_instructions
                )
                st.success("mesaage received!")
                with st.chat_message("assistant",avatar="😎"):
                    st.write(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("The AI is a bit busy right now — please try again in a moment.")

else:
        st.warning("please type a message first")