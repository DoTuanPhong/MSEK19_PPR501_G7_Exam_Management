from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    lecturer_id = Column(Integer, ForeignKey("users.id"))

    lecturer = relationship("User")
    questions = relationship("Question", back_populates="subject")