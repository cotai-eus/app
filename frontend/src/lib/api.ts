import axios from 'axios';
import { useAuthStore } from '@/store/authStore';
import { useUIStore } from '@/store/uiStore';
import { trackError } from '@/providers/ErrorBoundary';

const API_URL = import.meta.env.VITE_API_URL || 'https://api.example.com';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    trackError(error, { type: 'api_request' });
    return Promise.reject(error);
  }
);

// Adicionar função para renovação de token
export const refreshToken = async () => {
  try {
    const response = await axios.post(`${API_URL}/auth/refresh-token`, {}, {
      headers: {
        'Authorization': `Bearer ${useAuthStore.getState().token}`
      }
    });
    
    const { token, user } = response.data;
    useAuthStore.getState().setToken(token, user);
    return token;
  } catch (error) {
    useAuthStore.getState().logout();
    throw error;
  }
};

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const { response, config } = error;
    
    // Track error with Sentry
    trackError(error, { 
      type: 'api_response', 
      status: response?.status, 
      url: response?.config?.url,
      method: response?.config?.method
    });
    
    // Add token refresh logic
    if (response && response.status === 401 && !config._retry) {
      config._retry = true;
      try {
        const newToken = await refreshToken();
        config.headers.Authorization = `Bearer ${newToken}`;
        return api(config);
      } catch (refreshError) {
        // Token refresh failed, logout
        useAuthStore.getState().logout();
        useUIStore.getState().showToast('error', 'Sua sessão expirou. Por favor, faça login novamente.');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    const errorMessage = response?.data?.message || 'Ocorreu um erro na requisição';
    useUIStore.getState().showToast('error', errorMessage);
    
    return Promise.reject(error);
  }
);

// Adicionar método ao authStore para atualizar token
useAuthStore.setState({
  ...useAuthStore.getState(),
  setToken: (token, user) => {
    useAuthStore.setState({ token, user, isAuthenticated: true });
  }
});

export default api;

// API endpoints
export const authAPI = {
  login: (data: { email: string; password: string }) => api.post('/auth/login', data),
  register: (data: { name: string; email: string; password: string }) => api.post('/auth/register', data),
  forgotPassword: (data: { email: string }) => api.post('/auth/forgot-password', data),
  resetPassword: (data: { token: string; password: string }) => api.post('/auth/reset-password', data),
  me: () => api.get('/auth/me'),
};

export const licitacoesAPI = {
  getAll: () => api.get('/licitacoes'),
  getById: (id: string) => api.get(`/licitacoes/${id}`),
  create: (data: any) => api.post('/licitacoes', data),
  update: (id: string, data: any) => api.put(`/licitacoes/${id}`, data),
  delete: (id: string) => api.delete(`/licitacoes/${id}`),
};

export const editaisAPI = {
  getAll: () => api.get('/editais'),
  getById: (id: string) => api.get(`/editais/${id}`),
  create: (data: FormData) => api.post('/editais', data, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  update: (id: string, data: FormData) => api.put(`/editais/${id}`, data, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  delete: (id: string) => api.delete(`/editais/${id}`),
};

export const mensagensAPI = {
  getAll: () => api.get('/mensagens'),
  getById: (id: string) => api.get(`/mensagens/${id}`),
  create: (data: any) => api.post('/mensagens', data),
  update: (id: string, data: any) => api.put(`/mensagens/${id}`, data),
  delete: (id: string) => api.delete(`/mensagens/${id}`),
};

export const calendarioAPI = {
  getEvents: () => api.get('/calendario/eventos'),
  createEvent: (data: any) => api.post('/calendario/eventos', data),
  updateEvent: (id: string, data: any) => api.put(`/calendario/eventos/${id}`, data),
  deleteEvent: (id: string) => api.delete(`/calendario/eventos/${id}`),
};

// Adicionar endpoints para perfil
export const profileAPI = {
  update: (data: any) => api.put('/profile', data),
  updateAvatar: (file: File) => {
    const formData = new FormData();
    formData.append('avatar', file);
    return api.post('/profile/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};
