// store/auth-store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User } from '@/lib/types';
import { authApi } from '@/lib/api/auth';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (email: string, password: string) => Promise<boolean>;
  register: (email: string, password: string, firstName?: string, lastName?: string) => Promise<boolean>;
  logout: () => Promise<void>;
  fetchCurrentUser: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          await authApi.login({ email, password });
          const user = await authApi.getCurrentUser();
          
          // Check if user is admin
          if (user.role !== 'admin') {
            await authApi.logout();
            set({
              isLoading: false,
              error: 'Access denied. Admin privileges required.',
              isAuthenticated: false,
              user: null,
            });
            return false;
          }
          
          set({
            user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
          return true;
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.detail || 'Login failed',
            isAuthenticated: false,
            user: null,
          });
          return false;
        }
      },

      register: async (email: string, password: string, firstName?: string, lastName?: string) => {
        set({ isLoading: true, error: null });
        try {
          await authApi.register({
            email,
            password,
            first_name: firstName,
            last_name: lastName,
          });
          set({ isLoading: false });
          return true;
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.detail || 'Registration failed',
          });
          return false;
        }
      },

      logout: async () => {
        await authApi.logout();
        set({
          user: null,
          isAuthenticated: false,
          error: null,
        });
      },

      fetchCurrentUser: async () => {
        set({ isLoading: true });
        try {
          const user = await authApi.getCurrentUser();
          
          // Check if user is admin
          if (user.role !== 'admin') {
            await authApi.logout();
            set({
              isLoading: false,
              isAuthenticated: false,
              user: null,
            });
            return;
          }
          
          set({
            user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
          });
        }
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
