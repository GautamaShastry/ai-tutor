# Testing Guide for Telugu AI Tutor

## ✅ Phase 2 Testing Complete - All 15 Tests Passing!

## Running Tests

### Prerequisites
Make sure your infrastructure is running:
```bash
docker-compose up -d
```

### Run All Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Run Specific Test Files
```bash
# Test skill graph
python -m pytest tests/test_skill_service.py -v

# Test spaced repetition
python -m pytest tests/test_srs_service.py -v
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

## Test Results

✅ **All 15 tests passing!**

```
================================ 15 passed, 26 warnings in 4.02s =================================
```

## Test Structure

### `tests/conftest.py`
- Fixtures for database connection
- Test client setup
- Test learner creation with proper UUID format
- Fixed event loop configuration for pytest-asyncio

### `tests/test_skill_service.py` (6 tests)
Tests for skill graph system:
- ✅ Get skill graph
- ✅ Update mastery (success)
- ✅ Update mastery (failure)
- ✅ Mastery score bounds (0.0 to 1.0)
- ✅ Get next recommended concepts
- ✅ Check prerequisites

### `tests/test_srs_service.py` (9 tests)
Tests for spaced repetition (SM-2):
- ✅ Interval calculation (first interval = 1 day)
- ✅ Second interval (6 days)
- ✅ Exponential growth after second repetition
- ✅ Failure resets to 1 day
- ✅ Ease factor adjustment based on quality
- ✅ Ease factor minimum (1.3)
- ✅ Get due items (empty case)
- ✅ Add item to SRS
- ✅ Quality ratings ordering

## One-Time Setup (Already Done)

### Fix Foreign Key Constraints
If you encounter foreign key errors, run:
```bash
cd backend
$env:PYTHONPATH="C:\Users\gauta\OneDrive\Desktop\ai-tutor\backend"
python scripts/fix_foreign_keys.py
```

This updates foreign key constraints to reference `learner_profiles` instead of the old `learners` table.

## Manual Testing

### Test Authentication
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "native_language": "English",
    "target_goal": "speaking",
    "daily_time_minutes": 15,
    "style_preference": "gentle",
    "domains": []
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Test Skill Graph
```bash
# Get skill graph (replace TOKEN)
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/v1/skill/graph

# Get next concepts
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/v1/skill/next-concepts?limit=3

# Update mastery
curl -X POST http://localhost:8000/api/v1/skill/mastery \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "concept_id": "CONCEPT_ID",
    "success": true,
    "difficulty": 3
  }'
```

### Test Spaced Repetition
```bash
# Get due items
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/v1/review/due-items

# Submit review
curl -X POST http://localhost:8000/api/v1/review/submit \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": "ITEM_ID",
    "quality": 5
  }'
```

## Frontend Testing

### Test Review Page
1. Start backend: `cd backend && uvicorn app.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Navigate to http://localhost:3000
4. Register/Login
5. Go to http://localhost:3000/review
6. Test flashcard functionality

## Troubleshooting

### Database Connection Errors
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart if needed
docker-compose restart postgres
```

### Foreign Key Constraint Errors
If you see "ForeignKeyViolationError: ... not present in table learners":
```bash
cd backend
$env:PYTHONPATH="C:\Users\gauta\OneDrive\Desktop\ai-tutor\backend"
python scripts/fix_foreign_keys.py
```

### Import Errors
```bash
# Make sure you're in the backend directory
cd backend

# Run tests with Python module syntax
python -m pytest tests/
```

### Async Test Errors
Make sure `pytest-asyncio` is installed and configured:
```bash
pip install pytest-asyncio
```

Ensure `pytest.ini` has:
```ini
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
```

## Known Warnings (Non-Critical)

The tests show some deprecation warnings that don't affect functionality:
- `datetime.utcnow()` deprecation (should use `datetime.now(datetime.UTC)`)
- Pydantic class-based config deprecation (should use ConfigDict)

These can be addressed in future refactoring.

## Next Steps

✅ Phase 2 testing complete!

Ready to proceed with:
1. Phase 3: RAG and Chat System
2. Phase 4: LLM Integration
3. Additional integration tests for API endpoints
4. Performance testing with larger datasets
