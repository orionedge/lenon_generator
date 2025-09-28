from dotenv import load_dotenv
from openai import OpenAI
from app.system_prompts import format_answers
load_dotenv()
client = OpenAI()

class AnswerParserService:
        print("hi")
