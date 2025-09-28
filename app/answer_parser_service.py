from dotenv import load_dotenv
from openai import OpenAI
from app.system_prompts import format_answers
import os
load_dotenv()

def get_openai_client():
    """Get OpenAI client with proper API key handling"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)

class AnswerParserService:
        print("hi")
