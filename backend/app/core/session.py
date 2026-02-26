"""
Session management using Redis for the Telugu AI Tutor.
Handles user sessions, learning state persistence, and caching.
"""
import json
from datetime import datetime, timedelta
from typing import Optional, Any
from uuid import uuid4

from app.core.redis import redis_client
from app.core.config import settings


class SessionStore:
    """Redis-based session store for managing user sessions"""
    
    SESSION_PREFIX = "session:"
    STATE_PREFIX = "state:"
    CACHE_PREFIX = "cache:"
    
    # Session expiry in seconds (30 minutes by default)
    SESSION_EXPIRY = settings.access_token_expire_minutes * 60
    
    # Learning state expiry (24 hours for resumption)
    STATE_EXPIRY = 24 * 60 * 60
    
    async def create_session(self, learner_id: str, data: Optional[dict] = None) -> str:
        """Create a new session for a learner"""
        session_id = str(uuid4())
        session_data = {
            "learner_id": learner_id,
            "created_at": datetime.utcnow().isoformat(),
            "data": data or {},
        }
        
        key = f"{self.SESSION_PREFIX}{session_id}"
        await redis_client.set(
            key,
            json.dumps(session_data),
            expire=self.SESSION_EXPIRY,
        )
        
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[dict]:
        """Retrieve session data"""
        key = f"{self.SESSION_PREFIX}{session_id}"
        data = await redis_client.get(key)
        
        if data:
            return json.loads(data)
        return None
    
    async def update_session(self, session_id: str, data: dict) -> bool:
        """Update session data"""
        key = f"{self.SESSION_PREFIX}{session_id}"
        existing = await redis_client.get(key)
        
        if not existing:
            return False
        
        session_data = json.loads(existing)
        session_data["data"].update(data)
        session_data["updated_at"] = datetime.utcnow().isoformat()
        
        await redis_client.set(
            key,
            json.dumps(session_data),
            expire=self.SESSION_EXPIRY,
        )
        return True
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        key = f"{self.SESSION_PREFIX}{session_id}"
        await redis_client.delete(key)
        return True
    
    async def save_learning_state(self, learner_id: str, state_type: str, state: dict) -> None:
        """
        Save learning state for resumption.
        State types: placement_test, lesson, chat_session, review_session
        """
        key = f"{self.STATE_PREFIX}{learner_id}:{state_type}"
        state_data = {
            "state": state,
            "saved_at": datetime.utcnow().isoformat(),
        }
        
        await redis_client.set(
            key,
            json.dumps(state_data),
            expire=self.STATE_EXPIRY,
        )
    
    async def get_learning_state(self, learner_id: str, state_type: str) -> Optional[dict]:
        """Retrieve saved learning state"""
        key = f"{self.STATE_PREFIX}{learner_id}:{state_type}"
        data = await redis_client.get(key)
        
        if data:
            return json.loads(data)
        return None
    
    async def clear_learning_state(self, learner_id: str, state_type: str) -> None:
        """Clear saved learning state after completion"""
        key = f"{self.STATE_PREFIX}{learner_id}:{state_type}"
        await redis_client.delete(key)
    
    async def cache_get(self, cache_key: str) -> Optional[Any]:
        """Get cached value"""
        key = f"{self.CACHE_PREFIX}{cache_key}"
        data = await redis_client.get(key)
        
        if data:
            return json.loads(data)
        return None
    
    async def cache_set(self, cache_key: str, value: Any, expire: int = 3600) -> None:
        """Set cached value with expiration in seconds"""
        key = f"{self.CACHE_PREFIX}{cache_key}"
        await redis_client.set(key, json.dumps(value), expire=expire)
    
    async def cache_invalidate(self, cache_key: str) -> None:
        """Invalidate cached value"""
        key = f"{self.CACHE_PREFIX}{cache_key}"
        await redis_client.delete(key)


session_store = SessionStore()
