"""
Authentication API endpoints for the Telugu AI Tutor.
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional

from app.models.auth import LoginRequest, RegisterRequest, TokenResponse
from app.models.learner import LearnerProfileCreate, TargetGoal, StylePreference, LearningDomain
from app.services.auth import auth_service


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest):
    """
    Register a new learner account.
    
    Creates a new learner profile and returns an access token.
    """
    try:
        # Convert request to profile data
        profile_data = LearnerProfileCreate(
            email=request.email,
            password=request.password,
            native_language=request.native_language,
            target_goal=TargetGoal(request.target_goal),
            daily_time_minutes=request.daily_time_minutes,
            style_preference=StylePreference(request.style_preference),
            domains=[LearningDomain(d) for d in request.domains],
        )
        
        learner_id, access_token = await auth_service.register(profile_data)
        
        return TokenResponse(access_token=access_token)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Login with email and password.
    
    Returns an access token for authenticated requests.
    """
    try:
        learner_id, access_token = await auth_service.login(
            request.email,
            request.password
        )
        
        return TokenResponse(access_token=access_token)
    
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.post("/logout")
async def logout(authorization: Optional[str] = Header(None)):
    """
    Logout the current user.
    
    Invalidates the session.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    learner_id = auth_service.verify_token(token)
    
    if not learner_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Note: We're using JWT tokens which are stateless
    # In a production system, you might want to maintain a token blacklist
    return {"message": "Logged out successfully"}


async def get_current_learner_id(authorization: Optional[str] = Header(None)) -> str:
    """
    Dependency to get the current authenticated learner ID.
    
    Usage:
        @router.get("/protected")
        async def protected_route(learner_id: str = Depends(get_current_learner_id)):
            ...
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    learner_id = auth_service.verify_token(token)
    
    if not learner_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return learner_id
