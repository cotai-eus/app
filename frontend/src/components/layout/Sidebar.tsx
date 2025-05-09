
import { FC } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { LayoutDashboard, KanbanSquare, FileText, Mail, Calendar, LogOut } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { useUIStore } from '@/store/uiStore';
import { Button } from '@/components/ui/button';
import { SheetContent } from '@/components/ui/sheet';
import { useI18n } from '@/hooks/useI18n';
import { PermissionGate } from '@/components/auth/PermissionGate';
import { trackEvent } from '@/providers/ErrorBoundary';

interface NavItemProps {
  href: string;
  label: string;
  icon: JSX.Element;
  isActive: boolean;
  onClick?: () => void;
  permission?: string;
}

interface SidebarProps {
  isMobile?: boolean;
}

const NavItem: FC<NavItemProps> = ({ href, label, icon, isActive, onClick }) => {
  return (
    <Link
      to={href}
      className="w-full block"
      onClick={onClick}
    >
      <Button
        variant={isActive ? 'default' : 'ghost'}
        className={cn(
          "w-full justify-start gap-3 mb-1 rounded-lg",
          isActive && "bg-sidebar-primary text-sidebar-primary-foreground"
        )}
      >
        {icon}
        <span>{label}</span>
        {isActive && (
          <motion.div
            layoutId="sidebar-indicator"
            className="absolute right-2 w-1 h-4 bg-background rounded-full"
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
          />
        )}
      </Button>
    </Link>
  );
};

/**
 * Sidebar component for navigation
 * @param {boolean} isMobile - Whether the sidebar is rendered on mobile
 */
export const Sidebar: FC<SidebarProps> = ({ isMobile = false }) => {
  const location = useLocation();
  const { logout } = useAuth();
  const { setSidebarOpen } = useUIStore();
  const { t } = useI18n();
  
  const isActive = (path: string) => location.pathname === path;
  
  const handleItemClick = () => {
    if (isMobile) {
      setSidebarOpen(false);
    }
    
    // Track navigation events
    trackEvent('navigation', { path: location.pathname });
  };
  
  const handleLogout = () => {
    logout();
    handleItemClick();
  };

  const Content = (
    <div className="flex flex-col h-full">
      <div className="p-4">
        <h2 className="text-2xl font-bold mb-6 text-sidebar-foreground">Portal Licitações</h2>
        
        <nav className="space-y-1">
          <NavItem
            href="/app/dashboard"
            label={t('nav.dashboard')}
            icon={<LayoutDashboard size={18} />}
            isActive={isActive('/app/dashboard')}
            onClick={handleItemClick}
          />
          
          <PermissionGate permissions={['kanban:view']}>
            <NavItem
              href="/app/kanban"
              label={t('nav.kanban')}
              icon={<KanbanSquare size={18} />}
              isActive={isActive('/app/kanban')}
              onClick={handleItemClick}
            />
          </PermissionGate>
          
          <PermissionGate permissions={['editais:view']}>
            <NavItem
              href="/app/editais"
              label={t('nav.editais')}
              icon={<FileText size={18} />}
              isActive={isActive('/app/editais')}
              onClick={handleItemClick}
            />
          </PermissionGate>
          
          <PermissionGate permissions={['mensagens:view']}>
            <NavItem
              href="/app/mensagens"
              label={t('nav.mensagens')}
              icon={<Mail size={18} />}
              isActive={isActive('/app/mensagens')}
              onClick={handleItemClick}
            />
          </PermissionGate>
          
          <PermissionGate permissions={['calendario:view']}>
            <NavItem
              href="/app/calendario"
              label={t('nav.calendario')}
              icon={<Calendar size={18} />}
              isActive={isActive('/app/calendario')}
              onClick={handleItemClick}
            />
          </PermissionGate>
        </nav>
      </div>
      
      <div className="mt-auto p-4">
        <Button 
          variant="ghost" 
          className="w-full justify-start gap-3 text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
          onClick={handleLogout}
        >
          <LogOut size={18} />
          <span>{t('auth.logout')}</span>
        </Button>
      </div>
    </div>
  );
  
  if (isMobile) {
    return <SheetContent side="left" className="bg-sidebar p-0 w-[280px]">{Content}</SheetContent>;
  }
  
  return (
    <AnimatePresence>
      <motion.aside
        initial={{ width: 0, opacity: 0 }}
        animate={{ width: 280, opacity: 1 }}
        exit={{ width: 0, opacity: 0 }}
        transition={{ duration: 0.3 }}
        className="hidden md:block h-screen border-r border-border bg-sidebar sticky top-0 overflow-y-auto overflow-x-hidden w-[280px]"
      >
        {Content}
      </motion.aside>
    </AnimatePresence>
  );
};
