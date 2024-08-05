from sqlalchemy.orm import Session
from ..models.exam import Exam
# from ..schemas.exam import ExamCreate

def get_exam(db: Session, exam_id: int):
    return db.query(Exam).filter(Exam.id == exam_id).first()

def get_exams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Exam).offset(skip).limit(limit).all()

# def create_exam(db: Session, exam: ExamCreate):
#     db_exam = Exam(**exam.dict())
#     db.add(db_exam)
#     db.commit()
#     db.refresh(db_exam)
#     return db_exam

# def update_exam(db: Session, exam_id: int, exam_update: ExamCreate):
#     db_exam = get_exam(db, exam_id)
#     if db_exam:
#         for key, value in exam_update.dict().items():
#             setattr(db_exam, key, value)
#         db.commit()
#         db.refresh(db_exam)
#     return db_exam

def delete_exam(db: Session, exam_id: int):
    db_exam = get_exam(db, exam_id)
    if db_exam:
        db.delete(db_exam)
        db.commit()
    return db_exam