import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, AuthToken } from '../types';
import apiClient from '../api/client';

interface AuthStore {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  login: (token: AuthToken) => Promise<void>;
  logout: () => void;
  fetchMe: () => Promise<void>;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      token: null,
      user: null,
      isAuthenticated: false,
      login: async (authToken) => {
        set({ 
          token: authToken.access_token, 
          isAuthenticated: true 
        });
        await get().fetchMe();
      },
      logout: () => {
        set({ token: null, user: null, isAuthenticated: false });
        localStorage.removeItem('auth-storage');
      },
      fetchMe: async () => {
        try {
          const response = await apiClient.get('/users/me'); // Precisaremos criar este endpoint no back
          set({ user: response.data });
        } catch (error) {
          console.error('Error fetching user info:', error);
          get().logout();
        }
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
