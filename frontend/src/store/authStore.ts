import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import CryptoJS from 'crypto-js';

const STORAGE_KEY = 'auth-storage';
const ENCRYPTION_KEY = 'lovable-auth-secure-key'; // In production, use environment variables

// Create secure storage with encryption
const secureStorage = {
  getItem: (name: string) => {
    const persistedState = localStorage.getItem(name);
    if (!persistedState) return null;
    try {
      const decrypted = CryptoJS.AES.decrypt(persistedState, ENCRYPTION_KEY).toString(CryptoJS.enc.Utf8);
      return JSON.parse(decrypted);
    } catch (error) {
      console.error('Failed to decrypt auth state:', error);
      return null;
    }
  },
  setItem: (name: string, value: string) => {
    const encrypted = CryptoJS.AES.encrypt(value, ENCRYPTION_KEY).toString();
    localStorage.setItem(name, encrypted);
  },
  removeItem: (name: string) => localStorage.removeItem(name),
};

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
  updateProfile: (userData: Partial<User>) => Promise<void>; // Nova função
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
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

      updateProfile: async (userData) => {
        set({ isLoading: true, error: null });
        try {
          // Mock API call - in a real app, this would be an API call
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          const currentUser = get().user;
          if (!currentUser) {
            throw new Error('Usuário não autenticado');
          }
          
          // Update user with new data
          const updatedUser = { ...currentUser, ...userData };
          set({ user: updatedUser, isLoading: false });
        } catch (error) {
          set({ error: error instanceof Error ? error.message : 'Erro ao atualizar perfil', isLoading: false });
        }
      },
    }),
    {
      name: STORAGE_KEY,
      storage: createJSONStorage(() => secureStorage),
      partialize: (state) => ({ 
        user: state.user, 
        token: state.token, 
        isAuthenticated: state.isAuthenticated 
      }),
    }
  )
);
