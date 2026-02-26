'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { LearnerProfile } from '@/types';

interface AuthContextType {
  user: LearnerProfile | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  refreshProfile: () => Promise<void>;
}

interface RegisterData {
  email: string;
  password: string;
  native_language: string;
  target_goal: string;
  daily_time_minutes: number;
  style_preference: string;
  domains: string[];
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<LearnerProfile | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load token from localStorage on mount
    const storedToken = localStorage.getItem('auth_token');
    if (storedToken) {
      setToken(storedToken);
      loadProfile(storedToken);
    } else {
      setLoading(false);
    }
  }, []);

  const loadProfile = async (authToken: string) => {
    try {
      const profile = await api.get<LearnerProfile>('/learner/profile', {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });
      setUser(profile);
    } catch (error) {
      console.error('Failed to load profile:', error);
      // Clear invalid token
      localStorage.removeItem('auth_token');
      setToken(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const response = await api.post<{ access_token: string }>('/auth/login', {
      email,
      password,
    });

    const { access_token } = response;
    localStorage.setItem('auth_token', access_token);
    setToken(access_token);
    await loadProfile(access_token);
  };

  const register = async (data: RegisterData) => {
    const response = await api.post<{ access_token: string }>('/auth/register', data);

    const { access_token } = response;
    localStorage.setItem('auth_token', access_token);
    setToken(access_token);
    await loadProfile(access_token);
  };

  const logout = async () => {
    try {
      if (token) {
        await api.post('/auth/logout', undefined, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('auth_token');
      setToken(null);
      setUser(null);
    }
  };

  const refreshProfile = async () => {
    if (token) {
      await loadProfile(token);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login,
        register,
        logout,
        refreshProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
