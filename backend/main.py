from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from backend.ai import generate_ai_response
from backend.firebase_db import save_question_to_firebase

app = FastAPI(title="LearnMate API")

questions_db: List[dict] = []

class Question(BaseModel):
    student_name: str
    question_text: str

@app.get("/")
def root():
    return {"message": "LearnMate backend running"}

@app.post("/submit-question")
def submit_question(question: Question):

    ai_answer = generate_ai_response(question.question_text)

    record = {
        "student_name": question.student_name,
        "question_text": question.question_text,
        "ai_response": ai_answer
    }

    questions_db.append(record)
    save_question_to_firebase(record)

    return {
        "message": "Question received",
        "ai_response": ai_answer
    }

@app.get("/instructor-dashboard")
def instructor_dashboard():
    return {
        "questions": questions_db
    }