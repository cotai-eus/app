
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
  MessageSquare
} from "lucide-react";

interface AppLayoutProps {
  children: React.ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen overflow-hidden">
      <AnimatePresence initial={false}>
        {sidebarOpen ? (
          <motion.div
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: "240px", opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className="relative z-20"
          >
            <Sidebar setSidebarOpen={setSidebarOpen} />
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
                        "/app/dashboard",
                        "/app/acompanhamento",
                        "/app/nova-licitacao",
                        "/app/mensagens",
                        "/app/calendario",
                        "/app/notificacoes"
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
        <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
        <div className="flex-1 overflow-auto p-6 bg-perola-50 dark:bg-bluenight-900">
          {children}
        </div>
      </motion.main>
    </div>
  );
}
