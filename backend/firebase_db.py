import json
import os

import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    firebase_key = os.getenv("FIREBASE_KEY")
    
    if firebase_key:
        cred = credentials.Certificate(json.loads(firebase_key))
    else:
        cred = credentials.Certificate("firebase-key.json")
    
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_question_to_firebase(data: dict):
    question_id = data.get("id")
    if question_id:
        db.collection("questions").document(question_id).set(data)
    else:
        db.collection("questions").add(data)

def get_questions_from_firebase():
    docs = db.collection("questions").stream()

    questions = []

    for doc in docs:
        question_data = doc.to_dict()
        if "id" not in question_data:
            question_data["id"] = doc.id
        questions.append(question_data)

    return questions

def update_feedback_in_firebase(question_id: str, satisfaction_status: str):
    db.collection("questions").document(question_id).update({
        "satisfaction_status": satisfaction_status
    }) 

def create_user_in_firebase(user_data: dict):
    username = user_data.get("username")
    db.collection("users").document(username).set(user_data)

def get_user_from_firebase(username: str):
    doc = db.collection("users").document(username).get()
    if doc.exists:
        return doc.to_dict()
    return None