"""
Skill graph service for the Telugu AI Tutor.
Manages skill concepts, prerequisites, and learner mastery tracking.
"""
from typing import List, Optional
from app.repositories.skill import skill_repository
from app.models.skill import (
    SkillConcept,
    SkillGraph,
    LearnerSkill,
    SkillMasteryUpdate,
    NextConcept,
)


class SkillGraphService:
    """Service for skill graph operations"""
    
    MASTERY_THRESHOLD = 0.8  # 80% mastery to consider a skill "mastered"
    
    async def get_graph(self, learner_id: str) -> SkillGraph:
        """
        Get the complete skill graph with learner's progress.
        
        Returns all concepts and the learner's mastery levels.
        """
        concepts = await skill_repository.get_all_concepts()
        masteries = await skill_repository.get_learner_skills(learner_id)
        
        return SkillGraph(
            concepts=concepts,
            masteries=masteries,
        )
    
    async def update_mastery(
        self,
        learner_id: str,
        update: SkillMasteryUpdate
    ) -> LearnerSkill:
        """
        Update a learner's mastery of a concept based on practice attempt.
        
        Uses a simple algorithm:
        - Success: increase mastery by 0.1 (capped at 1.0)
        - Failure: decrease mastery by 0.05 (floored at 0.0)
        - Adjust based on difficulty
        """
        # Get current mastery or create new
        current = await skill_repository.get_learner_skill(
            learner_id,
            update.concept_id
        )
        
        if current:
            current_score = current.mastery_score
            attempts = current.attempts + 1
        else:
            current_score = 0.0
            attempts = 1
        
        # Calculate new mastery score
        if update.success:
            # Success increases mastery
            # Harder difficulty = more increase
            increase = 0.1 * (update.difficulty / 3.0)
            new_score = min(1.0, current_score + increase)
        else:
            # Failure decreases mastery slightly
            decrease = 0.05
            new_score = max(0.0, current_score - decrease)
        
        # Update in database
        return await skill_repository.upsert_learner_skill(
            learner_id=learner_id,
            concept_id=update.concept_id,
            mastery_score=new_score,
            attempts=attempts,
        )
    
    async def get_next_concepts(
        self,
        learner_id: str,
        limit: int = 3
    ) -> List[NextConcept]:
        """
        Get recommended next concepts for the learner to practice.
        
        Considers:
        1. Prerequisites must be met (mastered)
        2. Not yet mastered by learner
        3. Prioritizes concepts with all prerequisites met
        """
        # Get all concepts and learner's mastered concepts
        all_concepts = await skill_repository.get_all_concepts()
        mastered_ids = await skill_repository.get_mastered_concepts(
            learner_id,
            self.MASTERY_THRESHOLD
        )
        masteries = await skill_repository.get_learner_skills(learner_id)
        
        # Create mastery lookup
        mastery_map = {m.concept_id: m.mastery_score for m in masteries}
        
        # Find available concepts
        available = []
        
        for concept in all_concepts:
            # Skip if already mastered
            if concept.id in mastered_ids:
                continue
            
            # Check if prerequisites are met
            prerequisites_met = all(
                prereq in mastered_ids
                for prereq in concept.prerequisites
            )
            
            # Get current mastery score
            current_mastery = mastery_map.get(concept.id, 0.0)
            
            # Prioritize concepts with prerequisites met
            priority = 0
            if prerequisites_met:
                priority = 100
            
            # Add partial progress bonus
            priority += current_mastery * 50
            
            # Add to available list
            available.append({
                "concept": concept,
                "prerequisites_met": prerequisites_met,
                "priority": priority,
                "reason": self._get_recommendation_reason(
                    concept,
                    prerequisites_met,
                    current_mastery
                ),
            })
        
        # Sort by priority and return top N
        available.sort(key=lambda x: x["priority"], reverse=True)
        
        return [
            NextConcept(
                concept=item["concept"],
                reason=item["reason"],
                prerequisites_met=item["prerequisites_met"],
            )
            for item in available[:limit]
        ]
    
    def _get_recommendation_reason(
        self,
        concept: SkillConcept,
        prerequisites_met: bool,
        current_mastery: float
    ) -> str:
        """Generate a reason for recommending this concept"""
        if not prerequisites_met:
            return f"Complete prerequisites first: {', '.join(concept.prerequisites[:2])}"
        
        if current_mastery == 0.0:
            return "New concept ready to learn"
        elif current_mastery < 0.5:
            return f"Continue practicing ({int(current_mastery * 100)}% mastery)"
        else:
            return f"Almost there! ({int(current_mastery * 100)}% mastery)"
    
    async def check_prerequisites(
        self,
        learner_id: str,
        concept_id: str
    ) -> bool:
        """
        Check if a learner has met the prerequisites for a concept.
        
        Returns True if all prerequisites are mastered.
        """
        concept = await skill_repository.get_concept_by_id(concept_id)
        if not concept:
            return False
        
        if not concept.prerequisites:
            return True  # No prerequisites
        
        mastered_ids = await skill_repository.get_mastered_concepts(
            learner_id,
            self.MASTERY_THRESHOLD
        )
        
        return all(prereq in mastered_ids for prereq in concept.prerequisites)


skill_graph_service = SkillGraphService()
