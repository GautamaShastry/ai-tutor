from pydantic import BaseModel
from datetime import datetime


class ReviewItemResponse(BaseModel):
    id: str
    telugu_word: str
    transliteration: str
    english_meaning: str
    example_sentence: str
    next_review: datetime


class ReviewSubmission(BaseModel):
    item_id: str
    correct: bool
