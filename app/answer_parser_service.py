from dotenv import load_dotenv
from openai import OpenAI
from app.system_prompts import format_answers
import os
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AnswerParserService:
        print("hi")
