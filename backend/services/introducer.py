import base64
import re
from docx import Document
from io import BytesIO
from PIL import Image
from app.models import Question, Choice, Subject
from sqlalchemy.orm import Session

class IntroducerService:
    @staticmethod
    def process_docx(db: Session, file, subject_id: int):
        doc = Document(file)
        questions = []

       

        return IntroducerService.save_questions(db, questions)
