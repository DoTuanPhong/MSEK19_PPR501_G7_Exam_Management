from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..database import Base

quiz_set_questions = Table('quiz_set_questions', Base.metadata,
    Column('quiz_set_id', Integer, ForeignKey('quiz_sets.id')),
    Column('question_id', Integer, ForeignKey('questions.id'))
)

class QuizSet(Base):
    __tablename__ = "quiz_sets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    
    subject = relationship("Subject", back_populates="quiz_sets")
    questions = relationship("Question", secondary=quiz_set_questions, back_populates="quiz_sets")
    exams = relationship("Exam", back_populates="quiz_set")