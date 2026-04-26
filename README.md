# LearnMate – Distributed AI Tutor for Remote Learning

## Project Overview
LearnMate is a distributed web-based learning support platform designed to assist students and instructors during online classes.  
The system allows students to submit questions during lectures and receive AI-generated explanations instantly.  
Instructors can monitor all submitted questions through a dashboard and understand common learning difficulties in real time.

This project demonstrates the use of distributed computing concepts, AI-assisted responses and cloud database integration.

## Team Members
- Revanth Reddy Banala – Frontend development, documentation, presentation  
- Sai Sri Harsha Vardhan Chalichama – AI research, NLP integration, testing  
- Maha Lakshmi Malli – System design, backend development, project coordination

## Technologies Used

### Backend
- Python
- FastAPI
- Uvicorn

### Frontend
- HTML
- CSS
- JavaScript

### Database
- Firebase Firestore (Cloud Database)

### AI / NLP
- Gemini Ai

## Key Features

- Web-based student question submission portal
- AI-generated explanations for questions
- Instructor dashboard to monitor questions
- Cloud database storage using Firebase
- Distributed system architecture
- Real-time instructor monitoring with auto-refresh


### Firebase Setup

Download your Firebase service account key from the Firebase console  
and place it in the project root directory as:
firebase-key.json
This file is excluded from GitHub using .gitignore.

## How to Run the Project

### 1. Clone the Repository
git clone <https://github.com/mahalakshmi131202/Learnmate>
cd LearnMate

### 2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Run Backend Server
uvicorn backend.main:app --reload

Server will start at:
https://learnmate-backend-a96w.onrender.com

## Running the Frontend
Open the following files in a browser:
frontend/index.html
then 
frontend/signup.html for both student and instructor
then login with student
and in another window login as instructor
so accordingly dashbord will open as per roles
The student dashboard will show all the functionalities.
The instructor dashboard will display submitted questions and AI responses and other features.
## Live Demo
- Frontend: https://learnmateaitutor.netlify.app
- Backend API: https://learnmate-backend-a96w.onrender.com
- API Docs: https://learnmate-backend-a96w.onrender.com/docs
## Demo Workflow
1. Start the FastAPI backend server
2. Open the student portal
3. Submit a question
4. AI generates an explanation
5. Instructor dashboard displays the question
6. Data is stored in Firebase database

## Course
Distributed Computing Systems  
Spring 2026