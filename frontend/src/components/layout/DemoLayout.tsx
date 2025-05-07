
import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Sidebar } from "./Sidebar";
import { Header } from "./Header";
import { AnimatePresence, motion } from "framer-motion";
import {
  Bell,
  Calendar,
  ChevronRight,
  Columns,
  FilePlus,
  LayoutDashboard,
  MessageSquare,
  Info
} from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";

interface DemoLayoutProps {
  children: React.ReactNode;
}

export default function DemoLayout({ children }: DemoLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen overflow-hidden flex-col">
      {/* Demo Mode Alert Banner */}
      <Alert className="bg-primary text-primary-foreground border-none rounded-none">
        <Info className="h-4 w-4" />
        <AlertDescription>
          Você está no modo demonstração. 
          <Link to="/login" className="underline ml-2 font-medium">
            Faça login
          </Link> para acessar todas as funcionalidades.
        </AlertDescription>
      </Alert>

      <div className="flex flex-1 overflow-hidden">
        <AnimatePresence initial={false}>
          {sidebarOpen ? (
            <motion.div
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: "240px", opacity: 1 }}
              exit={{ width: 0, opacity: 0 }}
              transition={{ duration: 0.3, ease: "easeInOut" }}
              className="relative z-20"
            >
              <DemoSidebar setSidebarOpen={setSidebarOpen} />
            </motion.div>
          ) : (
            <motion.div
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: "60px", opacity: 1 }}
              transition={{ duration: 0.3, ease: "easeInOut" }}
              className="relative z-20 hidden md:block"
            >
              <aside className="w-[60px] h-screen flex flex-col border-r border-border bg-background overflow-hidden">
                <div className="h-16 border-b border-border flex items-center justify-center">
                  <div className="font-semibold">CA</div>
                </div>
                <div className="flex-1 py-6 overflow-hidden">
                  <nav className="space-y-1">
                    {[
                      <LayoutDashboard key="dashboard" className="h-5 w-5" />,
                      <Columns key="acompanhamento" className="h-5 w-5" />,
                      <FilePlus key="nova-licitacao" className="h-5 w-5" />,
                      <MessageSquare key="mensagens" className="h-5 w-5" />,
                      <Calendar key="calendario" className="h-5 w-5" />,
                      <Bell key="notificacoes" className="h-5 w-5" />
                    ].map((icon, index) => (
                      <Link
                        key={index}
                        to={[
                          "/demo/dashboard",
                          "/demo/acompanhamento",
                          "/demo/nova-licitacao",
                          "/demo/mensagens",
                          "/demo/calendario",
                          "/demo/notificacoes"
                        ][index]}
                        className="flex justify-center items-center h-10 w-10 mx-auto rounded-md hover:bg-accent hover:text-accent-foreground transition-colors"
                      >
                        {icon}
                      </Link>
                    ))}
                  </nav>
                </div>
                <div className="p-2 border-t border-border">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="w-full h-10 rounded-md flex items-center justify-center"
                    onClick={() => setSidebarOpen(true)}
                  >
                    <ChevronRight className="h-5 w-5" />
                  </Button>
                </div>
              </aside>
            </motion.div>
          )}
        </AnimatePresence>
        
        <motion.main 
          className="flex-1 flex flex-col overflow-hidden"
          initial={false}
          animate={{ 
            marginLeft: sidebarOpen ? "0px" : "0px" 
          }}
          transition={{ duration: 0.3, ease: "easeInOut" }}
        >
          <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} isDemo={true} />
          <div className="flex-1 overflow-auto p-6 bg-perola-50 dark:bg-bluenight-900">
            {children}
          </div>
        </motion.main>
      </div>
    </div>
  );
}

// Demo sidebar - points to demo routes instead of app routes
function DemoSidebar({ setSidebarOpen }: { setSidebarOpen: (open: boolean) => void }) {
  const navigationItems = [
    {
      name: "Dashboard",
      icon: <LayoutDashboard className="mr-2 h-5 w-5" />,
      href: "/demo/dashboard",
    },
    {
      name: "Acompanhamento",
      icon: <Columns className="mr-2 h-5 w-5" />,
      href: "/demo/acompanhamento",
    },
    {
      name: "Nova Licitação",
      icon: <FilePlus className="mr-2 h-5 w-5" />,
      href: "/demo/nova-licitacao",
    },
    {
      name: "Mensagens",
      icon: <MessageSquare className="mr-2 h-5 w-5" />,
      href: "/demo/mensagens",
    },
    {
      name: "Calendário",
      icon: <Calendar className="mr-2 h-5 w-5" />,
      href: "/demo/calendario",
    },
    {
      name: "Notificações",
      icon: <Bell className="mr-2 h-5 w-5" />,
      href: "/demo/notificacoes",
    },
  ];

  // Mock recents contacts data
  const recentContacts = [
    { id: 1, name: "João Silva", unread: 2 },
    { id: 2, name: "Maria Souza", unread: 0 },
    { id: 3, name: "Carlos Mendes", unread: 1 },
  ];

  return (
    <aside className="w-60 h-screen flex flex-col border-r border-border bg-background">
      <div className="h-16 px-4 border-b border-border flex items-center justify-between">
        <div className="font-semibold">CotAi (Demo)</div>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setSidebarOpen(false)}
          className="hover-glow lg:hidden"
          aria-label="Esconder barra lateral"
        >
          <ChevronRight className="h-5 w-5" />
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
              to={`/demo/mensagens/${contact.id}`}
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
      
      {/* Bottom Section 2: Login Button */}
      <div className="p-4 border-t border-border">
        <Button asChild className="w-full" variant="default">
          <Link to="/login">
            <Info className="mr-2 h-4 w-4" />
            Fazer Login
          </Link>
        </Button>
      </div>
    </aside>
  );
}
