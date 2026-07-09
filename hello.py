from google import genai 
import os
from dotenv import load_dotenv
load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
response=client.models.generate_content(
    model="gemini-2.5-flash",
    contents="explain to me how does a gemini api work in one semtence"
)
print(response)