from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from openai import OpenAI
from app.system_prompts import format_lesson_notes,lesson_notes_keys,lesson_notes_titles
import json
import os
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

import requests

engine = create_engine(os.getenv("DB_CONNECTION"))
Session = sessionmaker(bind=engine)

class LessonNotesService:
    def __init__(self,_school_id,_user_id,_lesson_id,_prompt):
        self.school_id = _school_id
        self.user_id = _user_id
        self.lesson_id = _lesson_id
        self.system_prompt = _prompt
        
    async def generate_notes(self,prompt):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                     {"role":"system","content":self.system_prompt},
                     {"role":"user","content":prompt},
                ],
                tools=format_lesson_notes,
                tool_choice={"type": "function", "function": {"name": "FormatLessonNotes"}},
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            if(tool_calls):
                tool_call = tool_calls[0]
                data = json.loads(tool_call.function.arguments)
                result = ""
                for key in lesson_notes_keys:
                     result += f"<h2>{lesson_notes_titles[key]}</h2>{data[key]}"
                await self._process_data(f"<div>{result}</div>")
                await self._update_tenant_tokens(response.usage)
            await self.notify_web_app("completed")
            print("Generated Successfully")
        except Exception as exception:
                print(exception)
                if(str(exception) != "stopped"):
                    await self.notify_web_app("failed")
    async def _process_data(self,data):
        try:
            session = Session()
            session.begin()
            stmt = text(f"UPDATE lesson_notes SET content = :x WHERE id = {self.lesson_id}")
            stmt = stmt.bindparams(x=json.dumps(data))
            session.execute(stmt)
            session.commit()
        except Exception as e:
                session.rollback()
                print("quesry error--------")
                raise e
        finally:
                session.close()

    async def notify_web_app(self,status):
        requests.post(os.getenv("LENON_API")+"/listen-for-gen-status",data = {"type":"notes","status":status,"id":self.lesson_id})

    async def _update_tenant_tokens(self,usage):
            input_credits = usage.prompt_tokens
            output_credits = usage.completion_tokens
            try:
                session = Session()
                session.begin()
                session.execute(text(f"UPDATE generator_credits SET input_credits = input_credits - {input_credits}, output_credits = output_credits - {output_credits} WHERE school_id = {self.school_id}"))
                if self.user_id:
                    session.execute(text(f"UPDATE user_credits SET input_credits = input_credits - {input_credits}, output_credits = output_credits - {output_credits} WHERE user_id = {self.user_id}"))
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
