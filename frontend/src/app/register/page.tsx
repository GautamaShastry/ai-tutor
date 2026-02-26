'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    native_language: 'English',
    target_goal: 'speaking',
    daily_time_minutes: 15,
    style_preference: 'gentle',
    domains: [] as string[],
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      const { confirmPassword, ...registerData } = formData;
      await register(registerData);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const toggleDomain = (domain: string) => {
    setFormData((prev) => ({
      ...prev,
      domains: prev.domains.includes(domain)
        ? prev.domains.filter((d) => d !== domain)
        : [...prev.domains, domain],
    }));
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12">
      <div className="w-full max-w-md space-y-8">
        <div>
          <h2 className="text-center text-3xl font-bold tracking-tight text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Already have an account?{' '}
            <Link href="/login" className="font-medium text-blue-600 hover:text-blue-500">
              Sign in
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <input
                id="email"
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="mt-1 block w-full rounded-md border-0 px-3 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="mt-1 block w-full rounded-md border-0 px-3 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                type="password"
                required
                value={formData.confirmPassword}
                onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                className="mt-1 block w-full rounded-md border-0 px-3 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="native_language" className="block text-sm font-medium text-gray-700">
                Native Language
              </label>
              <input
                id="native_language"
                type="text"
                required
                value={formData.native_language}
                onChange={(e) => setFormData({ ...formData, native_language: e.target.value })}
                className="mt-1 block w-full rounded-md border-0 px-3 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="target_goal" className="block text-sm font-medium text-gray-700">
                Learning Goal
              </label>
              <select
                id="target_goal"
                value={formData.target_goal}
                onChange={(e) => setFormData({ ...formData, target_goal: e.target.value })}
                className="mt-1 block w-full rounded-md border-0 px-3 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm"
              >
                <option value="speaking">Speaking</option>
                <option value="reading">Reading</option>
                <option value="grammar">Grammar</option>
                <option value="interview">Interview Prep</option>
                <option value="travel">Travel</option>
              </select>
            </div>

            <div>
              <label htmlFor="daily_time_minutes" className="block text-sm font-medium text-gray-700">
                Daily Practice Time (minutes)
              </label>
              <input
                id="daily_time_minutes"
                type="number"
                min="5"
                max="120"
                value={formData.daily_time_minutes}
                onChange={(e) => setFormData({ ...formData, daily_time_minutes: parseInt(e.target.value) })}
                className="mt-1 block w-full rounded-md border-0 px-3 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="style_preference" className="block text-sm font-medium text-gray-700">
                Feedback Style
              </label>
              <select
                id="style_preference"
                value={formData.style_preference}
                onChange={(e) => setFormData({ ...formData, style_preference: e.target.value })}
                className="mt-1 block w-full rounded-md border-0 px-3 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm"
              >
                <option value="gentle">Gentle (encouraging)</option>
                <option value="strict">Strict (detailed corrections)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Learning Domains (optional)
              </label>
              <div className="space-y-2">
                {['office', 'family', 'movies'].map((domain) => (
                  <label key={domain} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.domains.includes(domain)}
                      onChange={() => toggleDomain(domain)}
                      className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-600"
                    />
                    <span className="ml-2 text-sm text-gray-700 capitalize">{domain}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="flex w-full justify-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 disabled:opacity-50"
            >
              {loading ? 'Creating account...' : 'Create account'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
