"""
Learner profile API endpoints for the Telugu AI Tutor.
"""
from fastapi import APIRouter, HTTPException, Depends

from app.models.learner import LearnerProfile, LearnerProfileUpdate, LearnerStats
from app.services.learner import learner_service
from app.api.auth import get_current_learner_id


router = APIRouter(prefix="/learner", tags=["learner"])


@router.get("/profile", response_model=LearnerProfile)
async def get_profile(learner_id: str = Depends(get_current_learner_id)):
    """
    Get the current learner's profile.
    """
    profile = await learner_service.get_profile(learner_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile


@router.put("/profile", response_model=LearnerProfile)
async def update_profile(
    update_data: LearnerProfileUpdate,
    learner_id: str = Depends(get_current_learner_id)
):
    """
    Update the current learner's profile.
    
    Invalidates cached content when profile changes.
    """
    profile = await learner_service.update_profile(learner_id, update_data)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile


@router.get("/stats", response_model=LearnerStats)
async def get_stats(learner_id: str = Depends(get_current_learner_id)):
    """
    Get learner statistics for the dashboard.
    
    Includes:
    - Streak days
    - Total practice minutes
    - Vocabulary count
    - Concepts mastered
    """
    stats = await learner_service.get_stats(learner_id)
    
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found")
    
    return stats


@router.get("/needs-placement-test", response_model=dict)
async def needs_placement_test(learner_id: str = Depends(get_current_learner_id)):
    """
    Check if the learner needs to take the placement test.
    
    Returns true if proficiency_level is null.
    """
    needs_test = await learner_service.needs_placement_test(learner_id)
    
    return {"needs_placement_test": needs_test}


@router.post("/practice-time")
async def record_practice_time(
    minutes: int,
    learner_id: str = Depends(get_current_learner_id)
):
    """
    Record practice time for the learner.
    
    Also updates the streak.
    """
    await learner_service.record_practice_time(learner_id, minutes)
    
    return {"message": "Practice time recorded", "minutes": minutes}
