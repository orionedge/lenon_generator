from fastapi import FastAPI, Request,HTTPException,BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from generator_service import GeneratorService
from lesson_notes_service import LessonNotesService
from uploader_service import UploaderService
from answer_parser_service import AnswerParserService
from fastapi.responses import JSONResponse
from system_prompts import questions_prompt,answers,lesson_notes_general,lesson_notes,format_mc_parsed_questions,format_mc_questions,format_wr_questions,general_knowledge_mc,general_knowledge_written,mc,written
import asyncio
app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
async def notify_lenon_on_generation_status(data):
    print("not implemented")

@app.post("/api/generate-lesson-notes")
async def generate_lesson_notes(request: Request):
    data = await request.json()
    if (data!=None and data['id'] != None):
            subject = data['subject']
            title = data['title']
            class_name = data['class']
            topics = data['subject_area']
            duration = data['lesson_duration']
            average_age = data['average_age']
            documents = data['file_ids']
            lesson_id = data['id']
            school_id = data['school_id']
            user_id = data['user_id']
            system_prompt = lesson_notes if(documents and len(documents)>0) else lesson_notes_general
            user_input = f"TITLE: {title},Class: {class_name},Class Average Age: {average_age},Subject: {subject},Subject Area: {topics},Class Duration:{duration}"
            content = f"Generate Lesson Notes with the INPUT: {user_input}";            
            relevant_docs = ""
            if(documents != None):
                for document_id in documents:
                    u = UploaderService(document_id)
                    query = f"Retrieve all relevant documents on the toipcs/areas: {topics}, these documents will be used to generate lesson notes for teaching students."
                    relevant_docs += u.get_relevant_documents(query)+"\n"

            if(relevant_docs != ""):
                content = f"Generate lesson notes for the purposes of teaching students based on the INPUT:\nTITLE: {title}\nCONTENT:\n{relevant_docs}." 
            
            c = LessonNotesService(school_id,user_id,lesson_id,system_prompt)
            loop = asyncio.get_event_loop()
            loop.create_task(c.generate_notes(prompt=content))         
            return "Generation is in progress"
    else:
        raise HTTPException(status_code=422,detail="Invalid Data")
    
@app.post("/api/generate-questions")
async def generate_questions(request: Request):
    data = await request.json()
    assistant = request.headers.get("X-Lena-Assistant")
    if (data!=None and data['id'] != None):
            qtype = "multiple choice"
            question_type = data['type']
            subject = data['subject']
            focus = data['focus']
            topics = data['topics']
            average_age = data['average_age']
            difficulty = data['difficulty']
            documents = data['file_ids']
            total_questions = data['total_questions']
            thread_id = data['id']
            school_id = data['school_id']
            user_id = data['user_id']
            focus_content = ""
            system_prompt = mc if (documents!=None and len(documents)>0) else general_knowledge_mc
            tools = format_mc_questions
            tool_name = "FormatMCQuestions"
            if(question_type=='wr'):
                system_prompt = written if (documents!=None and len(documents)>0) else general_knowledge_written
                tools = format_wr_questions
                tool_name = "FormatWrQuestions"
                focus_content = f"\n5.Focus: {focus}"
                qtype = f"{focus}"
            content = f"Generate {qtype} questions based on the following input:\n1.Subject: {subject}\n2.Topics: {topics}\n3.Difficulty: {difficulty}\n4.Average Age: {average_age}{focus_content}"
            
            relevant_docs = ""
            if(documents != None):
                for document_id in documents:
                    u = UploaderService(document_id)
                    query = f"I want to generate {qtype} questions on the subject area {topics}."
                    relevant_docs += u.get_relevant_documents(query)+"\n"

            if(relevant_docs != ""):
                content = f"Generate {qtype} questions based on the input:\nContent:{relevant_docs}\n2.Difficulty: {difficulty}." 
            c = GeneratorService(thread_id,assistant,school_id,user_id,total_questions,content,system_prompt,tools,tool_name)
            loop = asyncio.get_event_loop()
            loop.create_task(c.generate_questions(prompt=content))         
            return "Generation is in progress"
    else:
        raise HTTPException(status_code=422,detail="Invalid Data")

@app.post("/api/upload-document")
async def upload_documents(request: Request):
    data = await request.json()
    u = UploaderService(data['document_id'])
    res = await u.upload_document(data['path'],data['type'])
    if(res):
        return "Uploaded Successfully"
    raise HTTPException(status_code=500, detail="Upload Failed")

@app.post("/api/parse-custom-questions")
async def upload_documents(request: Request):
    data = await request.json()
    u = GeneratorService(data['thread_id'],'',data['school_id'],'','','','',format_mc_parsed_questions,'FormatMCParsedQuestions')
    loop = asyncio.get_event_loop()
    loop.create_task(u.parse_questions(questions_prompt,data['questions'],data['answers'],data['total']))         
    return "Parsing is in progress"

@app.delete("/api/delete-document/{document_id}")
async def delete_documents(document_id):
    u = UploaderService(document_id)
    res = u.delete_document()
    if(res):
        return "Deleted Successfully"
    raise HTTPException(status_code=500, detail="Deletion Failed")

@app.post("/api/upload-answer-booklets")
async def upload_answers(request: Request):
    data = await request.json()
    u = GeneratorService('','',data['school_id'],'','','','','','')
    loop = asyncio.get_event_loop()
    loop.create_task(u.parse_answers(f"{answers}  The total number of answers in the list is exactly {data['total']}.",data['booklets']))         
    return "Generation is in progress"

@app.post("/api/upload-answers-to-questions")
async def upload_answers(request: Request):
    data = await request.json()
    u = GeneratorService("","",data['school_id'],data["user_id"],"","","","","")
    res = await u.generate_answers_to_questions(data['answer'])
    if(res):
        return res
    raise HTTPException(status_code=500, detail="Upload Failed")
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)