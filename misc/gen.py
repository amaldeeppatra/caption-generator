import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

prompt = ""

result = model.generate_content([prompt])

print(result.text)