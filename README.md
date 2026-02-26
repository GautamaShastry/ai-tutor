# Telugu AI Tutor 🇮🇳

An intelligent, adaptive Telugu language learning platform powered by AI. Features personalized learning paths, spaced repetition, and interactive chat practice.

## 🎯 Project Status

### ✅ Completed (Phases 1 & 2)

**Phase 1: Core Infrastructure**
- Authentication system with JWT
- Learner profile management
- PostgreSQL database with 22 Telugu skill concepts
- Redis session management
- Qdrant vector database with 5,106 learning items
- Next.js frontend with TypeScript
- FastAPI backend

**Phase 2: Learning Mechanics**
- Skill graph system with prerequisite tracking
- SM-2 spaced repetition algorithm
- Vocabulary flashcard review interface
- Mastery tracking (0.0 to 1.0 scale)
- 15 comprehensive pytest tests (all passing ✅)

### 🚧 Upcoming (Phases 3 & 4)

**Phase 3: AI Integration**
- RAG (Retrieval-Augmented Generation) system
- Chat practice with Gemini LLM
- Real-time feedback and corrections
- Grammar and vocabulary suggestions

**Phase 4: Advanced Features**
- Pronunciation assessment
- Daily lesson planning
- Achievement system
- Analytics dashboard

---

## 🚀 Quick Start

### Prerequisites

- Docker Desktop (for PostgreSQL, Redis, Qdrant)
- Python 3.10+
- Node.js 18+

### 1. Start Infrastructure

```bash
docker-compose up -d
```

### 2. Setup Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python app/db/migrate.py

# Fix foreign key constraints (one-time)
$env:PYTHONPATH="$(pwd)"
python scripts/fix_foreign_keys.py
```

### 3. Start Backend Server

```bash
cd backend
uvicorn app.main:app --reload
```

Backend available at: http://localhost:8000  
API docs at: http://localhost:8000/docs

### 4. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: http://localhost:3000

---

## 📊 What's Built

### Features

#### Authentication & Profiles
- User registration and login
- JWT-based authentication
- Learner profile with preferences:
  - Native language
  - Learning goals (speaking, reading, writing, listening)
  - Daily practice time commitment
  - Feedback style (gentle vs strict)
  - Domain preferences (office, family, travel, movies)

#### Skill Graph System
- 22 Telugu skill concepts organized hierarchically
- Prerequisite-based learning progression
- Mastery tracking (0.0 to 1.0 scale)
- Smart concept recommendations
- Adaptive difficulty adjustment

**Skill Categories:**
- Telugu Script Basics
- Vowels and Consonants
- Basic Greetings
- Numbers and Counting
- Family Relationships
- Common Verbs
- Sentence Structure
- And 15 more...

#### Spaced Repetition System (SM-2)
- Intelligent review scheduling
- Quality-based interval adjustment (0-5 scale)
- Ease factor optimization
- Flashcard review interface

**How it works:**
- First review: 1 day
- Second review: 6 days
- Subsequent: Exponential growth
- Failed reviews: Reset to 1 day

#### Data
- 5,106 Telugu learning items with embeddings
- 112 curated vocabulary and phrases
- 4,994 Samanantar Telugu-English sentence pairs
- OpenAI text-embedding-3-small (1536 dimensions)

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React Context for state management

**Backend:**
- FastAPI (Python)
- asyncpg (PostgreSQL async driver)
- Redis for caching
- Qdrant for vector search
- Pydantic for validation

**Infrastructure:**
- PostgreSQL 16 (primary database)
- Redis 7 (session management)
- Qdrant (vector database)
- Docker Compose

### Project Structure

```
ai-tutor/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # Pages (login, register, dashboard, review)
│   │   ├── components/      # React components
│   │   ├── contexts/        # Auth context
│   │   ├── lib/             # API client
│   │   └── types/           # TypeScript types
│   └── package.json
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/             # API routes (auth, learner, skill, review)
│   │   ├── core/            # Core utilities (DB, Redis, Vector DB)
│   │   ├── models/          # Pydantic models
│   │   ├── repositories/    # Data access layer
│   │   ├── services/        # Business logic
│   │   └── db/              # Database schema and migrations
│   ├── tests/               # Pytest test suite (15 tests)
│   ├── scripts/             # Utility scripts
│   ├── data/                # Learning content
│   └── requirements.txt
│
├── docker-compose.yml        # Infrastructure services
└── README.md                # This file
```

---

## 🧪 Testing

### Run Tests

```bash
cd backend
python -m pytest tests/ -v
```

### Test Coverage

**15 tests, all passing ✅**

**Skill Graph Tests (6):**
- Get skill graph
- Update mastery (success/failure)
- Mastery score bounds
- Get next concepts
- Check prerequisites

**SM-2 Algorithm Tests (9):**
- Interval calculation (1 day, 6 days, exponential)
- Failure resets
- Ease factor adjustment
- Quality rating ordering
- Add/get due items

---

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new account
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/logout` - Logout

### Learner Profile
- `GET /api/v1/learner/profile` - Get profile
- `PUT /api/v1/learner/profile` - Update profile
- `GET /api/v1/learner/stats` - Get statistics

### Skill Graph
- `GET /api/v1/skill/graph` - Get complete skill graph
- `POST /api/v1/skill/mastery` - Update mastery
- `GET /api/v1/skill/next-concepts` - Get recommendations
- `GET /api/v1/skill/check-prerequisites/{id}` - Check prerequisites

### Spaced Repetition
- `GET /api/v1/review/due-items` - Get items due for review
- `POST /api/v1/review/submit` - Submit review with quality rating
- `POST /api/v1/review/add-item` - Add vocabulary to SRS

Full API documentation: http://localhost:8000/docs

---

## 🗄️ Database Schema

### Core Tables

**learner_profiles** - User accounts and preferences  
**skill_concepts** - 22 Telugu skill concepts with prerequisites  
**learner_skills** - Mastery tracking per learner per concept  
**vocabulary_items** - Telugu vocabulary words  
**spaced_repetition_items** - SRS scheduling data  
**sessions** - Authentication sessions  

### Additional Tables

**placement_tests** - Placement test results  
**lessons** - Daily lesson plans  
**chat_sessions** - Chat practice sessions  
**chat_messages** - Chat history  
**error_memory** - Common learner errors  
**achievements** - Gamification  
**pronunciation_attempts** - Pronunciation practice  

---

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```bash
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/telugu_tutor

# Redis
REDIS_URL=redis://localhost:6379

# Qdrant
QDRANT_URL=http://localhost:6333

# JWT
JWT_SECRET_KEY=your-secret-key-here

# LLM (for Phase 3)
GEMINI_API_KEY=your-gemini-key  # Optional for now
LLM_PROVIDER=gemini

# OpenAI (for embeddings)
OPENAI_API_KEY=your-openai-key  # Optional

# CORS
CORS_ORIGINS=http://localhost:3000
```

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## 📈 Progress Summary

### What We've Built

1. **Infrastructure** - Complete backend/frontend setup with Docker
2. **Authentication** - Secure JWT-based auth with bcrypt
3. **Data Pipeline** - 5,106 items ingested with embeddings
4. **Skill System** - Prerequisite-based learning progression
5. **SRS Algorithm** - SM-2 implementation for optimal retention
6. **Testing** - 15 comprehensive tests, all passing
7. **UI** - Login, register, dashboard, and review pages

### Key Achievements

- ✅ Fixed event loop configuration for pytest-asyncio
- ✅ Fixed UUID format in test fixtures
- ✅ Fixed foreign key constraints (learners → learner_profiles)
- ✅ Implemented complete SM-2 algorithm
- ✅ Created skill graph with 22 concepts
- ✅ Built flashcard review interface

---

## 🎯 Next Steps

### Phase 3: AI Integration (Upcoming)

1. **RAG System**
   - Implement semantic search with Qdrant
   - Context retrieval for chat responses
   - Relevance scoring

2. **Chat Practice**
   - Integrate Gemini LLM
   - Real-time Telugu conversation
   - Grammar and vocabulary feedback
   - Error pattern detection

3. **Content Generation**
   - Personalized examples
   - Adaptive difficulty
   - Domain-specific content

### Phase 4: Advanced Features (Future)

1. **Pronunciation Assessment**
   - Speech-to-text integration
   - Pronunciation scoring
   - Feedback on Telugu sounds

2. **Lesson Planning**
   - Daily personalized lessons
   - Activity scheduling
   - Progress-based adaptation

3. **Gamification**
   - Achievement system
   - Streak tracking
   - Leaderboards

4. **Analytics**
   - Learning insights
   - Progress visualization
   - Weak area identification

---

## 🐛 Troubleshooting

### Services Not Running

```bash
docker-compose up -d
docker ps  # Verify all 3 containers running
```

### Database Connection Errors

```bash
cd backend
python app/db/migrate.py
```

### Foreign Key Constraint Errors

```bash
cd backend
$env:PYTHONPATH="$(pwd)"
python scripts/fix_foreign_keys.py
```

### Import Errors

```bash
cd backend
pip install -r requirements.txt
```

### Frontend Build Errors

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📚 Documentation

- **TESTING_GUIDE.md** - Complete testing instructions
- **backend/app/db/schema.sql** - Database schema
- **frontend/README.md** - Frontend-specific docs

---

## 📝 License

This project is for educational purposes.

**Data Sources:**
- Samanantar: CC0 (Public Domain)
- Custom content: Original

---

## 🤝 Contributing

This is a personal learning project. Feel free to fork and adapt for your own use!

---

## 🎓 Learning Resources

**Telugu Language:**
- [Telugu Script](https://en.wikipedia.org/wiki/Telugu_script)
- [Telugu Grammar](https://en.wikibooks.org/wiki/Telugu)

**Technologies Used:**
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [Qdrant](https://qdrant.tech/)
- [SM-2 Algorithm](https://en.wikipedia.org/wiki/SuperMemo#SM-2_algorithm)

---

## 📊 Statistics

- **Lines of Code:** ~15,000+
- **API Endpoints:** 15+
- **Database Tables:** 15
- **Learning Items:** 5,106
- **Skill Concepts:** 22
- **Tests:** 15 (all passing ✅)
- **Test Coverage:** Skill Graph + SM-2 Algorithm

---

**Built with ❤️ for Telugu language learners**
