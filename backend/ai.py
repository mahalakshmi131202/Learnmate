import os
import re
from google import genai
from dotenv import load_dotenv
load_dotenv() 

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def clean_text(text: str) -> str:
    text = re.sub(r"\*\*", "", text)   # remove bold 
    text = re.sub(r"\*", "", text)     # remove * 
    text = re.sub(r"#+", "", text)     # remove headings
    text = re.sub(r"\n\s*\n", "\n", text)  # remove extra empty lines
    return text.strip()

def generate_ai_response(question_text: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Answer the following student question in a short and simple academic way. Keep the answer within 60 to 90 words: {question_text}"
        )

        if response and response.text:
            return clean_text(response.text)

        return "Unable to generate response at the moment. Please try again."

    except Exception:
        return "AI service is temporarily unavailable. Please try again later."
