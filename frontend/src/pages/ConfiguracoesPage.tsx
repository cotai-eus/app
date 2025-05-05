
import React, { useState } from "react";
import { motion } from "framer-motion";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";
import { useToast } from "@/hooks/use-toast";
import {
  Moon,
  Sun,
  Bell,
  Shield,
  Key,
  Smartphone,
  Mail,
  PanelLeft,
  Eye,
  EyeOff,
  Trash,
  Plus,
  Info,
  Check,
  X
} from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose,
} from "@/components/ui/dialog";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { useTheme } from "next-themes";

const ConfiguracoesPage = () => {
  // Estado para gerenciar as preferências do usuário
  const [notificacoesEmail, setNotificacoesEmail] = useState(true);
  const [notificacoesPush, setNotificacoesPush] = useState(true);
  const [mostrarSessoes, setMostrarSessoes] = useState(false);
  const [novaChaveDialogOpen, setNovaChaveDialogOpen] = useState(false);
  const [nomeChave, setNomeChave] = useState("");
  const [chaveGerada, setChaveGerada] = useState("");
  const [confirmarSenha, setConfirmarSenha] = useState("");
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const { theme, setTheme } = useTheme();
  const { toast } = useToast();

  // Dados simulados para sessões ativas
  const sessoesAtivas = [
    {
      dispositivo: "Windows 10 - Chrome",
      localizacao: "São Paulo, Brasil",
      ultimoAcesso: new Date(2025, 4, 1, 14, 30),
      atual: true
    },
    {
      dispositivo: "iPhone 15 - Safari",
      localizacao: "Rio de Janeiro, Brasil",
      ultimoAcesso: new Date(2025, 4, 1, 10, 15),
      atual: false
    },
    {
      dispositivo: "MacBook Pro - Firefox",
      localizacao: "Belo Horizonte, Brasil",
      ultimoAcesso: new Date(2025, 3, 30, 8, 45),
      atual: false
    }
  ];

  // Dados simulados para chaves API
  const [chavesAPI, setChavesAPI] = useState([
    {
      id: "1",
      nome: "Integração ERP",
      criada: new Date(2025, 2, 15),
      ultimoUso: new Date(2025, 4, 1)
    },
    {
      id: "2",
      nome: "Dashboard Externo",
      criada: new Date(2025, 3, 10),
      ultimoUso: new Date(2025, 3, 28)
    }
  ]);

  // Função para encerrar uma sessão
  const encerrarSessao = (index: number) => {
    // Em um app real, faria uma chamada à API para invalidar o token
    toast({
      title: "Sessão encerrada",
      description: `A sessão em ${sessoesAtivas[index].dispositivo} foi encerrada com sucesso.`,
    });
  };

  // Função para excluir uma chave API
  const excluirChave = (id: string) => {
    setChavesAPI(chavesAPI.filter(chave => chave.id !== id));
    toast({
      title: "Chave API excluída",
      description: "A chave API foi excluída com sucesso.",
    });
  };

  // Função para gerar uma nova chave API
  const gerarNovaChave = () => {
    if (!nomeChave) {
      toast({
        title: "Erro",
        description: "Por favor, insira um nome para a chave.",
        variant: "destructive",
      });
      return;
    }

    if (!confirmarSenha) {
      toast({
        title: "Erro",
        description: "Por favor, confirme sua senha para continuar.",
        variant: "destructive",
      });
      return;
    }

    // Em um app real, verificaria a senha e faria uma chamada à API
    // Simula geração de chave
    const chaveAleatoria = Array.from({ length: 32 }, () => 
      Math.floor(Math.random() * 16).toString(16)
    ).join('');
    
    setChaveGerada(chaveAleatoria);
    
    // Adicionar à lista após confirmação
    setTimeout(() => {
      const novaChave = {
        id: Date.now().toString(),
        nome: nomeChave,
        criada: new Date(),
        ultimoUso: new Date()
      };
      setChavesAPI([...chavesAPI, novaChave]);
      setNomeChave("");
      setConfirmarSenha("");
      setNovaChaveDialogOpen(false);
      setChaveGerada("");
      
      toast({
        title: "Chave API criada",
        description: "Nova chave API criada com sucesso.",
      });
    }, 1000);
  };

  // Função para copiar a chave para a área de transferência
  const copiarChave = () => {
    navigator.clipboard.writeText(chaveGerada);
    toast({
      title: "Chave copiada",
      description: "A chave API foi copiada para a área de transferência.",
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="container mx-auto py-6"
    >
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Configurações</h1>
        <p className="text-muted-foreground mt-1">
          Personalize sua experiência no sistema
        </p>
      </div>

      <Tabs defaultValue="aparencia" className="w-full">
        <TabsList className="mb-6 w-full max-w-md flex flex-wrap">
          <TabsTrigger value="aparencia" className="flex items-center">
            <Sun className="h-4 w-4 mr-2" />
            Aparência
          </TabsTrigger>
          <TabsTrigger value="notificacoes" className="flex items-center">
            <Bell className="h-4 w-4 mr-2" />
            Notificações
          </TabsTrigger>
          <TabsTrigger value="seguranca" className="flex items-center">
            <Shield className="h-4 w-4 mr-2" />
            Segurança
          </TabsTrigger>
          <TabsTrigger value="api" className="flex items-center">
            <Key className="h-4 w-4 mr-2" />
            API
          </TabsTrigger>
        </TabsList>

        {/* Aba de Aparência */}
        <TabsContent value="aparencia">
          <Card>
            <CardHeader>
              <CardTitle>Aparência</CardTitle>
              <CardDescription>
                Personalize a interface visual do sistema
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="theme">Tema</Label>
                <div className="flex flex-wrap gap-4">
                  <Button
                    variant={theme === "light" ? "default" : "outline"}
                    onClick={() => setTheme("light")}
                    className="flex items-center"
                  >
                    <Sun className="h-4 w-4 mr-2" />
                    Claro
                  </Button>
                  <Button
                    variant={theme === "dark" ? "default" : "outline"}
                    onClick={() => setTheme("dark")}
                    className="flex items-center"
                  >
                    <Moon className="h-4 w-4 mr-2" />
                    Escuro
                  </Button>
                  <Button
                    variant={theme === "system" ? "default" : "outline"}
                    onClick={() => setTheme("system")}
                    className="flex items-center"
                  >
                    <PanelLeft className="h-4 w-4 mr-2" />
                    Sistema
                  </Button>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="densidade">Densidade da interface</Label>
                <Select defaultValue="normal">
                  <SelectTrigger className="w-full max-w-xs">
                    <SelectValue placeholder="Selecionar densidade" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectGroup>
                      <SelectItem value="compacta">Compacta</SelectItem>
                      <SelectItem value="normal">Normal</SelectItem>
                      <SelectItem value="confortavel">Confortável</SelectItem>
                    </SelectGroup>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Aba de Notificações */}
        <TabsContent value="notificacoes">
          <Card>
            <CardHeader>
              <CardTitle>Notificações</CardTitle>
              <CardDescription>
                Configure como deseja receber informações do sistema
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Notificações por e-mail</Label>
                    <p className="text-sm text-muted-foreground">
                      Receba atualizações sobre licitações por email
                    </p>
                  </div>
                  <Switch
                    checked={notificacoesEmail}
                    onCheckedChange={setNotificacoesEmail}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Notificações push</Label>
                    <p className="text-sm text-muted-foreground">
                      Receba atualizações em tempo real no navegador
                    </p>
                  </div>
                  <Switch
                    checked={notificacoesPush}
                    onCheckedChange={setNotificacoesPush}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label>Frequência de resumo</Label>
                <Select defaultValue="diario">
                  <SelectTrigger className="w-full max-w-xs">
                    <SelectValue placeholder="Selecionar frequência" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectGroup>
                      <SelectItem value="tempo-real">Tempo real</SelectItem>
                      <SelectItem value="diario">Diário</SelectItem>
                      <SelectItem value="semanal">Semanal</SelectItem>
                    </SelectGroup>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Canais de notificação</Label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="flex items-center space-x-2">
                    <Smartphone className="h-4 w-4" />
                    <span>Aplicativo móvel</span>
                    <Switch defaultChecked />
                  </div>
                  <div className="flex items-center space-x-2">
                    <Mail className="h-4 w-4" />
                    <span>Email</span>
                    <Switch defaultChecked />
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter>
              <Button>Salvar preferências</Button>
            </CardFooter>
          </Card>
        </TabsContent>

        {/* Aba de Segurança */}
        <TabsContent value="seguranca">
          <Card>
            <CardHeader>
              <CardTitle>Segurança da conta</CardTitle>
              <CardDescription>
                Gerencie a segurança e o acesso à sua conta
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-medium">Autenticação de dois fatores</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Adicione uma camada extra de segurança à sua conta
                  </p>
                  <Button variant="outline">Configurar 2FA</Button>
                </div>

                <div>
                  <h3 className="text-lg font-medium">Alterar senha</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Atualize sua senha periodicamente para aumentar a segurança
                  </p>
                  <div className="grid gap-4 max-w-md">
                    <div className="space-y-2">
                      <Label htmlFor="senha-atual">Senha atual</Label>
                      <div className="relative">
                        <Input
                          id="senha-atual"
                          type={mostrarSenha ? "text" : "password"}
                          placeholder="Digite sua senha atual"
                        />
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          className="absolute right-0 top-0 h-full"
                          onClick={() => setMostrarSenha(!mostrarSenha)}
                        >
                          {mostrarSenha ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </Button>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="nova-senha">Nova senha</Label>
                      <Input
                        id="nova-senha"
                        type="password"
                        placeholder="Digite sua nova senha"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="confirmar-senha">Confirmar nova senha</Label>
                      <Input
                        id="confirmar-senha"
                        type="password"
                        placeholder="Confirme sua nova senha"
                      />
                    </div>
                    <Button>Atualizar senha</Button>
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-medium">Sessões ativas</h3>
                    <Button
                      variant="ghost"
                      onClick={() => setMostrarSessoes(!mostrarSessoes)}
                      className="text-sm"
                    >
                      {mostrarSessoes ? "Esconder" : "Mostrar"}
                    </Button>
                  </div>
                  
                  {mostrarSessoes && (
                    <div className="overflow-x-auto">
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>Dispositivo</TableHead>
                            <TableHead>Localização</TableHead>
                            <TableHead>Último acesso</TableHead>
                            <TableHead>Ação</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {sessoesAtivas.map((sessao, index) => (
                            <TableRow key={index}>
                              <TableCell className="font-medium">
                                {sessao.dispositivo}
                                {sessao.atual && (
                                  <span className="ml-2 text-xs bg-green-500/20 text-green-600 dark:text-green-400 px-2 py-0.5 rounded-full">
                                    Atual
                                  </span>
                                )}
                              </TableCell>
                              <TableCell>{sessao.localizacao}</TableCell>
                              <TableCell>
                                {format(sessao.ultimoAcesso, "dd/MM/yyyy HH:mm", { locale: ptBR })}
                              </TableCell>
                              <TableCell>
                                {!sessao.atual && (
                                  <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={() => encerrarSessao(index)}
                                    className="text-destructive"
                                  >
                                    Encerrar
                                  </Button>
                                )}
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Aba de API */}
        <TabsContent value="api">
          <Card>
            <CardHeader>
              <CardTitle>Chaves de API</CardTitle>
              <CardDescription>
                Crie e gerencie chaves de acesso para integrações externas
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <p className="text-sm text-muted-foreground">
                  Chaves de API permitem que outros sistemas acessem seus dados de forma segura
                </p>
                <Dialog open={novaChaveDialogOpen} onOpenChange={setNovaChaveDialogOpen}>
                  <DialogTrigger asChild>
                    <Button className="flex items-center">
                      <Plus className="h-4 w-4 mr-2" />
                      Nova chave API
                    </Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Criar nova chave API</DialogTitle>
                      <DialogDescription>
                        Uma vez criada, você verá a chave apenas uma vez. Guarde-a em um local seguro.
                      </DialogDescription>
                    </DialogHeader>
                    
                    {chaveGerada ? (
                      <div className="space-y-4">
                        <div className="p-4 bg-muted rounded-md">
                          <p className="text-sm mb-2 font-medium">Sua nova chave API:</p>
                          <code className="break-all text-xs bg-background p-2 rounded border block">
                            {chaveGerada}
                          </code>
                        </div>
                        <div className="flex items-center p-2 bg-amber-100 dark:bg-amber-900/30 text-amber-800 dark:text-amber-300 rounded-md">
                          <Info className="h-4 w-4 mr-2 flex-shrink-0" />
                          <p className="text-xs">
                            Esta chave só será exibida uma vez. Copie-a agora para um local seguro.
                          </p>
                        </div>
                        <Button onClick={copiarChave} className="w-full">
                          Copiar chave para área de transferência
                        </Button>
                      </div>
                    ) : (
                      <div className="space-y-4 py-4">
                        <div className="space-y-2">
                          <Label htmlFor="nome-chave">Nome da chave</Label>
                          <Input
                            id="nome-chave"
                            placeholder="Ex: Integração ERP"
                            value={nomeChave}
                            onChange={(e) => setNomeChave(e.target.value)}
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="confirmar-senha-api">Confirme sua senha</Label>
                          <div className="relative">
                            <Input
                              id="confirmar-senha-api"
                              type={mostrarSenha ? "text" : "password"}
                              placeholder="Digite sua senha para confirmar"
                              value={confirmarSenha}
                              onChange={(e) => setConfirmarSenha(e.target.value)}
                            />
                            <Button
                              type="button"
                              variant="ghost"
                              size="icon"
                              className="absolute right-0 top-0 h-full"
                              onClick={() => setMostrarSenha(!mostrarSenha)}
                            >
                              {mostrarSenha ? (
                                <EyeOff className="h-4 w-4" />
                              ) : (
                                <Eye className="h-4 w-4" />
                              )}
                            </Button>
                          </div>
                        </div>
                      </div>
                    )}
                    
                    <DialogFooter>
                      {chaveGerada ? (
                        <DialogClose asChild>
                          <Button variant="default">Fechar</Button>
                        </DialogClose>
                      ) : (
                        <>
                          <Button variant="outline" onClick={() => setNovaChaveDialogOpen(false)}>
                            Cancelar
                          </Button>
                          <Button onClick={gerarNovaChave}>
                            Gerar chave
                          </Button>
                        </>
                      )}
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              </div>

              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Nome</TableHead>
                      <TableHead>Criada em</TableHead>
                      <TableHead>Último uso</TableHead>
                      <TableHead>Ações</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {chavesAPI.map((chave) => (
                      <TableRow key={chave.id}>
                        <TableCell className="font-medium">{chave.nome}</TableCell>
                        <TableCell>
                          {format(chave.criada, "dd/MM/yyyy", { locale: ptBR })}
                        </TableCell>
                        <TableCell>
                          {format(chave.ultimoUso, "dd/MM/yyyy", { locale: ptBR })}
                        </TableCell>
                        <TableCell>
                          <Dialog>
                            <DialogTrigger asChild>
                              <Button variant="ghost" size="sm" className="text-destructive">
                                <Trash className="h-4 w-4 mr-1" />
                                Excluir
                              </Button>
                            </DialogTrigger>
                            <DialogContent>
                              <DialogHeader>
                                <DialogTitle>Confirmar exclusão</DialogTitle>
                                <DialogDescription>
                                  Tem certeza que deseja excluir a chave "{chave.nome}"? Esta ação não pode ser desfeita.
                                </DialogDescription>
                              </DialogHeader>
                              <DialogFooter>
                                <DialogClose asChild>
                                  <Button variant="outline">Cancelar</Button>
                                </DialogClose>
                                <Button
                                  variant="destructive"
                                  onClick={() => excluirChave(chave.id)}
                                >
                                  Excluir
                                </Button>
                              </DialogFooter>
                            </DialogContent>
                          </Dialog>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </motion.div>
  );
};

export default ConfiguracoesPage;
