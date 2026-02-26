"""
Repository for learner profile database operations.
"""
from typing import Optional, List
from datetime import datetime

from app.core.database import db
from app.models.learner import (
    LearnerProfile,
    LearnerProfileUpdate,
    LearnerStats,
    TargetGoal,
    StylePreference,
    LearningDomain,
)


class LearnerRepository:
    """Repository for learner profile CRUD operations"""
    
    async def get_by_id(self, learner_id: str) -> Optional[LearnerProfile]:
        """Get learner profile by ID"""
        row = await db.fetchrow(
            """
            SELECT id, email, native_language, target_goal, daily_time_minutes,
                   style_preference, domains, proficiency_level, streak_days,
                   total_practice_minutes
            FROM learner_profiles
            WHERE id = $1
            """,
            learner_id
        )
        
        if not row:
            return None
        
        return LearnerProfile(
            id=str(row["id"]),
            email=row["email"],
            native_language=row["native_language"],
            target_goal=TargetGoal(row["target_goal"]),
            daily_time_minutes=row["daily_time_minutes"],
            style_preference=StylePreference(row["style_preference"]),
            domains=[LearningDomain(d) for d in row["domains"]],
            proficiency_level=row["proficiency_level"],
            streak_days=row["streak_days"],
            total_practice_minutes=row["total_practice_minutes"],
        )
    
    async def get_by_email(self, email: str) -> Optional[LearnerProfile]:
        """Get learner profile by email"""
        row = await db.fetchrow(
            """
            SELECT id, email, native_language, target_goal, daily_time_minutes,
                   style_preference, domains, proficiency_level, streak_days,
                   total_practice_minutes
            FROM learner_profiles
            WHERE email = $1
            """,
            email
        )
        
        if not row:
            return None
        
        return LearnerProfile(
            id=str(row["id"]),
            email=row["email"],
            native_language=row["native_language"],
            target_goal=TargetGoal(row["target_goal"]),
            daily_time_minutes=row["daily_time_minutes"],
            style_preference=StylePreference(row["style_preference"]),
            domains=[LearningDomain(d) for d in row["domains"]],
            proficiency_level=row["proficiency_level"],
            streak_days=row["streak_days"],
            total_practice_minutes=row["total_practice_minutes"],
        )
    
    async def update(self, learner_id: str, update_data: LearnerProfileUpdate) -> Optional[LearnerProfile]:
        """Update learner profile"""
        # Build dynamic update query
        updates = []
        values = []
        param_count = 1
        
        if update_data.native_language is not None:
            updates.append(f"native_language = ${param_count}")
            values.append(update_data.native_language)
            param_count += 1
        
        if update_data.target_goal is not None:
            updates.append(f"target_goal = ${param_count}")
            values.append(update_data.target_goal.value)
            param_count += 1
        
        if update_data.daily_time_minutes is not None:
            updates.append(f"daily_time_minutes = ${param_count}")
            values.append(update_data.daily_time_minutes)
            param_count += 1
        
        if update_data.style_preference is not None:
            updates.append(f"style_preference = ${param_count}")
            values.append(update_data.style_preference.value)
            param_count += 1
        
        if update_data.domains is not None:
            updates.append(f"domains = ${param_count}")
            values.append([d.value for d in update_data.domains])
            param_count += 1
        
        if not updates:
            return await self.get_by_id(learner_id)
        
        values.append(learner_id)
        query = f"""
            UPDATE learner_profiles
            SET {', '.join(updates)}
            WHERE id = ${param_count}
        """
        
        await db.execute(query, *values)
        return await self.get_by_id(learner_id)
    
    async def update_proficiency_level(self, learner_id: str, level: int) -> None:
        """Update learner's proficiency level (from placement test)"""
        await db.execute(
            "UPDATE learner_profiles SET proficiency_level = $1 WHERE id = $2",
            level,
            learner_id
        )
    
    async def update_streak(self, learner_id: str, streak_days: int) -> None:
        """Update learner's streak"""
        await db.execute(
            "UPDATE learner_profiles SET streak_days = $1 WHERE id = $2",
            streak_days,
            learner_id
        )
    
    async def add_practice_time(self, learner_id: str, minutes: int) -> None:
        """Add practice time to learner's total"""
        await db.execute(
            """
            UPDATE learner_profiles
            SET total_practice_minutes = total_practice_minutes + $1
            WHERE id = $2
            """,
            minutes,
            learner_id
        )
    
    async def get_stats(self, learner_id: str) -> Optional[LearnerStats]:
        """Get learner statistics"""
        profile = await self.get_by_id(learner_id)
        if not profile:
            return None
        
        # Get vocabulary count
        vocab_count = await db.fetchval(
            """
            SELECT COUNT(*)
            FROM spaced_repetition_items
            WHERE learner_id = $1
            """,
            learner_id
        ) or 0
        
        # Get concepts mastered
        concepts_mastered = await db.fetchval(
            """
            SELECT COUNT(*)
            FROM learner_skills
            WHERE learner_id = $1 AND mastery_level >= 0.8
            """,
            learner_id
        ) or 0
        
        # Get total concepts
        total_concepts = await db.fetchval(
            "SELECT COUNT(*) FROM skill_concepts"
        ) or 0
        
        return LearnerStats(
            streak_days=profile.streak_days,
            total_practice_minutes=profile.total_practice_minutes,
            vocabulary_count=vocab_count,
            concepts_mastered=concepts_mastered,
            total_concepts=total_concepts,
        )


learner_repository = LearnerRepository()
