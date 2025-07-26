import os
import google.generativeai as genai

# Get the Gemini API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

# Raise an error if the API key is not set
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")

# Configure the Gemini API with the key
genai.configure(api_key=API_KEY)

# Define the model to use
MODEL = "models/gemini-2.5-pro"
model = genai.GenerativeModel(MODEL)

def ask_llm(prompt: str) -> str:
    """
    Sends a prompt to the Gemini LLM and retrieves the response.

    Args:
        prompt (str): The prompt string to send to the model.

    Returns:
        str: The generated response from the model, or an error message if something fails.
    """
    try:
        # Generate content from the prompt
        resp = model.generate_content(prompt)
        return resp.candidates[0].content.parts[0].text
    except Exception as e:
        # Return error message in case of failure
        return f"Error contacting Gemini LLM: {e}"
