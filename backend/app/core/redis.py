import redis.asyncio as redis
from typing import Optional
from app.core.config import settings


class RedisClient:
    client: Optional[redis.Redis] = None

    async def connect(self):
        """Create Redis connection"""
        self.client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )

    async def disconnect(self):
        """Close Redis connection"""
        if self.client:
            await self.client.close()

    async def get(self, key: str) -> Optional[str]:
        """Get a value by key"""
        return await self.client.get(key)

    async def set(self, key: str, value: str, expire: Optional[int] = None):
        """Set a value with optional expiration in seconds"""
        await self.client.set(key, value, ex=expire)

    async def delete(self, key: str):
        """Delete a key"""
        await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        return await self.client.exists(key) > 0


redis_client = RedisClient()
