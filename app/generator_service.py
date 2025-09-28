from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from openai import OpenAI
from app.system_prompts import format_answers
from app.system_prompts import format_answers_to_questions
from PIL import Image
try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False
    print("Warning: PaddleOCR not available, OCR functionality will be disabled")
import base64
from io import BytesIO
import numpy as np
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

import time
import os
import json
import requests

engine = create_engine(os.getenv("DB_CONNECTION"))
Session = sessionmaker(bind=engine)
session = Session()

class GeneratorService:
    def __init__(self, _thread_id,_assistant,_school_id,_user_id,_total,_prompt,_system_prompt,_tools,_tool_name):
        self.thread_id = _thread_id
        self.assistant = _assistant
        self.school_id = _school_id
        self.user_id = _user_id
        self.total_pending = _total
        self.system_prompt = _system_prompt
        self.tools = _tools
        self.tool_name = _tool_name
        self.continue_prompt = f"{_prompt}\nContinue Generating Questions."
    async def generate_questions(self,prompt,old_q=None):
        try:
            print(f"---------------------{self.total_pending} Questions Left--------------")
            messages = [
                     {"role":"system","content":self.system_prompt},
                     {"role":"user","content":prompt}
                ]
            if(old_q):
                messages.append({"role":"user","content":f"These are previously generated questions, duplicate questions are not allowed:\n{old_q}"}, )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=self.tools,
                tool_choice={"type": "function", "function": {"name": self.tool_name}},
            )
            response_message = response.choices[0].message
            generated_questions = []
            tool_calls = response_message.tool_calls
            if(tool_calls):
                for tool_call in tool_calls:
                    input_data = json.loads(tool_call.function.arguments)
                    g = await self._process_data(input_data['questions'])
                    generated_questions.extend(g)
                    await self._update_tenant_tokens(response.usage)
            
            if(self.total_pending>0):
                print("----------------NEXT----------------")
                await self.generate_questions(prompt=self.continue_prompt,old_q=generated_questions)
            else:
                 print("Completed Successfully")
                 await self.notify_web_app("completed")
        except Exception as exception:
                print(exception)
                if(str(exception) != "stopped"):
                    await self.notify_web_app("failed")
    
    async def assistant_generate_questions(self,prompt):
        try:
            print(f"---------------------{self.total_pending} Questions Left--------------")
            client.beta.threads.messages.create(
                self.thread_id,
                role="user",
                content=prompt,
                )
            run = client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant
                )
            while(True):
                run = client.beta.threads.runs.retrieve(
                    thread_id=self.thread_id,
                    run_id=run.id
                    )
                if(run.status == 'requires_action'):
                    print(f"STATUS: {run.status} for RUN: {run.id}")
                    tools = []
                    for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                         tools.append({
                        "tool_call_id": tool_call.id,
                        "output": "success"
                        })
                         
                    run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=run.thread_id,
                    run_id= run.id,
                    tool_outputs=tools
                    )
                    input_data = json.loads(tool_call.function.arguments)
                    await self._process_data(input_data['questions'])
                if(run.status == 'completed'):
                    print(run.usage)
                    # thread_messages = client.beta.threads.messages.list(thread_id=run.thread_id,run_id=run.id,limit=1,order="desc")
                    await self._update_tenant_tokens(run.usage)
                    if(self.total_pending<=0):
                        print("Completed Successfully")
                        await self.notify_web_app("completed")
                    break
                if(run.status == 'cancelled' or run.status=='expired' or run.status=='failed'):
                    print(run.usage)
                    await self._update_tenant_tokens(run.usage)
                    print("Retrying----------------")
                    break
            if(self.total_pending>0):
                time.sleep(5)
                print("----------------NEXT----------------")
                await self.generate_questions(prompt=self.continue_prompt)
        except Exception as exception:
                print(exception)
                client.beta.threads.runs.cancel(
                thread_id=self.thread_id,
                run_id=run.id
                )
                if(str(exception) != "stopped"):
                    await self.notify_web_app("failed")
    async def generate_answers_to_questions(self,answer):
        messages = [
            {"role":"user","content":[
                {
                    "type":"text",
                    "text": f"This image contains a list of {self.total_pending} multiple choice answers from A - E, generate an array of objects from the image, each object has a field called 'answer'. If the image does not look like what is described, return and empty string for each answer in the array.",
                },{
                    "type":"image_url",
                    "image_url":{"url":answer}
                }
            ]}
        ]
        print("Processing Request")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=format_answers_to_questions,
            tool_choice={"type": "function", "function": {"name": "FormatAnswersToQuestions"}},
        )
        print("Received Response")
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        data = None
        if(tool_calls):
            for tool_call in tool_calls:
                input_data = json.loads(tool_call.function.arguments)
                await self._update_tenant_tokens(response.usage)
                # if(len(input_data['answers'])==int(self.total_pending)):
                data = input_data["answers"]
        print("Generated Answers")
        return data
    async def _generate_answer_from_image(self,prompt,answer):
        messages = [
            {"role":"user","content":[
                {
                    "type":"text",
                    "text": prompt,
                },
                {
                    "type":"image_url",
                    "image_url":{"url":answer["b64"]}
                }
            ]}
        ]
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=messages,
            tools=format_answers,
            tool_choice={"type": "function", "function": {"name": "FormatAnswers"}},
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        if(tool_calls):
            for tool_call in tool_calls:
                input_data = json.loads(tool_call.function.arguments)
                await self._update_tenant_tokens(response.usage)
                input_data['path'] = answer['path']
                await self._process_answers(input_data)
        print("Generated for Image")
    async def _extract_text(self,data):
        if not PADDLEOCR_AVAILABLE:
            print("PaddleOCR not available, skipping OCR extraction")
            return ""
        
        try:
            # Initialize PaddleOCR with CPU-only mode to prevent segfaults
            ocr = PaddleOCR(lang='en', use_angle_cls=True, use_gpu=False, show_log=False)
            data = data.split(',')[1]
            decoded_bytes = base64.b64decode(data)
            result = ocr.ocr(decoded_bytes, cls=True)
            if result and result[0]:
                inner_result = result[0]
                data = ""
                for res in inner_result:
                    if res and len(res) > 1 and res[1]:
                        data += "\n"+res[1][0]
            return data
        except Exception as e:
            print(f"OCR extraction failed: {e}")
            return ""
    
    async def parse_questions(self,prompt,questions,answers,total):
        print(f"---------------------Parsing Questions--------------")
        try:
            messages = [
                     {"role":"system","content":prompt},
                     {"role":"user","content":f"QUESTIONS\n{questions}\n\nANSWERS\n{answers}\n\nTOTAL QUESTIONS\n{total}"}
                ]
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=self.tools,
                tool_choice={"type": "function", "function": {"name": self.tool_name}},
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            if(tool_calls):
                for tool_call in tool_calls:
                    input_data = json.loads(tool_call.function.arguments)
                    await self._process_parsed_data(input_data['questions'])
                    await self._update_tenant_tokens(response.usage)
            else:
                 print("Completed Successfully")
                 await self.notify_web_app("completed")
        except Exception as exception:
                print(exception)
                if(str(exception) != "stopped"):
                    await self.notify_web_app("failed")
    async def parse_answers(self,prompt,answers):
                try:
                    for answer in answers:
                        # extract text from image
                        content = await self._extract_text(answer["b64"])
                        # add text to image for processing by gpt
                        await self._generate_answer_from_image(prompt+"\n\n"+content,answer)
                    await self.notify_web_app("completed","answers")
                    return True
                except Exception as exception:
                    print(exception)
                    await self.notify_web_app("failed","answers")
                    return False
    async def _process_parsed_data(self,questionsToSave)->list:
        try:
            session.begin()
            row = session.execute(text(f"SELECT * FROM user_threads WHERE id = {self.thread_id} LIMIT 1")).fetchone()
            thread = row._asdict()
            if not thread:
                return
            status = "completed"
            self.total_pending = 0
            stmt = text(f"UPDATE user_threads SET progress = {self.total_pending},status = '{status}', questions = :x WHERE id = {self.thread_id}")
            stmt = stmt.bindparams(x=json.dumps(questionsToSave))
            session.execute(stmt)
            session.commit()
            if status == "stopped":
                raise ValueError("stopped")
            return questionsToSave
        except Exception as e:
                session.rollback()
                print("quesry error--------")
                raise e
        finally:
             session.close()
    async def _process_data(self,data)->list:
        try:
            session.begin()
            row = session.execute(text(f"SELECT * FROM user_threads WHERE id = {self.thread_id} LIMIT 1")).fetchone()
            thread = row._asdict()
            if not thread:
                return
            jsonData = data
            questionsToSave = []
            if thread['questions']:
                questionsFromDB = json.loads(thread['questions'])
                questionsToSave.extend(questionsFromDB)
            questionsToSave.extend(jsonData)
            total = len(jsonData)
            self.total_pending = self.total_pending - total
            print(f"----------------{total} Questions Generated-------------")
            status = thread['status']
            if self.total_pending <= 0:
                status = "completed"
                self.total_pending = 0
            stmt = text(f"UPDATE user_threads SET progress = {self.total_pending},status = '{status}', questions = :x WHERE id = {self.thread_id}")
            stmt = stmt.bindparams(x=json.dumps(questionsToSave))
            session.execute(stmt)
            session.commit()
            if status == "stopped":
                raise ValueError("stopped")
            return questionsToSave
        except Exception as e:
                session.rollback()
                print("quesry error--------")
                raise e
        finally:
             session.close()
    
    async def _process_answers(self,data):
        try:
            session.begin()
            stmt = text("""
    INSERT INTO answers (marker_id, student_id, school_id,original_answer_sheet_path, choices,created_at,updated_at) 
    VALUES (:marker_id, :student_id, :school_id, :original_answer_sheet_path, :choices,NOW(),NOW())
    ON DUPLICATE KEY UPDATE 
        original_answer_sheet_path = VALUES(original_answer_sheet_path),
        choices = VALUES(choices),
        status = 'marked',
        updated_at = NOW()
        """)
            stmt = stmt.bindparams(marker_id=data['code'],student_id=data['id'],school_id=self.school_id,original_answer_sheet_path=data['path'],choices=json.dumps(data['answers']))
            session.execute(stmt)
            session.commit()
        except Exception as e:
                session.rollback()
                print("quesry error--------")
        finally:
            session.close()
        
    async def notify_web_app(self,status,req_type="questions"):
        requests.post(os.getenv("LENON_API")+"/listen-for-gen-status",data = {"type":req_type,"status":status,"id":self.thread_id})

    async def _update_tenant_tokens(self,usage):
            input_credits = usage.prompt_tokens
            output_credits = usage.completion_tokens
            try:
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
