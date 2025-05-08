import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// At the top of your file
console.log("API URL:", API_URL);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = JSON.parse(localStorage.getItem('auth-storage') || '{}')?.state?.token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  is_admin?: boolean;
  is_active?: boolean;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: { username: string; email: string; password: string; full_name: string }) => Promise<void>;
  logout: () => void;
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
          console.log('Attempting login:', { email });
          
          // This endpoint should match your FastAPI backend
          const response = await api.post('/api/v1/auth/login/access-token', 
            new URLSearchParams({
              username: email,
              password,
            }),
            {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
              },
            }
          );
          
          const { access_token } = response.data;
          console.log('Login successful, token received');
          
          // Get user data with the token
          const userResponse = await api.get('/api/v1/users/me', {
            headers: {
              Authorization: `Bearer ${access_token}`
            }
          });
          
          console.log('User data retrieved:', userResponse.data);
          
          set({ 
            user: userResponse.data, 
            token: access_token, 
            isAuthenticated: true, 
            isLoading: false 
          });
        } catch (error) {
          console.error("Login error:", error.response || error);
          set({ 
            error: error.response?.data?.detail || 'Credenciais inválidas', 
            isLoading: false 
          });
          throw error;
        }
      },
      
      register: async (userData) => {
        set({ isLoading: true, error: null });
        try {
          console.log('Attempting registration:', userData);
          
          // Adjust payload format if necessary to match backend expectations
          const registrationData = {
            email: userData.email,
            password: userData.password,
            username: userData.username,
            full_name: userData.full_name,
            // Add any other required fields
          };
          
          // Try one of these endpoints
          await api.post('/api/v1/auth/signup', registrationData);
          // or
          // await api.post('/api/v1/auth/register', registrationData);
          // or 
          // await api.post('/api/v1/users/', registrationData);
          
          console.log('Registration successful, now logging in');
          
          // Login automatically after successful registration
          const loginResponse = await api.post('/api/v1/auth/login/access-token', 
            new URLSearchParams({
              username: userData.email,
              password: userData.password,
            }),
            {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
              },
            }
          );
          
          const { access_token } = loginResponse.data;
          console.log('Login successful, token received');
          
          // Get user data
          const userResponse = await api.get('/api/v1/users/me', {
            headers: {
              Authorization: `Bearer ${access_token}`
            }
          });
          
          console.log('User data retrieved:', userResponse.data);
          
          set({ 
            user: userResponse.data, 
            token: access_token, 
            isAuthenticated: true,
            isLoading: false 
          });
        } catch (error) {
          console.error("Registration error:", error);
          
          // Log detailed error information
          if (error.response) {
            // The request was made and the server responded with an error status
            console.error("Error response:", {
              data: error.response.data,
              status: error.response.status,
              headers: error.response.headers
            });
            
            // If backend returns validation errors, they may be in data.detail or another format
            const errorMessage = typeof error.response.data === 'object' ? 
              JSON.stringify(error.response.data) : 
              error.response.data?.detail || 'Erro ao registrar. Verifique os dados e tente novamente.';
            
            set({ error: errorMessage, isLoading: false });
          } else if (error.request) {
            // The request was made but no response was received
            console.error("No response received:", error.request);
            set({ error: "Servidor não respondeu. Verifique sua conexão.", isLoading: false });
          } else {
            // Something happened in setting up the request
            console.error("Request setup error:", error.message);
            set({ error: "Erro ao configurar requisição: " + error.message, isLoading: false });
          }
          
          throw error;
        }
      },
      
      logout: () => {
        set({ user: null, token: null, isAuthenticated: false });
      },
      
      clearError: () => {
        set({ error: null });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        user: state.user, 
        token: state.token, 
        isAuthenticated: state.isAuthenticated 
      }),
    }
  )
);
