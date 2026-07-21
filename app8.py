import streamlit as st 
import os
import json 
import requests

import urllib.parse
import io 
from gtts import gTTS
from dotenv import load_dotenv
from google import genai 
load_dotenv()
st.set_page_config(page_title="AI VISUAL NOVEL",page_icon="📖",layout="wide")
st.title("AI VISUAL NOVEL 📖")

@st.cache_resource
def get_ai_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
client=get_ai_client()

def generate_image(prompt):
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content
    except Exception as e:
        st.toast("Image server is busy, skipping visual...")
        return None
def generate_audio(text):
    try:
        tts = gTTS(text=text, lang="en")
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        st.toast("Narration failed, continuing without audio...")
        return None
def parse_story_response(response_text):
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        st.toast("The AI sent a malformed response, please try again...")
        return None
with st.sidebar:
    st.markdown("### Story Settings")
    genre=st.selectbox("Story genre",["Fantasy","Sci-fi","Horror","Mystery"])
    art_style=st.selectbox("Art style",["anime","realistic","Pixel art","watercolor"])
    st.write("Genre selected:",genre)
    st.write("Art style:",art_style)
    image_width = st.slider("Image size", min_value=200, max_value=800, value=500)
SYSTEM_PROMPT=f""" you are a visual novel narrator for a {genre}story .
    Every time you reply reply with a JSON object — no extra text, no markdown code fences, nothing before or after it.

    The JSON must have exactly these three keys
    1. "story_text": a short narrative paragraph continuing the story (2-4 sentences).
2. "image_prompt": a detailed visual description for an AI image generator, in the style of {art_style}.
3. "options": a list of exactly 3 short strings representing what the user can choose to do next.

Example format:
{{"story_text": "...", "image_prompt": "...", "options": ["...", "...", "..."]}}
"""
    
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat=client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction":SYSTEM_PROMPT}
                    )
if "story_data" not in st.session_state:
    st.session_state.story_data=None
if st.session_state.story_data is None:
   if st.button("Begin story"):
     try:
        response=st.session_state.gemini_chat.send_message("Start of the story")
        data = parse_story_response(response.text)
        if data is not None:
             st.session_state.story_data = data
             st.session_state.story_image = generate_image(data["image_prompt"])
             st.session_state.story_audio = generate_audio(data["story_text"])
     except Exception as e:
          st.toast("The story engine is busy, please try again in a moment...")
def parse_story_response(response_text):
    try:
       return json.loads(response_text)
    except json.JSONDecodeError:
       st.toast("The AI sent a malformed response, please try again...")
       return None


if st.session_state.story_data is not None:
   story=st.session_state.story_data
   if st.session_state.story_image is not None:
       st.image(st.session_state.story_image, width=image_width)
   st.write(story["story_text"])
   if st.session_state.story_audio is not None:
       st.audio(st.session_state.story_audio)
   for option in story["options"]:
     if st.button(option):
        try:
            response = st.session_state.gemini_chat.send_message(option)
            data = parse_story_response(response.text)
            if data is not None:
              st.session_state.story_data = data
              st.session_state.story_image = generate_image(data["image_prompt"])
              st.session_state.story_audio = generate_audio(data["story_text"])
              st.rerun()
        except Exception as e:
            st.toast("The story engine is busy, please try again in a moment...")

