from pydantic import BaseModel
from typing import Optional

class ChoiceBase(BaseModel):
    text: str
    is_correct: bool

class QuestionBase(BaseModel):
    text: str
    image_data: str | None  # Base64-encoded image
    answer: str
    mark: float
    unit: str
    mix_choices: bool = True

class QuestionCreate(QuestionBase):
    subject_id: int
    choices: list[ChoiceBase]

class Question(QuestionBase):
    id: int
    subject_id: int

    class Config:
        orm_mode = True

class QuestionWithChoices(Question):
    choices: list[ChoiceBase]