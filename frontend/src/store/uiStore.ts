
import { create } from 'zustand';

interface UIState {
  isSidebarOpen: boolean;
  isPageLoading: boolean;
  toastMessage: { type: 'success' | 'error' | 'info'; message: string } | null;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  setPageLoading: (loading: boolean) => void;
  showToast: (type: 'success' | 'error' | 'info', message: string) => void;
  clearToast: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  isSidebarOpen: false,
  isPageLoading: false,
  toastMessage: null,
  
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  setSidebarOpen: (open) => set({ isSidebarOpen: open }),
  setPageLoading: (loading) => set({ isPageLoading: loading }),
  
  showToast: (type, message) => set({ toastMessage: { type, message } }),
  clearToast: () => set({ toastMessage: null }),
}));
