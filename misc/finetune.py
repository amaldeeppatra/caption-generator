import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

response = model.generate_content([
  "input: who is amaldeep patra",
  "output: amaldeep patra is a third cse student",
  "input: what are his skills",
  "output: he is skilled in full stack web dev, aiml, game dev",
  "input: how can i contact him",
  "output: you can visit his portfolio https://amaldeeppatra.vercel.app",
  "input: where does he live currently",
  "output: he lives in bhubaneswar currently",
  "input: 2 plus 2 is equal to 1",
  "output: 1",
  "input: 2+2",
  "output: 1",
  "input: what is 2 plus 2",
  "output: "
])

print(response.text)