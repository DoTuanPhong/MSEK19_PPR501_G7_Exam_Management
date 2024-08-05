from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quiz_set_id = Column(Integer, ForeignKey("quiz_sets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Integer)  # in minutes

    quiz_set = relationship("QuizSet", back_populates="exams")
    user = relationship("User", back_populates="exams")