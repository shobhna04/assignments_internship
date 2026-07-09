import streamlit as it 
import os
from_dotenv import load_dotenv
load_dotenv()
env_var=os.getenv("GEMINI_API_KEY")
print(env_var)