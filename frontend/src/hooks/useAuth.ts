
import { useState } from 'react';
import { useAuthStore } from '@/store/authStore';
import { setUserContext, clearUserContext, trackError } from '@/providers/ErrorBoundary';

export const useAuth = () => {
  const { 
    user, 
    token, 
    isAuthenticated, 
    isLoading, 
    error,
    login,
    register,
    logout,
    forgotPassword,
    resetPassword,
    clearError
  } = useAuthStore();
  
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Enhanced login with error tracking
  const handleLogin = async (email: string, password: string) => {
    setIsSubmitting(true);
    try {
      await login(email, password);
      
      // If login successful, set user context for error tracking
      if (user) {
        setUserContext({
          id: user.id,
          email: user.email,
          role: user.role
        });
      }
    } catch (error) {
      trackError(error, { action: 'login', email });
      throw error;
    } finally {
      setIsSubmitting(false);
    }
  };

  // Enhanced registration with error tracking
  const handleRegister = async (email: string, password: string, name: string) => {
    setIsSubmitting(true);
    try {
      await register(email, password, name);
      
      // If registration successful, set user context for error tracking
      if (user) {
        setUserContext({
          id: user.id,
          email: user.email,
          role: user.role
        });
      }
    } catch (error) {
      trackError(error, { action: 'register', email });
      throw error;
    } finally {
      setIsSubmitting(false);
    }
  };

  // Enhanced logout with error tracking
  const handleLogout = () => {
    try {
      logout();
      // Clear user context from error tracking
      clearUserContext();
    } catch (error) {
      trackError(error, { action: 'logout' });
    }
  };

  return {
    user,
    token,
    isAuthenticated,
    isLoading: isLoading || isSubmitting,
    error,
    login: handleLogin,
    register: handleRegister,
    logout: handleLogout,
    forgotPassword,
    resetPassword,
    clearError
  };
};
