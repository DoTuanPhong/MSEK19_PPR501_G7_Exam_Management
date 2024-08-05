from sqlalchemy.orm import Session
from ..models.quiz_set import QuizSet
from ..schemas.quiz_set import QuizSetCreate

def get_quiz_set(db: Session, quiz_set_id: int):
    return db.query(QuizSet).filter(QuizSet.id == quiz_set_id).first()

def get_quiz_sets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(QuizSet).offset(skip).limit(limit).all()

def create_quiz_set(db: Session, quiz_set: QuizSetCreate):
    db_quiz_set = QuizSet(**quiz_set.dict())
    db.add(db_quiz_set)
    db.commit()
    db.refresh(db_quiz_set)
    return db_quiz_set

def update_quiz_set(db: Session, quiz_set_id: int, quiz_set_update: QuizSetCreate):
    db_quiz_set = get_quiz_set(db, quiz_set_id)
    if db_quiz_set:
        for key, value in quiz_set_update.dict().items():
            setattr(db_quiz_set, key, value)
        db.commit()
        db.refresh(db_quiz_set)
    return db_quiz_set

def delete_quiz_set(db: Session, quiz_set_id: int):
    db_quiz_set = get_quiz_set(db, quiz_set_id)
    if db_quiz_set:
        db.delete(db_quiz_set)
        db.commit()
    return db_quiz_set