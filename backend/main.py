from datetime import datetime, timezone
import uuid
import re
from collections import Counter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.ai import generate_ai_response
from backend.firebase_db import (
    save_question_to_firebase,
    get_questions_from_firebase,
    update_feedback_in_firebase,
    create_user_in_firebase,
    get_user_from_firebase
)

app = FastAPI(title="LearnMate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    student_name: str
    question_text: str
    subject: str

class Feedback(BaseModel):
    question_id: str
    satisfaction_status: str

class UserSignup(BaseModel):
    name: str
    username: str
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str
    role: str

def extract_topic_with_ai(question_text: str, subject: str, existing_topics: list) -> str:
    existing_str = ", ".join(existing_topics) if existing_topics else "None"

    prompt = f"""Extract the single main topic from this student question.
    subject area: {subject}
    Question : {question_text}
    Already existing topics in this subject: {existing_str}

    Rules:
    - Return ONLY the main topic name with 2 to 4 words maximum.
    - it should be a proper concept name related to the subject.
    - if the question matches an existing topic, return EXACTLY that existing topic name.
    - no explanations, just the topic name.
Topic:"""
    topic = generate_ai_response(prompt)
    return topic.strip()

@app.get("/")
def root():
    return {"message": "LearnMate backend is running"}

@app.post("/signup")
def signup(user: UserSignup):
    existing_user = get_user_from_firebase(user.username)

    if existing_user:
        return {"message": "Username already exists"}

    user_data = {
        "name": user.name,
        "username": user.username,
        "password": user.password,
        "role": user.role
    }

    create_user_in_firebase(user_data)

    return {"message": "Signup successful"}

@app.post("/login")
def login(user: UserLogin):
    existing_user = get_user_from_firebase(user.username)

    if not existing_user:
        return {"message": "User not found"}

    if (
        existing_user.get("password") == user.password and
        existing_user.get("role") == user.role
    ):
        return {
            "message": "Login successful",
            "name": existing_user.get("name"),
            "role": existing_user.get("role")
        }

    return {"message": "Invalid username, password, or role"}

@app.post("/submit-question")
def submit_question(question: Question):
    ai_answer = generate_ai_response(question.question_text)

    all_questions = get_questions_from_firebase()
    existing_topics = list(set(
        q.get("topic", "").strip()
        for q in all_questions
        if q.get("subject", "").strip().lower() == question.subject.strip().lower()
        and q.get("topic", "").strip()
    ))

    topic = extract_topic_with_ai(question.question_text, question.subject, existing_topics)

    record = {
        "id": str(uuid.uuid4()),
        "student_name": question.student_name,
        "question_text": question.question_text,
        "subject": question.subject,
        "topic": topic,
        "ai_response": ai_answer,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "satisfaction_status": "pending"
    }

    save_question_to_firebase(record)

    return {
        "message": "Question received successfully",
        "question_id": record["id"],
        "ai_response": ai_answer,
        "timestamp": record["timestamp"]
    }

@app.post("/submit-feedback")
def submit_feedback(feedback: Feedback):
    update_feedback_in_firebase(feedback.question_id, feedback.satisfaction_status)
    return {"message": "Feedback submitted successfully"}

@app.get("/instructor-dashboard")
def instructor_dashboard(subject: str = "All"):
    questions = get_questions_from_firebase()

    if subject != "All":
        questions = [
            q for q in questions
            if q.get("subject", "").strip().lower() == subject.strip().lower()
        ]

    questions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)


    topic_analytics = Counter()
    not_satisfied_count = 0
    subjects_set = set()


    all_questions = get_questions_from_firebase()
    for item in all_questions:
        subject_name = item.get("subject", "").strip()
        if subject_name:
            subjects_set.add(subject_name)

    for q in questions:
        topic = q.get("topic", "").strip()
        if topic:
            topic_analytics[topic] += 1

        if q.get("satisfaction_status") == "not_satisfied":
            not_satisfied_count += 1

    return {
        "total_questions": len(questions),
        "not_satisfied_count": not_satisfied_count,
        "questions": questions,
        "topic_analytics": dict(topic_analytics),
        "subjects": sorted(list(subjects_set))
    }