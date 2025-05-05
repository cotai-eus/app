
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
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
            
            {/* Rotas da aplicação com layout compartilhado */}
            <Route 
              path="/app/*" 
              element={
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
