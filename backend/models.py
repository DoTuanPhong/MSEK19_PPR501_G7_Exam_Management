# Import các thư viện cần thiết từ SQLAlchemy và các module khác
from sqlalchemy import Column, String, Text, Date, Integer, Boolean, ForeignKey, Time
from sqlalchemy.dialects.postgresql import UUID as pg_UUID
from sqlalchemy.orm import relationship
from database import Base
import uuid

# Định nghĩa model User
class User(Base):
    # Tên bảng trong DB
    __tablename__ = "User"

    user_id = Column(pg_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    mobile = Column(String(15))
    fullname = Column(String(100))
    role = Column(String(20), nullable=False)


# Định nghĩa model Question
class Question(Base):
    # Tên bảng trong DB
    __tablename__ = "Question"

    question_id = Column(pg_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_number = Column(String(15), nullable=False)
    exam_subject = Column(String(100), nullable=False)
    exam_maker = Column(pg_UUID(as_uuid=True), ForeignKey('User.user_id'), nullable=False)  # khóa ngoại PK tham chiếu đến User
    question_date = Column(Date, nullable=False)
    question_content = Column(Text, nullable=False)
    question_image = Column(Text)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    correct_answer = Column(String(1), nullable=False)
    question_mark = Column(Integer, nullable=False)
    question_unit = Column(String(50), nullable=False)
    question_mixchoices = Column(Boolean, default=False)

    # Định nghĩa mối quan hệ với bảng User
    exam_maker_user = relationship("User", backref="questions")


# Định nghĩa bảng Exam
class Exam(Base):
    __tablename__ = "Exam"

    exam_id = Column(pg_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_subject = Column(String(100), nullable=False)
    exam_code = Column(String(20), nullable=False)
    duration = Column(Integer, nullable=False)
    number_of_questions = Column(Integer, nullable=False)

class ExamQuestion(Base):
    __tablename__ = "Exam_Question"

    id = Column(pg_UUID(as_uuid=True), primary_key = True, default = uuid.uuid4)
    exam_id = Column(pg_UUID(as_uuid=True), ForeignKey("Exam.exam_id"), nullable = False)
    question_id = Column(pg_UUID(as_uuid=True), ForeignKey("Question.question_id"), nullable = False)
    option_a = Column(Text, nullable = False)
    option_b = Column(Text, nullable = False)
    option_c = Column(Text, nullable = False)
    option_d = Column(Text, nullable = False)
    correct_answer = Column(String[1])

# Định nghĩa bảng Schedule
class Schedule(Base):
    __tablename__ = "Schedule"
    schedule_id = Column(pg_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_id = Column(pg_UUID(as_uuid=True), ForeignKey('Exam.exam_id'), nullable=False)
    schedule_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
