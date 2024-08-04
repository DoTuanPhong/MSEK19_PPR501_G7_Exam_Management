# app/services/docx_processor.py
import base64
from io import BytesIO
from spire.doc import *
from spire.doc.common import *
from app.models import Question, Choice, Subject, User
from sqlalchemy.orm import Session

class DocxProcessor:
    def __init__(self, db: Session):
        self.db = db

    def process_docx(self, file_path):
        doc = Document()
        doc.LoadFromFile(file_path)

        subject_name = None
        num_quiz = None
        lecturer = None
        date = None
        questions = []

        # Process the first part
        for i in range(min(4, doc.Sections[0].Paragraphs.Count)):
            paragraph = doc.Sections[0].Paragraphs[i]
            line = paragraph.Text.strip()
            if line.startswith("Subject:"):
                subject_name = line.split(":")[1].strip()
            elif line.startswith("Number of Quiz:"):
                num_quiz = int(line.split(":")[1].strip())
            elif line.startswith("Lecturer:"):
                lecturer = line.split(":")[1].strip()
            elif line.startswith("Date:"):
                date = line.split(":")[1].strip()

        if not all([subject_name, num_quiz, lecturer, date]):
            raise ValueError("Missing required information in the document header")

        # Process the tables
        for table in doc.Sections[0].Tables:
            question = self.process_question_table(table)
            if question:
                questions.append(question)

        subject = self.get_or_create_subject(subject_name, lecturer)
        self.save_questions(subject, questions)

        return {
            "subject": subject_name,
            "lecturer": lecturer,
            "date": date,
            "num_quiz": num_quiz,
            "questions_processed": len(questions)
        }

    def process_question_table(self, table):
        question_data = {}
        choices = []

        for row in table.Rows:
            if row.Cells.Count < 2:
                continue

            key = row.Cells[0].Paragraphs[0].Text.strip().lower()
            value_cell = row.Cells[1]

            if key.startswith("qn="):
                question_data["text"], question_data["image_data"] = self.extract_text_and_image(value_cell)
            elif key.startswith(("a.", "b.", "c.", "d.")):
                choices.append(value_cell.Paragraphs[0].Text.strip())
            elif key == "answer:":
                question_data["answer"] = value_cell.Paragraphs[0].Text.strip()
            elif key == "mark:":
                question_data["mark"] = float(value_cell.Paragraphs[0].Text.strip())
            elif key == "unit:":
                question_data["unit"] = value_cell.Paragraphs[0].Text.strip()
            elif key == "mix choices:":
                question_data["mix_choices"] = value_cell.Paragraphs[0].Text.strip().lower() == "yes"

        if all(k in question_data for k in ("text", "answer", "mark", "unit")) and choices:
            question_data["choices"] = choices
            return question_data
        return None

    def extract_text_and_image(self, cell):
        text_parts = []
        image_data = None

        for paragraph in cell.Paragraphs:
            text_parts.append(paragraph.Text)
            for item in paragraph.ChildObjects:
                if isinstance(item, DocPicture):
                    image_data = self.extract_image_data(item)
                    if image_data:
                        break
            if image_data:
                break

        return " ".join(text_parts), image_data

    def extract_image_data(self, doc_picture):
        image_stream = BytesIO()
        doc_picture.Image.Save(image_stream, ImageFormat.Png)
        image_bytes = image_stream.getvalue()
        return base64.b64encode(image_bytes).decode('utf-8')

    def get_or_create_subject(self, name, lecturer_name):
        subject = self.db.query(Subject).filter(Subject.name == name).first()
        if not subject:
            raise ValueError(f"Subject {name} not found")
            lecturer = self.db.query(User).filter(User.username == lecturer_name).first()
            if not lecturer:
                raise ValueError(f"Lecturer {lecturer_name} not found")
            subject = Subject(name=name, lecturer_id=lecturer.id)
            # self.db.add(subject)
            # self.db.commit()
        return subject

    def save_questions(self, subject, questions):
        for q_data in questions:
            question = Question(
                subject_id=subject.id,
                text=q_data["text"],
                image_data=q_data.get("image_data"),
                answer=q_data["answer"],
                mark=q_data["mark"],
                unit=q_data["unit"],
                mix_choices=q_data.get("mix_choices", True)
            )
            self.db.add(question)
            self.db.flush()  # Get the question ID

            for choice_text in q_data["choices"]:
                choice = Choice(
                    question_id=question.id,
                    text=choice_text,
                    is_correct=(choice_text == q_data["answer"])
                )
                self.db.add(choice)

        self.db.commit()