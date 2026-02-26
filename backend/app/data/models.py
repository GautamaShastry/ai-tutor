"""
Data models for ingested content.
"""
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class ContentType(str, Enum):
    """Types of learning content"""
    SENTENCE = "sentence"           # Example sentence
    VOCABULARY = "vocabulary"       # Word with definition
    GRAMMAR_RULE = "grammar_rule"   # Grammar explanation
    TRANSLITERATION = "transliteration"  # Script conversion
    DIALOGUE = "dialogue"           # Conversation example
    EXERCISE = "exercise"           # Practice item


class DifficultyLevel(str, Enum):
    """Content difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class SentenceContent(BaseModel):
    """A Telugu sentence with translation"""
    telugu: str
    english: str
    transliteration: Optional[str] = None
    source: str
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    domains: List[str] = []
    grammar_tags: List[str] = []


class VocabularyContent(BaseModel):
    """A vocabulary entry"""
    telugu_word: str
    transliteration: Optional[str] = None
    english_meaning: str
    part_of_speech: Optional[str] = None
    example_sentence: Optional[str] = None
    example_translation: Optional[str] = None
    synonyms: List[str] = []
    domains: List[str] = []
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    source: str


class TransliterationPair(BaseModel):
    """Telugu script to romanized form mapping"""
    telugu: str
    romanized: str
    source: str


class GrammarContent(BaseModel):
    """Grammar rule or explanation"""
    title: str
    telugu_pattern: str
    english_explanation: str
    examples: List[SentenceContent] = []
    related_concepts: List[str] = []
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    source: str


class ProcessedContent(BaseModel):
    """Unified content ready for vector storage"""
    id: str
    content_type: ContentType
    text: str                    # Primary text for embedding
    telugu_text: str             # Telugu content
    english_text: str            # English translation/meaning
    transliteration: Optional[str] = None
    metadata: dict = {}
    domains: List[str] = []
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    source: str
    license: str
