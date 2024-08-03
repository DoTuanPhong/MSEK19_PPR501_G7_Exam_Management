from sqlalchemy import String, Column, Integer, Text, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key = True, index = True)
    answer = Column(String)
    mark = Column(Float)
    unit = Column(String)
    mix_choice = Column(Boolean, default = True)

    subject_id = Column(Integer, ForeignKey("subject.id"))
    subject = relationship("Subject", back_populates("questions"))
    choices = relationship("Choice", back_populates("question"))
    choices1 = relationship()


class Choice(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship("Question", back_populates="choices")
