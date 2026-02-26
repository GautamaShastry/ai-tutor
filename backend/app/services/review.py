"""
Spaced Repetition Service implementing the SM-2 algorithm.
Manages vocabulary review scheduling and interval calculation.
"""
from typing import List
from datetime import datetime, timedelta

from app.repositories.review import review_repository
from app.models.review import (
    ReviewSession,
    ReviewItemDetail,
    ReviewSubmission,
    ReviewResult,
    ReviewQuality,
)


class SpacedRepetitionService:
    """Service for spaced repetition system using SM-2 algorithm"""
    
    async def get_due_items(self, learner_id: str, limit: int = 20) -> ReviewSession:
        """
        Get items due for review.
        
        Returns a review session with vocabulary items that need review.
        """
        srs_items = await review_repository.get_due_items(learner_id, limit)
        all_items = await review_repository.get_all_items(learner_id)
        
        # Get vocabulary details for each item
        review_items = []
        for srs_item in srs_items:
            vocab = await review_repository.get_vocabulary_item(srs_item.vocab_id)
            if vocab:
                review_items.append(
                    ReviewItemDetail(
                        srs_item=srs_item,
                        vocabulary=vocab,
                    )
                )
        
        return ReviewSession(
            due_items=review_items,
            total_due=len(srs_items),
            total_items=len(all_items),
        )
    
    async def process_review(
        self,
        learner_id: str,
        submission: ReviewSubmission
    ) -> ReviewResult:
        """
        Process a review submission and update the item using SM-2 algorithm.
        
        SM-2 Algorithm:
        - Quality 0-2: Reset repetitions, interval = 1 day
        - Quality 3+: Increase interval based on ease factor
        - Ease factor adjusted based on quality
        """
        # Get the SRS item
        srs_item = await review_repository.get_srs_item(submission.item_id)
        if not srs_item:
            raise ValueError("Review item not found")
        
        # Verify ownership
        if srs_item.learner_id != learner_id:
            raise ValueError("Unauthorized access to review item")
        
        # Calculate new values using SM-2
        new_ease, new_interval, new_reps = self.calculate_next_interval(
            ease_factor=srs_item.ease_factor,
            interval_days=srs_item.interval_days,
            repetitions=srs_item.repetitions,
            quality=submission.quality,
        )
        
        # Calculate next review date
        next_review = datetime.utcnow() + timedelta(days=new_interval)
        
        # Update the item
        updated_item = await review_repository.update_srs_item(
            item_id=submission.item_id,
            ease_factor=new_ease,
            interval_days=new_interval,
            repetitions=new_reps,
            next_review=next_review,
        )
        
        return ReviewResult(
            item_id=updated_item.id,
            next_review=updated_item.next_review,
            interval_days=updated_item.interval_days,
            ease_factor=updated_item.ease_factor,
            repetitions=updated_item.repetitions,
        )
    
    def calculate_next_interval(
        self,
        ease_factor: float,
        interval_days: int,
        repetitions: int,
        quality: ReviewQuality,
    ) -> tuple[float, int, int]:
        """
        Calculate next interval using SM-2 algorithm.
        
        Returns: (new_ease_factor, new_interval_days, new_repetitions)
        """
        # Adjust ease factor based on quality
        new_ease = ease_factor + (0.1 - (5 - quality.value) * (0.08 + (5 - quality.value) * 0.02))
        
        # Ensure ease factor stays within reasonable bounds
        new_ease = max(1.3, new_ease)
        
        # Calculate interval based on quality
        if quality.value < 3:
            # Failed recall - reset
            new_reps = 0
            new_interval = 1
        else:
            # Successful recall
            new_reps = repetitions + 1
            
            if new_reps == 1:
                new_interval = 1
            elif new_reps == 2:
                new_interval = 6
            else:
                new_interval = int(interval_days * new_ease)
        
        return new_ease, new_interval, new_reps
    
    async def add_item(self, learner_id: str, vocab_id: str) -> ReviewResult:
        """
        Add a new vocabulary item to the learner's SRS.
        
        Initializes with default SM-2 values.
        """
        srs_item = await review_repository.add_item(learner_id, vocab_id)
        
        return ReviewResult(
            item_id=srs_item.id,
            next_review=srs_item.next_review,
            interval_days=srs_item.interval_days,
            ease_factor=srs_item.ease_factor,
            repetitions=srs_item.repetitions,
        )


srs_service = SpacedRepetitionService()
