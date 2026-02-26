-- Telugu AI Tutor Database Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Learner profiles table
CREATE TABLE IF NOT EXISTS learner_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    native_language VARCHAR(50) NOT NULL,
    target_goal VARCHAR(50) NOT NULL,
    daily_time_minutes INTEGER NOT NULL DEFAULT 15,
    style_preference VARCHAR(20) NOT NULL DEFAULT 'gentle',
    domains TEXT[] NOT NULL DEFAULT '{}',
    proficiency_level INTEGER,
    streak_days INTEGER DEFAULT 0,
    total_practice_minutes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Placement tests table
CREATE TABLE IF NOT EXISTS placement_tests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id UUID REFERENCES learner_profiles(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'in_progress',
    current_question INTEGER DEFAULT 0,
    answers JSONB DEFAULT '[]',
    score INTEGER,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    expires_at TIMESTAMP
);

-- Skill concepts table
CREATE TABLE IF NOT EXISTS skill_concepts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    prerequisites UUID[] DEFAULT '{}'
);

-- Learner skill mastery table
CREATE TABLE IF NOT EXISTS learner_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id UUID REFERENCES learner_profiles(id) ON DELETE CASCADE,
    concept_id UUID REFERENCES skill_concepts(id) ON DELETE CASCADE,
    mastery_score FLOAT DEFAULT 0.0,
    attempts INTEGER DEFAULT 0,
    last_practiced TIMESTAMP,
    UNIQUE(learner_id, concept_id)
);


-- Vocabulary items table
CREATE TABLE IF NOT EXISTS vocabulary_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telugu_word VARCHAR(255) NOT NULL,
    transliteration VARCHAR(255),
    english_meaning TEXT NOT NULL,
    example_sentence TEXT,
    domains TEXT[] DEFAULT '{}',
    difficulty_level INTEGER DEFAULT 1
);

-- Spaced repetition items table
CREATE TABLE IF NOT EXISTS spaced_repetition_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id UUID REFERENCES learner_profiles(id) ON DELETE CASCADE,
    vocab_id UUID REFERENCES vocabulary_items(id) ON DELETE CASCADE,
    ease_factor FLOAT DEFAULT 2.5,
    interval_days INTEGER DEFAULT 1,
    repetitions INTEGER DEFAULT 0,
    next_review TIMESTAMP NOT NULL,
    last_review TIMESTAMP,
    UNIQUE(learner_id, vocab_id)
);

-- Error memory table
CREATE TABLE IF NOT EXISTS error_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id UUID REFERENCES learner_profiles(id) ON DELETE CASCADE,
    error_type VARCHAR(50) NOT NULL,
    error_pattern TEXT NOT NULL,
    correct_form TEXT NOT NULL,
    occurrence_count INTEGER DEFAULT 1,
    last_occurred TIMESTAMP DEFAULT NOW(),
    priority_score FLOAT DEFAULT 1.0
);

-- Lessons table
CREATE TABLE IF NOT EXISTS lessons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id UUID REFERENCES learner_profiles(id) ON DELETE CASCADE,
    lesson_date DATE NOT NULL,
    plan JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    completed_activities INTEGER DEFAULT 0,
    total_activities INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Chat sessions table
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id UUID REFERENCES learner_profiles(id) ON DELETE CASCADE,
    difficulty_level INTEGER DEFAULT 1,
    domain VARCHAR(50),
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP
);

-- Chat messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    feedback JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Sessions table (for auth)
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id UUID REFERENCES learner_profiles(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Achievements table
CREATE TABLE IF NOT EXISTS achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    xp_reward INTEGER DEFAULT 0,
    criteria JSONB NOT NULL
);

-- Learner achievements table
CREATE TABLE IF NOT EXISTS learner_achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id UUID REFERENCES learner_profiles(id) ON DELETE CASCADE,
    achievement_id UUID REFERENCES achievements(id) ON DELETE CASCADE,
    earned_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(learner_id, achievement_id)
);

-- Pronunciation attempts table
CREATE TABLE IF NOT EXISTS pronunciation_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id UUID REFERENCES learner_profiles(id) ON DELETE CASCADE,
    target_text TEXT NOT NULL,
    audio_url VARCHAR(500),
    score FLOAT,
    feedback JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- LLM configuration table
CREATE TABLE IF NOT EXISTS llm_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider VARCHAR(50) NOT NULL DEFAULT 'gemini',
    model_name VARCHAR(100) NOT NULL DEFAULT 'gemini-1.5-flash',
    api_key_encrypted VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_learner_skills_learner ON learner_skills(learner_id);
CREATE INDEX IF NOT EXISTS idx_learner_skills_concept ON learner_skills(concept_id);
CREATE INDEX IF NOT EXISTS idx_spaced_repetition_learner ON spaced_repetition_items(learner_id);
CREATE INDEX IF NOT EXISTS idx_spaced_repetition_next_review ON spaced_repetition_items(next_review);
CREATE INDEX IF NOT EXISTS idx_error_memory_learner ON error_memory(learner_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_lessons_learner_date ON lessons(learner_id, lesson_date);
