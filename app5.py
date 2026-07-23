import streamlit as st
import requests
from urllib.parse import quote

st.title("🤖THE AI IMAGE STUDIO🤖")
st.sidebar.header("Settings")

imagetype = st.sidebar.selectbox("select your image type", ["photorealistic", "ghibli style", "black and white", "cartoon style"])
imagewidth = st.sidebar.slider("Image width", min_value=256, max_value=1024, value=768)
imageheight = st.sidebar.slider("Image height", min_value=256, max_value=1024, value=768)

user_prompt = st.text_input("Describe the image you want to generate")

if st.button("Generate image"):
    if user_prompt:
        with st.spinner("Rendering the image..."):
            full_prompt = f"{user_prompt}, art style: {imagetype}, width {imagewidth}, height {imageheight}"
            encoded_prompt = quote(full_prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={imagewidth}&height={imageheight}"
            response = requests.get(url)

            if response.status_code == 200:
                st.success("Image generated")
                st.image(response.content, caption=full_prompt)
                st.download_button(
                    label="Download image",
                    data=response.content,
                    file_name="my ai image.png",
                    #multipopose internet mail extension
                    mime="image/png"
                )
            else:
                st.error("API is not working")
    else:
        st.warning("Please enter a description first.")