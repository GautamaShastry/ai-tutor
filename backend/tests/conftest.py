"""
Pytest configuration and fixtures for testing.
"""
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from app.main import app
from app.core.database import db


@pytest.fixture(scope="function")
async def test_db():
    """Set up test database connection"""
    await db.connect()
    yield db
    await db.disconnect()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP client for testing"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_learner_id(test_db) -> str:
    """Create a test learner and return their ID"""
    import uuid
    learner_id = str(uuid.uuid4())
    
    # Clean up if exists
    await db.execute("DELETE FROM learner_profiles WHERE id = $1", learner_id)
    
    # Create test learner
    await db.execute(
        """
        INSERT INTO learner_profiles (
            id, email, password_hash, native_language, target_goal,
            daily_time_minutes, style_preference, domains,
            proficiency_level, streak_days, total_practice_minutes
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """,
        learner_id,
        "test@example.com",
        "hashed_password",
        "English",
        "speaking",
        15,
        "gentle",
        [],
        None,
        0,
        0,
    )
    
    yield learner_id
    
    # Cleanup
    await db.execute("DELETE FROM learner_profiles WHERE id = $1", learner_id)


@pytest.fixture
async def test_concept_id(test_db) -> str:
    """Get a test skill concept ID"""
    row = await db.fetchrow("SELECT id FROM skill_concepts LIMIT 1")
    if row:
        return str(row["id"])
    return None
