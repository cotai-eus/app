import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Search, Send, User, Users, Star, Inbox, Archive, AlertCircle, CheckCircle } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';

interface Message {
  id: string;
  sender: {
    id: string;
    name: string;
    avatar?: string;
  };
  content: string;
  timestamp: Date;
  read: boolean;
  starred: boolean;
}

interface Conversation {
  id: string;
  participants: {
    id: string;
    name: string;
    avatar?: string;
  }[];
  lastMessage: {
    content: string;
    timestamp: Date;
    read: boolean;
  };
  messages: Message[];
  title?: string;
  isGroup: boolean;
  unreadCount: number;
}

const mockConversations: Conversation[] = [
  {
    id: '1',
    participants: [
      { id: '2', name: 'Ana Silva', avatar: '' },
    ],
    lastMessage: {
      content: 'Vamos revisar os documentos para o edital municipal.',
      timestamp: new Date(2023, 5, 15, 14, 30),
      read: false,
    },
    messages: [
      {
        id: 'm1',
        sender: { id: '2', name: 'Ana Silva' },
        content: 'Olá! Precisamos revisar os documentos para o edital municipal.',
        timestamp: new Date(2023, 5, 15, 14, 0),
        read: true,
        starred: false,
      },
      {
        id: 'm2',
        sender: { id: '1', name: 'Admin User' },
        content: 'Sim, vamos organizar isso hoje à tarde.',
        timestamp: new Date(2023, 5, 15, 14, 15),
        read: true,
        starred: false,
      },
      {
        id: 'm3',
        sender: { id: '2', name: 'Ana Silva' },
        content: 'Vamos revisar os documentos para o edital municipal.',
        timestamp: new Date(2023, 5, 15, 14, 30),
        read: false,
        starred: false,
      },
    ],
    isGroup: false,
    unreadCount: 1,
  },
  {
    id: '2',
    participants: [
      { id: '3', name: 'Carlos Mendes', avatar: '' },
    ],
    lastMessage: {
      content: 'O prazo para o pregão eletrônico foi estendido.',
      timestamp: new Date(2023, 5, 14, 11, 45),
      read: true,
    },
    messages: [
      {
        id: 'm4',
        sender: { id: '3', name: 'Carlos Mendes' },
        content: 'Olá! Só para avisar que o prazo para o pregão eletrônico foi estendido.',
        timestamp: new Date(2023, 5, 14, 11, 45),
        read: true,
        starred: true,
      },
    ],
    isGroup: false,
    unreadCount: 0,
  },
  {
    id: '3',
    title: 'Equipe de Licitações',
    participants: [
      { id: '2', name: 'Ana Silva', avatar: '' },
      { id: '3', name: 'Carlos Mendes', avatar: '' },
      { id: '4', name: 'Mariana Costa', avatar: '' },
    ],
    lastMessage: {
      content: 'Reunião marcada para amanhã às 10h.',
      timestamp: new Date(2023, 5, 14, 9, 0),
      read: true,
    },
    messages: [
      {
        id: 'm5',
        sender: { id: '4', name: 'Mariana Costa' },
        content: 'Pessoal, reunião marcada para amanhã às 10h para discutirmos os próximos editais.',
        timestamp: new Date(2023, 5, 14, 9, 0),
        read: true,
        starred: false,
      },
    ],
    isGroup: true,
    unreadCount: 0,
  },
];

/**
 * Mensagens page component for internal messaging
 */
const MensagensPage = () => {
  const { user } = useAuthStore();
  const [conversations, setConversations] = useState<Conversation[]>(mockConversations);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [messageInput, setMessageInput] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  
  useEffect(() => {
    if (conversations.length > 0 && !selectedConversation) {
      setSelectedConversation(conversations[0]);
    }
  }, [conversations, selectedConversation]);
  
  const handleSendMessage = () => {
    if (!messageInput.trim() || !selectedConversation) return;
    
    const newMessage: Message = {
      id: `m${Math.random().toString(36).substring(2, 9)}`,
      sender: { id: user?.id || '1', name: user?.name || 'Admin User' },
      content: messageInput,
      timestamp: new Date(),
      read: true,
      starred: false,
    };
    
    const updatedConversations = conversations.map(conv => {
      if (conv.id === selectedConversation.id) {
        return {
          ...conv,
          lastMessage: {
            content: messageInput,
            timestamp: new Date(),
            read: true,
          },
          messages: [...conv.messages, newMessage],
        };
      }
      return conv;
    });
    
    setConversations(updatedConversations);
    setSelectedConversation({
      ...selectedConversation,
      lastMessage: {
        content: messageInput,
        timestamp: new Date(),
        read: true,
      },
      messages: [...selectedConversation.messages, newMessage],
    });
    setMessageInput('');
  };

  const filteredConversations = conversations.filter(conv => {
    if (!searchTerm) return true;
    
    const participantsMatch = conv.participants.some(p => 
      p.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    const titleMatch = conv.title?.toLowerCase().includes(searchTerm.toLowerCase());
    
    return participantsMatch || titleMatch;
  });

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };
  
  const formatMessageTime = (date: Date) => {
    return format(date, 'HH:mm');
  };
  
  const formatLastMessageTime = (date: Date) => {
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    if (date.toDateString() === today.toDateString()) {
      return format(date, 'HH:mm');
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Ontem';
    } else {
      return format(date, 'dd/MM/yyyy');
    }
  };
  
  return (
    <motion.div 
      className="space-y-6"
      variants={container}
      initial="hidden"
      animate="show"
    >
      <div className="flex flex-col space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Mensagens</h2>
        <p className="text-muted-foreground">
          Comunicação interna e notificações
        </p>
      </div>
      
      <motion.div variants={item} className="h-[calc(100vh-240px)] flex border rounded-lg overflow-hidden">
        {/* Left sidebar - Conversations list */}
        <Card className="w-1/3 border-r border-t-0 border-b-0 border-l-0 rounded-none">
          <div className="p-3 border-b">
            <div className="flex items-center">
              <Search className="h-4 w-4 mr-2 text-muted-foreground" />
              <Input 
                placeholder="Pesquisar mensagens..." 
                className="w-full"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          
          <Tabs defaultValue="inbox" className="px-3 pt-3">
            <TabsList className="w-full">
              <TabsTrigger value="inbox" className="flex-1">
                <Inbox className="h-4 w-4 mr-2" />
                Inbox
              </TabsTrigger>
              <TabsTrigger value="starred" className="flex-1">
                <Star className="h-4 w-4 mr-2" />
                Favoritos
              </TabsTrigger>
              <TabsTrigger value="archived" className="flex-1">
                <Archive className="h-4 w-4 mr-2" />
                Arquivados
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="inbox" className="m-0 mt-3">
              <ScrollArea className="h-[calc(100vh-340px)]">
                <div className="space-y-1 pr-3">
                  {filteredConversations.map((conversation) => (
                    <div
                      key={conversation.id}
                      className={`flex items-center p-3 rounded-md cursor-pointer hover:bg-muted transition-colors ${
                        selectedConversation?.id === conversation.id ? 'bg-muted' : ''
                      }`}
                      onClick={() => setSelectedConversation(conversation)}
                    >
                      {conversation.isGroup ? (
                        <div className="flex-shrink-0 bg-primary/10 rounded-full p-2">
                          <Users className="h-5 w-5 text-primary" />
                        </div>
                      ) : (
                        <Avatar className="h-9 w-9">
                          <AvatarImage src={conversation.participants[0].avatar} />
                          <AvatarFallback>{conversation.participants[0].name[0]}</AvatarFallback>
                        </Avatar>
                      )}
                      <div className="ml-3 flex-1 overflow-hidden">
                        <div className="flex justify-between items-center">
                          <p className="font-medium truncate">
                            {conversation.title || conversation.participants[0].name}
                          </p>
                          <span className="text-xs text-muted-foreground">
                            {formatLastMessageTime(conversation.lastMessage.timestamp)}
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <p className="text-sm text-muted-foreground truncate">
                            {conversation.lastMessage.content}
                          </p>
                          {conversation.unreadCount > 0 && (
                            <Badge variant="default" className="ml-2 h-5 w-5 rounded-full p-0 flex items-center justify-center">
                              {conversation.unreadCount}
                            </Badge>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {filteredConversations.length === 0 && (
                    <div className="py-8 text-center">
                      <Search className="h-10 w-10 mx-auto text-muted-foreground mb-2" />
                      <p className="text-muted-foreground">Nenhuma conversa encontrada</p>
                    </div>
                  )}
                </div>
              </ScrollArea>
            </TabsContent>
            
            <TabsContent value="starred" className="m-0 mt-3 h-[calc(100vh-340px)] flex items-center justify-center">
              <div className="text-center">
                <Star className="h-10 w-10 mx-auto text-muted-foreground mb-2" />
                <h3 className="text-lg font-medium">Favoritos</h3>
                <p className="text-muted-foreground text-sm mt-1">
                  Marque mensagens como favoritas para acesso rápido
                </p>
              </div>
            </TabsContent>
            
            <TabsContent value="archived" className="m-0 mt-3 h-[calc(100vh-340px)] flex items-center justify-center">
              <div className="text-center">
                <Archive className="h-10 w-10 mx-auto text-muted-foreground mb-2" />
                <h3 className="text-lg font-medium">Arquivados</h3>
                <p className="text-muted-foreground text-sm mt-1">
                  Conversas arquivadas aparecem aqui
                </p>
              </div>
            </TabsContent>
          </Tabs>
        </Card>
        
        {/* Right side - Selected conversation */}
        <div className="flex-1 flex flex-col">
          {selectedConversation ? (
            <>
              {/* Conversation header */}
              <CardHeader className="p-4 border-b flex-row items-center justify-between">
                <div className="flex items-center">
                  {selectedConversation.isGroup ? (
                    <div className="flex-shrink-0 bg-primary/10 rounded-full p-2 mr-3">
                      <Users className="h-5 w-5 text-primary" />
                    </div>
                  ) : (
                    <Avatar className="h-9 w-9 mr-3">
                      <AvatarImage src={selectedConversation.participants[0].avatar} />
                      <AvatarFallback>{selectedConversation.participants[0].name[0]}</AvatarFallback>
                    </Avatar>
                  )}
                  <div>
                    <h3 className="font-semibold">
                      {selectedConversation.title || selectedConversation.participants[0].name}
                    </h3>
                    {selectedConversation.isGroup && (
                      <p className="text-xs text-muted-foreground">
                        {selectedConversation.participants.length} participantes
                      </p>
                    )}
                  </div>
                </div>
              </CardHeader>
              
              {/* Messages area */}
              <ScrollArea className="flex-1 p-4">
                <div className="space-y-4">
                  {selectedConversation.messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${
                        message.sender.id === user?.id ? 'justify-end' : 'justify-start'
                      }`}
                    >
                      <div
                        className={`max-w-[70%] p-3 rounded-lg ${
                          message.sender.id === user?.id
                            ? 'bg-primary text-primary-foreground'
                            : 'bg-secondary'
                        }`}
                      >
                        {selectedConversation.isGroup && message.sender.id !== user?.id && (
                          <p className="text-xs font-medium mb-1">{message.sender.name}</p>
                        )}
                        <p className="text-sm">{message.content}</p>
                        <div
                          className={`text-xs mt-1 ${
                            message.sender.id === user?.id
                              ? 'text-primary-foreground/80'
                              : 'text-muted-foreground'
                          } text-right`}
                        >
                          {formatMessageTime(message.timestamp)}
                          {message.sender.id === user?.id && (
                            <CheckCircle className="inline ml-1 h-3 w-3" />
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>
              
              {/* Message input */}
              <CardContent className="p-4 border-t">
                <div className="flex items-end gap-2">
                  <Textarea
                    placeholder="Digite sua mensagem..."
                    className="flex-1 min-h-[60px]"
                    value={messageInput}
                    onChange={(e) => setMessageInput(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSendMessage();
                      }
                    }}
                  />
                  <Button
                    className="h-10"
                    onClick={handleSendMessage}
                    disabled={!messageInput.trim()}
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <div className="text-center">
                <div className="bg-primary/10 rounded-full p-4 mx-auto w-16 h-16 flex items-center justify-center">
                  <User className="h-8 w-8 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mt-4">Mensagens</h3>
                <p className="text-muted-foreground mt-1">
                  Selecione uma conversa para iniciar
                </p>
              </div>
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
};

export default MensagensPage;
