"""
Tests for spaced repetition service (SM-2 algorithm).
"""
import pytest
from datetime import datetime, timedelta
from app.services.review import srs_service
from app.models.review import ReviewSubmission, ReviewQuality


@pytest.mark.asyncio
async def test_sm2_interval_calculation():
    """Test SM-2 algorithm interval calculation"""
    # Test initial intervals
    ease, interval, reps = srs_service.calculate_next_interval(
        ease_factor=2.5,
        interval_days=1,
        repetitions=0,
        quality=ReviewQuality.CORRECT_PERFECT,
    )
    
    assert reps == 1
    assert interval == 1  # First repetition is always 1 day
    assert ease >= 2.5  # Ease should increase with perfect recall


@pytest.mark.asyncio
async def test_sm2_second_interval():
    """Test second interval is 6 days"""
    ease, interval, reps = srs_service.calculate_next_interval(
        ease_factor=2.5,
        interval_days=1,
        repetitions=1,
        quality=ReviewQuality.CORRECT_PERFECT,
    )
    
    assert reps == 2
    assert interval == 6  # Second repetition is always 6 days


@pytest.mark.asyncio
async def test_sm2_exponential_growth():
    """Test that intervals grow exponentially after second repetition"""
    ease, interval, reps = srs_service.calculate_next_interval(
        ease_factor=2.5,
        interval_days=6,
        repetitions=2,
        quality=ReviewQuality.CORRECT_PERFECT,
    )
    
    assert reps == 3
    assert interval > 6  # Should be larger than previous interval


@pytest.mark.asyncio
async def test_sm2_failure_resets():
    """Test that failure resets the interval"""
    ease, interval, reps = srs_service.calculate_next_interval(
        ease_factor=2.5,
        interval_days=30,
        repetitions=5,
        quality=ReviewQuality.INCORRECT_HARD,
    )
    
    assert reps == 0  # Repetitions reset
    assert interval == 1  # Back to 1 day


@pytest.mark.asyncio
async def test_sm2_ease_factor_adjustment():
    """Test that ease factor adjusts based on quality"""
    # Perfect recall should increase ease
    ease_perfect, _, _ = srs_service.calculate_next_interval(
        ease_factor=2.5,
        interval_days=1,
        repetitions=0,
        quality=ReviewQuality.CORRECT_PERFECT,
    )
    
    # Hard recall should decrease ease
    ease_hard, _, _ = srs_service.calculate_next_interval(
        ease_factor=2.5,
        interval_days=1,
        repetitions=0,
        quality=ReviewQuality.CORRECT_HARD,
    )
    
    assert ease_perfect > 2.5
    assert ease_hard < 2.5


@pytest.mark.asyncio
async def test_sm2_ease_factor_minimum():
    """Test that ease factor doesn't go below 1.3"""
    ease, _, _ = srs_service.calculate_next_interval(
        ease_factor=1.3,
        interval_days=1,
        repetitions=0,
        quality=ReviewQuality.BLACKOUT,
    )
    
    assert ease >= 1.3


@pytest.mark.asyncio
async def test_get_due_items_empty(test_learner_id):
    """Test getting due items when none exist"""
    session = await srs_service.get_due_items(test_learner_id, limit=20)
    
    assert session is not None
    assert isinstance(session.due_items, list)
    assert session.total_due >= 0
    assert session.total_items >= 0


@pytest.mark.asyncio
async def test_add_item(test_learner_id, test_db):
    """Test adding a vocabulary item to SRS"""
    # Create a test vocabulary item
    vocab_row = await test_db.fetchrow(
        """
        INSERT INTO vocabulary_items (
            telugu_word, english_meaning, difficulty_level
        ) VALUES ($1, $2, $3)
        RETURNING id
        """,
        "పుస్తకం",
        "book",
        1
    )
    vocab_id = str(vocab_row["id"])
    
    try:
        result = await srs_service.add_item(test_learner_id, vocab_id)
        
        assert result is not None
        assert result.interval_days == 1
        assert result.ease_factor == 2.5
        assert result.repetitions == 0
    finally:
        # Cleanup
        await test_db.execute(
            "DELETE FROM spaced_repetition_items WHERE learner_id = $1 AND vocab_id = $2",
            test_learner_id,
            vocab_id
        )
        await test_db.execute("DELETE FROM vocabulary_items WHERE id = $1", vocab_id)


@pytest.mark.asyncio
async def test_quality_ratings_order():
    """Test that different quality ratings produce expected ordering"""
    results = []
    
    for quality in [ReviewQuality.BLACKOUT, ReviewQuality.CORRECT_HARD, 
                    ReviewQuality.CORRECT_HESITANT, ReviewQuality.CORRECT_PERFECT]:
        ease, interval, reps = srs_service.calculate_next_interval(
            ease_factor=2.5,
            interval_days=6,
            repetitions=2,
            quality=quality,
        )
        results.append((quality.value, ease, interval, reps))
    
    # Higher quality should generally lead to longer intervals (except for failures)
    assert results[0][2] == 1  # Blackout resets to 1 day
    assert results[-1][2] > results[1][2]  # Perfect > Hard
