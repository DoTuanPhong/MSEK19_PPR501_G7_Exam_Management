from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ..crud import question as question_crud, subject as subject_crud
from ..schemas.question import QuestionCreate, Question
from typing import List
from datetime import date

router = APIRouter()

@router.post("/questions/import", response_model=List[Question])
async def import_questions(
    background_tasks: BackgroundTasks,
    info: dict,
    questions: List[QuestionCreate],
    db: Session
):
    # Create or get subject
    subject = subject_crud.get_subject_by_name(db, info['subject'])
    if not subject:
        # subject_create = SubjectCreate(
        #     name=info['subject'],
        #     lecturer=info['lecturer'],
        #     date=info['date']
        # )
        # subject = subject_crud.create_subject(db, subject_create)
        return {"message": "Subject is not exist in database! Import process cancel."}

    # Import questions in the background
    background_tasks.add_task(import_questions_task, db, subject.id, questions)

    return {"message": "Import started. Questions will be added in the background."}

def import_questions_task(db: Session, subject_id: int, questions: List[QuestionCreate]):
    for question in questions:
        question_crud.create_question(db, question, subject_id)