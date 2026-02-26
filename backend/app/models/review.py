"""
Spaced repetition system models for the Telugu AI Tutor.
Implements SM-2 algorithm for vocabulary review scheduling.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ReviewQuality(int, Enum):
    """Quality of recall in spaced repetition (0-5 scale)"""
    BLACKOUT = 0  # Complete blackout
    INCORRECT_HARD = 1  # Incorrect, but remembered on seeing answer
    INCORRECT_EASY = 2  # Incorrect, but seemed easy on seeing answer
    CORRECT_HARD = 3  # Correct with serious difficulty
    CORRECT_HESITANT = 4  # Correct after hesitation
    CORRECT_PERFECT = 5  # Perfect response


class VocabularyItem(BaseModel):
    """A Telugu vocabulary item"""
    id: str
    telugu_word: str
    transliteration: Optional[str]
    english_meaning: str
    example_sentence: Optional[str]
    domains: list[str]
    difficulty_level: int  # 1-5


class SpacedRepetitionItem(BaseModel):
    """A vocabulary item in the spaced repetition system"""
    id: str
    learner_id: str
    vocab_id: str
    ease_factor: float  # SM-2 ease factor (default 2.5)
    interval_days: int  # Days until next review
    repetitions: int  # Number of successful repetitions
    next_review: datetime
    last_review: Optional[datetime]


class ReviewItemDetail(BaseModel):
    """Complete review item with vocabulary details"""
    srs_item: SpacedRepetitionItem
    vocabulary: VocabularyItem


class ReviewSubmission(BaseModel):
    """Submission of a review attempt"""
    item_id: str  # SpacedRepetitionItem ID
    quality: ReviewQuality  # 0-5 rating


class ReviewSession(BaseModel):
    """A review session with due items"""
    due_items: list[ReviewItemDetail]
    total_due: int
    total_items: int


class ReviewResult(BaseModel):
    """Result of a review submission"""
    item_id: str
    next_review: datetime
    interval_days: int
    ease_factor: float
    repetitions: int
