import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMMA_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMMA_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

# Create model instance
model = genai.GenerativeModel(
    model_name="gemma-3-27b-it",
    generation_config={
        "temperature": 0.3,
        "top_p": 0.9,
        "max_output_tokens": 512
    }
)

def call_gemma(messages):
    """
    messages = [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "..."}
    ]
    """

    # Gemini does not support system/user roles directly
    # We merge them safely
    combined_prompt = ""

    for msg in messages:
        combined_prompt += msg["content"].strip() + "\n\n"

    response = model.generate_content(combined_prompt)

    return response.text.strip()

