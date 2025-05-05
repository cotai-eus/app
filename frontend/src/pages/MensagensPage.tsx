import React, { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Send,
  Paperclip,
  Calendar,
  FileText,
  Search,
  MoreVertical,
  User,
  AtSign,
  X,
  Plus,
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useParams } from "react-router-dom";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
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
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

// Mock contacts data
const contacts = [
  { 
    id: "1", 
    name: "João Silva", 
    avatar: null, 
    lastMessage: "Precisamos revisar a proposta",
    lastTime: new Date(2025, 3, 1, 14, 35),
    unread: 2,
    online: true,
  },
  { 
    id: "2", 
    name: "Maria Souza", 
    avatar: null, 
    lastMessage: "Documento enviado",
    lastTime: new Date(2025, 3, 1, 9, 20),
    unread: 0,
    online: true,
  },
  { 
    id: "3", 
    name: "Carlos Mendes", 
    avatar: null, 
    lastMessage: "Verificou o prazo da licitação?",
    lastTime: new Date(2025, 2, 29, 17, 10),
    unread: 0,
    online: false,
  },
  { 
    id: "4", 
    name: "Ana Ferreira", 
    avatar: null, 
    lastMessage: "Reunião agendada para amanhã",
    lastTime: new Date(2025, 2, 29, 10, 5),
    unread: 0,
    online: false,
  },
  { 
    id: "5", 
    name: "Roberto Alves", 
    avatar: null, 
    lastMessage: "Nova licitação disponível",
    lastTime: new Date(2025, 2, 28, 14, 22),
    unread: 0,
    online: true,
  },
];

// Mock messages data
const messagesData: Record<string, Array<{id: string; content: string; sender: string; time: Date; attachments?: {type: string; name: string}[]}>> = {
  "1": [
    {
      id: "msg1-1",
      content: "Olá João, tudo bem?",
      sender: "user",
      time: new Date(2025, 3, 1, 14, 30),
    },
    {
      id: "msg1-2",
      content: "Tudo ótimo! Precisamos revisar a proposta para a licitação #2025/045",
      sender: "contact",
      time: new Date(2025, 3, 1, 14, 35),
    },
    {
      id: "msg1-3",
      content: "Claro, estou disponível para discutir agora. Quais são os principais pontos a revisar?",
      sender: "user",
      time: new Date(2025, 3, 1, 14, 38),
    },
  ],
  "2": [
    {
      id: "msg2-1",
      content: "Maria, encaminhei o documento para você analisar.",
      sender: "user",
      time: new Date(2025, 3, 1, 9, 15),
      attachments: [
        { type: "file", name: "Proposta_Tecnica_v2.pdf" }
      ],
    },
    {
      id: "msg2-2",
      content: "Documento enviado. Vou analisar ainda hoje.",
      sender: "contact",
      time: new Date(2025, 3, 1, 9, 20),
    },
  ],
  "3": [
    {
      id: "msg3-1",
      content: "Verificou o prazo da licitação?",
      sender: "contact",
      time: new Date(2025, 2, 29, 17, 10),
    },
  ],
  "4": [
    {
      id: "msg4-1",
      content: "Ana, vamos agendar uma reunião para discutir o projeto?",
      sender: "user",
      time: new Date(2025, 2, 29, 10, 0),
    },
    {
      id: "msg4-2",
      content: "Reunião agendada para amanhã às 14h. Confirma?",
      sender: "contact",
      time: new Date(2025, 2, 29, 10, 5),
    },
  ],
  "5": [
    {
      id: "msg5-1",
      content: "Roberto, encontrei uma oportunidade interessante para nós.",
      sender: "user",
      time: new Date(2025, 2, 28, 14, 20),
    },
    {
      id: "msg5-2",
      content: "Nova licitação disponível da Prefeitura de Curitiba. Vamos participar?",
      sender: "contact",
      time: new Date(2025, 2, 28, 14, 22),
    },
  ],
};

// Mock kanban items for linking
const kanbanItems = [
  { id: "bid-1", title: "Aquisição de Equipamentos de TI", number: "2025/001" },
  { id: "bid-2", title: "Serviços de Limpeza e Conservação", number: "2025/045" },
  { id: "bid-3", title: "Fornecimento de Material de Escritório", number: "2025/078" },
];

// Mock users for mentions
const teamMembers = [
  { id: "user1", name: "Ana Silva", role: "Gerente de Licitações" },
  { id: "user2", name: "Pedro Costa", role: "Analista Jurídico" },
  { id: "user3", name: "Carla Mendes", role: "Analista Financeiro" },
  { id: "user4", name: "Eduardo Santos", role: "Diretor Comercial" },
];

const MensagensPage = () => {
  const { id: paramId } = useParams();
  const [selectedContactId, setSelectedContactId] = useState<string | undefined>(paramId);
  const [newMessage, setNewMessage] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [isCalendarDialogOpen, setIsCalendarDialogOpen] = useState(false);
  const [isAttachmentMenuOpen, setIsAttachmentMenuOpen] = useState(false);
  const [isMentionsMenuOpen, setIsMentionsMenuOpen] = useState(false);
  const { toast } = useToast();

  // Filter contacts based on search term
  const filteredContacts = contacts.filter(
    (contact) =>
      contact.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Get current selected contact
  const selectedContact = contacts.find((c) => c.id === selectedContactId);
  
  // Get messages for selected contact
  const messages = selectedContactId ? messagesData[selectedContactId] || [] : [];

  const handleSendMessage = () => {
    if (newMessage.trim() === "" || !selectedContactId) return;
    
    // In a real app, this would send the message to the server
    const now = new Date();
    const newMsg = {
      id: `new-${Date.now()}`,
      content: newMessage,
      sender: "user",
      time: now,
    };
    
    // Update local state
    messagesData[selectedContactId] = [...(messagesData[selectedContactId] || []), newMsg];
    
    // Reset input
    setNewMessage("");
    
    toast({
      title: "Mensagem enviada",
      description: "Sua mensagem foi enviada com sucesso.",
    });
  };

  const handleCreateEvent = () => {
    // In a real app, this would create a calendar event
    setIsCalendarDialogOpen(false);
    
    toast({
      title: "Evento criado",
      description: "Evento adicionado ao calendário com sucesso.",
    });
  };
  
  const handleAddMention = (userId: string, userName: string) => {
    setNewMessage((prev) => `${prev} @${userName} `);
    setIsMentionsMenuOpen(false);
    
    toast({
      title: "Usuário mencionado",
      description: `${userName} será notificado quando você enviar a mensagem.`,
    });
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };
  
  // Helper function to get initials from name
  const getInitials = (name: string) => {
    const names = name.split(' ');
    if (names.length >= 2) {
      return `${names[0].charAt(0)}${names[names.length - 1].charAt(0)}`.toUpperCase();
    }
    return names[0].charAt(0).toUpperCase();
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="container mx-auto py-6 h-full"
    >
      <div className="bg-card border border-border rounded-lg flex flex-col md:flex-row h-[calc(100vh-160px)] overflow-hidden">
        {/* Contacts Sidebar */}
        <div className="w-full md:w-80 border-b md:border-b-0 md:border-r border-border flex flex-col">
          <div className="p-4 border-b border-border">
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Pesquisar contatos..."
                className="pl-8"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto">
            {filteredContacts.map((contact) => (
              <div 
                key={contact.id}
                className={`flex items-center p-3 gap-3 cursor-pointer hover:bg-accent transition-colors relative ${selectedContactId === contact.id ? 'bg-accent' : ''}`}
                onClick={() => setSelectedContactId(contact.id)}
              >
                <Avatar className="h-10 w-10">
                  <AvatarImage src={contact.avatar || ""} alt={contact.name} />
                  <AvatarFallback>{getInitials(contact.name)}</AvatarFallback>
                </Avatar>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="font-medium truncate">{contact.name}</span>
                    <span className="text-xs text-muted-foreground">
                      {format(contact.lastTime, "HH:mm", { locale: ptBR })}
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground truncate">
                    {contact.lastMessage}
                  </p>
                </div>
                
                {contact.unread > 0 && (
                  <span className="absolute top-3 right-3 flex items-center justify-center h-5 w-5 rounded-full bg-primary text-primary-foreground text-xs">
                    {contact.unread}
                  </span>
                )}
                
                <div className={`absolute bottom-0 left-12 h-2 w-2 rounded-full ${contact.online ? 'bg-green-500' : 'bg-muted'}`} />
              </div>
            ))}
            {filteredContacts.length === 0 && (
              <div className="flex flex-col items-center justify-center h-32 text-muted-foreground">
                <User className="h-6 w-6 mb-2" />
                <p className="text-sm">Nenhum contato encontrado</p>
              </div>
            )}
          </div>
        </div>
        
        {/* Chat Area */}
        <div className="flex-1 flex flex-col overflow-hidden h-full">
          {selectedContact ? (
            <>
              {/* Chat Header */}
              <div className="p-4 border-b border-border flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Avatar className="h-10 w-10">
                    <AvatarImage src={selectedContact.avatar || ""} alt={selectedContact.name} />
                    <AvatarFallback>{getInitials(selectedContact.name)}</AvatarFallback>
                  </Avatar>
                  <div>
                    <h3 className="font-medium">{selectedContact.name}</h3>
                    <p className="text-xs text-muted-foreground">
                      {selectedContact.online ? "Online agora" : "Offline"}
                    </p>
                  </div>
                </div>
                
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon">
                      <MoreVertical className="h-5 w-5" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>Ver perfil</DropdownMenuItem>
                    <DropdownMenuItem>Buscar na conversa</DropdownMenuItem>
                    <DropdownMenuItem>Silenciar notificações</DropdownMenuItem>
                    <DropdownMenuItem className="text-destructive">Limpar conversa</DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
              
              {/* Messages */}
              <div className="flex-1 p-4 overflow-y-auto space-y-4">
                {messages.map((message) => (
                  <div 
                    key={message.id}
                    className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div 
                      className={`max-w-[70%] rounded-lg p-3 ${
                        message.sender === 'user' 
                          ? 'bg-primary text-primary-foreground' 
                          : 'bg-muted'
                      }`}
                    >
                      <p>{message.content}</p>
                      
                      {/* Display attachments if any */}
                      {message.attachments?.map((attachment, index) => (
                        <div 
                          key={index}
                          className="mt-2 p-2 rounded bg-background/10 flex items-center gap-2"
                        >
                          <FileText className="h-4 w-4" />
                          <span className="text-sm truncate">{attachment.name}</span>
                        </div>
                      ))}
                      
                      <div className="text-xs opacity-70 text-right mt-1">
                        {format(message.time, "HH:mm", { locale: ptBR })}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              {/* Message Input */}
              <div className="p-4 border-t border-border">
                <div className="flex items-center gap-2">
                  <Popover open={isAttachmentMenuOpen} onOpenChange={setIsAttachmentMenuOpen}>
                    <PopoverTrigger asChild>
                      <Button variant="ghost" size="icon">
                        <Paperclip className="h-5 w-5" />
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-48" align="start">
                      <div className="grid gap-1">
                        <Button variant="ghost" className="justify-start" onClick={() => {
                          setIsCalendarDialogOpen(true);
                          setIsAttachmentMenuOpen(false);
                        }}>
                          <Calendar className="h-4 w-4 mr-2" />
                          Agendar evento
                        </Button>
                        
                        <DialogTrigger asChild>
                          <Button variant="ghost" className="justify-start" onClick={() => setIsAttachmentMenuOpen(false)}>
                            <FileText className="h-4 w-4 mr-2" />
                            Anexar licitação
                          </Button>
                        </DialogTrigger>
                        
                        <Button variant="ghost" className="justify-start">
                          <Paperclip className="h-4 w-4 mr-2" />
                          Anexar arquivo
                        </Button>
                      </div>
                    </PopoverContent>
                  </Popover>
                  
                  <Popover open={isMentionsMenuOpen} onOpenChange={setIsMentionsMenuOpen}>
                    <PopoverTrigger asChild>
                      <Button variant="ghost" size="icon">
                        <AtSign className="h-5 w-5" />
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-64" align="start">
                      <h4 className="text-sm font-medium mb-2">Mencionar usuário</h4>
                      <div className="space-y-1">
                        {teamMembers.map(member => (
                          <Button
                            key={member.id}
                            variant="ghost"
                            className="w-full justify-start text-left"
                            onClick={() => handleAddMention(member.id, member.name)}
                          >
                            <Avatar className="h-6 w-6 mr-2">
                              <AvatarFallback className="text-xs">{getInitials(member.name)}</AvatarFallback>
                            </Avatar>
                            <div className="overflow-hidden">
                              <p className="truncate">{member.name}</p>
                              <p className="text-xs text-muted-foreground truncate">{member.role}</p>
                            </div>
                          </Button>
                        ))}
                      </div>
                    </PopoverContent>
                  </Popover>
                  
                  <Input
                    placeholder="Digite sua mensagem..."
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    className="flex-1"
                  />
                  
                  <Button size="icon" disabled={!newMessage.trim()} onClick={handleSendMessage}>
                    <Send className="h-5 w-5" />
                  </Button>
                </div>
              </div>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <div className="text-center text-muted-foreground">
                <User className="h-12 w-12 mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">Nenhuma conversa selecionada</h3>
                <p>Selecione um contato para iniciar uma conversa</p>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Calendar Event Dialog */}
      <Dialog open={isCalendarDialogOpen} onOpenChange={setIsCalendarDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Agendar Evento</DialogTitle>
            <DialogDescription>
              Crie um evento no calendário e compartilhe com seus contatos.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div>
              <label htmlFor="event-title" className="block mb-1 text-sm font-medium">
                Título
              </label>
              <Input id="event-title" placeholder="Título do evento" />
            </div>
            <div>
              <label htmlFor="event-date" className="block mb-1 text-sm font-medium">
                Data
              </label>
              <Input id="event-date" type="date" />
            </div>
            <div>
              <label htmlFor="event-time" className="block mb-1 text-sm font-medium">
                Horário
              </label>
              <Input id="event-time" type="time" />
            </div>
            <div>
              <label htmlFor="event-description" className="block mb-1 text-sm font-medium">
                Descrição
              </label>
              <Input id="event-description" placeholder="Descrição do evento" />
            </div>
            <div>
              <label htmlFor="event-participants" className="block mb-1 text-sm font-medium">
                Participantes
              </label>
              <div className="flex flex-wrap gap-2 mb-2">
                {teamMembers.slice(0, 2).map(member => (
                  <div key={member.id} className="flex items-center bg-accent rounded-full px-2 py-1">
                    <Avatar className="h-5 w-5 mr-1">
                      <AvatarFallback className="text-[10px]">{getInitials(member.name)}</AvatarFallback>
                    </Avatar>
                    <span className="text-xs">{member.name}</span>
                    <Button variant="ghost" size="icon" className="h-4 w-4 ml-1">
                      <X className="h-3 w-3" />
                    </Button>
                  </div>
                ))}
              </div>
              <div className="relative">
                <Input id="event-participants" placeholder="Adicionar participantes..." />
                <Button className="absolute right-1 top-1 h-6" size="sm" variant="ghost">
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsCalendarDialogOpen(false)}>
              Cancelar
            </Button>
            <Button onClick={handleCreateEvent}>Criar Evento</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      
      {/* Attach Bid Dialog */}
      <Dialog>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Anexar Licitação</DialogTitle>
            <DialogDescription>
              Selecione uma licitação para compartilhar nesta conversa.
            </DialogDescription>
          </DialogHeader>
          <div className="py-4 space-y-2">
            {kanbanItems.map(item => (
              <Card 
                key={item.id}
                className="cursor-pointer hover:bg-accent transition-colors"
                onClick={() => {
                  toast({
                    title: "Licitação anexada",
                    description: `${item.title} foi compartilhada na conversa.`,
                  });
                }}
              >
                <CardHeader className="p-3">
                  <CardTitle className="text-sm">{item.title}</CardTitle>
                  <p className="text-xs text-muted-foreground">#{item.number}</p>
                </CardHeader>
              </Card>
            ))}
          </div>
          <DialogFooter>
            <DialogClose asChild>
              <Button variant="outline">Cancelar</Button>
            </DialogClose>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </motion.div>
  );
};

export default MensagensPage;
