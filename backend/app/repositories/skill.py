"""
Repository for skill graph database operations.
"""
from typing import List, Optional
from datetime import datetime

from app.core.database import db
from app.models.skill import SkillConcept, LearnerSkill, SkillCategory


class SkillRepository:
    """Repository for skill concept and mastery operations"""
    
    async def get_all_concepts(self) -> List[SkillConcept]:
        """Get all skill concepts"""
        rows = await db.fetch("SELECT * FROM skill_concepts ORDER BY name")
        
        return [
            SkillConcept(
                id=str(row["id"]),
                name=row["name"],
                category=SkillCategory(row["category"]),
                description=row["description"],
                prerequisites=[str(p) for p in row["prerequisites"]],
            )
            for row in rows
        ]
    
    async def get_concept_by_id(self, concept_id: str) -> Optional[SkillConcept]:
        """Get a specific skill concept"""
        row = await db.fetchrow(
            "SELECT * FROM skill_concepts WHERE id = $1",
            concept_id
        )
        
        if not row:
            return None
        
        return SkillConcept(
            id=str(row["id"]),
            name=row["name"],
            category=SkillCategory(row["category"]),
            description=row["description"],
            prerequisites=[str(p) for p in row["prerequisites"]],
        )
    
    async def get_learner_skills(self, learner_id: str) -> List[LearnerSkill]:
        """Get all skill masteries for a learner"""
        rows = await db.fetch(
            "SELECT * FROM learner_skills WHERE learner_id = $1",
            learner_id
        )
        
        return [
            LearnerSkill(
                id=str(row["id"]),
                learner_id=str(row["learner_id"]),
                concept_id=str(row["concept_id"]),
                mastery_score=row["mastery_score"],
                attempts=row["attempts"],
                last_practiced=row["last_practiced"],
            )
            for row in rows
        ]
    
    async def get_learner_skill(
        self,
        learner_id: str,
        concept_id: str
    ) -> Optional[LearnerSkill]:
        """Get a learner's mastery of a specific concept"""
        row = await db.fetchrow(
            """
            SELECT * FROM learner_skills
            WHERE learner_id = $1 AND concept_id = $2
            """,
            learner_id,
            concept_id
        )
        
        if not row:
            return None
        
        return LearnerSkill(
            id=str(row["id"]),
            learner_id=str(row["learner_id"]),
            concept_id=str(row["concept_id"]),
            mastery_score=row["mastery_score"],
            attempts=row["attempts"],
            last_practiced=row["last_practiced"],
        )
    
    async def upsert_learner_skill(
        self,
        learner_id: str,
        concept_id: str,
        mastery_score: float,
        attempts: int,
    ) -> LearnerSkill:
        """Insert or update a learner's skill mastery"""
        row = await db.fetchrow(
            """
            INSERT INTO learner_skills (learner_id, concept_id, mastery_score, attempts, last_practiced)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (learner_id, concept_id)
            DO UPDATE SET
                mastery_score = $3,
                attempts = $4,
                last_practiced = $5
            RETURNING *
            """,
            learner_id,
            concept_id,
            mastery_score,
            attempts,
            datetime.utcnow()
        )
        
        return LearnerSkill(
            id=str(row["id"]),
            learner_id=str(row["learner_id"]),
            concept_id=str(row["concept_id"]),
            mastery_score=row["mastery_score"],
            attempts=row["attempts"],
            last_practiced=row["last_practiced"],
        )
    
    async def get_mastered_concepts(
        self,
        learner_id: str,
        threshold: float = 0.8
    ) -> List[str]:
        """Get list of concept IDs the learner has mastered"""
        rows = await db.fetch(
            """
            SELECT concept_id FROM learner_skills
            WHERE learner_id = $1 AND mastery_score >= $2
            """,
            learner_id,
            threshold
        )
        
        return [str(row["concept_id"]) for row in rows]


skill_repository = SkillRepository()
