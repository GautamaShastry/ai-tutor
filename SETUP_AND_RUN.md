# Telugu AI Tutor - Complete Setup and Run Guide

## Current Status ✅

- ✅ Frontend created (Next.js + TypeScript + Tailwind)
- ✅ Backend created (FastAPI + Python)
- ✅ Database schema ready (PostgreSQL)
- ✅ Data downloaded: **5,112 Telugu learning items**
  - 112 sample items (vocabulary, sentences, phrases)
  - 5,000 Samanantar sentence pairs

## Quick Start (3 Steps)

### Step 1: Start Infrastructure Services

```bash
# Start PostgreSQL, Redis, and Qdrant
docker-compose up -d

# Wait 10 seconds for services to start
# Verify they're running
docker ps
```

You should see 3 containers running:
- `telugu-tutor-postgres` (port 5432)
- `telugu-tutor-redis` (port 6379)
- `telugu-tutor-qdrant` (ports 6333, 6334)

### Step 2: Setup Database and Ingest Data

```bash
cd backend

# Run database migrations (create tables and seed data)
python app/db/migrate.py

# Ingest sample data (112 items, ~30 seconds)
python -m scripts.ingest_data --source custom --path ./data/sample

# Ingest Samanantar data (5000 items, ~10-15 minutes)
python -m scripts.ingest_data --source samanantar --path ./data/samanantar
```

### Step 3: Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Qdrant Dashboard: http://localhost:6333/dashboard

---

## Detailed Setup Instructions

### Prerequisites

1. **Docker Desktop** (for PostgreSQL, Redis, Qdrant)
   - Download: https://www.docker.com/products/docker-desktop/
   - Or install services individually

2. **Python 3.10+** with pip
   ```bash
   python --version
   ```

3. **Node.js 18+** with npm
   ```bash
   node --version
   npm --version
   ```

### Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file (already exists, verify settings)
# DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/telugu_tutor
# REDIS_URL=redis://localhost:6379
# QDRANT_URL=http://localhost:6333

# Run database migrations
python app/db/migrate.py

# Verify database
# You should see: "Migration completed!"
```

### Frontend Setup

```bash
cd frontend

# Install dependencies (already done during setup)
npm install

# Verify .env.local exists
# NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Data Ingestion

```bash
cd backend

# Option 1: Ingest sample data only (fast, for testing)
python -m scripts.ingest_data --source custom --path ./data/sample

# Option 2: Ingest Samanantar only
python -m scripts.ingest_data --source samanantar --path ./data/samanantar

# Option 3: Ingest all data
python -m scripts.ingest_data --source all --path ./data

# Monitor progress
# You'll see: "Total processed: X, Total stored: Y"
```

---

## Running the Application

### Development Mode

**Backend (Terminal 1):**
```bash
cd backend
uvicorn app.main:app --reload
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

### Production Mode

**Backend:**
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend:**
```bash
cd frontend
npm run build
npm start
```

---

## Verification Steps

### 1. Check Infrastructure

```bash
# Check Docker containers
docker ps

# Check PostgreSQL
docker exec -it telugu-tutor-postgres psql -U postgres -d telugu_tutor -c "SELECT COUNT(*) FROM skill_concepts;"

# Check Redis
docker exec -it telugu-tutor-redis redis-cli ping

# Check Qdrant
curl http://localhost:6333/collections/telugu_content
```

### 2. Check Backend

```bash
# Health check
curl http://localhost:8000/health

# API documentation
# Open: http://localhost:8000/docs
```

### 3. Check Data Ingestion

```bash
cd backend

# Check vector database
python -c "
import asyncio
from app.core.vector_db import vector_db

async def check():
    await vector_db.connect()
    info = await vector_db.get_collection_info()
    print(f'Collection: {info[\"name\"]}')
    print(f'Items: {info[\"points_count\"]}')
    await vector_db.disconnect()

asyncio.run(check())
"
```

---

## Troubleshooting

### "Connection refused" errors

**Problem:** Services not running

**Solution:**
```bash
docker-compose up -d
docker ps  # Verify all 3 containers are running
```

### "Database does not exist"

**Problem:** Database not created

**Solution:**
```bash
cd backend
python app/db/migrate.py
```

### "No module named 'qdrant_client'"

**Problem:** Missing Python dependencies

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Slow data ingestion

**Problem:** Embedding model download or processing

**Solution:**
- First run downloads ~2GB bge-m3 model (one-time)
- Use `--max-items` to limit: `--max-items 1000`
- Processing ~100 items/minute is normal

### Frontend build errors

**Problem:** Missing dependencies

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## Next Steps

After setup:

1. **Test the placement test flow**
   - Create a new learner account
   - Complete placement test
   - View skill graph

2. **Try chat practice**
   - Start a chat session
   - Send Telugu messages
   - Receive feedback

3. **Review spaced repetition**
   - Add vocabulary items
   - Review due items
   - Track progress

4. **Explore the dashboard**
   - View skill mastery
   - Check streak days
   - See weekly progress

---

## Development Workflow

### Adding More Data

```bash
cd backend

# Download more Samanantar data
python -m scripts.download_samanantar_simple 10000

# Ingest new data
python -m scripts.ingest_data --source samanantar --path ./data/samanantar
```

### Creating Custom Content

1. Create JSON file in `backend/data/custom/my_content.json`
2. Follow format in DATA_SETUP_GUIDE.md
3. Ingest: `python -m scripts.ingest_data --source custom --path ./data/custom`

### Running Tests

```bash
cd backend
pytest

cd ../frontend
npm test
```

---

## Architecture Overview

```
┌─────────────────┐
│   Frontend      │  Next.js (localhost:3000)
│   (React)       │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   Backend       │  FastAPI (localhost:8000)
│   (Python)      │
└────────┬────────┘
         │
    ┌────┴────┬────────┬──────────┐
    ▼         ▼        ▼          ▼
┌────────┐ ┌──────┐ ┌──────┐ ┌────────┐
│Postgres│ │Redis │ │Qdrant│ │Gemini/ │
│  DB    │ │Cache │ │Vector│ │Ollama  │
└────────┘ └──────┘ └──────┘ └────────┘
```

---

## Data Flow

1. **Learner Registration** → PostgreSQL (learner profile)
2. **Placement Test** → PostgreSQL (test results, proficiency level)
3. **Chat Practice** → 
   - Qdrant (retrieve relevant examples via RAG)
   - LLM (generate responses and feedback)
   - PostgreSQL (save chat history, error patterns)
4. **Spaced Repetition** → 
   - PostgreSQL (review items, intervals)
   - Redis (session state)
5. **Progress Dashboard** → 
   - PostgreSQL (skill mastery, stats)
   - Redis (cached aggregations)

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review DATA_SETUP_GUIDE.md for data-related issues
3. Check logs: `docker-compose logs -f`
4. Verify all services: `docker ps`

Happy learning Telugu! 🎉
