
import { useState } from 'react';
import { Bell } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuGroup,
  DropdownMenuItem, 
  DropdownMenuLabel, 
  DropdownMenuSeparator, 
  DropdownMenuTrigger 
} from '@/components/ui/dropdown-menu';
import { Badge } from '@/components/ui/badge';
import { Link } from 'react-router-dom';

interface Notification {
  id: string;
  type: 'edital' | 'mensagem' | 'calendario';
  title: string;
  description: string;
  date: string;
  read: boolean;
  link: string;
}

// Mock notifications data
const mockNotifications: Notification[] = [
  {
    id: '1',
    type: 'edital',
    title: 'Novo edital disponível',
    description: 'Edital municipal nº 45/2023 foi publicado.',
    date: '2023-06-15',
    read: false,
    link: '/app/editais'
  },
  {
    id: '2',
    type: 'mensagem',
    title: 'Nova mensagem recebida',
    description: 'Prefeitura Municipal respondeu à sua proposta.',
    date: '2023-06-16',
    read: false,
    link: '/app/mensagens'
  },
  {
    id: '3',
    type: 'calendario',
    title: 'Evento próximo',
    description: 'Abertura de propostas amanhã às 10h.',
    date: '2023-06-17',
    read: true,
    link: '/app/calendario'
  }
];

export const NotificationDropdown = () => {
  const [notifications, setNotifications] = useState<Notification[]>(mockNotifications);
  
  const unreadCount = notifications.filter(notification => !notification.read).length;
  
  const markAsRead = (id: string) => {
    setNotifications(notifications.map(notification => 
      notification.id === id 
        ? { ...notification, read: true } 
        : notification
    ));
  };
  
  const markAllAsRead = () => {
    setNotifications(notifications.map(notification => ({ ...notification, read: true })));
  };
  
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="h-5 w-5" />
          {unreadCount > 0 && (
            <Badge 
              className="absolute -top-1 -right-1 px-1.5 py-0.5 min-w-[16px] h-4 text-[10px] bg-red-500 hover:bg-red-600"
              variant="destructive"
            >
              {unreadCount}
            </Badge>
          )}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-80">
        <DropdownMenuLabel className="flex items-center justify-between">
          <span>Notificações</span>
          {unreadCount > 0 && (
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={markAllAsRead}
              className="text-xs h-7 px-2"
            >
              Marcar todas como lidas
            </Button>
          )}
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        
        <DropdownMenuGroup>
          {notifications.length > 0 ? (
            notifications.map((notification) => (
              <DropdownMenuItem 
                key={notification.id} 
                className={`p-0 focus:bg-transparent ${!notification.read ? 'bg-muted/50' : ''}`}
              >
                <Link 
                  to={notification.link}
                  className="p-3 flex flex-col w-full"
                  onClick={() => markAsRead(notification.id)}
                >
                  <div className="flex justify-between items-baseline">
                    <h4 className="font-medium text-sm">{notification.title}</h4>
                    <span className="text-xs text-muted-foreground">
                      {new Date(notification.date).toLocaleDateString('pt-BR')}
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">{notification.description}</p>
                  
                  <Badge 
                    className="self-start mt-2" 
                    variant={
                      notification.type === 'edital' ? 'default' : 
                      notification.type === 'mensagem' ? 'outline' : 'secondary'
                    }
                  >
                    {notification.type === 'edital' ? 'Edital' : 
                     notification.type === 'mensagem' ? 'Mensagem' : 'Calendário'}
                  </Badge>
                </Link>
              </DropdownMenuItem>
            ))
          ) : (
            <div className="py-6 text-center text-muted-foreground">
              Nenhuma notificação disponível
            </div>
          )}
        </DropdownMenuGroup>
        
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem asChild className="justify-center">
            <Link to="/app/notificacoes" className="w-full text-center">
              Ver todas as notificações
            </Link>
          </DropdownMenuItem>
        </DropdownMenuGroup>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
