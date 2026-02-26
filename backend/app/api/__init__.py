from fastapi import APIRouter

router = APIRouter()

# Import and include route modules as they are created
from app.api.auth import router as auth_router
from app.api.learner import router as learner_router
from app.api.skill import router as skill_router
from app.api.review import router as review_router
# from app.api.placement import router as placement_router
# from app.api.lesson import router as lesson_router
# from app.api.chat import router as chat_router

router.include_router(auth_router)
router.include_router(learner_router)
router.include_router(skill_router)
router.include_router(review_router)
# router.include_router(placement_router, prefix="/placement", tags=["Placement Test"])
# router.include_router(lesson_router, prefix="/lesson", tags=["Lessons"])
# router.include_router(chat_router, prefix="/chat", tags=["Chat Practice"])


@router.get("/")
async def api_root():
    return {"message": "Telugu AI Tutor API v1"}
