
import React from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ChevronLeft } from "lucide-react";
import {
  Bell,
  Calendar,
  LayoutDashboard,
  MessageSquare,
  FilePlus,
  Columns,
} from "lucide-react";

interface SidebarProps {
  setSidebarOpen: (open: boolean) => void;
}

const navigationItems = [
  {
    name: "Dashboard",
    icon: <LayoutDashboard className="mr-2 h-5 w-5" />,
    href: "/app/dashboard",
  },
  {
    name: "Acompanhamento",
    icon: <Columns className="mr-2 h-5 w-5" />,
    href: "/app/acompanhamento",
  },
  {
    name: "Nova Licitação",
    icon: <FilePlus className="mr-2 h-5 w-5" />,
    href: "/app/nova-licitacao",
  },
  {
    name: "Mensagens",
    icon: <MessageSquare className="mr-2 h-5 w-5" />,
    href: "/app/mensagens",
  },
  {
    name: "Calendário",
    icon: <Calendar className="mr-2 h-5 w-5" />,
    href: "/app/calendario",
  },
  {
    name: "Notificações",
    icon: <Bell className="mr-2 h-5 w-5" />,
    href: "/app/notificacoes",
  },
];

// Mock recents contacts data
const recentContacts = [
  { id: 1, name: "João Silva", unread: 2 },
  { id: 2, name: "Maria Souza", unread: 0 },
  { id: 3, name: "Carlos Mendes", unread: 1 },
];

export function Sidebar({ setSidebarOpen }: SidebarProps) {
  return (
    <aside className="w-60 h-screen flex flex-col border-r border-border bg-background">
      <div className="h-16 px-4 border-b border-border flex items-center justify-between">
        <div className="font-semibold">CotAi</div>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setSidebarOpen(false)}
          className="hover-glow lg:hidden"
          aria-label="Esconder barra lateral"
        >
          <ChevronLeft className="h-5 w-5" />
        </Button>
      </div>
      
      <div className="flex-1 py-6 overflow-y-auto">
        <nav className="space-y-1 px-2">
          {navigationItems.map((item) => (
            <Link
              key={item.name}
              to={item.href}
              className="flex items-center px-3 py-2 text-sm font-medium rounded-md hover:bg-accent hover:text-accent-foreground transition-colors"
            >
              {item.icon}
              {item.name}
            </Link>
          ))}
        </nav>
      </div>
      
      {/* Bottom Section 1: Recent Contacts */}
      <div className="px-4 py-2 border-t border-border">
        <h3 className="text-xs font-semibold text-muted-foreground mb-2">Últimos Contatos</h3>
        <div className="space-y-1">
          {recentContacts.map((contact) => (
            <Link
              key={contact.id}
              to={`/app/mensagens/${contact.id}`}
              className="flex items-center justify-between px-2 py-1.5 text-sm rounded-md hover:bg-accent hover:text-accent-foreground transition-colors"
            >
              <span>{contact.name}</span>
              {contact.unread > 0 && (
                <span className="inline-flex items-center justify-center w-5 h-5 text-xs font-medium bg-primary text-primary-foreground rounded-full">
                  {contact.unread}
                </span>
              )}
            </Link>
          ))}
        </div>
      </div>
      
      {/* Bottom Section 2: New Bid Button */}
      <div className="p-4 border-t border-border">
        <Button asChild className="w-full" variant="default">
          <Link to="/app/nova-licitacao">
            <FilePlus className="mr-2 h-4 w-4" />
            Nova Licitação
          </Link>
        </Button>
      </div>
    </aside>
  );
}
