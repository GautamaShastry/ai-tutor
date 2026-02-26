from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum


class TargetGoal(str, Enum):
    SPEAKING = "speaking"
    READING = "reading"
    GRAMMAR = "grammar"
    INTERVIEW = "interview"
    TRAVEL = "travel"


class StylePreference(str, Enum):
    STRICT = "strict"
    GENTLE = "gentle"


class LearningDomain(str, Enum):
    OFFICE = "office"
    FAMILY = "family"
    MOVIES = "movies"


class LearnerProfileCreate(BaseModel):
    email: str
    password: str
    native_language: str
    target_goal: TargetGoal
    daily_time_minutes: int = 15
    style_preference: StylePreference = StylePreference.GENTLE
    domains: List[LearningDomain] = []


class LearnerProfileUpdate(BaseModel):
    native_language: Optional[str] = None
    target_goal: Optional[TargetGoal] = None
    daily_time_minutes: Optional[int] = None
    style_preference: Optional[StylePreference] = None
    domains: Optional[List[LearningDomain]] = None


class LearnerProfile(BaseModel):
    id: str
    email: str
    native_language: str
    target_goal: TargetGoal
    daily_time_minutes: int
    style_preference: StylePreference
    domains: List[LearningDomain]
    proficiency_level: Optional[int]
    streak_days: int
    total_practice_minutes: int


class LearnerStats(BaseModel):
    streak_days: int
    total_practice_minutes: int
    vocabulary_count: int
    concepts_mastered: int
    total_concepts: int
