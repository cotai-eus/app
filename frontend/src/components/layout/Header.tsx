
import React, { useState } from "react";
import { ThemeToggle } from "../theme/ThemeToggle";
import { Button } from "@/components/ui/button";
import { ChevronLeft, ChevronRight, Bell, User, Info } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useLocation, Link } from "react-router-dom";

interface HeaderProps {
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  isDemo?: boolean;
}

export function Header({ sidebarOpen, setSidebarOpen, isDemo = false }: HeaderProps) {
  const location = useLocation();
  const [hasNotifications, setHasNotifications] = useState(true);

  // Function to get the page title based on current path
  const getPageTitle = () => {
    const path = location.pathname;
    
    if (path.includes("/dashboard")) return "Dashboard";
    if (path.includes("/acompanhamento")) return "Acompanhamento";
    if (path.includes("/nova-licitacao")) return "Nova Licitação";
    if (path.includes("/mensagens")) return "Mensagens";
    if (path.includes("/calendario")) return "Calendário";
    if (path.includes("/notificacoes")) return "Notificações";
    
    return "CotAi Licitação Hub";
  };

  // Get the correct route prefix based on demo mode
  const getRoutePrefix = () => isDemo ? "/demo" : "/app";

  return (
    <header className="h-16 px-4 border-b border-border flex items-center justify-between bg-background/80 backdrop-blur-sm">
      <div className="flex items-center">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="hover-glow mr-4"
          aria-label={sidebarOpen ? "Esconder barra lateral" : "Mostrar barra lateral"}
        >
          {sidebarOpen ? (
            <ChevronLeft className="h-5 w-5" />
          ) : (
            <ChevronRight className="h-5 w-5" />
          )}
        </Button>
        <h1 className="text-xl font-semibold">
          {isDemo ? "Demo: " : ""}{getPageTitle()}
        </h1>
      </div>
      
      <div className="flex items-center gap-4">
        {/* Login Button for Demo Mode */}
        {isDemo && (
          <Button variant="outline" size="sm" asChild className="mr-2">
            <Link to="/login">
              <User className="mr-2 h-4 w-4" />
              Login
            </Link>
          </Button>
        )}
        
        {/* Notification Bell */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" className="relative hover-glow">
              <Bell className="h-5 w-5" />
              {hasNotifications && (
                <span className="absolute top-1 right-1 h-2 w-2 bg-red-500 rounded-full"></span>
              )}
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-72">
            <DropdownMenuLabel>Notificações</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <div className="max-h-80 overflow-y-auto">
              <DropdownMenuItem className="flex flex-col items-start py-2">
                <p className="font-medium">Nova licitação disponível</p>
                <p className="text-sm text-muted-foreground">Prefeitura de São Paulo - Edital 2025/001</p>
              </DropdownMenuItem>
              <DropdownMenuItem className="flex flex-col items-start py-2">
                <p className="font-medium">Prazo se aproximando</p>
                <p className="text-sm text-muted-foreground">Edital 2025/003 - 2 dias restantes</p>
              </DropdownMenuItem>
            </div>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="justify-center font-medium">
              <Link to={`${getRoutePrefix()}/notificacoes`}>Ver todas as notificações</Link>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
        
        {/* User Menu */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" className="hover-glow">
              <User className="h-5 w-5" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Minha Conta</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem asChild>
              <Link to={`${getRoutePrefix()}/perfil`}>Perfil</Link>
            </DropdownMenuItem>
            <DropdownMenuItem asChild>
              <Link to={`${getRoutePrefix()}/configuracoes`}>Configurações</Link>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            {isDemo ? (
              <DropdownMenuItem asChild>
                <Link to="/login">Fazer Login</Link>
              </DropdownMenuItem>
            ) : (
              <DropdownMenuItem>Sair</DropdownMenuItem>
            )}
          </DropdownMenuContent>
        </DropdownMenu>
        
        <ThemeToggle />
      </div>
    </header>
  );
}
