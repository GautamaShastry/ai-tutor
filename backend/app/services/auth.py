"""
Authentication service for the Telugu AI Tutor.
Handles user registration, login, password hashing, and JWT token generation.
"""
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
import uuid

from app.core.config import settings
from app.core.database import db
from app.core.session import session_store
from app.models.auth import TokenResponse
from app.models.learner import LearnerProfileCreate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for authentication operations"""
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, learner_id: str) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode = {
            "sub": learner_id,
            "exp": expire,
        }
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[str]:
        """Verify JWT token and return learner_id"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            learner_id: str = payload.get("sub")
            if learner_id is None:
                return None
            return learner_id
        except JWTError:
            return None
    
    async def register(self, profile_data: LearnerProfileCreate) -> tuple[str, str]:
        """
        Register a new learner.
        Returns (learner_id, access_token)
        """
        # Check if email already exists
        existing = await db.fetchrow(
            "SELECT id FROM learner_profiles WHERE email = $1",
            profile_data.email
        )
        
        if existing:
            raise ValueError("Email already registered")
        
        # Hash password
        hashed_password = self.hash_password(profile_data.password)
        
        # Generate learner ID
        learner_id = str(uuid.uuid4())
        
        # Insert learner profile
        await db.execute(
            """
            INSERT INTO learner_profiles (
                id, email, password_hash, native_language, target_goal,
                daily_time_minutes, style_preference, domains,
                proficiency_level, streak_days, total_practice_minutes
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """,
            learner_id,
            profile_data.email,
            hashed_password,
            profile_data.native_language,
            profile_data.target_goal.value,
            profile_data.daily_time_minutes,
            profile_data.style_preference.value,
            [d.value for d in profile_data.domains],
            None,  # proficiency_level - set after placement test
            0,     # streak_days
            0,     # total_practice_minutes
        )
        
        # Create access token
        access_token = self.create_access_token(learner_id)
        
        # Create session
        await session_store.create_session(learner_id)
        
        return learner_id, access_token
    
    async def login(self, email: str, password: str) -> tuple[str, str]:
        """
        Authenticate a learner.
        Returns (learner_id, access_token)
        """
        # Fetch learner
        learner = await db.fetchrow(
            "SELECT id, password_hash FROM learner_profiles WHERE email = $1",
            email
        )
        
        if not learner:
            raise ValueError("Invalid email or password")
        
        # Verify password
        if not self.verify_password(password, learner["password_hash"]):
            raise ValueError("Invalid email or password")
        
        learner_id = str(learner["id"])  # Convert UUID to string
        
        # Create access token
        access_token = self.create_access_token(learner_id)
        
        # Create session
        await session_store.create_session(learner_id)
        
        return learner_id, access_token
    
    async def logout(self, session_id: str) -> bool:
        """Logout a learner by deleting their session"""
        return await session_store.delete_session(session_id)
    
    async def get_current_learner_id(self, token: str) -> Optional[str]:
        """Get learner ID from access token"""
        return self.verify_token(token)


auth_service = AuthService()
