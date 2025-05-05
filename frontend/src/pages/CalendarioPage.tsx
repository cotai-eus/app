
import React, { useState } from "react";
import { motion } from "framer-motion";
import { Calendar as CalendarIcon, Plus, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Calendar } from "@/components/ui/calendar";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { ptBR } from "date-fns/locale";
import { format, addDays, isToday } from "date-fns";

// Mock events
const mockEvents = [
  {
    id: "event-1",
    title: "Entrega da Proposta - Prefeitura SP",
    date: new Date(2025, 3, 15),
    time: "14:00",
    description: "Entrega final da proposta técnica e comercial",
    type: "deadline",
  },
  {
    id: "event-2",
    title: "Reunião com Equipe",
    date: new Date(2025, 3, 8),
    time: "10:00",
    description: "Análise dos documentos da licitação",
    type: "meeting",
  },
  {
    id: "event-3",
    title: "Abertura dos Envelopes",
    date: new Date(2025, 3, 20),
    time: "09:00",
    description: "Cerimônia de abertura dos envelopes",
    type: "deadline",
  },
  {
    id: "event-4",
    title: "Visita Técnica",
    date: addDays(new Date(), 1),
    time: "13:30",
    description: "Visita técnica no local da obra",
    type: "visit",
  },
  {
    id: "event-5",
    title: "Prazo Final para Recursos",
    date: new Date(),
    time: "18:00",
    description: "Prazo final para envio de recursos",
    type: "deadline",
  },
];

// Event types and colors
const eventTypes = {
  deadline: { name: "Prazo", color: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300" },
  meeting: { name: "Reunião", color: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300" },
  visit: { name: "Visita", color: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300" },
  other: { name: "Outro", color: "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300" },
};

interface EventFormData {
  title: string;
  date: Date | null;
  time: string;
  description: string;
  type: string;
}

const CalendarioPage = () => {
  const [date, setDate] = useState<Date | undefined>(new Date());
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState<typeof mockEvents[0] | null>(null);
  const [newEvent, setNewEvent] = useState<EventFormData>({
    title: "",
    date: new Date(),
    time: "",
    description: "",
    type: "other",
  });
  const { toast } = useToast();

  // Format date for display
  const formatEventDate = (date: Date) => {
    return format(date, "d 'de' MMMM", { locale: ptBR });
  };

  // Get events for selected date
  const eventsForSelectedDate = date 
    ? mockEvents.filter(
        event => 
          event.date.getDate() === date.getDate() &&
          event.date.getMonth() === date.getMonth() &&
          event.date.getFullYear() === date.getFullYear()
      )
    : [];

  // Get events for today
  const todaysEvents = mockEvents.filter(
    event => isToday(event.date)
  );

  // Get upcoming events (next 5 days)
  const upcomingEvents = mockEvents
    .filter(event => 
      event.date > new Date() && 
      event.date <= addDays(new Date(), 5)
    )
    .sort((a, b) => a.date.getTime() - b.date.getTime());

  // Handle creating a new event
  const handleCreateEvent = () => {
    if (!newEvent.title || !newEvent.date || !newEvent.time) {
      toast({
        title: "Campos obrigatórios",
        description: "Preencha todos os campos obrigatórios.",
        variant: "destructive",
      });
      return;
    }
    
    // In a real app, this would save the event to the database
    toast({
      title: "Evento criado",
      description: "O evento foi adicionado ao calendário com sucesso.",
    });
    
    setIsDialogOpen(false);
    setNewEvent({
      title: "",
      date: new Date(),
      time: "",
      description: "",
      type: "other",
    });
  };

  // Function to render calendar day contents with badges for events
  const renderDay = (day: Date) => {
    const eventsOnThisDay = mockEvents.filter(
      event => 
        event.date.getDate() === day.getDate() &&
        event.date.getMonth() === day.getMonth() &&
        event.date.getFullYear() === day.getFullYear()
    );

    if (eventsOnThisDay.length === 0) return null;

    return (
      <div className="flex items-center justify-center w-full">
        <div className="h-1.5 w-1.5 bg-primary rounded-full" />
      </div>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="container mx-auto py-6"
    >
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Calendário</h1>
        <Button onClick={() => setIsDialogOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Novo Evento
        </Button>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Calendar */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Calendário de Eventos</CardTitle>
              <CardDescription>
                Visualize e gerencie todos os eventos relacionados às licitações.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Calendar
                mode="single"
                selected={date}
                onSelect={setDate}
                locale={ptBR}
                className="rounded-md border"
                components={{
                  DayContent: ({ date, ...props }) => (
                    <div className="flex flex-col items-center justify-center w-full h-full">
                      <div>{date.getDate()}</div>
                      {renderDay(date)}
                    </div>
                  ),
                }}
              />
            </CardContent>
          </Card>
          
          {/* Events for selected date */}
          <Card className="mt-6">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center">
                <CalendarIcon className="mr-2 h-5 w-5" />
                Eventos de {date ? formatEventDate(date) : "hoje"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {eventsForSelectedDate.length > 0 ? (
                  eventsForSelectedDate.map(event => (
                    <div 
                      key={event.id} 
                      className="p-3 rounded-md border border-border hover:bg-accent transition-colors"
                      onClick={() => setSelectedEvent(event)}
                    >
                      <div className="flex justify-between items-start">
                        <h4 className="font-medium">{event.title}</h4>
                        <Badge variant="outline" className={eventTypes[event.type as keyof typeof eventTypes].color}>
                          {eventTypes[event.type as keyof typeof eventTypes].name}
                        </Badge>
                      </div>
                      <div className="flex items-center mt-2 text-sm text-muted-foreground">
                        <Clock className="mr-1 h-4 w-4" />
                        <span>{event.time}</span>
                      </div>
                      {event.description && (
                        <p className="mt-2 text-sm">{event.description}</p>
                      )}
                    </div>
                  ))
                ) : (
                  <p className="text-center text-muted-foreground py-8">
                    Nenhum evento para esta data.
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
        
        {/* Upcoming Events Sidebar */}
        <div className="space-y-6">
          {/* Today's Events */}
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-lg">Eventos de Hoje</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {todaysEvents.length > 0 ? (
                  todaysEvents.map(event => (
                    <div key={event.id} className="flex items-center p-2 rounded-md hover:bg-accent transition-colors">
                      <div className="mr-2">
                        <div className={`h-3 w-3 rounded-full ${event.type === 'deadline' ? 'bg-red-500' : event.type === 'meeting' ? 'bg-blue-500' : 'bg-green-500'}`} />
                      </div>
                      <div className="flex-1">
                        <p className="font-medium truncate">{event.title}</p>
                        <p className="text-xs text-muted-foreground">{event.time}</p>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-center text-muted-foreground py-4">
                    Nenhum evento hoje.
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
          
          {/* Upcoming Events */}
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-lg">Próximos Eventos</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {upcomingEvents.length > 0 ? (
                  upcomingEvents.map(event => (
                    <div key={event.id} className="flex items-center p-2 rounded-md hover:bg-accent transition-colors">
                      <div className="mr-2">
                        <div className={`h-3 w-3 rounded-full ${event.type === 'deadline' ? 'bg-red-500' : event.type === 'meeting' ? 'bg-blue-500' : 'bg-green-500'}`} />
                      </div>
                      <div className="flex-1">
                        <p className="font-medium truncate">{event.title}</p>
                        <div className="flex items-center text-xs text-muted-foreground">
                          <CalendarIcon className="mr-1 h-3 w-3" />
                          <span>{formatEventDate(event.date)}</span>
                          <span className="mx-1">•</span>
                          <Clock className="mr-1 h-3 w-3" />
                          <span>{event.time}</span>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-center text-muted-foreground py-4">
                    Nenhum evento próximo.
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
          
          {/* Quick Actions */}
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-lg">Ações Rápidas</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" className="w-full justify-start" onClick={() => setIsDialogOpen(true)}>
                <Plus className="mr-2 h-4 w-4" />
                Novo Evento
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <CalendarIcon className="mr-2 h-4 w-4" />
                Exportar Calendário
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
      
      {/* New Event Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Criar Novo Evento</DialogTitle>
            <DialogDescription>
              Adicione todos os detalhes do evento abaixo.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="event-title">Título *</Label>
              <Input 
                id="event-title" 
                value={newEvent.title}
                onChange={e => setNewEvent({...newEvent, title: e.target.value})}
                placeholder="Nome do evento"
              />
            </div>
            
            <div className="grid gap-2">
              <Label>Data *</Label>
              <div className="border rounded-md p-2">
                <Calendar
                  mode="single"
                  selected={newEvent.date}
                  onSelect={(date) => setNewEvent({...newEvent, date})}
                  locale={ptBR}
                  className="w-full"
                />
              </div>
            </div>
            
            <div className="grid gap-2">
              <Label htmlFor="event-time">Horário *</Label>
              <Input 
                id="event-time" 
                type="time"
                value={newEvent.time}
                onChange={e => setNewEvent({...newEvent, time: e.target.value})}
              />
            </div>
            
            <div className="grid gap-2">
              <Label htmlFor="event-type">Tipo</Label>
              <Select 
                value={newEvent.type}
                onValueChange={(value) => setNewEvent({...newEvent, type: value})}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione o tipo" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="deadline">Prazo</SelectItem>
                  <SelectItem value="meeting">Reunião</SelectItem>
                  <SelectItem value="visit">Visita</SelectItem>
                  <SelectItem value="other">Outro</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="grid gap-2">
              <Label htmlFor="event-desc">Descrição</Label>
              <Input 
                id="event-desc" 
                value={newEvent.description}
                onChange={e => setNewEvent({...newEvent, description: e.target.value})}
                placeholder="Detalhes do evento"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
              Cancelar
            </Button>
            <Button onClick={handleCreateEvent}>Criar Evento</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      
      {/* Event Details Dialog */}
      {selectedEvent && (
        <Dialog open={Boolean(selectedEvent)} onOpenChange={() => setSelectedEvent(null)}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle className="flex items-center justify-between">
                <span>{selectedEvent.title}</span>
                <Badge variant="outline" className={eventTypes[selectedEvent.type as keyof typeof eventTypes].color}>
                  {eventTypes[selectedEvent.type as keyof typeof eventTypes].name}
                </Badge>
              </DialogTitle>
            </DialogHeader>
            <div className="py-4 space-y-4">
              <div className="flex items-center">
                <CalendarIcon className="h-5 w-5 mr-2" />
                <span>{formatEventDate(selectedEvent.date)}</span>
              </div>
              <div className="flex items-center">
                <Clock className="h-5 w-5 mr-2" />
                <span>{selectedEvent.time}</span>
              </div>
              {selectedEvent.description && (
                <div className="pt-2">
                  <h4 className="font-medium mb-1">Descrição:</h4>
                  <p>{selectedEvent.description}</p>
                </div>
              )}
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setSelectedEvent(null)}>
                Fechar
              </Button>
              <Button variant="default">
                Editar Evento
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      )}
    </motion.div>
  );
};

export default CalendarioPage;
