from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class SkillConceptResponse(BaseModel):
    id: str
    name: str
    category: str
    description: str
    prerequisites: List[str]


class SkillMasteryResponse(BaseModel):
    concept_id: str
    mastery_score: float
    attempts: int
    last_practiced: Optional[datetime] = None


class SkillGraphResponse(BaseModel):
    concepts: List[SkillConceptResponse]
    masteries: List[SkillMasteryResponse]
