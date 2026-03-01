from fastapi import FastAPI

app = FastAPI(title="LearnMate API - Week 1")

@app.get("/")
def root():
    return {"message": "LearnMate backend setup completed"}