
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "@/providers/ThemeProvider";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { AppLayout } from "@/components/layout/AppLayout";
import LandingPage from "@/pages/LandingPage";
import LoginPage from "@/pages/LoginPage";
import SignupPage from "@/pages/SignupPage";
import ForgotPasswordPage from "@/pages/ForgotPasswordPage";
import DemoPage from "@/pages/DemoPage";
import DashboardPage from "@/pages/dashboard/DashboardPage";
import KanbanPage from "@/pages/kanban/KanbanPage";
import EditaisPage from "@/pages/editais/EditaisPage";
import MensagensPage from "@/pages/mensagens/MensagensPage";
import CalendarioPage from "@/pages/calendario/CalendarioPage";
import PerfilPage from "@/pages/perfil/PerfilPage";
import ConfiguracoesPage from "@/pages/configuracoes/ConfiguracoesPage";
import NotFound from "@/pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <ThemeProvider>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />
            <Route path="/demo" element={<DemoPage />} />
            
            {/* Protected routes */}
            <Route path="/app" element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
              <Route index element={<Navigate to="/app/dashboard" replace />} />
              <Route path="dashboard" element={<DashboardPage />} />
              <Route path="kanban" element={<KanbanPage />} />
              <Route path="editais" element={<EditaisPage />} />
              <Route path="mensagens" element={<MensagensPage />} />
              <Route path="calendario" element={<CalendarioPage />} />
              <Route path="perfil" element={<PerfilPage />} />
              <Route path="configuracoes" element={<ConfiguracoesPage />} />
            </Route>
            
            {/* Catch-all route */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </ThemeProvider>
  </QueryClientProvider>
);

export default App;
