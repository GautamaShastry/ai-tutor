"""
Tests for skill graph service.
"""
import pytest
from app.services.skill import skill_graph_service
from app.models.skill import SkillMasteryUpdate


@pytest.mark.asyncio
async def test_get_skill_graph(test_learner_id):
    """Test getting the complete skill graph"""
    graph = await skill_graph_service.get_graph(test_learner_id)
    
    assert graph is not None
    assert len(graph.concepts) > 0
    assert isinstance(graph.masteries, list)


@pytest.mark.asyncio
async def test_update_mastery_success(test_learner_id, test_concept_id):
    """Test updating mastery with successful attempt"""
    if not test_concept_id:
        pytest.skip("No skill concepts in database")
    
    update = SkillMasteryUpdate(
        concept_id=test_concept_id,
        success=True,
        difficulty=3,
    )
    
    result = await skill_graph_service.update_mastery(test_learner_id, update)
    
    assert result is not None
    assert result.concept_id == test_concept_id
    assert result.mastery_score > 0.0
    assert result.attempts == 1


@pytest.mark.asyncio
async def test_update_mastery_failure(test_learner_id, test_concept_id):
    """Test updating mastery with failed attempt"""
    if not test_concept_id:
        pytest.skip("No skill concepts in database")
    
    # First, set some mastery
    update_success = SkillMasteryUpdate(
        concept_id=test_concept_id,
        success=True,
        difficulty=3,
    )
    await skill_graph_service.update_mastery(test_learner_id, update_success)
    
    # Then fail
    update_fail = SkillMasteryUpdate(
        concept_id=test_concept_id,
        success=False,
        difficulty=3,
    )
    
    result = await skill_graph_service.update_mastery(test_learner_id, update_fail)
    
    assert result is not None
    assert result.attempts == 2


@pytest.mark.asyncio
async def test_mastery_score_bounds(test_learner_id, test_concept_id):
    """Test that mastery score stays within 0.0 to 1.0"""
    if not test_concept_id:
        pytest.skip("No skill concepts in database")
    
    # Try to exceed 1.0
    for _ in range(20):
        update = SkillMasteryUpdate(
            concept_id=test_concept_id,
            success=True,
            difficulty=5,
        )
        result = await skill_graph_service.update_mastery(test_learner_id, update)
    
    assert result.mastery_score <= 1.0
    assert result.mastery_score >= 0.0


@pytest.mark.asyncio
async def test_get_next_concepts(test_learner_id):
    """Test getting recommended next concepts"""
    concepts = await skill_graph_service.get_next_concepts(test_learner_id, limit=3)
    
    assert isinstance(concepts, list)
    assert len(concepts) <= 3
    
    for concept in concepts:
        assert concept.concept is not None
        assert concept.reason is not None
        assert isinstance(concept.prerequisites_met, bool)


@pytest.mark.asyncio
async def test_check_prerequisites(test_learner_id, test_concept_id):
    """Test prerequisite checking"""
    if not test_concept_id:
        pytest.skip("No skill concepts in database")
    
    result = await skill_graph_service.check_prerequisites(
        test_learner_id,
        test_concept_id
    )
    
    assert isinstance(result, bool)
