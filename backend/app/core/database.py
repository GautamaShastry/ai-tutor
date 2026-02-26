import asyncpg
from typing import Optional
from app.core.config import settings


class Database:
    pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Create connection pool to PostgreSQL"""
        # Parse the database URL to extract components
        # Format: postgresql+asyncpg://user:password@host:port/database
        url = settings.database_url.replace("postgresql+asyncpg://", "")
        
        if "@" in url:
            credentials, host_part = url.split("@")
            user, password = credentials.split(":")
            host_db = host_part.split("/")
            host_port = host_db[0].split(":")
            host = host_port[0]
            port = int(host_port[1]) if len(host_port) > 1 else 5432
            database = host_db[1] if len(host_db) > 1 else "telugu_tutor"
        else:
            user = "postgres"
            password = "postgres"
            host = "localhost"
            port = 5432
            database = "telugu_tutor"

        self.pool = await asyncpg.create_pool(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
            min_size=5,
            max_size=20,
        )

    async def disconnect(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()

    async def execute(self, query: str, *args):
        """Execute a query"""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args):
        """Fetch multiple rows"""
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        """Fetch a single row"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query: str, *args):
        """Fetch a single value"""
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)


db = Database()
