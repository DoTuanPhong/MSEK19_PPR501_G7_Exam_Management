# Import các thư viện cần thiết từ Pydantic
from pydantic import BaseModel, EmailStr

from uuid import UUID
from typing import Optional
from datetime import date, time

# Định nghĩa schema cơ bản cho User
class UserBase(BaseModel):
    username: str  
    email: Optional[str] = None
    mobile: Optional[str] = None
    fullname: Optional[str] = None
    role: str  # Vai trò của người dùng

# Schema cho việc tạo User mới, kế thừa từ UserBase
class UserCreate(UserBase):
    password: str  # Mật khẩu người dùng

# Schema cho việc cập nhật User, kế thừa từ UserBase
class UserUpdate(UserBase):
    password: Optional[str] = None  

# Schema cho phản hồi User, kế thừa từ UserBase
class UserOut(UserBase):
    user_id: UUID  # ID người dùng

# Định nghĩa schema cơ bản cho Question
class QuestionBase(BaseModel):
    question_number: str  # Số câu hỏi
    exam_subject: str  # Môn thi
    exam_maker: UUID  # ID người tạo câu hỏi
    question_date: date  # Ngày tạo câu hỏi
    question_content: str  # Nội dung câu hỏi
    question_image: Optional[str] = None  # Hình ảnh câu hỏi (base64)
    option_a: str  # Lựa chọn A
    option_b: str  # Lựa chọn B
    option_c: str  # Lựa chọn C
    option_d: str  # Lựa chọn D
    correct_answer: str  # Đáp án đúng (phải kiểm tra hợp lệ trong CRUD)
    question_mark: int  # Điểm của câu hỏi
    question_unit: str  # Đơn vị câu hỏi
    question_mixchoices: Optional[bool] = False  # Trộn lựa chọn (mặc định là False)

# Schema cho việc tạo Question mới, kế thừa từ QuestionBase
class QuestionCreate(QuestionBase):
    pass

# Schema cho việc cập nhật Question, kế thừa từ QuestionBase
class QuestionUpdate(QuestionBase):
    question_id: UUID  # ID câu hỏi

# Schema cho phản hồi Question, kế thừa từ QuestionBase
class QuestionOut(QuestionBase):
    question_id: UUID  # ID câu hỏi


# Schema cơ bản cho Exam
class ExamBase(BaseModel):
    exam_subject: str  # Môn thi
    exam_code: str  # Mã đề thi
    duration: int  # Thời lượng thi
    number_of_questions: int  # Số lượng câu hỏi

# Schema cho việc tạo Exam
class ExamCreate(ExamBase):
    pass

# Schema cho việc cập nhật Exam
class ExamUpdate(ExamBase):
    exam_id: UUID

# Schema để trả về thông tin Exam
class ExamOut(ExamBase):
    exam_id: UUID  # ID đề thi

    class Config:
        orm_mode = True  # Cho phép Pydantic tương thích với ORM


# Schema cho Schedule
class ScheduleBase(BaseModel):
    exam_id: UUID
    schedule_date: date
    start_time: time
    end_time: time

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(ScheduleBase):
    pass

class ScheduleOut(ScheduleBase):
    schedule_id: UUID

class ImporterResponse(BaseModel):
    status: str 
    message: str
    exam_subject: str
    questions_created: int
    warnings: list[str]

    