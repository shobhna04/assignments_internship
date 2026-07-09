import streamlit as st
st.title("BLACK HOLE")
st.write("welcome to the world of uncertainaities")
user_name=st.text_input("Write your name ")
user_message=st.text_input("Write a message ")
if st.button("TRANSIT"):
    if not user_name:
        st.error("please enter your name")
    elif not user_message:
        st.warning("enter you message")
    else:
        st.success(f"Transmission Successful! Greetings, We received your name : {user_name} and your message: {user_message}")
        char_count=len(user_message)
        token_count=char_count//4
        st.info(f"System Check: Your message will consume approximately {token_count} tokens from our context window.") 