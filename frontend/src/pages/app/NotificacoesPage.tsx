
import React, { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Bell,
  Calendar,
  FileText,
  AlertTriangle,
  CheckCircle,
  Clock,
  Filter,
  CheckCheck,
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { format, isToday, isYesterday, addDays, subDays } from "date-fns";
import { ptBR } from "date-fns/locale";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";

// Mock notification data
const mockNotifications = [
  {
    id: "notif-1",
    title: "Novo Edital Disponível",
    message: "Um novo edital foi publicado que corresponde aos seus critérios de busca.",
    date: new Date(),
    read: false,
    type: "info",
    link: "/app/nova-licitacao",
    urgent: false,
  },
  {
    id: "notif-2",
    title: "Prazo se Aproximando",
    message: "O prazo para submissão da proposta #2025/045 vence em 2 dias.",
    date: new Date(),
    read: false,
    type: "warning",
    link: "/app/acompanhamento",
    urgent: true,
  },
  {
    id: "notif-3",
    title: "Documento Assinado",
    message: "A proposta técnica foi assinada com sucesso por João Silva.",
    date: subDays(new Date(), 1),
    read: true,
    type: "success",
    link: "/app/acompanhamento",
    urgent: false,
  },
  {
    id: "notif-4",
    title: "Reunião Agendada",
    message: "Uma reunião de revisão da proposta foi agendada para amanhã às 14:00.",
    date: subDays(new Date(), 1),
    read: false,
    type: "info",
    link: "/app/calendario",
    urgent: false,
  },
  {
    id: "notif-5",
    title: "Análise de Edital Concluída",
    message: "A análise automática do edital #2025/078 foi concluída com sucesso.",
    date: subDays(new Date(), 2),
    read: true,
    type: "success",
    link: "/app/acompanhamento",
    urgent: false,
  },
  {
    id: "notif-6",
    title: "Erro na Submissão",
    message: "Houve um erro ao submeter sua proposta. Verifique os documentos e tente novamente.",
    date: subDays(new Date(), 3),
    read: false,
    type: "error",
    link: "/app/acompanhamento",
    urgent: true,
  },
  {
    id: "notif-7",
    title: "Nova Mensagem",
    message: "Você recebeu uma nova mensagem de Maria Souza.",
    date: subDays(new Date(), 4),
    read: true,
    type: "info",
    link: "/app/mensagens/2",
    urgent: false,
  },
];

const NotificacoesPage = () => {
  const [notifications, setNotifications] = useState(mockNotifications);
  const [activeTab, setActiveTab] = useState("todas");
  const { toast } = useToast();

  // Format date for display
  const formatNotificationDate = (date: Date) => {
    if (isToday(date)) {
      return `Hoje, ${format(date, "HH:mm", { locale: ptBR })}`;
    } else if (isYesterday(date)) {
      return `Ontem, ${format(date, "HH:mm", { locale: ptBR })}`;
    } else {
      return format(date, "d 'de' MMMM, HH:mm", { locale: ptBR });
    }
  };

  // Mark all as read
  const markAllAsRead = () => {
    setNotifications(
      notifications.map((notif) => ({
        ...notif,
        read: true,
      }))
    );
    
    toast({
      title: "Notificações",
      description: "Todas as notificações foram marcadas como lidas.",
    });
  };

  // Mark a single notification as read
  const markAsRead = (id: string) => {
    setNotifications(
      notifications.map((notif) =>
        notif.id === id ? { ...notif, read: true } : notif
      )
    );
  };

  // Filter notifications based on active tab
  const filteredNotifications = notifications.filter((notif) => {
    if (activeTab === "todas") return true;
    if (activeTab === "urgentes") return notif.urgent;
    if (activeTab === "lidas") return notif.read;
    if (activeTab === "nao-lidas") return !notif.read;
    return true;
  });

  // Get icon for notification type
  const getNotificationIcon = (type: string) => {
    switch (type) {
      case "warning":
        return <AlertTriangle className="h-5 w-5 text-amber-500" />;
      case "success":
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case "error":
        return <AlertTriangle className="h-5 w-5 text-red-500" />;
      case "info":
      default:
        return <Bell className="h-5 w-5 text-blue-500" />;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="container mx-auto py-6"
    >
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold">Notificações</h1>
          <p className="text-muted-foreground mt-1">
            Gerencie e visualize todas as suas notificações
          </p>
        </div>
        
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" onClick={markAllAsRead}>
            <CheckCheck className="h-4 w-4 mr-2" />
            Marcar todas como lidas
          </Button>
          
          <Button variant="outline">
            <Filter className="h-4 w-4 mr-2" />
            Filtros
          </Button>
        </div>
      </div>
      
      <Tabs defaultValue="todas" value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="mb-6">
          <TabsTrigger value="todas">
            Todas
            <Badge variant="secondary" className="ml-2">{notifications.length}</Badge>
          </TabsTrigger>
          <TabsTrigger value="urgentes">
            Urgentes
            <Badge variant="secondary" className="ml-2">
              {notifications.filter(notif => notif.urgent).length}
            </Badge>
          </TabsTrigger>
          <TabsTrigger value="nao-lidas">
            Não Lidas
            <Badge variant="secondary" className="ml-2">
              {notifications.filter(notif => !notif.read).length}
            </Badge>
          </TabsTrigger>
          <TabsTrigger value="lidas">
            Lidas
            <Badge variant="secondary" className="ml-2">
              {notifications.filter(notif => notif.read).length}
            </Badge>
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value={activeTab} className="space-y-4">
          {filteredNotifications.length > 0 ? (
            filteredNotifications.map((notification) => (
              <Card 
                key={notification.id} 
                className={`transition-colors hover:bg-accent cursor-pointer ${!notification.read ? 'border-l-4 border-l-primary' : ''}`}
                onClick={() => markAsRead(notification.id)}
              >
                <CardContent className="p-4">
                  <div className="flex items-start gap-4">
                    <div className="p-2 rounded-full bg-muted">
                      {getNotificationIcon(notification.type)}
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2">
                        <h3 className="font-semibold">
                          {notification.title}
                          {notification.urgent && (
                            <Badge variant="destructive" className="ml-2">Urgente</Badge>
                          )}
                        </h3>
                        <div className="flex items-center text-xs text-muted-foreground">
                          <Clock className="h-3 w-3 mr-1" />
                          {formatNotificationDate(notification.date)}
                        </div>
                      </div>
                      <p className="mt-1">{notification.message}</p>
                      
                      <div className="mt-3 flex justify-between items-center">
                        <Button variant="link" className="p-0 h-auto" asChild>
                          <a href={notification.link}>Ver detalhes</a>
                        </Button>
                        
                        {!notification.read && (
                          <Badge variant="outline">Não lida</Badge>
                        )}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          ) : (
            <div className="flex flex-col items-center justify-center py-12 bg-muted rounded-lg">
              <Bell className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-medium">Nenhuma notificação encontrada</h3>
              <p className="text-muted-foreground">
                {activeTab === "todas" 
                  ? "Você não tem notificações no momento."
                  : activeTab === "urgentes"
                  ? "Você não tem notificações urgentes no momento."
                  : activeTab === "lidas"
                  ? "Você não tem notificações lidas."
                  : "Você não tem notificações não lidas."}
              </p>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </motion.div>
  );
};

export default NotificacoesPage;
