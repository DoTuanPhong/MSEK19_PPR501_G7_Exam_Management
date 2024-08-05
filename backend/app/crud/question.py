from sqlalchemy.orm import Session
from models.question import Question
from schemas.question import QuestionCreate

def create_question(db: Session, question: QuestionCreate, subject_id: int):
    db_question = Question(
        subject_id=subject_id,
        text=question.text,
        image=question.image,
        choices=",".join(question.choices),
        correct_answer=question.correct_answer,
        mark=question.mark,
        unit=question.unit,
        mix_choices=question.mix_choices
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question