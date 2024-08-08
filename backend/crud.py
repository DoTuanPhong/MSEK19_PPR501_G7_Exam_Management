# Import các thư viện cần thiết từ SQLAlchemy và các module khác
from sqlalchemy.orm import Session
from models import User, Question, Exam
from schemas import UserCreate, UserUpdate, QuestionCreate, QuestionUpdate, ExamCreate, ExamUpdate
import models
import schemas
import uuid

# Hàm tạo User mới
def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        mobile=user.mobile,
        fullname=user.fullname,
        role=user.role
    )
    db.add(db_user)  # Thêm User vào session
    db.commit()  # Lưu các thay đổi vào cơ sở dữ liệu
    db.refresh(db_user)  # Làm mới đối tượng User từ cơ sở dữ liệu
    return db_user  # Trả về đối tượng User mới tạo

# Hàm lấy thông tin User theo user_id
def get_user(db: Session, user_id: uuid.UUID):
    return db.query(User).filter(User.user_id == user_id).first()

# Hàm lấy danh sách các User với phân trang
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

# Hàm cập nhật thông tin User
def update_user(db: Session, user_id: uuid.UUID, user_data: UserUpdate):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        update_data = user_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    return None

# Hàm xóa User theo user_id
def delete_user(db: Session, user_id: uuid.UUID):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return user
    return None



# Hàm tạo Question mới
def create_question(db: Session, question: QuestionCreate):
    db_question = Question(
        question_number=question.question_number,
        exam_subject=question.exam_subject,
        exam_maker=question.exam_maker,
        question_date=question.question_date,
        question_content=question.question_content,
        question_image=question.question_image,
        option_a=question.option_a,
        option_b=question.option_b,
        option_c=question.option_c,
        option_d=question.option_d,
        correct_answer=question.correct_answer,
        question_mark=question.question_mark,
        question_unit=question.question_unit,
        question_mixchoices=question.question_mixchoices
    )
    db.add(db_question)  # Thêm Question vào session
    db.commit()  # Lưu các thay đổi vào cơ sở dữ liệu
    db.refresh(db_question)  # Làm mới đối tượng Question từ cơ sở dữ liệu
    return db_question  # Trả về đối tượng Question mới tạo

# Hàm lấy thông tin Question theo question_id
def get_question(db: Session, question_id: uuid.UUID):
    return db.query(Question).filter(Question.question_id == question_id).first()

# Hàm lấy danh sách các Question với phân trang
def get_questions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Question).offset(skip).limit(limit).all()

# Hàm cập nhật thông tin Question
def update_question(db: Session, question_id: uuid.UUID, question_data: QuestionUpdate):
    question = db.query(Question).filter(Question.question_id == question_id).first()
    if question:
        update_data = question_data.dict(exclude_unset=True)  # Chỉ cập nhật các trường được cung cấp
        for key, value in update_data.items():
            setattr(question, key, value)  # Cập nhật giá trị mới vào question
        db.commit()  # Lưu các thay đổi vào cơ sở dữ liệu
        db.refresh(question)  # Làm mới đối tượng Question từ cơ sở dữ liệu
        return question
    return None  # Trả về None nếu không tìm thấy question

# Hàm xóa Question theo question_id
def delete_question(db: Session, question_id: uuid.UUID):
    question = db.query(Question).filter(Question.question_id == question_id).first()
    if question:
        db.delete(question)  # Xóa Question khỏi session
        db.commit()  # Lưu các thay đổi vào cơ sở dữ liệu
        return question
    return None  # Trả về None nếu không tìm thấy question


# CRUD cho Exam
def get_exam(db: Session, exam_id: uuid.UUID):
    return db.query(Exam).filter(Exam.exam_id == exam_id).first()  # Lấy đề thi theo exam_id

def create_exam(db: Session, exam: ExamCreate):
    db_exam = Exam(**exam.dict())  # Tạo đối tượng Exam từ schema ExamCreate
    db.add(db_exam)  # Thêm đối tượng Exam vào session
    db.commit()  # Lưu thay đổi vào cơ sở dữ liệu
    db.refresh(db_exam)  # Làm mới đối tượng Exam
    return db_exam  # Trả về đối tượng Exam đã tạo

def get_exams(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Exam).offset(skip).limit(limit).all()  # Lấy danh sách đề thi với phân trang

def update_exam(db: Session, exam_id: uuid.UUID, exam_data: ExamUpdate):
    db_exam = get_exam(db, exam_id)  # Lấy đề thi từ cơ sở dữ liệu
    if db_exam:
        for key, value in exam_data.dict().items():  # Cập nhật các trường của đề thi
            setattr(db_exam, key, value)
        db.commit()  # Lưu thay đổi vào cơ sở dữ liệu
        db.refresh(db_exam)  # Làm mới đối tượng Exam
    return db_exam  # Trả về đối tượng Exam đã cập nhật

def delete_exam(db: Session, exam_id: uuid.UUID):
    db_exam = get_exam(db, exam_id)  # Lấy đề thi từ cơ sở dữ liệu
    if db_exam:
        db.delete(db_exam)  # Xóa đối tượng Exam
        db.commit()  # Lưu thay đổi vào cơ sở dữ liệu
    return db_exam  # Trả về đối tượng Exam đã xóa


# Tạo mới Schedule
def create_schedule(db: Session, schedule: schemas.ScheduleCreate):
    db_schedule = models.Schedule(
        schedule_id=uuid.uuid4(),
        exam_id=schedule.exam_id,
        schedule_date=schedule.schedule_date,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

# Lấy thông tin Schedule theo schedule_id
def get_schedule(db: Session, schedule_id: uuid.UUID):
    return db.query(models.Schedule).filter(models.Schedule.schedule_id == schedule_id).first()

# Lấy danh sách các Schedule
def get_schedules(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Schedule).offset(skip).limit(limit).all()

# Cập nhật Schedule theo schedule_id
def update_schedule(db: Session, schedule_id: uuid.UUID, schedule_data: schemas.ScheduleUpdate):
    db_schedule = get_schedule(db, schedule_id)
    if db_schedule:
        for key, value in schedule_data.dict().items():
            setattr(db_schedule, key, value)
        db.commit()
        db.refresh(db_schedule)
    return db_schedule

# Xóa Schedule theo schedule_id
def delete_schedule(db: Session, schedule_id: uuid.UUID):
    db_schedule = get_schedule(db, schedule_id)
    if db_schedule:
        db.delete(db_schedule)
        db.commit()
    return db_schedule