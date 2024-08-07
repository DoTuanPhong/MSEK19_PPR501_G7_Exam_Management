# Import các thư viện cần thiết từ FastAPI, SQLAlchemy và các module khác
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.services import process_uploaded_file
from database import SessionLocal, engine, Base
from models import User, Question, Exam, Schedule
from schemas import ImporterResponse, UserCreate, UserOut, UserUpdate, QuestionCreate, QuestionOut, QuestionUpdate, ExamCreate, ExamOut, ExamUpdate, ScheduleCreate, ScheduleOut, ScheduleUpdate 
import uuid
import crud

# Tạo ứng dụng FastAPI
app = FastAPI()

# Tạo tất cả các bảng trong cơ sở dữ liệu (nếu chưa tồn tại)
Base.metadata.create_all(bind=engine)

# Hàm lấy session cơ sở dữ liệu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint tạo User mới
@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

# Endpoint lấy thông tin User theo user_id
@app.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Endpoint lấy danh sách các User
@app.get("/users/", response_model=list[UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

# Endpoint cập nhật thông tin User
@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: uuid.UUID, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = crud.update_user(db=db, user_id=user_id, user_data=user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Endpoint xóa User theo user_id
@app.delete("/users/{user_id}", response_model=UserOut)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = crud.delete_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user



# Endpoint tạo Question mới
@app.post("/questions/", response_model=QuestionOut)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db=db, question=question)  # Gọi hàm tạo câu hỏi trong CRUD

# Endpoint lấy thông tin Question theo question_id
@app.get("/questions/{question_id}", response_model=QuestionOut)
def read_question(question_id: uuid.UUID, db: Session = Depends(get_db)):
    question = crud.get_question(db=db, question_id=question_id)  # Lấy câu hỏi từ cơ sở dữ liệu
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")  # Nếu không tìm thấy câu hỏi, trả về lỗi 404
    return question  # Trả về câu hỏi tìm được

# Endpoint lấy danh sách các Question
@app.get("/questions/", response_model=list[QuestionOut])
def read_questions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    questions = crud.get_questions(db=db, skip=skip, limit=limit)  # Lấy danh sách câu hỏi từ cơ sở dữ liệu với phân trang
    return questions  # Trả về danh sách các câu hỏi

# Endpoint cập nhật Question theo question_id
@app.put("/questions/{question_id}", response_model=QuestionOut)
def update_question(question_id: uuid.UUID, question_data: QuestionUpdate, db: Session = Depends(get_db)):
    question = crud.update_question(db=db, question_id=question_id, question_data=question_data)  # Cập nhật câu hỏi trong cơ sở dữ liệu
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")  # Nếu không tìm thấy câu hỏi, trả về lỗi 404
    return question  # Trả về câu hỏi đã được cập nhật

# Endpoint xóa Question theo question_id
@app.delete("/questions/{question_id}", response_model=QuestionOut)
def delete_question(question_id: uuid.UUID, db: Session = Depends(get_db)):
    question = crud.delete_question(db=db, question_id=question_id)  # Xóa câu hỏi khỏi cơ sở dữ liệu
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")  # Nếu không tìm thấy câu hỏi, trả về lỗi 404
    return question  # Trả về câu hỏi đã bị xóa


# Endpoint tạo mới Exam
@app.post("/exams/", response_model=ExamOut)
def create_exam(exam: ExamCreate, db: Session = Depends(get_db)):
    return crud.create_exam(db=db, exam=exam)

# Endpoint lấy thông tin Exam theo exam_id
@app.get("/exams/{exam_id}", response_model=ExamOut)
def read_exam(exam_id: uuid.UUID, db: Session = Depends(get_db)):
    exam = crud.get_exam(db=db, exam_id=exam_id)
    if exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

# Endpoint lấy danh sách các Exam
@app.get("/exams/", response_model=list[ExamOut])
def read_exams(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    exams = crud.get_exams(db=db, skip=skip, limit=limit)
    return exams

# Endpoint cập nhật Exam theo exam_id
@app.put("/exams/{exam_id}", response_model=ExamOut)
def update_exam(exam_id: uuid.UUID, exam_data: ExamUpdate, db: Session = Depends(get_db)):
    exam = crud.update_exam(db=db, exam_id=exam_id, exam_data=exam_data)
    if exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

# Endpoint xóa Exam theo exam_id
@app.delete("/exams/{exam_id}", response_model=ExamOut)
def delete_exam(exam_id: uuid.UUID, db: Session = Depends(get_db)):
    exam = crud.delete_exam(db=db, exam_id=exam_id)
    if exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam



@app.post("/schedules/", response_model=ScheduleOut)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    return crud.create_schedule(db=db, schedule=schedule)

@app.get("/schedules/", response_model=list[ScheduleOut])
def read_schedules(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    schedules = crud.get_schedules(db, skip=skip, limit=limit)
    return schedules

@app.get("/schedules/{schedule_id}", response_model=ScheduleOut)
def read_schedule(schedule_id: uuid.UUID, db: Session = Depends(get_db)):
    db_schedule = crud.get_schedule(db, schedule_id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_schedule

@app.put("/schedules/{schedule_id}", response_model=ScheduleOut)
def update_schedule(schedule_id: uuid.UUID, schedule: ScheduleUpdate, db: Session = Depends(get_db)):
    db_schedule = crud.get_schedule(db, schedule_id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return crud.update_schedule(db=db, schedule_id=schedule_id, schedule_data=schedule)

@app.delete("/schedules/{schedule_id}", response_model=ScheduleOut)
def delete_schedule(schedule_id: uuid.UUID, db: Session = Depends(get_db)):
    db_schedule = crud.get_schedule(db, schedule_id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return crud.delete_schedule(db=db, schedule_id=schedule_id)

@app.post("/upload-and-process/", response_model=ImporterResponse)
def upload_and_process(
    user_id: uuid.UUID,
    file_path: str,
    db: Session = Depends(get_db)
):
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=400, detail="File not found")
        user = crud.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.role not in ['admin', 'exam inputter']:
            raise HTTPException(status_code=403, detail="Permission denied!")
        
        response = process_uploaded_file(user_id, file_path, db)
        
        os.unlink(file_path)
        return response

@app.post("/exams/", response_model=ExamOut)
def create_exam(
    exam_data: ExamCreate,
    db: Session = Depends(get_db)
    # ,current_user: User = Depends(get_current_user)
):
    # if current_user.role != "exam_creator":
    #     raise HTTPException(status_code=403, detail="Not authorized to create exams")
    
    # new_exam = create_exam(exam_data, current_user.user_id)
    new_exam = create_exam(exam_data)
    return new_exam