import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")  


if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")

genai.configure(api_key=API_KEY)

MODEL = "models/gemini-2.5-pro"
model = genai.GenerativeModel(MODEL)

def ask_llm(prompt: str) -> str:
    try:
        resp = model.generate_content(prompt)
        return resp.candidates[0].content.parts[0].text
    except Exception as e:
        return f"Error contacting Gemini LLM: {e}"
