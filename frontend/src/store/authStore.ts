
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user';
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
  forgotPassword: (email: string) => Promise<void>;
  resetPassword: (token: string, password: string) => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
      
      login: async (email, password) => {
        set({ isLoading: true, error: null });
        try {
          // Mock API call - in a real app, this would be an API call
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          if (email === 'admin@example.com' && password === 'password') {
            const user = { id: '1', email, name: 'Admin User', role: 'admin' as const };
            const token = 'mock-jwt-token';
            set({ user, token, isAuthenticated: true, isLoading: false });
          } else if (email === 'user@example.com' && password === 'password') {
            const user = { id: '2', email, name: 'Regular User', role: 'user' as const };
            const token = 'mock-jwt-token';
            set({ user, token, isAuthenticated: true, isLoading: false });
          } else {
            throw new Error('Credenciais inválidas');
          }
        } catch (error) {
          set({ error: error instanceof Error ? error.message : 'Erro ao fazer login', isLoading: false });
        }
      },
      
      register: async (email, password, name) => {
        set({ isLoading: true, error: null });
        try {
          // Mock API call - in a real app, this would be an API call
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Simulate successful registration
          if (email && password && name) {
            const user = { id: '3', email, name, role: 'user' as const };
            const token = 'mock-jwt-token';
            set({ user, token, isAuthenticated: true, isLoading: false });
          } else {
            throw new Error('Campos inválidos');
          }
        } catch (error) {
          set({ error: error instanceof Error ? error.message : 'Erro ao registrar', isLoading: false });
        }
      },
      
      logout: () => {
        set({ user: null, token: null, isAuthenticated: false });
      },
      
      forgotPassword: async (email) => {
        set({ isLoading: true, error: null });
        try {
          // Mock API call
          await new Promise(resolve => setTimeout(resolve, 1000));
          set({ isLoading: false });
        } catch (error) {
          set({ error: error instanceof Error ? error.message : 'Erro ao recuperar senha', isLoading: false });
        }
      },
      
      resetPassword: async (token, password) => {
        set({ isLoading: true, error: null });
        try {
          // Mock API call
          await new Promise(resolve => setTimeout(resolve, 1000));
          set({ isLoading: false });
        } catch (error) {
          set({ error: error instanceof Error ? error.message : 'Erro ao redefinir senha', isLoading: false });
        }
      },
      
      clearError: () => {
        set({ error: null });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user, token: state.token, isAuthenticated: state.isAuthenticated }),
    }
  )
);
