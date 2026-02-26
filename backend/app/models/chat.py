from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ErrorType(str, Enum):
    POSTPOSITION = "postposition"
    VERB_AGREEMENT = "verb_agreement"
    TENSE_MARKER = "tense_marker"
    SPELLING = "spelling"
    SANDHI = "sandhi"


class GrammarError(BaseModel):
    original: str
    corrected: str
    error_type: ErrorType
    explanation: str


class VocabSuggestion(BaseModel):
    original: str
    suggested: str
    reason: str


class ChatFeedback(BaseModel):
    grammar_errors: List[GrammarError]
    vocabulary_suggestions: List[VocabSuggestion]
    naturalness_score: float
    corrected_text: str
    explanation: str


class ChatMessageRequest(BaseModel):
    content: str
    difficulty: int = 1


class ChatResponse(BaseModel):
    id: str
    content: str
    feedback: Optional[ChatFeedback] = None


class ChatMessage(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    feedback: Optional[ChatFeedback] = None
    created_at: datetime
