'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import { api } from '@/lib/api';

interface VocabularyItem {
  id: string;
  teluguWord: string;
  transliteration: string | null;
  englishMeaning: string;
  exampleSentence: string | null;
}

interface SRSItem {
  id: string;
  learnerId: string;
  vocabId: string;
  easeFactor: number;
  intervalDays: number;
  repetitions: number;
  nextReview: string;
}

interface ReviewItem {
  srs_item: SRSItem;
  vocabulary: VocabularyItem;
}

interface ReviewSession {
  due_items: ReviewItem[];
  total_due: number;
  total_items: number;
}

function ReviewContent() {
  const { token } = useAuth();
  const [session, setSession] = useState<ReviewSession | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDueItems();
  }, []);

  const loadDueItems = async () => {
    try {
      const data = await api.get<ReviewSession>('/review/due-items', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSession(data);
    } catch (error) {
      console.error('Failed to load review items:', error);
    } finally {
      setLoading(false);
    }
  };

  const submitReview = async (quality: number) => {
    if (!session || !session.due_items[currentIndex]) return;

    try {
      await api.post(
        '/review/submit',
        {
          item_id: session.due_items[currentIndex].srs_item.id,
          quality,
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      // Move to next item
      if (currentIndex < session.due_items.length - 1) {
        setCurrentIndex(currentIndex + 1);
        setShowAnswer(false);
      } else {
        // Review session complete
        loadDueItems();
        setCurrentIndex(0);
        setShowAnswer(false);
      }
    } catch (error) {
      console.error('Failed to submit review:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
          <p className="mt-4 text-gray-600">Loading review items...</p>
        </div>
      </div>
    );
  }

  if (!session || session.due_items.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="mx-auto max-w-2xl">
          <div className="rounded-lg bg-white p-8 text-center shadow">
            <div className="text-6xl mb-4">🎉</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              All caught up!
            </h2>
            <p className="text-gray-600">
              No items due for review right now. Come back later!
            </p>
            <p className="mt-4 text-sm text-gray-500">
              Total items in your collection: {session?.total_items || 0}
            </p>
          </div>
        </div>
      </div>
    );
  }

  const currentItem = session.due_items[currentIndex];
  const progress = ((currentIndex + 1) / session.due_items.length) * 100;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-2xl">
        {/* Progress bar */}
        <div className="mb-6">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>
              {currentIndex + 1} of {session.due_items.length}
            </span>
            <span>{Math.round(progress)}% complete</span>
          </div>
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-600 transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>

        {/* Flashcard */}
        <div className="bg-white rounded-lg shadow-lg p-8 min-h-[400px] flex flex-col justify-between">
          <div className="flex-1 flex flex-col items-center justify-center">
            <div className="text-center mb-8">
              <h3 className="text-4xl font-bold text-gray-900 mb-4">
                {currentItem.vocabulary.teluguWord}
              </h3>
              {currentItem.vocabulary.transliteration && (
                <p className="text-xl text-gray-600 mb-2">
                  {currentItem.vocabulary.transliteration}
                </p>
              )}
            </div>

            {showAnswer && (
              <div className="text-center animate-fade-in">
                <p className="text-2xl text-gray-900 mb-4">
                  {currentItem.vocabulary.englishMeaning}
                </p>
                {currentItem.vocabulary.exampleSentence && (
                  <p className="text-gray-600 italic">
                    "{currentItem.vocabulary.exampleSentence}"
                  </p>
                )}
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="mt-8">
            {!showAnswer ? (
              <button
                onClick={() => setShowAnswer(true)}
                className="w-full rounded-md bg-blue-600 px-4 py-3 text-lg font-semibold text-white hover:bg-blue-500"
              >
                Show Answer
              </button>
            ) : (
              <div className="space-y-3">
                <p className="text-center text-sm text-gray-600 mb-4">
                  How well did you remember?
                </p>
                <div className="grid grid-cols-3 gap-3">
                  <button
                    onClick={() => submitReview(1)}
                    className="rounded-md bg-red-100 px-4 py-3 text-sm font-semibold text-red-700 hover:bg-red-200"
                  >
                    Hard
                  </button>
                  <button
                    onClick={() => submitReview(3)}
                    className="rounded-md bg-yellow-100 px-4 py-3 text-sm font-semibold text-yellow-700 hover:bg-yellow-200"
                  >
                    Good
                  </button>
                  <button
                    onClick={() => submitReview(5)}
                    className="rounded-md bg-green-100 px-4 py-3 text-sm font-semibold text-green-700 hover:bg-green-200"
                  >
                    Easy
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ReviewPage() {
  return (
    <ProtectedRoute>
      <ReviewContent />
    </ProtectedRoute>
  );
}
