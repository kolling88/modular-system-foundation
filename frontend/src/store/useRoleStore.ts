import { create } from 'zustand';
import { Role, RoleCreate } from '../types';
import apiClient from '../api/client';

interface RoleState {
  roles: Role[];
  loading: boolean;
  fetchRoles: () => Promise<void>;
  createRole: (role: RoleCreate) => Promise<void>;
}

export const useRoleStore = create<RoleState>((set) => ({
  roles: [],
  loading: false,
  fetchRoles: async () => {
    set({ loading: true });
    try {
      const response = await apiClient.get('/roles/');
      set({ roles: response.data, loading: false });
    } catch (error) {
      set({ loading: false });
      console.error('Error fetching roles:', error);
    }
  },
  createRole: async (role) => {
    await apiClient.post('/roles/', role);
    const response = await apiClient.get('/roles/');
    set({ roles: response.data });
  },
}));
