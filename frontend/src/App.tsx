
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "@/providers/ThemeProvider";
import { AppLayout } from "@/components/layout/AppLayout";
import Index from "./pages/Index";
import DashboardPage from "./pages/DashboardPage";
import NotFound from "./pages/NotFound";
import NovaLicitacaoPage from "./pages/NovaLicitacaoPage";
import AcompanhamentoPage from "./pages/AcompanhamentoPage";
import MensagensPage from "./pages/MensagensPage";
import CalendarioPage from "./pages/CalendarioPage";
import NotificacoesPage from "./pages/NotificacoesPage";
import LoginPage from "./pages/auth/LoginPage";
import SignupPage from "./pages/auth/SignupPage";
import ForgotPasswordPage from "./pages/auth/ForgotPasswordPage";
import ResetPasswordPage from "./pages/auth/ResetPasswordPage";
import PerfilPage from "./pages/PerfilPage";
import ConfiguracoesPage from "./pages/ConfiguracoesPage";
import DemoLayout from "./components/layout/DemoLayout";

// Mock authentication state for demonstration purposes
const isAuthenticated = () => {
  return false; // Change this to implement real authentication later
};

// Auth guard component
const RequireAuth = ({ children }: { children: JSX.Element }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <ThemeProvider defaultTheme="dark">
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Index />} />
            
            {/* Auth routes */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/esqueci-senha" element={<ForgotPasswordPage />} />
            <Route path="/resetar-senha" element={<ResetPasswordPage />} />
            
            {/* Demo routes - publicly accessible */}
            <Route 
              path="/demo/*" 
              element={
                <DemoLayout>
                  <Routes>
                    <Route path="/dashboard" element={<DashboardPage />} />
                    <Route path="/acompanhamento" element={<AcompanhamentoPage />} />
                    <Route path="/nova-licitacao" element={<NovaLicitacaoPage />} />
                    <Route path="/mensagens" element={<MensagensPage />} />
                    <Route path="/mensagens/:id" element={<MensagensPage />} />
                    <Route path="/calendario" element={<CalendarioPage />} />
                    <Route path="/notificacoes" element={<NotificacoesPage />} />
                    <Route path="/perfil" element={<PerfilPage />} />
                    <Route path="/configuracoes" element={<ConfiguracoesPage />} />
                    <Route path="*" element={<NotFound />} />
                  </Routes>
                </DemoLayout>
              } 
            />
            
            {/* Protected app routes - requires authentication */}
            <Route 
              path="/app/*" 
              element={
                <RequireAuth>
                  <AppLayout>
                    <Routes>
                      <Route path="/dashboard" element={<DashboardPage />} />
                      <Route path="/acompanhamento" element={<AcompanhamentoPage />} />
                      <Route path="/nova-licitacao" element={<NovaLicitacaoPage />} />
                      <Route path="/mensagens" element={<MensagensPage />} />
                      <Route path="/mensagens/:id" element={<MensagensPage />} />
                      <Route path="/calendario" element={<CalendarioPage />} />
                      <Route path="/notificacoes" element={<NotificacoesPage />} />
                      <Route path="/perfil" element={<PerfilPage />} />
                      <Route path="/configuracoes" element={<ConfiguracoesPage />} />
                      <Route path="*" element={<NotFound />} />
                    </Routes>
                  </AppLayout>
                </RequireAuth>
              } 
            />
            
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </ThemeProvider>
  </QueryClientProvider>
);

export default App;
