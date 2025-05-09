
import { useEffect, createContext, useContext } from 'react';
import { useThemeStore } from '@/store/themeStore';

// Create a context for theme
const ThemeContext = createContext<{
  theme: 'light' | 'dark' | 'system';
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
}>({
  theme: 'system',
  setTheme: () => {},
});

/**
 * Custom hook to access theme context
 */
export const useTheme = () => {
  return useContext(ThemeContext);
};

/**
 * Theme provider component that manages the application's theme
 */
export const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const { theme, setTheme } = useThemeStore();
  
  useEffect(() => {
    const root = window.document.documentElement;
    
    root.classList.remove('light', 'dark');
    
    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      root.classList.add(systemTheme);
    } else {
      root.classList.add(theme);
    }
  }, [theme]);
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
