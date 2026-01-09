import { create } from 'zustand';
import { User, UserCreate } from '../types';
import apiClient from '../api/client';

interface UserState {
  users: User[];
  loading: boolean;
  fetchUsers: () => Promise<void>;
  createUser: (user: UserCreate) => Promise<void>;
  updateUser: (id: number, user: Partial<UserCreate>) => Promise<void>;
}

export const useUserStore = create<UserState>((set) => ({
  users: [],
  loading: false,
  fetchUsers: async () => {
    set({ loading: true });
    try {
      const response = await apiClient.get('/users/');
      set({ users: response.data, loading: false });
    } catch (error) {
      set({ loading: false });
      console.error('Error fetching users:', error);
    }
  },
  createUser: async (user) => {
    await apiClient.post('/users/', user);
    const response = await apiClient.get('/users/');
    set({ users: response.data });
  },
  updateUser: async (id, user) => {
    await apiClient.put(`/users/${id}`, user);
    const response = await apiClient.get('/users/');
    set({ users: response.data });
  },
}));
