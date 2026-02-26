"""
Repository for spaced repetition database operations.
"""
from typing import List, Optional
from datetime import datetime

from app.core.database import db
from app.models.review import VocabularyItem, SpacedRepetitionItem


class ReviewRepository:
    """Repository for spaced repetition operations"""
    
    async def get_vocabulary_item(self, vocab_id: str) -> Optional[VocabularyItem]:
        """Get a vocabulary item by ID"""
        row = await db.fetchrow(
            "SELECT * FROM vocabulary_items WHERE id = $1",
            vocab_id
        )
        
        if not row:
            return None
        
        return VocabularyItem(
            id=str(row["id"]),
            telugu_word=row["telugu_word"],
            transliteration=row["transliteration"],
            english_meaning=row["english_meaning"],
            example_sentence=row["example_sentence"],
            domains=row["domains"],
            difficulty_level=row["difficulty_level"],
        )
    
    async def get_srs_item(self, item_id: str) -> Optional[SpacedRepetitionItem]:
        """Get a spaced repetition item by ID"""
        row = await db.fetchrow(
            "SELECT * FROM spaced_repetition_items WHERE id = $1",
            item_id
        )
        
        if not row:
            return None
        
        return SpacedRepetitionItem(
            id=str(row["id"]),
            learner_id=str(row["learner_id"]),
            vocab_id=str(row["vocab_id"]),
            ease_factor=row["ease_factor"],
            interval_days=row["interval_days"],
            repetitions=row["repetitions"],
            next_review=row["next_review"],
            last_review=row["last_review"],
        )
    
    async def get_due_items(
        self,
        learner_id: str,
        limit: int = 20
    ) -> List[SpacedRepetitionItem]:
        """Get items due for review"""
        rows = await db.fetch(
            """
            SELECT * FROM spaced_repetition_items
            WHERE learner_id = $1 AND next_review <= $2
            ORDER BY next_review ASC
            LIMIT $3
            """,
            learner_id,
            datetime.utcnow(),
            limit
        )
        
        return [
            SpacedRepetitionItem(
                id=str(row["id"]),
                learner_id=str(row["learner_id"]),
                vocab_id=str(row["vocab_id"]),
                ease_factor=row["ease_factor"],
                interval_days=row["interval_days"],
                repetitions=row["repetitions"],
                next_review=row["next_review"],
                last_review=row["last_review"],
            )
            for row in rows
        ]
    
    async def get_all_items(self, learner_id: str) -> List[SpacedRepetitionItem]:
        """Get all SRS items for a learner"""
        rows = await db.fetch(
            "SELECT * FROM spaced_repetition_items WHERE learner_id = $1",
            learner_id
        )
        
        return [
            SpacedRepetitionItem(
                id=str(row["id"]),
                learner_id=str(row["learner_id"]),
                vocab_id=str(row["vocab_id"]),
                ease_factor=row["ease_factor"],
                interval_days=row["interval_days"],
                repetitions=row["repetitions"],
                next_review=row["next_review"],
                last_review=row["last_review"],
            )
            for row in rows
        ]
    
    async def update_srs_item(
        self,
        item_id: str,
        ease_factor: float,
        interval_days: int,
        repetitions: int,
        next_review: datetime,
    ) -> SpacedRepetitionItem:
        """Update a spaced repetition item after review"""
        row = await db.fetchrow(
            """
            UPDATE spaced_repetition_items
            SET ease_factor = $2,
                interval_days = $3,
                repetitions = $4,
                next_review = $5,
                last_review = $6
            WHERE id = $1
            RETURNING *
            """,
            item_id,
            ease_factor,
            interval_days,
            repetitions,
            next_review,
            datetime.utcnow()
        )
        
        return SpacedRepetitionItem(
            id=str(row["id"]),
            learner_id=str(row["learner_id"]),
            vocab_id=str(row["vocab_id"]),
            ease_factor=row["ease_factor"],
            interval_days=row["interval_days"],
            repetitions=row["repetitions"],
            next_review=row["next_review"],
            last_review=row["last_review"],
        )
    
    async def add_item(
        self,
        learner_id: str,
        vocab_id: str,
    ) -> SpacedRepetitionItem:
        """Add a new vocabulary item to the learner's SRS"""
        row = await db.fetchrow(
            """
            INSERT INTO spaced_repetition_items (
                learner_id, vocab_id, ease_factor, interval_days,
                repetitions, next_review
            )
            VALUES ($1, $2, 2.5, 1, 0, $3)
            ON CONFLICT (learner_id, vocab_id) DO NOTHING
            RETURNING *
            """,
            learner_id,
            vocab_id,
            datetime.utcnow()
        )
        
        if not row:
            # Item already exists, fetch it
            row = await db.fetchrow(
                """
                SELECT * FROM spaced_repetition_items
                WHERE learner_id = $1 AND vocab_id = $2
                """,
                learner_id,
                vocab_id
            )
        
        return SpacedRepetitionItem(
            id=str(row["id"]),
            learner_id=str(row["learner_id"]),
            vocab_id=str(row["vocab_id"]),
            ease_factor=row["ease_factor"],
            interval_days=row["interval_days"],
            repetitions=row["repetitions"],
            next_review=row["next_review"],
            last_review=row["last_review"],
        )


review_repository = ReviewRepository()
