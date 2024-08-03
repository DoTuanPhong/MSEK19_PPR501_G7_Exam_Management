from fastapi import FastAPI
from app.api.endpoints import auth, exam, introducer

app = FastAPI(title="Exam System API")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(exam.router, prefix="/exam", tags=["exam"])
app.include_router(introducer.router, prefix="/introducer", tags=["introducer"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Exam System API"}