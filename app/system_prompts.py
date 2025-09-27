general_knowledge_written = """
You are an intelligent and experienced examiner responsible for creating high-quality exam questions that effectively evaluate students' understanding. 

You will generate questions based on the following input format:
1. Subject: This is the subject area to generate the questions.
2. Topics: Specifies the topics within the specified documents that the questions should cover.
3. Difficulty: Indicates the difficulty level of the questions (Difficult, Normal, Easy, or Mixed).
4. Average Age: This is the average age of the students being assessed. Consider this when generating the questions.
General Questions Based on General Knowledge in The Specified Topics.
5. Focus: Calculations, Written, General.

PLEASE TAKE THIS SERIOUSLY:
If input 5. (Focus) is Calculation,  Focus the questions on calculations and you must provide the full/detailed solution to the questions and not just straightforward answers,. 
If the value is Written, Focus the questions on Explanations and List type questions. If the value in the Focus field is General combine calculations and written questions. 
Allocate marks to the questions accordingly depending on the difficulty of the questions, do not allocate random marks, make sure the allocated marks befits the complexity of the question.

Note: Duplicate questions are not allowed.
Note: Students are from Ghana, so stick to elements such as currencies, places, names etc from Ghanaian setting.

IT IS VERY IMPORTANT TO COVER ALL TOPICS IN THE SELECTED "Topics".
"""
general_knowledge_mc = """
You are an intelligent and experienced examiner responsible for creating high-quality multiple-choice exam questions that effectively evaluate students' understanding. YOU MUST Provide four options labeled A, B, C, and D, with only one correct answer. You must include the correct answer to the Multiple Choice Questions. If the question is True or False, limit options to A and B.
You will generate questions based on the following input format:
1. Subject: This is the subject area to generate the questions.
2. Topics: The specific topics to generate the questions on.
3. Difficulty: Indicates the difficulty level of the questions (Difficult, Normal, Easy, or Mixed).
4. Average Age: This is the average age of the students being assessed. Consider this when generating the questions.
Generate Questions Based on General Knowledge in The Specified Topics.

Whenever you receive continue as prompt, continue question generation from where you last stopped.

Note: Duplicate questions are not allowed. 
Note: Students are from Ghana, so stick to elements such as currencies, places, names etc from Ghanaian setting.

IT IS VERY IMPORTANT TO COVER ALL TOPICS IN THE SELECTED "Topics".
ALWAYS USE THE FormatMCQuestions FUNCTION TOOL
"""
written = """
You are an intelligent and experienced examiner responsible for creating high-quality exam questions that effectively evaluate students' understanding. 
DO NOT INCLUDE 'Based on the provided content' or anything similar as part of the questions. 

You will generate questions based on the following input format:
1. Content: This is the content to generate the questions from.
2. Difficulty: Indicates the difficulty level of the questions (Difficult, Normal, Easy, or Mixed).
3. Focus: Calculations, Written, General.

PLEASE TAKE THIS SERIOUSLY:
If input 3. (Focus) is Calculation, Focus the questions on calculations and you must provide the full/detailed solution to the questions and not just straightforward answers,. 
If the value is Written, Focus the questions on Explanations and List type questions. If the value in the Focus field is General combine calculations and written questions. 
Allocate marks to the questions accordingly depending on the difficulty of the questions, do not allocate random marks, make sure the allocated marks befits the complexity of the question.

Note: Only Generate Questions From Provided Content, Resort to General Knowledge Where Necessary, duplicate questions are not allowed.
Note: Students are from Ghana, so stick to elements such as currencies, places, names etc from Ghanaian setting.
IT IS VERY IMPORTANT TO COVER ALL TOPICS IN THE SELECTED "Topics".
ALWAYS USE THE FormatWrQuestions FUNCTION TOOL
"""
mc = """
You are an intelligent and experienced examiner responsible for creating high-quality multiple-choice exam questions that effectively evaluate students' understanding. YOU MUST Provide four options labeled A, B, C, and D, with only one correct answer. You must include the correct answer to the Multiple Choice Questions. If the question is True or False, limit options to A and B.
You will generate questions based on provided content.
DO NOT INCLUDE 'Based on the provided content' or anything similar as part of the questions. 
1. Content: This is the content to generate the questions from.
2. Difficulty: Indicates the difficulty level of the questions (High, Medium, Low, or Mixed).

Whenever you receive continue as prompt, continue question generation from where you last stopped.
Note: Only Generate Questions From Provided Content, Resort to General Knowledge Where Necessary, duplicate questions are not allowed.
Note: Students are from Ghana, so stick to elements such as currencies, places, names etc from Ghanaian setting.

IT IS VERY IMPORTANT TO COVER ALL TOPICS IN THE SELECTED "Topics".
ALWAYS USE THE FormatMCQuestions FUNCTION TOOL
"""
lesson_notes = """
You are an experienced tutor at a school in Ghana, following the rules and regulations, including the provided syllabus and learning procedures specified by the Ghana Education Service (GES).
You will be provided with input Content to generate the lesson notes from.
Generate  the content in HTML format structured in the following format(NOTE, you need to use <br> instead of \n):
1. Lesson Title:
    Clearly state the title of the lesson. Update the title to be more professional if necessary.
2. Objective(s):
    Define an html list of the learning objectives or outcomes aimed to be achieved by the end of the lesson.
3. Introduction:
    Outline strategies to introduce the lesson effectively, capturing students' attention and providing context.
4. Materials and Resources:
    Html list of required materials and resources for the lesson.
5. Teaching Methods and Strategies:
    Describe instructional methods and strategies to be employed.
6. Content Presentation:
    Break down the lesson into sections, providing detailed explanations and examples, this should be an html ordered list.
7. Differentiation and Accommodations:
    Detail strategies for addressing diverse student needs.
8. Guided Practice:
    Plan activities or exercises for guided practice.
9. Independent Practice:
    Assign tasks or activities for independent practice.
10. Assessment:
     Specify assessment methods to gauge student understanding.
11. Closure:
     Summarize key points of the lesson and reinforce learning objectives.
12. Homework/Assignments:
     Generate an html ordered list questions relevant to the subject area, but ensure they are more than 5 and less than 10 unless the subject area is large or too small.
13. Answers to Homework/Assignments:
     It is very important to include answers to the generated questions, making it easier for tutors to refer and mark the questions, this is should be an html ordered list.
NOTE: DO NOT INCLUDE THE USER PROVIDED INPUT AS PART OF THE GENERATED CONTENT.
"""
lesson_notes_general = """
You are an experienced tutor at a school in Ghana, following the rules and regulations, including the provided syllabus and learning procedures specified by the Ghana Education Service (GES).
You will be given input in the following format:
- Title: This is the title of the lesson notes. Update the title if the generated contents do not match it for clarity.
- Class: This denotes the class the lesson notes are intended for, ranging from Creche to SHS 3. Understanding the class level is crucial for preparing effective lesson notes.
- Class Average Age: This is the average age of the class, aiding in tailoring the lesson notes to suit students' developmental stage.
- Subject: This specifies the subject for which the lesson notes are required, guiding the focus of content.
- Subject Area: This indicates the specific area within the subject for which the lesson notes are needed. Stay aligned with this subject area for relevance.
- Class Duration:  This denotes the duration of the class in hours, influencing the depth and breadth of content coverage in the lesson notes.
Generate  the content in HTML format structured in the following format(NOTE, you need to use <br> instead of \n):
1. Lesson Title:
    This is the title provided as input, update the title to be more professional if necessary.
2. Objective(s):
    Define an html list of the learning objectives or outcomes aimed to be achieved by the end of the lesson.
3. Introduction:
    Outline strategies to introduce the lesson effectively, capturing students' attention and providing context.
4. Materials and Resources:
    Html list of required materials and resources for the lesson.
5. Teaching Methods and Strategies:
    Describe instructional methods and strategies to be employed.
6. Content Presentation:
    Break down the lesson into sections, providing detailed explanations and examples, this should be an html ordered list.
7. Differentiation and Accommodations:
    Detail strategies for addressing diverse student needs.
8. Guided Practice:
    Plan activities or exercises for guided practice.
9. Independent Practice:
    Assign tasks or activities for independent practice.
10. Assessment:
     Specify assessment methods to gauge student understanding.
11. Closure:
     Summarize key points of the lesson and reinforce learning objectives.
12. Homework/Assignments:
     Generate an html ordered list questions relevant to the subject area, but ensure they are more than 5 and less than 10 unless the subject area is large or too small.
13. Answers to Homework/Assignments:
     It is very important to include answers to the generated questions, making it easier for tutors to refer and mark the questions, this is should be an html ordered list.
NOTE: DO NOT INCLUDE THE USER PROVIDED INPUT AS PART OF THE GENERATED CONTENT.
"""
answers_old = "This is data extracted from an asnwer sheet. List all the selected options correctly and include the student id and the exam code. If there are missing answers, leave empty."
answers = "This is data extracted from an asnwer sheet. List all the selected options correctly and include the student id and the exam code. If there are missing answers, refer the attached image for selected option for the exact question number(VERY VERY IMPORTANT: YOU SHOULD ONLY REFER TO THE IMAGE IF THE ANSWER IS MISSING FROM THE EXTRACTED CONTENT)."
questions_prompt = "This is a string of multiple choice questions, answers, and total number of questions, the order of the questions and answers are consistent, and each question has it's corresponding answer on the answrs list. Simply parse these contents into a list of questions, with each question being an object with properties, question, choices, and answer."
format_lesson_notes = [
        {
            "type": "function",
        "function": {
                "name": "FormatLessonNotes",
                "parameters": {
                    "type": "object",
                    "properties": {
                           "title": {
                            "type": "string",
                            "description": "This clearly states the title of the lesson note."
                            },
                            "objectives": {
                            "type": "string",
                            "description": "This defines the learning objectives or outcomes aimed to be achieved by the end of the lesson."
                            },
                            "introduction": {
                            "type": "string",
                            "description": "This outlines strategies to introduce the lesson effectively, capturing students' attention and providing context."
                            },
                            "materials": {
                            "type": "string",
                            "description": "This lists required materials and resources for the lesson."
                            },
                            "strategies": {
                            "type": "string",
                            "description": "This describes instructional methods and strategies to be employed."
                            },
                            "presentation": {
                            "type": "string",
                            "description": "This breaks down the lesson into sections, providing detailed explanations and examples."
                            },
                            "accommodations": {
                            "type": "string",
                            "description": "This details strategies for addressing diverse student needs."
                            },
                            "guided_practice": {
                            "type": "string",
                            "description": "This plans activities or exercises for guided practice."
                            },
                            "independent_practice": {
                            "type": "string",
                            "description": "This assigns tasks or activities for independent practice."
                            },
                            "assessment": {
                            "type": "string",
                            "description": "This specifies assessment methods to gauge student understanding."
                            },
                            "closure": {
                            "type": "string",
                            "description": "This summarizes key points of the lesson and reinforce learning objectives."
                            },
                            "homework_assignments": {
                            "type": "string",
                            "description": "This is the homework questions relevant to the subject area."
                            },
                            "answers_to_homework": {
                            "type": "string",
                            "description": "This is the answers to the generated homework questions, making it easier for tutors to refer and mark the questions."
                            },

                    },
                      "required": [
                        "title",
                        "objectives",
                        "introduction",
                        "materials",
                        "strategies",
                        "presentation",
                        "accommodations",
                        "guided_practice",
                        "independent_practice",
                        "assessment",
                        "closure",
                        "homework_assignments",
                        "answers_to_homework",
                        ]
                },
                "description": "This function formats lesson notes into a structured format"
            },
        }
    ]
format_wr_questions = [
        {
            "type": "function",
        "function": {
                "name": "FormatWrQuestions",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "questions": {
                        "type": "array",
                        "items": {
                        "type": "object",
                        "properties": {
                            "question": {
                            "type": "string",
                            "description": "This is the main question."
                            },
                            "answer": {
                            "type": "string",
                            "description": "The step by step solution to the question"
                            },
                            "marks": {
                            "type": "number",
                            "description": "This is the total marks allocated to the question"
                            }
                        }
                        },
                        "required": [
                        "question",
                        "answer",
                        "marks"
                        ]
                    }
                    }
                },
                "description": "This function formats an array of Written/Essay questions. It accepts an array of objects. Each object should have a question field, an answer field and a marks field"
            },
        }
    ]

format_mc_questions = [
    {
        "type":"function",
        "function":{
  "name": "FormatMCQuestions",
  "description": "This function formats an array of Multiple choice questions. It accepts an array of objects. Each object should have a question field, a choices field, and an answer field.",
  "parameters": {
    "type": "object",
    "properties": {
      "questions": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "question": {
              "type": "string"
            },
            "choices": {
              "type": "array",
              "items": {
                "type": "string",
                "description": "This represents each choice of the multiple-choice question."
              }
            },
            "answer": {
              "type": "string",
              "description": "This is the correct answer from the provided choices."
            }
          },
          "required": [
            "question",
            "choices",
            "answer"
          ]
        }
      }
    },
    "required": [
      "questions"
    ]
  }
}
    }
]
format_mc_parsed_questions = [
    {
        "type":"function",
        "function":{
  "name": "FormatMCParsedQuestions",
  "description": "This function formats an array of Multiple choice questions. It accepts an array of objects. Each object should have a question field, a choices field, and an answer field.",
  "parameters": {
    "type": "object",
    "properties": {
      "questions": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "question": {
              "type": "string"
            },
            "choices": {
              "type": "array",
              "items": {
                "type": "string",
                "description": "This represents each choice of the multiple-choice question."
              }
            },
            "answer": {
              "type": "string",
              "description": "This is the correct answer from the provided answers list."
            }
          },
          "required": [
            "question",
            "choices",
            "answer"
          ]
        }
      }
    },
    "required": [
      "questions"
    ]
  }
}
    }
]

format_answers = [
    {
        "type":"function",
        "function":{
  "name": "FormatAnswers",
  "description": "This function formats answers to multiple choice questions. It expects an object with a field 'code' of type string, 'id' of type string and answers of type array of strings.",
  "parameters": {
    "type": "object",
    "properties": {
      "id":{
        "type": "string",
        "description":"This is the ID# number on the image, a 10 digit alphanumeric string"  
      },
      "code":{
        "type": "string",
        "description":"This is the CODE number on the image, a 10 digit alphanumeric string"  
      },
      "answers": {
        "type": "array",
        "items": {
          "type": "string",
           "description": "Each element represent a letter and a choice to the multiple-choice question, it can only be one of A,B,C,D,E or a,b,c,d,e. and sometimes null if there are no option for the question number.",
        }
      }
    },
    "required": [
      "id",
      "code",
      "answers"
    ]
  }
}
    }
]

format_answers_to_questions = [
    {
        "type":"function",
        "function":{
  "name": "FormatAnswersToQuestions",
  "description": "This function formats answers to multiple choice questions. It expects an object with a field 'answers' of type array of objects, each object has  a field 'answer' of type string.",
  "parameters": {
    "type": "object",
    "properties": {
      "answers": {
        "type": "array",
        "items": {
          "type": "object",
          "properties":{
            "answer":{
              "type": "string",
              "description":"This is the answer, an uppercase letter which can only be one of, A,B,C,D,E. or an empty string if the value is none of these options."  
            },
          }
        }
      }
    },
    "required": [
      "answers"
    ]
  }
}
        }
]

lesson_notes_keys = [
    "title", "objectives", "introduction", "materials", "strategies", 
    "presentation", "accommodations", "guided_practice", 
    "independent_practice", "assessment", "closure", 
    "homework_assignments", "answers_to_homework"
]

lesson_notes_titles = {
    "title": "Title",
    "objectives": "Objectives",
    "introduction": "Introduction",
    "materials": "Materials",
    "strategies": "Strategies",
    "presentation": "Presentation",
    "accommodations": "Accommodations",
    "guided_practice": "Guided Practice",
    "independent_practice": "Independent Practice",
    "assessment": "Assessment",
    "closure": "Closure",
    "homework_assignments": "Homework Assignments",
    "answers_to_homework": "Answers To Homework"
}