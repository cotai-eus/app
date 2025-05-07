
import { useState } from 'react';
import { motion } from 'framer-motion';
import { DragDropContext, Droppable, Draggable, DropResult } from 'react-beautiful-dnd';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { PlusCircle, MoreHorizontal } from 'lucide-react';

interface Task {
  id: string;
  title: string;
  description: string;
  dueDate?: string;
}

interface Column {
  id: string;
  title: string;
  tasks: Task[];
}

const initialColumns: Column[] = [
  {
    id: 'backlog',
    title: 'Backlog',
    tasks: [
      { 
        id: 'task-1', 
        title: 'Edital municipal nº 45/2023', 
        description: 'Revisar documentação',
        dueDate: '2023-06-15'
      },
      { 
        id: 'task-2', 
        title: 'Licitação estadual nº 78/2023', 
        description: 'Preparar proposta técnica',
        dueDate: '2023-06-22'
      },
      { 
        id: 'task-3', 
        title: 'Edital federal nº 12/2023', 
        description: 'Análise inicial de viabilidade',
      },
    ],
  },
  {
    id: 'todo',
    title: 'A Fazer',
    tasks: [
      { 
        id: 'task-4', 
        title: 'Pregão eletrônico nº 56/2023', 
        description: 'Preparar documentação técnica',
        dueDate: '2023-07-01'
      },
      { 
        id: 'task-5', 
        title: 'Concorrência pública nº 23/2023', 
        description: 'Montar equipe técnica',
        dueDate: '2023-06-25'
      },
    ],
  },
  {
    id: 'doing',
    title: 'Em Progresso',
    tasks: [
      { 
        id: 'task-6', 
        title: 'Tomada de preços nº 34/2023', 
        description: 'Finalização da proposta comercial',
        dueDate: '2023-06-10'
      },
    ],
  },
  {
    id: 'done',
    title: 'Concluído',
    tasks: [
      { 
        id: 'task-7', 
        title: 'Licitação municipal nº 67/2023', 
        description: 'Proposta enviada com sucesso',
      },
    ],
  },
];

/**
 * Kanban page component for task management
 */
const KanbanPage = () => {
  const [columns, setColumns] = useState<Column[]>(initialColumns);
  
  const handleDragEnd = (result: DropResult) => {
    if (!result.destination) return;
    
    const { source, destination } = result;
    
    if (source.droppableId === destination.droppableId && source.index === destination.index) {
      return;
    }
    
    const sourceColIndex = columns.findIndex(col => col.id === source.droppableId);
    const destColIndex = columns.findIndex(col => col.id === destination.droppableId);
    
    const sourceCol = columns[sourceColIndex];
    const destCol = columns[destColIndex];
    
    const sourceTasks = [...sourceCol.tasks];
    const destTasks = sourceCol === destCol ? sourceTasks : [...destCol.tasks];
    
    const [removed] = sourceTasks.splice(source.index, 1);
    destTasks.splice(destination.index, 0, removed);
    
    const newColumns = [...columns];
    
    newColumns[sourceColIndex] = {
      ...sourceCol,
      tasks: sourceTasks,
    };
    
    if (sourceCol !== destCol) {
      newColumns[destColIndex] = {
        ...destCol,
        tasks: destTasks,
      };
    }
    
    setColumns(newColumns);
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
        <h2 className="text-3xl font-bold tracking-tight">Kanban</h2>
        <p className="text-muted-foreground">
          Acompanhe o progresso das licitações e editais.
        </p>
      </div>
      
      <div className="flex justify-end">
        <Button size="sm" className="flex items-center gap-2">
          <PlusCircle className="h-4 w-4" />
          Adicionar Tarefa
        </Button>
      </div>
      
      <motion.div variants={item} className="h-[calc(100vh-280px)]">
        <DragDropContext onDragEnd={handleDragEnd}>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 h-full">
            {columns.map(column => (
              <div key={column.id} className="flex flex-col h-full">
                <div className="text-sm font-medium flex items-center justify-between mb-3">
                  <span>{column.title}</span>
                  <span className="bg-secondary text-secondary-foreground px-2 py-0.5 rounded-full text-xs">
                    {column.tasks.length}
                  </span>
                </div>
                
                <Droppable droppableId={column.id}>
                  {(provided) => (
                    <div
                      {...provided.droppableProps}
                      ref={provided.innerRef}
                      className="bg-muted/50 rounded-lg p-2 flex-1 overflow-y-auto"
                    >
                      {column.tasks.map((task, index) => (
                        <Draggable key={task.id} draggableId={task.id} index={index}>
                          {(provided) => (
                            <div
                              ref={provided.innerRef}
                              {...provided.draggableProps}
                              {...provided.dragHandleProps}
                              className="mb-2"
                            >
                              <Card>
                                <CardHeader className="p-3 pb-1 flex flex-row items-start justify-between">
                                  <CardTitle className="text-sm">{task.title}</CardTitle>
                                  <Button variant="ghost" size="icon" className="h-6 w-6">
                                    <MoreHorizontal className="h-4 w-4" />
                                  </Button>
                                </CardHeader>
                                <CardContent className="p-3 pt-1">
                                  <p className="text-xs text-muted-foreground">{task.description}</p>
                                  {task.dueDate && (
                                    <div className="mt-2 text-xs bg-secondary px-2 py-1 rounded-sm inline-block">
                                      Prazo: {new Date(task.dueDate).toLocaleDateString('pt-BR')}
                                    </div>
                                  )}
                                </CardContent>
                              </Card>
                            </div>
                          )}
                        </Draggable>
                      ))}
                      {provided.placeholder}
                    </div>
                  )}
                </Droppable>
              </div>
            ))}
          </div>
        </DragDropContext>
      </motion.div>
    </motion.div>
  );
};

export default KanbanPage;

