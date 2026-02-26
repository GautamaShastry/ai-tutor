// Learner types
export interface LearnerProfile {
  id: string;
  email: string;
  nativeLanguage: string;
  targetGoal: 'speaking' | 'reading' | 'grammar' | 'interview' | 'travel';
  dailyTimeMinutes: number;
  stylePreference: 'strict' | 'gentle';
  domains: ('office' | 'family' | 'movies')[];
  proficiencyLevel: number | null;
  streakDays: number;
  totalPracticeMinutes: number;
}

// Skill graph types
export interface SkillConcept {
  id: string;
  name: string;
  category: 'tense' | 'marker' | 'case' | 'pronunciation' | 'script';
  description: string;
  prerequisites: string[];
}

export interface SkillMastery {
  conceptId: string;
  masteryScore: number;
  attempts: number;
  lastPracticed: Date | null;
}

export interface SkillGraph {
  concepts: SkillConcept[];
  masteries: SkillMastery[];
}

// Spaced repetition types
export interface ReviewItem {
  id: string;
  teluguWord: string;
  transliteration: string;
  englishMeaning: string;
  exampleSentence: string;
  nextReview: Date;
  intervalDays: number;
}


// Chat types
export interface ChatMessage {
  id: string;
  role: 'learner' | 'tutor';
  content: string;
  feedback: ChatFeedback | null;
  createdAt: Date;
}

export interface ChatFeedback {
  grammarErrors: GrammarError[];
  vocabularySuggestions: VocabSuggestion[];
  naturalnessScore: number;
  correctedText: string;
  explanation: string;
}

export interface GrammarError {
  original: string;
  corrected: string;
  errorType: 'postposition' | 'verb_agreement' | 'tense_marker' | 'spelling' | 'sandhi';
  explanation: string;
}

export interface VocabSuggestion {
  original: string;
  suggested: string;
  reason: string;
}

// Error memory types
export interface ErrorPattern {
  id: string;
  errorType: string;
  errorPattern: string;
  correctForm: string;
  occurrenceCount: number;
  priorityScore: number;
}

// Lesson types
export interface LessonPlan {
  id: string;
  date: Date;
  activities: LessonActivity[];
  estimatedMinutes: number;
  focusConcepts: string[];
}

export interface LessonActivity {
  id: string;
  type: 'vocabulary' | 'grammar' | 'reading' | 'chat' | 'review';
  title: string;
  description: string;
  estimatedMinutes: number;
  completed: boolean;
}

// Placement test types
export interface PlacementTest {
  id: string;
  status: 'in_progress' | 'completed' | 'abandoned';
  currentQuestion: number;
  totalQuestions: number;
  expiresAt: Date;
}

export interface PlacementQuestion {
  id: string;
  type: 'multiple_choice' | 'translation' | 'fill_blank';
  prompt: string;
  options?: string[];
  difficulty: number;
}

// Dashboard stats
export interface LearnerStats {
  streakDays: number;
  totalPracticeMinutes: number;
  vocabularyCount: number;
  conceptsMastered: number;
  totalConcepts: number;
  weeklyProgress: DailyProgress[];
}

export interface DailyProgress {
  date: Date;
  minutesPracticed: number;
  itemsReviewed: number;
  newItemsLearned: number;
}

// Gamification types
export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  xpReward: number;
  earnedAt?: Date;
}

export interface LearnerXP {
  totalXp: number;
  level: number;
  xpToNextLevel: number;
  achievements: Achievement[];
}

// Voice types
export interface PronunciationAttempt {
  id: string;
  targetText: string;
  score: number;
  feedback: PronunciationFeedback;
  createdAt: Date;
}

export interface PronunciationFeedback {
  overallScore: number;
  phonemeScores: PhonemeScore[];
  suggestions: string[];
}

export interface PhonemeScore {
  phoneme: string;
  score: number;
  expected: string;
  actual: string;
}

// LLM Provider types
export type LLMProvider = 'gemini' | 'ollama';

export interface LLMConfig {
  provider: LLMProvider;
  modelName: string;
  isActive: boolean;
}
