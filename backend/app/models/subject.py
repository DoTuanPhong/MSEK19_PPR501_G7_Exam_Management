from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from ..database import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    lecturer = Column(String)
    date = Column(Date)

    questions = relationship("Question", back_populates="subject")
    quiz_sets = relationship("QuizSet", back_populates="subject")