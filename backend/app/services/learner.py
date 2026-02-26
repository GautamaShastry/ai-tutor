"""
Learner profile service for the Telugu AI Tutor.
Handles learner profile operations and business logic.
"""
from typing import Optional
from datetime import datetime, timedelta

from app.repositories.learner import learner_repository
from app.models.learner import LearnerProfile, LearnerProfileUpdate, LearnerStats
from app.core.session import session_store


class LearnerService:
    """Service for learner profile operations"""
    
    async def get_profile(self, learner_id: str) -> Optional[LearnerProfile]:
        """Get learner profile by ID"""
        return await learner_repository.get_by_id(learner_id)
    
    async def update_profile(
        self,
        learner_id: str,
        update_data: LearnerProfileUpdate
    ) -> Optional[LearnerProfile]:
        """
        Update learner profile.
        Invalidates cached content when profile changes.
        """
        profile = await learner_repository.update(learner_id, update_data)
        
        if profile:
            # Invalidate cached content for this learner
            await session_store.cache_invalidate(f"lesson_plan:{learner_id}")
            await session_store.cache_invalidate(f"skill_graph:{learner_id}")
        
        return profile
    
    async def set_proficiency_level(self, learner_id: str, level: int) -> None:
        """Set learner's proficiency level (from placement test)"""
        await learner_repository.update_proficiency_level(learner_id, level)
    
    async def update_streak(self, learner_id: str) -> int:
        """
        Update learner's streak based on last practice date.
        Returns the new streak count.
        """
        profile = await learner_repository.get_by_id(learner_id)
        if not profile:
            return 0
        
        # Get last practice date from session state
        last_practice = await session_store.cache_get(f"last_practice:{learner_id}")
        
        today = datetime.utcnow().date()
        
        if last_practice:
            last_date = datetime.fromisoformat(last_practice).date()
            days_diff = (today - last_date).days
            
            if days_diff == 0:
                # Already practiced today
                return profile.streak_days
            elif days_diff == 1:
                # Consecutive day - increment streak
                new_streak = profile.streak_days + 1
            else:
                # Streak broken - reset to 1
                new_streak = 1
        else:
            # First practice
            new_streak = 1
        
        await learner_repository.update_streak(learner_id, new_streak)
        await session_store.cache_set(
            f"last_practice:{learner_id}",
            today.isoformat(),
            expire=86400 * 2  # 2 days
        )
        
        return new_streak
    
    async def record_practice_time(self, learner_id: str, minutes: int) -> None:
        """Record practice time for a learner"""
        await learner_repository.add_practice_time(learner_id, minutes)
        await self.update_streak(learner_id)
    
    async def get_stats(self, learner_id: str) -> Optional[LearnerStats]:
        """Get learner statistics for dashboard"""
        return await learner_repository.get_stats(learner_id)
    
    async def needs_placement_test(self, learner_id: str) -> bool:
        """Check if learner needs to take placement test"""
        profile = await learner_repository.get_by_id(learner_id)
        if not profile:
            return False
        
        return profile.proficiency_level is None


learner_service = LearnerService()
