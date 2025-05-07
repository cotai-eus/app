import { useState } from 'react';
import { motion } from 'framer-motion';
import { Calendar as CalendarIcon, Plus, ChevronLeft, ChevronRight, AlertCircle, CheckCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Textarea } from '@/components/ui/textarea';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { cn } from '@/lib/utils';
import { format, addMonths, subMonths, isSameDay, parseISO, isAfter, isBefore, addDays } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { toast } from '@/hooks/use-toast';

interface Event {
  id: string;
  title: string;
  description?: string;
  date: Date;
  startTime?: string;
  endTime?: string;
  type: 'prazo' | 'reuniao' | 'licitacao' | 'outro';
  priority: 'baixa' | 'media' | 'alta';
}

const eventTypes = {
  prazo: { label: 'Prazo', color: 'bg-yellow-500' },
  reuniao: { label: 'Reunião', color: 'bg-blue-500' },
  licitacao: { label: 'Licitação', color: 'bg-green-500' },
  outro: { label: 'Outro', color: 'bg-gray-500' },
};

const priorityTypes = {
  baixa: { label: 'Baixa', color: 'bg-green-500' },
  media: { label: 'Média', color: 'bg-yellow-500' },
  alta: { label: 'Alta', color: 'bg-red-500' },
};

const eventFormSchema = z.object({
  title: z.string().min(3, { message: 'O título deve ter pelo menos 3 caracteres' }),
  description: z.string().optional(),
  date: z.date({ required_error: 'Uma data é obrigatória' }),
  startTime: z.string().optional(),
  endTime: z.string().optional(),
  type: z.enum(['prazo', 'reuniao', 'licitacao', 'outro']),
  priority: z.enum(['baixa', 'media', 'alta']),
});

type EventFormValues = z.infer<typeof eventFormSchema>;

const mockEvents: Event[] = [
  {
    id: '1',
    title: 'Prazo final para submissão de documentos',
    description: 'Entrega de documentação para o pregão eletrônico nº 56/2023',
    date: addDays(new Date(), 2),
    type: 'prazo',
    priority: 'alta',
  },
  {
    id: '2',
    title: 'Reunião com equipe de compras',
    description: 'Discussão sobre os próximos editais',
    date: new Date(),
    startTime: '14:00',
    endTime: '15:30',
    type: 'reuniao',
    priority: 'media',
  },
  {
    id: '3',
    title: 'Abertura da licitação',
    description: 'Abertura da licitação para fornecimento de materiais de escritório',
    date: addDays(new Date(), 7),
    startTime: '10:00',
    type: 'licitacao',
    priority: 'alta',
  },
  {
    id: '4',
    title: 'Prazo de impugnação',
    description: 'Último dia para impugnação do edital',
    date: addDays(new Date(), -2),
    type: 'prazo',
    priority: 'media',
  },
];

/**
 * Calendario page component for managing events and deadlines
 */
const CalendarioPage = () => {
  const [date, setDate] = useState<Date>(new Date());
  const [events, setEvents] = useState<Event[]>(mockEvents);
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(new Date());
  const [month, setMonth] = useState<Date>(new Date());
  const [isAddEventDialogOpen, setIsAddEventDialogOpen] = useState(false);
  
  const form = useForm<EventFormValues>({
    resolver: zodResolver(eventFormSchema),
    defaultValues: {
      title: '',
      description: '',
      date: new Date(),
      type: 'prazo',
      priority: 'media',
    },
  });
  
  const onSubmit = (data: EventFormValues) => {
    const newEvent: Event = {
      id: Math.random().toString(36).substring(2, 9),
      title: data.title, // Explicitly assign required fields
      date: data.date,   // Explicitly assign required fields
      type: data.type,   // Explicitly assign required fields
      priority: data.priority, // Explicitly assign required fields
      description: data.description,
      startTime: data.startTime,
      endTime: data.endTime
    };
    
    setEvents([...events, newEvent]);
    setIsAddEventDialogOpen(false);
    form.reset();
    
    toast({
      title: "Evento adicionado",
      description: "O evento foi adicionado com sucesso ao calendário.",
    });
  };
  
  const handlePrevMonth = () => {
    setMonth(subMonths(month, 1));
  };
  
  const handleNextMonth = () => {
    setMonth(addMonths(month, 1));
  };
  
  const getEventsForDate = (date: Date) => {
    return events.filter(event => isSameDay(event.date, date));
  };
  
  const eventsForSelectedDate = selectedDate ? getEventsForDate(selectedDate) : [];
  
  const isDateInPast = (date: Date) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return isBefore(date, today);
  };
  
  const hasEventsOnDate = (date: Date) => {
    return events.some(event => isSameDay(event.date, date));
  };
  
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
  
  return (
    <motion.div 
      className="space-y-6"
      variants={container}
      initial="hidden"
      animate="show"
    >
      <div className="flex flex-col space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Calendário</h2>
        <p className="text-muted-foreground">
          Gerencie prazos, licitações e reuniões importantes.
        </p>
      </div>
      
      <div className="flex justify-end">
        <Dialog open={isAddEventDialogOpen} onOpenChange={setIsAddEventDialogOpen}>
          <DialogTrigger asChild>
            <Button className="flex items-center gap-2">
              <Plus className="h-4 w-4" />
              Adicionar Evento
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[550px]">
            <DialogHeader>
              <DialogTitle>Adicionar Novo Evento</DialogTitle>
              <DialogDescription>
                Crie um novo evento ou prazo no calendário.
              </DialogDescription>
            </DialogHeader>
            
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <FormField
                  control={form.control}
                  name="title"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Título</FormLabel>
                      <FormControl>
                        <Input placeholder="Título do evento" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="description"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Descrição</FormLabel>
                      <FormControl>
                        <Textarea placeholder="Descrição do evento" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <FormField
                    control={form.control}
                    name="date"
                    render={({ field }) => (
                      <FormItem className="flex flex-col">
                        <FormLabel>Data</FormLabel>
                        <Popover>
                          <PopoverTrigger asChild>
                            <FormControl>
                              <Button
                                variant="outline"
                                className={cn(
                                  "w-full pl-3 text-left font-normal",
                                  !field.value && "text-muted-foreground"
                                )}
                              >
                                {field.value ? (
                                  format(field.value, "P", { locale: ptBR })
                                ) : (
                                  <span>Selecione uma data</span>
                                )}
                                <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                              </Button>
                            </FormControl>
                          </PopoverTrigger>
                          <PopoverContent className="w-auto p-0" align="start">
                            <Calendar
                              mode="single"
                              selected={field.value}
                              onSelect={field.onChange}
                              initialFocus
                            />
                          </PopoverContent>
                        </Popover>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  <div className="grid grid-cols-2 gap-2">
                    <FormField
                      control={form.control}
                      name="startTime"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Hora Início</FormLabel>
                          <FormControl>
                            <Input type="time" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <FormField
                      control={form.control}
                      name="endTime"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Hora Fim</FormLabel>
                          <FormControl>
                            <Input type="time" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <FormField
                    control={form.control}
                    name="type"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Tipo</FormLabel>
                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Selecione o tipo" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="prazo">Prazo</SelectItem>
                            <SelectItem value="reuniao">Reunião</SelectItem>
                            <SelectItem value="licitacao">Licitação</SelectItem>
                            <SelectItem value="outro">Outro</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  <FormField
                    control={form.control}
                    name="priority"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Prioridade</FormLabel>
                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Selecione a prioridade" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="baixa">Baixa</SelectItem>
                            <SelectItem value="media">Média</SelectItem>
                            <SelectItem value="alta">Alta</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                
                <DialogFooter>
                  <Button type="submit">Salvar Evento</Button>
                </DialogFooter>
              </form>
            </Form>
          </DialogContent>
        </Dialog>
      </div>
      
      <motion.div 
        className="grid grid-cols-1 lg:grid-cols-4 gap-6"
        variants={container}
        initial="hidden"
        animate="show"
      >
        <motion.div variants={item} className="lg:col-span-3">
          <Card>
            <CardHeader className="pb-3 flex flex-row items-center justify-between">
              <div>
                <CardTitle>{format(month, 'MMMM yyyy', { locale: ptBR })}</CardTitle>
                <CardDescription>Calendário de eventos e prazos</CardDescription>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="icon"
                  onClick={handlePrevMonth}
                >
                  <ChevronLeft className="h-5 w-5" />
                </Button>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => setMonth(new Date())}
                >
                  <CalendarIcon className="h-5 w-5" />
                </Button>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={handleNextMonth}
                >
                  <ChevronRight className="h-5 w-5" />
                </Button>
              </div>
            </CardHeader>
            <CardContent className="pt-0">
              <Calendar
                mode="single"
                selected={selectedDate}
                onSelect={setSelectedDate}
                month={month}
                onMonthChange={setMonth}
                className="rounded-md border shadow"
                locale={ptBR}
                modifiers={{
                  event: (date) => hasEventsOnDate(date),
                }}
                modifiersClassNames={{
                  event: "font-bold text-primary",
                }}
                components={{
                  DayContent: (props) => {
                    const eventsOnDay = getEventsForDate(props.date);
                    const hasHighPriorityEvent = eventsOnDay.some(
                      (event) => event.priority === 'alta'
                    );
                    
                    return (
                      <div className="relative w-full h-full">
                        <div className="flex justify-center items-center h-full">
                          {props.date.getDate()}
                        </div>
                        {eventsOnDay.length > 0 && (
                          <div 
                            className={`absolute bottom-1 left-1/2 transform -translate-x-1/2 w-1 h-1 rounded-full ${
                              hasHighPriorityEvent ? 'bg-red-500' : 'bg-primary'
                            }`}
                          />
                        )}
                      </div>
                    );
                  },
                }}
              />
            </CardContent>
          </Card>
        </motion.div>
        
        <motion.div variants={item} className="lg:col-span-1">
          <Card className="h-full">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Eventos</span>
                {selectedDate && (
                  <Badge variant="outline">
                    {format(selectedDate, "P", { locale: ptBR })}
                  </Badge>
                )}
              </CardTitle>
              <CardDescription>
                {eventsForSelectedDate.length === 0
                  ? "Nenhum evento para esta data"
                  : `${eventsForSelectedDate.length} evento(s) para esta data`}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {eventsForSelectedDate.length > 0 ? (
                  eventsForSelectedDate.map((event) => (
                    <div
                      key={event.id}
                      className="border rounded-md p-3"
                    >
                      <div className="flex items-center gap-2">
                        <div className={`h-3 w-3 rounded-full ${eventTypes[event.type].color}`} />
                        <h4 className="font-medium">{event.title}</h4>
                      </div>
                      {event.description && (
                        <p className="text-sm text-muted-foreground mt-1">
                          {event.description}
                        </p>
                      )}
                      <div className="flex items-center justify-between mt-2 text-xs text-muted-foreground">
                        <div>
                          {event.startTime && (
                            <span className="bg-secondary px-2 py-1 rounded">
                              {event.startTime}
                              {event.endTime && ` - ${event.endTime}`}
                            </span>
                          )}
                        </div>
                        <Badge className={priorityTypes[event.priority].color}>
                          {priorityTypes[event.priority].label}
                        </Badge>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="flex flex-col items-center justify-center py-8">
                    <CalendarIcon className="h-12 w-12 text-muted-foreground" />
                    <p className="mt-2 text-muted-foreground">
                      Selecione uma data para ver eventos ou adicione um novo
                    </p>
                    <Button
                      className="mt-4"
                      onClick={() => {
                        form.setValue('date', selectedDate || new Date());
                        setIsAddEventDialogOpen(true);
                      }}
                    >
                      <Plus className="h-4 w-4 mr-2" /> Adicionar Evento
                    </Button>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </motion.div>
      
      <motion.div variants={item}>
        <Card>
          <CardHeader>
            <CardTitle>Próximos Prazos</CardTitle>
            <CardDescription>Prazos importantes nos próximos 7 dias</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {events
                .filter(
                  (event) =>
                    event.type === 'prazo' &&
                    isAfter(event.date, new Date()) &&
                    isBefore(event.date, addDays(new Date(), 7))
                )
                .sort((a, b) => a.date.getTime() - b.date.getTime())
                .map((event) => (
                  <div key={event.id} className="flex items-start gap-3">
                    <div className={`p-2 rounded-full ${priorityTypes[event.priority].color}`}>
                      <AlertCircle className="h-4 w-4 text-white" />
                    </div>
                    <div className="flex-1 border-l-2 border-l-muted pl-3">
                      <h4 className="font-medium">{event.title}</h4>
                      <p className="text-sm text-muted-foreground">
                        {event.description}
                      </p>
                      <div className="flex justify-between items-center mt-1">
                        <span className="text-xs text-muted-foreground">
                          {format(event.date, "P", { locale: ptBR })}
                        </span>
                        <Badge variant="outline" className="text-xs">
                          {format(event.date, "'Faltam' d 'dias'", { locale: ptBR })}
                        </Badge>
                      </div>
                    </div>
                  </div>
                ))}
              
              {events.filter(
                (event) =>
                  event.type === 'prazo' &&
                  isAfter(event.date, new Date()) &&
                  isBefore(event.date, addDays(new Date(), 7))
              ).length === 0 && (
                <div className="text-center py-6">
                  <CheckCircle className="h-12 w-12 mx-auto text-muted-foreground mb-2" />
                  <p className="text-muted-foreground">Não há prazos nos próximos 7 dias</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </motion.div>
  );
};

export default CalendarioPage;
