"""
Skill graph API endpoints for the Telugu AI Tutor.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models.skill import SkillGraph, SkillConcept, SkillMasteryUpdate, NextConcept
from app.services.skill import skill_graph_service
from app.api.auth import get_current_learner_id


router = APIRouter(prefix="/skill", tags=["skill"])


@router.get("/graph", response_model=SkillGraph)
async def get_skill_graph(learner_id: str = Depends(get_current_learner_id)):
    """
    Get the complete skill graph with learner's progress.
    
    Returns all Telugu skill concepts and the learner's mastery levels.
    """
    return await skill_graph_service.get_graph(learner_id)


@router.get("/concept/{concept_id}", response_model=SkillConcept)
async def get_concept(
    concept_id: str,
    learner_id: str = Depends(get_current_learner_id)
):
    """
    Get details about a specific skill concept.
    """
    from app.repositories.skill import skill_repository
    
    concept = await skill_repository.get_concept_by_id(concept_id)
    
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    
    return concept


@router.post("/mastery")
async def update_mastery(
    update: SkillMasteryUpdate,
    learner_id: str = Depends(get_current_learner_id)
):
    """
    Update learner's mastery of a skill concept after practice.
    
    Records whether the practice was successful and adjusts mastery score.
    """
    try:
        result = await skill_graph_service.update_mastery(learner_id, update)
        return {
            "concept_id": result.concept_id,
            "new_mastery": result.mastery_score,
            "attempts": result.attempts,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update mastery: {str(e)}")


@router.get("/next-concepts", response_model=List[NextConcept])
async def get_next_concepts(
    limit: int = 3,
    learner_id: str = Depends(get_current_learner_id)
):
    """
    Get recommended next concepts for the learner to practice.
    
    Returns concepts that:
    - Have prerequisites met
    - Are not yet mastered
    - Are prioritized based on progress
    """
    return await skill_graph_service.get_next_concepts(learner_id, limit)


@router.get("/check-prerequisites/{concept_id}")
async def check_prerequisites(
    concept_id: str,
    learner_id: str = Depends(get_current_learner_id)
):
    """
    Check if learner has met prerequisites for a concept.
    """
    met = await skill_graph_service.check_prerequisites(learner_id, concept_id)
    
    return {
        "concept_id": concept_id,
        "prerequisites_met": met,
    }
