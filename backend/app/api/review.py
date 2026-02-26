"""
Spaced Repetition API endpoints for the Telugu AI Tutor.
"""
from fastapi import APIRouter, HTTPException, Depends

from app.models.review import ReviewSession, ReviewSubmission, ReviewResult
from app.services.review import srs_service
from app.api.auth import get_current_learner_id


router = APIRouter(prefix="/review", tags=["review"])


@router.get("/due-items", response_model=ReviewSession)
async def get_due_items(
    limit: int = 20,
    learner_id: str = Depends(get_current_learner_id)
):
    """
    Get vocabulary items due for review.
    
    Returns items that need to be reviewed based on spaced repetition schedule.
    """
    return await srs_service.get_due_items(learner_id, limit)


@router.post("/submit", response_model=ReviewResult)
async def submit_review(
    submission: ReviewSubmission,
    learner_id: str = Depends(get_current_learner_id)
):
    """
    Submit a review attempt for a vocabulary item.
    
    Updates the item's schedule using SM-2 algorithm based on recall quality.
    """
    try:
        return await srs_service.process_review(learner_id, submission)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process review: {str(e)}")


@router.post("/add-item", response_model=ReviewResult)
async def add_item(
    vocab_id: str,
    learner_id: str = Depends(get_current_learner_id)
):
    """
    Add a new vocabulary item to the learner's spaced repetition system.
    
    Initializes with default SM-2 values.
    """
    try:
        return await srs_service.add_item(learner_id, vocab_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add item: {str(e)}")
