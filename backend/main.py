from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

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

    record = {
        "student_name": question.student_name,
        "question_text": question.question_text
    }

    questions_db.append(record)

    return {"message": "Question received"}

@app.get("/instructor-dashboard")
def instructor_dashboard():
    return {
        "questions": questions_db
    }