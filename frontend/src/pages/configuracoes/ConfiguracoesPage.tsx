import { useState } from 'react';
import { motion } from 'framer-motion';
import { Settings, Bell, Shield, Key, LogIn, Check, Copy, X } from 'lucide-react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { toast } from '@/hooks/use-toast';
import { useTheme } from '@/providers/ThemeProvider';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';

// Tipos de notificação
type NotificationType = 'email' | 'app' | 'sms';
type NotificationEvent = 'novaLicitacao' | 'prazoProximo' | 'mensagemRecebida' | 'sistema';

// Dados de login para o audit log
interface LoginData {
  id: string;
  date: Date;
  ip: string;
  device: string;
  location: string;
  status: 'success' | 'failed';
}

// Interface de sessão ativa
interface ActiveSession {
  id: string;
  device: string;
  ip: string;
  location: string;
  lastActive: Date;
  current: boolean;
}

// Interface para chave de API
interface ApiKey {
  id: string;
  name: string;
  key: string;
  createdAt: Date;
  lastUsed?: Date;
  permissions: string[];
}

// Schema de validação para configurações de notificação
const notificationsSchema = z.object({
  email: z.object({
    novaLicitacao: z.boolean(),
    prazoProximo: z.boolean(),
    mensagemRecebida: z.boolean(),
    sistema: z.boolean(),
  }),
  app: z.object({
    novaLicitacao: z.boolean(),
    prazoProximo: z.boolean(),
    mensagemRecebida: z.boolean(),
    sistema: z.boolean(),
  }),
  sms: z.object({
    novaLicitacao: z.boolean(),
    prazoProximo: z.boolean(),
    mensagemRecebida: z.boolean(),
    sistema: z.boolean(),
  }),
  horarios: z.object({
    inicio: z.string(),
    fim: z.string(),
    diasUteis: z.boolean(),
  }),
});

// Schema para verificação de senha
const passwordSchema = z.object({
  password: z.string().min(6, 'Senha deve ter pelo menos 6 caracteres'),
});

// Schema para criação de chave de API
const apiKeySchema = z.object({
  name: z.string().min(3, 'Nome deve ter pelo menos 3 caracteres'),
  permissions: z.array(z.string()).min(1, 'Selecione pelo menos uma permissão'),
});

/**
 * Componente para configurações de aparência
 */
const ApareciaTab = () => {
  const { theme, setTheme } = useTheme();
  const [density, setDensity] = useState<'compact' | 'normal' | 'comfortable'>('normal');

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Tema</CardTitle>
          <CardDescription>Escolha o tema do sistema</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card 
              className={`cursor-pointer transition ${theme === 'light' ? 'border-primary' : 'border-border'}`}
              onClick={() => setTheme('light')}
            >
              <CardContent className="p-4 text-center">
                <div className="h-24 bg-[#f9f9fb] border rounded-md mb-2"></div>
                <p className="text-sm font-medium">Claro</p>
                {theme === 'light' && <Check className="h-4 w-4 text-primary mx-auto mt-2" />}
              </CardContent>
            </Card>
            
            <Card 
              className={`cursor-pointer transition ${theme === 'dark' ? 'border-primary' : 'border-border'}`}
              onClick={() => setTheme('dark')}
            >
              <CardContent className="p-4 text-center">
                <div className="h-24 bg-[#0e0e10] border rounded-md mb-2"></div>
                <p className="text-sm font-medium">Escuro</p>
                {theme === 'dark' && <Check className="h-4 w-4 text-primary mx-auto mt-2" />}
              </CardContent>
            </Card>
            
            <Card 
              className={`cursor-pointer transition ${theme === 'system' ? 'border-primary' : 'border-border'}`}
              onClick={() => setTheme('system')}
            >
              <CardContent className="p-4 text-center">
                <div className="h-24 bg-gradient-to-r from-[#f9f9fb] to-[#0e0e10] border rounded-md mb-2"></div>
                <p className="text-sm font-medium">Sistema</p>
                {theme === 'system' && <Check className="h-4 w-4 text-primary mx-auto mt-2" />}
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>Densidade</CardTitle>
          <CardDescription>Configurar a densidade da interface</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card 
              className={`cursor-pointer transition ${density === 'compact' ? 'border-primary' : 'border-border'}`}
              onClick={() => setDensity('compact')}
            >
              <CardContent className="p-2 text-center">
                <div className="h-16 border rounded-md mb-1 flex flex-col justify-center">
                  <div className="h-1 mx-4 bg-muted-foreground/20 mb-1"></div>
                  <div className="h-1 mx-4 bg-muted-foreground/20"></div>
                </div>
                <p className="text-xs font-medium">Compacta</p>
                {density === 'compact' && <Check className="h-3 w-3 text-primary mx-auto mt-1" />}
              </CardContent>
            </Card>
            
            <Card 
              className={`cursor-pointer transition ${density === 'normal' ? 'border-primary' : 'border-border'}`}
              onClick={() => setDensity('normal')}
            >
              <CardContent className="p-2 text-center">
                <div className="h-16 border rounded-md mb-1 flex flex-col justify-center">
                  <div className="h-1 mx-4 bg-muted-foreground/20 mb-2"></div>
                  <div className="h-1 mx-4 bg-muted-foreground/20"></div>
                </div>
                <p className="text-xs font-medium">Normal</p>
                {density === 'normal' && <Check className="h-3 w-3 text-primary mx-auto mt-1" />}
              </CardContent>
            </Card>
            
            <Card 
              className={`cursor-pointer transition ${density === 'comfortable' ? 'border-primary' : 'border-border'}`}
              onClick={() => setDensity('comfortable')}
            >
              <CardContent className="p-2 text-center">
                <div className="h-16 border rounded-md mb-1 flex flex-col justify-center">
                  <div className="h-1 mx-4 bg-muted-foreground/20 mb-3"></div>
                  <div className="h-1 mx-4 bg-muted-foreground/20"></div>
                </div>
                <p className="text-xs font-medium">Confortável</p>
                {density === 'comfortable' && <Check className="h-3 w-3 text-primary mx-auto mt-1" />}
              </CardContent>
            </Card>
          </div>
        </CardContent>
        <CardFooter>
          <Button onClick={() => {
            toast({
              title: "Configurações salvas",
              description: "Suas preferências de interface foram salvas.",
            });
          }}>
            Salvar preferências
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

/**
 * Componente para configurações de notificações
 */
const NotificacoesTab = () => {
  const form = useForm<z.infer<typeof notificationsSchema>>({
    resolver: zodResolver(notificationsSchema),
    defaultValues: {
      email: {
        novaLicitacao: true,
        prazoProximo: true,
        mensagemRecebida: true,
        sistema: true,
      },
      app: {
        novaLicitacao: true,
        prazoProximo: true,
        mensagemRecebida: true,
        sistema: true,
      },
      sms: {
        novaLicitacao: false,
        prazoProximo: true,
        mensagemRecebida: false,
        sistema: false,
      },
      horarios: {
        inicio: '08:00',
        fim: '18:00',
        diasUteis: true,
      },
    },
  });
  
  const onSubmit = async (data: z.infer<typeof notificationsSchema>) => {
    try {
      // Mock de API
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Salva os dados no localStorage
      localStorage.setItem('notificationPreferences', JSON.stringify(data));
      
      toast({
        title: "Notificações configuradas",
        description: "Suas preferências de notificação foram salvas.",
      });
    } catch (error) {
      toast({
        title: "Erro ao salvar",
        description: "Ocorreu um erro ao salvar as configurações.",
        variant: "destructive",
      });
    }
  };
  
  // Labels para tipos de notificação
  const notificationLabels: Record<NotificationEvent, string> = {
    novaLicitacao: "Nova licitação",
    prazoProximo: "Prazo próximo",
    mensagemRecebida: "Mensagem recebida",
    sistema: "Notificações do sistema",
  };
  
  // Renderiza uma linha de configuração
  const renderNotificationRow = (
    event: NotificationEvent, 
    eventLabel: string
  ) => {
    return (
      <div className="flex items-center justify-between py-2 border-b">
        <div>
          <p className="font-medium">{eventLabel}</p>
        </div>
        <div className="flex gap-4">
          <FormField
            control={form.control}
            name={`email.${event}`}
            render={({ field }) => (
              <FormItem className="flex items-center space-x-2 space-y-0">
                <FormControl>
                  <Switch
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                </FormControl>
              </FormItem>
            )}
          />
          
          <FormField
            control={form.control}
            name={`app.${event}`}
            render={({ field }) => (
              <FormItem className="flex items-center space-x-2 space-y-0">
                <FormControl>
                  <Switch
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                </FormControl>
              </FormItem>
            )}
          />
          
          <FormField
            control={form.control}
            name={`sms.${event}`}
            render={({ field }) => (
              <FormItem className="flex items-center space-x-2 space-y-0">
                <FormControl>
                  <Switch
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                </FormControl>
              </FormItem>
            )}
          />
        </div>
      </div>
    );
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Configurações de Notificação</CardTitle>
            <CardDescription>
              Defina como você deseja receber notificações
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="mb-4">
              <div className="grid grid-cols-4 mb-2">
                <div className="col-span-1">
                  <p className="font-medium text-sm">Tipo</p>
                </div>
                <div className="col-span-3 grid grid-cols-3 gap-4">
                  <p className="text-center text-sm font-medium">E-mail</p>
                  <p className="text-center text-sm font-medium">App</p>
                  <p className="text-center text-sm font-medium">SMS</p>
                </div>
              </div>
              
              <div className="space-y-1">
                {Object.entries(notificationLabels).map(([event, label]) => (
                  renderNotificationRow(event as NotificationEvent, label)
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Horários de Notificação</CardTitle>
            <CardDescription>
              Defina quando deseja receber notificações
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="horarios.inicio"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Horário inicial</FormLabel>
                      <FormControl>
                        <Input
                          type="time"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="horarios.fim"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Horário final</FormLabel>
                      <FormControl>
                        <Input
                          type="time"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              
              <FormField
                control={form.control}
                name="horarios.diasUteis"
                render={({ field }) => (
                  <FormItem className="flex flex-row items-center space-x-3 space-y-0">
                    <FormControl>
                      <Switch
                        checked={field.value}
                        onCheckedChange={field.onChange}
                      />
                    </FormControl>
                    <div className="space-y-1 leading-none">
                      <FormLabel>Apenas dias úteis</FormLabel>
                      <FormDescription>
                        Não receber notificações em finais de semana
                      </FormDescription>
                    </div>
                  </FormItem>
                )}
              />
            </div>
          </CardContent>
          <CardFooter>
            <Button type="submit">
              Salvar preferências
            </Button>
          </CardFooter>
        </Card>
      </form>
    </Form>
  );
};

/**
 * Log de auditoria para segurança
 */
const SecurityAuditLog = ({ logs }: { logs: LoginData[] }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Histórico de Login</CardTitle>
        <CardDescription>
          Atividades recentes de login na sua conta
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {logs.map((log) => (
            <div key={log.id} className="flex items-center justify-between border-b pb-4 last:border-0">
              <div className="flex items-center space-x-4">
                <div className={`p-2 rounded-full ${log.status === 'success' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
                  <LogIn className="h-5 w-5" />
                </div>
                <div>
                  <p className="font-medium">{log.device}</p>
                  <p className="text-sm text-muted-foreground">
                    {log.location} • {log.ip}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm font-medium">{log.date.toLocaleDateString('pt-BR')}</p>
                <p className="text-sm text-muted-foreground">{log.date.toLocaleTimeString('pt-BR')}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

/**
 * Componente para configurações de segurança
 */
const SegurancaTab = () => {
  const [twoFactorEnabled, setTwoFactorEnabled] = useState(false);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [activeSessions, setActiveSessions] = useState<ActiveSession[]>([
    {
      id: "1",
      device: "Chrome em Windows",
      ip: "187.123.45.67",
      location: "São Paulo, Brasil",
      lastActive: new Date(),
      current: true,
    },
    {
      id: "2",
      device: "Safari em iPhone",
      ip: "187.123.45.68",
      location: "São Paulo, Brasil",
      lastActive: new Date(Date.now() - 86400000), // 1 dia atrás
      current: false,
    },
    {
      id: "3",
      device: "Firefox em MacBook",
      ip: "45.67.89.123",
      location: "Rio de Janeiro, Brasil",
      lastActive: new Date(Date.now() - 172800000), // 2 dias atrás
      current: false,
    },
  ]);
  
  const [auditLogs] = useState<LoginData[]>([
    {
      id: "1",
      date: new Date(),
      ip: "187.123.45.67",
      device: "Chrome em Windows",
      location: "São Paulo, Brasil",
      status: "success",
    },
    {
      id: "2",
      date: new Date(Date.now() - 86400000), // 1 dia atrás
      ip: "187.123.45.68",
      device: "Safari em iPhone",
      location: "São Paulo, Brasil",
      status: "success",
    },
    {
      id: "3",
      date: new Date(Date.now() - 172800000), // 2 dias atrás
      ip: "45.67.89.123",
      device: "Firefox em MacBook",
      location: "Rio de Janeiro, Brasil",
      status: "success",
    },
    {
      id: "4",
      date: new Date(Date.now() - 259200000), // 3 dias atrás
      ip: "98.76.54.32",
      device: "Desconhecido",
      location: "Curitiba, Brasil",
      status: "failed",
    },
  ]);
  
  const passwordForm = useForm<z.infer<typeof passwordSchema>>({
    resolver: zodResolver(passwordSchema),
    defaultValues: {
      password: "",
    },
  });
  
  const handleToggleTwoFactor = () => {
    setConfirmDialogOpen(true);
  };
  
  const confirmTwoFactor = () => {
    setTwoFactorEnabled(!twoFactorEnabled);
    setConfirmDialogOpen(false);
    
    toast({
      title: twoFactorEnabled ? "2FA desativado" : "2FA ativado",
      description: twoFactorEnabled 
        ? "A autenticação de dois fatores foi desativada." 
        : "A autenticação de dois fatores foi ativada para sua conta.",
    });
  };
  
  const terminateSession = (sessionId: string) => {
    setActiveSessions(activeSessions.filter(session => session.id !== sessionId));
    
    toast({
      title: "Sessão encerrada",
      description: "A sessão selecionada foi encerrada com sucesso.",
    });
  };
  
  const terminateAllSessions = () => {
    // Manter apenas a sessão atual
    setActiveSessions(activeSessions.filter(session => session.current));
    
    toast({
      title: "Sessões encerradas",
      description: "Todas as outras sessões foram encerradas com sucesso.",
    });
  };
  
  const changePassword = (data: z.infer<typeof passwordSchema>) => {
    // Mock de API
    toast({
      title: "Senha alterada",
      description: "Sua senha foi alterada com sucesso.",
    });
    
    passwordForm.reset();
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Autenticação de Dois Fatores</CardTitle>
          <CardDescription>
            Aumente a segurança da sua conta com 2FA
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <p className="font-medium">Autenticação de dois fatores</p>
              <p className="text-sm text-muted-foreground">
                {twoFactorEnabled 
                  ? "2FA está ativado. Um código será enviado para seu email ao fazer login." 
                  : "Ative para adicionar uma camada extra de segurança."}
              </p>
            </div>
            <Switch 
              checked={twoFactorEnabled} 
              onCheckedChange={handleToggleTwoFactor}
            />
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>Sessões Ativas</CardTitle>
          <CardDescription>
            Dispositivos conectados à sua conta
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {activeSessions.map((session) => (
            <div key={session.id} className="flex items-center justify-between border-b pb-4 last:border-0">
              <div>
                <p className="font-medium">
                  {session.device} {session.current && "(Dispositivo atual)"}
                </p>
                <p className="text-sm text-muted-foreground">
                  {session.location} • {session.ip}
                </p>
                <p className="text-xs text-muted-foreground">
                  Último acesso: {session.lastActive.toLocaleDateString('pt-BR')} às {session.lastActive.toLocaleTimeString('pt-BR')}
                </p>
              </div>
              {!session.current && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => terminateSession(session.id)}
                >
                  <X className="h-4 w-4 mr-2" />
                  Encerrar
                </Button>
              )}
            </div>
          ))}
        </CardContent>
        <CardFooter>
          {activeSessions.length > 1 && (
            <Button onClick={terminateAllSessions}>
              Encerrar todas as outras sessões
            </Button>
          )}
        </CardFooter>
      </Card>
      
      <SecurityAuditLog logs={auditLogs} />
      
      <Card>
        <CardHeader>
          <CardTitle>Alterar Senha</CardTitle>
          <CardDescription>
            Atualize sua senha de acesso
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...passwordForm}>
            <form onSubmit={passwordForm.handleSubmit(changePassword)} className="space-y-4">
              <FormField
                control={passwordForm.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Nova senha</FormLabel>
                    <FormControl>
                      <Input
                        type="password"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              
              <Button type="submit">
                Alterar senha
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>
      
      <Dialog open={confirmDialogOpen} onOpenChange={setConfirmDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {twoFactorEnabled ? "Desativar 2FA?" : "Ativar 2FA?"}
            </DialogTitle>
            <DialogDescription>
              {twoFactorEnabled
                ? "Ao desativar a autenticação de dois fatores, sua conta ficará menos protegida."
                : "A autenticação de dois fatores aumenta a segurança da sua conta."}
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setConfirmDialogOpen(false)}>
              Cancelar
            </Button>
            <Button onClick={confirmTwoFactor}>
              Confirmar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

/**
 * Componente para configurações de API
 */
const ApiTab = () => {
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([
    {
      id: "1",
      name: "API Portal",
      key: "74cb0e8d-2622-4c8c-a19c-8f08ca8a3214",
      createdAt: new Date(Date.now() - 1000000000),
      lastUsed: new Date(Date.now() - 100000),
      permissions: ["Leitura", "Escrita"],
    },
  ]);
  
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedKey, setSelectedKey] = useState<ApiKey | null>(null);
  
  const apiKeyForm = useForm<z.infer<typeof apiKeySchema>>({
    resolver: zodResolver(apiKeySchema),
    defaultValues: {
      name: "",
      permissions: [],
    },
  });
  
  const passwordForm = useForm<z.infer<typeof passwordSchema>>({
    resolver: zodResolver(passwordSchema),
    defaultValues: {
      password: "",
    },
  });
  
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Chave copiada",
      description: "A chave API foi copiada para a área de transferência.",
    });
  };
  
  const generateApiKey = () => {
    // Função para gerar um UUID v4
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  };
  
  const createApiKey = (data: z.infer<typeof apiKeySchema>) => {
    const newKey: ApiKey = {
      id: Math.random().toString(36).slice(2, 9),
      name: data.name,
      key: generateApiKey(),
      createdAt: new Date(),
      permissions: data.permissions,
    };
    
    setApiKeys([...apiKeys, newKey]);
    setSelectedKey(newKey);
    setShowCreateModal(false);
    apiKeyForm.reset();
  };
  
  const deleteApiKey = (id: string) => {
    setApiKeys(apiKeys.filter(key => key.id !== id));
    
    toast({
      title: "Chave API excluída",
      description: "A chave API foi excluída com sucesso.",
    });
  };
  
  const permissionOptions = [
    { value: "Leitura", label: "Leitura" },
    { value: "Escrita", label: "Escrita" },
    { value: "Exclusão", label: "Exclusão" },
    { value: "Administração", label: "Administração" },
  ];

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <div>
            <CardTitle>Chaves de API</CardTitle>
            <CardDescription className="mt-1">
              Gerencie chaves para integração com sistemas externos
            </CardDescription>
          </div>
          <Button onClick={() => setShowCreateModal(true)}>
            Gerar Nova Chave
          </Button>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {apiKeys.length === 0 ? (
              <div className="text-center py-6">
                <p className="text-muted-foreground">Nenhuma chave API criada</p>
              </div>
            ) : (
              apiKeys.map((apiKey) => (
                <div key={apiKey.id} className="flex items-center justify-between border-b pb-4 last:border-0">
                  <div>
                    <p className="font-medium">{apiKey.name}</p>
                    <div className="flex items-center mt-1">
                      <p className="text-sm font-mono bg-muted p-1 rounded">
                        {apiKey.key.substring(0, 8)}...{apiKey.key.substring(apiKey.key.length - 8)}
                      </p>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <Button
                            variant="ghost"
                            size="icon"
                            className="h-8 w-8 ml-2"
                            onClick={() => copyToClipboard(apiKey.key)}
                          >
                            <Copy className="h-4 w-4" />
                          </Button>
                        </TooltipTrigger>
                        <TooltipContent>Copiar chave</TooltipContent>
                      </Tooltip>
                    </div>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {apiKey.permissions.map((permission) => (
                        <span key={permission} className="text-xs bg-primary/10 text-primary px-2 py-1 rounded-full">
                          {permission}
                        </span>
                      ))}
                    </div>
                    <p className="text-xs text-muted-foreground mt-2">
                      Criado em {apiKey.createdAt.toLocaleDateString('pt-BR')}
                      {apiKey.lastUsed && ` • Último uso: ${apiKey.lastUsed.toLocaleDateString('pt-BR')}`}
                    </p>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => deleteApiKey(apiKey.id)}
                  >
                    <X className="h-4 w-4 mr-2" />
                    Excluir
                  </Button>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>
      
      {/* Modal para criar nova chave */}
      <Dialog open={showCreateModal} onOpenChange={setShowCreateModal}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Nova Chave API</DialogTitle>
            <DialogDescription>
              Crie uma nova chave para integração com sistemas externos
            </DialogDescription>
          </DialogHeader>
          <Form {...apiKeyForm}>
            <form onSubmit={apiKeyForm.handleSubmit(createApiKey)} className="space-y-4">
              <FormField
                control={apiKeyForm.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Nome da chave</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Portal Integração"
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Um nome para identificar o uso desta chave
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
              
              <FormField
                control={apiKeyForm.control}
                name="permissions"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Permissões</FormLabel>
                    <FormControl>
                      <Select 
                        onValueChange={(value) => {
                          const currentValues = field.value || [];
                          const newValues = currentValues.includes(value)
                            ? currentValues.filter(v => v !== value)
                            : [...currentValues, value];
                          field.onChange(newValues);
                        }}
                      >
                        <SelectTrigger className="w-full">
                          <SelectValue placeholder="Selecione as permissões" />
                        </SelectTrigger>
                        <SelectContent>
                          {permissionOptions.map((option) => (
                            <SelectItem key={option.value} value={option.value}>
                              {option.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </FormControl>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {field.value?.map((permission) => (
                        <div 
                          key={permission} 
                          className="flex items-center bg-primary/10 text-primary px-2 py-1 rounded-full text-xs"
                        >
                          <span>{permission}</span>
                          <Button 
                            variant="ghost" 
                            size="icon" 
                            className="h-4 w-4 ml-1"
                            onClick={() => {
                              field.onChange(field.value.filter(v => v !== permission));
                            }}
                          >
                            <X className="h-3 w-3" />
                          </Button>
                        </div>
                      ))}
                    </div>
                    <FormDescription>
                      Selecione as permissões para esta chave
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
              
              <DialogFooter>
                <Button type="submit">
                  Gerar chave
                </Button>
              </DialogFooter>
            </form>
          </Form>
        </DialogContent>
      </Dialog>
      
      {/* Modal para exibir nova chave */}
      <Dialog open={!!selectedKey} onOpenChange={() => setSelectedKey(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Chave API criada</DialogTitle>
            <DialogDescription>
              Esta é a única vez que você verá a chave completa. Copie-a agora.
            </DialogDescription>
          </DialogHeader>
          {selectedKey && (
            <>
              <div className="bg-muted p-4 rounded-md font-mono text-sm break-all">
                {selectedKey.key}
              </div>
              <DialogFooter>
                <Button onClick={() => copyToClipboard(selectedKey.key)}>
                  <Copy className="mr-2 h-4 w-4" />
                  Copiar chave
                </Button>
              </DialogFooter>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

/**
 * Página principal de configurações do sistema
 */
const ConfiguracoesPage = () => {
  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold">Configurações</h1>
        <p className="text-muted-foreground mt-2">
          Gerencie as configurações do sistema
        </p>
      </motion.div>
      
      <Tabs defaultValue="aparencia" className="space-y-6">
        <TabsList className="grid w-full md:w-auto grid-cols-4">
          <TabsTrigger value="aparencia" className="flex items-center">
            <Settings className="h-4 w-4 mr-2" />
            <span className="hidden sm:inline">Aparência</span>
          </TabsTrigger>
          <TabsTrigger value="notificacoes" className="flex items-center">
            <Bell className="h-4 w-4 mr-2" />
            <span className="hidden sm:inline">Notificações</span>
          </TabsTrigger>
          <TabsTrigger value="seguranca" className="flex items-center">
            <Shield className="h-4 w-4 mr-2" />
            <span className="hidden sm:inline">Segurança</span>
          </TabsTrigger>
          <TabsTrigger value="api" className="flex items-center">
            <Key className="h-4 w-4 mr-2" />
            <span className="hidden sm:inline">API</span>
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="aparencia">
          <ApareciaTab />
        </TabsContent>
        
        <TabsContent value="notificacoes">
          <NotificacoesTab />
        </TabsContent>
        
        <TabsContent value="seguranca">
          <SegurancaTab />
        </TabsContent>
        
        <TabsContent value="api">
          <ApiTab />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ConfiguracoesPage;
