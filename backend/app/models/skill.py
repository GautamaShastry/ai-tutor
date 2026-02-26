"""
Skill graph models for the Telugu AI Tutor.
Represents skill concepts, mastery levels, and the learning graph.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class SkillCategory(str, Enum):
    """Categories of Telugu language skills"""
    TENSE = "tense"
    MARKER = "marker"
    CASE = "case"
    PRONUNCIATION = "pronunciation"
    SCRIPT = "script"


class SkillConcept(BaseModel):
    """A skill concept in the Telugu learning graph"""
    id: str
    name: str
    category: SkillCategory
    description: str
    prerequisites: List[str]  # List of concept IDs


class LearnerSkill(BaseModel):
    """A learner's mastery of a specific skill concept"""
    id: str
    learner_id: str
    concept_id: str
    mastery_score: float  # 0.0 to 1.0
    attempts: int
    last_practiced: Optional[datetime]


class SkillGraph(BaseModel):
    """Complete skill graph with learner's progress"""
    concepts: List[SkillConcept]
    masteries: List[LearnerSkill]


class SkillMasteryUpdate(BaseModel):
    """Update to a learner's skill mastery"""
    concept_id: str
    success: bool  # Whether the practice attempt was successful
    difficulty: int  # 1-5, how difficult the learner found it


class NextConcept(BaseModel):
    """Next recommended concept for learning"""
    concept: SkillConcept
    reason: str  # Why this concept is recommended
    prerequisites_met: bool
