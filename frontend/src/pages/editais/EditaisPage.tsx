
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { FileText, Upload, Download, Eye, Search, Plus, Trash2 } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { toast } from '@/hooks/use-toast';

const platforms = [
  'Gov.br',
  'BEC-SP',
  'Banco do Brasil',
  'Caixa Econômica Federal',
  'Licitações do RJ',
  'Compras MG',
  'Compras PR',
  'Compras BA',
  'Compras SC',
  'Compras RS',
  'Compras CE',
  'Petrobras',
  'Compras MT',
  'Compras MS',
];

const editaisFormSchema = z.object({
  platform: z.string().min(1, { message: 'Selecione uma plataforma' }),
  type: z.string().min(1, { message: 'Selecione um tipo de edital' }),
  number: z.string().min(1, { message: 'O número é obrigatório' }),
  entity: z.string().min(3, { message: 'O órgão deve ter pelo menos 3 caracteres' }),
  description: z.string().optional(),
  file: z.instanceof(File).optional(),
});

type EditaisFormValues = z.infer<typeof editaisFormSchema>;

interface Edital {
  id: string;
  platform: string;
  type: string;
  number: string;
  entity: string;
  description?: string;
  date: string;
  file?: File | null;
}

const mockEditais: Edital[] = [
  {
    id: '1',
    platform: 'Gov.br',
    type: 'Pregão Eletrônico',
    number: '001/2023',
    entity: 'Prefeitura Municipal de São Paulo',
    description: 'Aquisição de computadores, notebooks e impressoras para setores administrativos',
    date: '2023-06-10',
  },
  {
    id: '2',
    platform: 'BEC-SP',
    type: 'Tomada de Preços',
    number: '045/2023',
    entity: 'Governo do Estado',
    description: 'Contratação de empresa especializada em serviços de manutenção predial preventiva e corretiva',
    date: '2023-06-15',
  },
  {
    id: '3',
    platform: 'Banco do Brasil',
    type: 'Concorrência',
    number: '023/2023',
    entity: 'Secretaria de Saúde',
    description: 'Fornecimento contínuo de materiais hospitalares para unidades de saúde',
    date: '2023-06-20',
  },
];

/**
 * Editais page component for managing public notices
 */
const EditaisPage = () => {
  const [editais, setEditais] = useState<Edital[]>(mockEditais);
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  
  const form = useForm<EditaisFormValues>({
    resolver: zodResolver(editaisFormSchema),
    defaultValues: {
      platform: '',
      type: '',
      number: '',
      entity: '',
      description: '',
    },
  });

  const filteredEditais = editais.filter(edital => 
    edital.platform.toLowerCase().includes(searchTerm.toLowerCase()) ||
    edital.entity.toLowerCase().includes(searchTerm.toLowerCase()) ||
    edital.number.toLowerCase().includes(searchTerm.toLowerCase()) ||
    edital.type.toLowerCase().includes(searchTerm.toLowerCase())
  );
  
  const onSubmit = async (data: EditaisFormValues) => {
    setIsLoading(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const newEdital: Edital = {
        id: Math.random().toString(36).substring(2, 9),
        platform: data.platform,
        type: data.type,
        number: data.number,
        entity: data.entity,
        description: data.description,
        date: new Date().toISOString().split('T')[0],
        file: data.file,
      };
      
      setEditais([newEdital, ...editais]);
      setIsAddDialogOpen(false);
      form.reset();
      
      toast({
        title: "Edital adicionado",
        description: "O edital foi adicionado com sucesso.",
      });
    } catch (error) {
      toast({
        title: "Erro",
        description: "Ocorreu um erro ao adicionar o edital.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      form.setValue('file', file);
    }
  };
  
  const handleDeleteEdital = (id: string) => {
    setEditais(editais.filter(edital => edital.id !== id));
    toast({
      title: "Edital removido",
      description: "O edital foi removido com sucesso.",
    });
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
        <h2 className="text-3xl font-bold tracking-tight">Editais</h2>
        <p className="text-muted-foreground">
          Gerencie os editais de licitações e outras comunicações oficiais.
        </p>
      </div>
      
      <Tabs defaultValue="all">
        <div className="flex justify-between items-center">
          <TabsList>
            <TabsTrigger value="all">Todos</TabsTrigger>
            <TabsTrigger value="active">Ativos</TabsTrigger>
            <TabsTrigger value="archived">Arquivados</TabsTrigger>
          </TabsList>
          
          <div className="flex items-center gap-2">
            <div className="relative">
              <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input 
                placeholder="Buscar editais..." 
                className="pl-8 w-64" 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            
            <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
              <DialogTrigger asChild>
                <Button className="flex items-center gap-2">
                  <Plus className="h-4 w-4" />
                  Novo Edital
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[550px]">
                <DialogHeader>
                  <DialogTitle>Adicionar Novo Edital</DialogTitle>
                  <DialogDescription>
                    Preencha as informações do edital e faça o upload do arquivo.
                  </DialogDescription>
                </DialogHeader>
                
                <Form {...form}>
                  <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                    <FormField
                      control={form.control}
                      name="platform"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Plataforma</FormLabel>
                          <Select onValueChange={field.onChange} defaultValue={field.value}>
                            <FormControl>
                              <SelectTrigger>
                                <SelectValue placeholder="Selecione a plataforma" />
                              </SelectTrigger>
                            </FormControl>
                            <SelectContent>
                              {platforms.map((platform) => (
                                <SelectItem key={platform} value={platform}>
                                  {platform}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <div className="grid grid-cols-2 gap-4">
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
                                <SelectItem value="Pregão Eletrônico">Pregão Eletrônico</SelectItem>
                                <SelectItem value="Tomada de Preços">Tomada de Preços</SelectItem>
                                <SelectItem value="Concorrência">Concorrência</SelectItem>
                                <SelectItem value="Leilão">Leilão</SelectItem>
                                <SelectItem value="Convite">Convite</SelectItem>
                              </SelectContent>
                            </Select>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      
                      <FormField
                        control={form.control}
                        name="number"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Número</FormLabel>
                            <FormControl>
                              <Input placeholder="Número do edital" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>
                    
                    <FormField
                      control={form.control}
                      name="entity"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Órgão</FormLabel>
                          <FormControl>
                            <Input placeholder="Nome do órgão" {...field} />
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
                            <Textarea placeholder="Descrição do edital" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <FormItem>
                      <FormLabel>Arquivo</FormLabel>
                      <FormControl>
                        <div className="border border-input rounded-md p-2">
                          <label htmlFor="file-upload" className="flex cursor-pointer items-center justify-center gap-2 py-2">
                            <Upload className="h-4 w-4" />
                            <span>Selecionar arquivo</span>
                            <Input
                              id="file-upload"
                              type="file"
                              className="hidden"
                              onChange={handleFileChange}
                              accept=".pdf,.doc,.docx,.xls,.xlsx"
                            />
                          </label>
                          {form.watch('file') && (
                            <div className="mt-2 text-sm text-muted-foreground">
                              Arquivo selecionado: {form.watch('file')?.name}
                            </div>
                          )}
                        </div>
                      </FormControl>
                      <FormDescription>
                        Formatos aceitos: PDF, DOC, DOCX, XLS, XLSX.
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                    
                    <DialogFooter>
                      <Button type="submit" disabled={isLoading}>
                        {isLoading ? 'Salvando...' : 'Salvar Edital'}
                      </Button>
                    </DialogFooter>
                  </form>
                </Form>
              </DialogContent>
            </Dialog>
          </div>
        </div>
        
        <TabsContent value="all" className="mt-6">
          <motion.div variants={item}>
            <Card>
              <CardContent className="p-0">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Plataforma</TableHead>
                      <TableHead>Tipo</TableHead>
                      <TableHead>Número</TableHead>
                      <TableHead>Órgão</TableHead>
                      <TableHead>Data</TableHead>
                      <TableHead className="text-right">Ações</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    <AnimatePresence>
                      {filteredEditais.length > 0 ? (
                        filteredEditais.map((edital) => (
                          <motion.tr
                            key={edital.id}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.2 }}
                          >
                            <TableCell className="font-medium">{edital.platform}</TableCell>
                            <TableCell>{edital.type}</TableCell>
                            <TableCell>{edital.number}</TableCell>
                            <TableCell>{edital.entity}</TableCell>
                            <TableCell>{new Date(edital.date).toLocaleDateString('pt-BR')}</TableCell>
                            <TableCell className="text-right">
                              <div className="flex justify-end gap-2">
                                <Button variant="ghost" size="icon">
                                  <Eye className="h-4 w-4" />
                                </Button>
                                <Button variant="ghost" size="icon">
                                  <Download className="h-4 w-4" />
                                </Button>
                                <Button 
                                  variant="ghost" 
                                  size="icon"
                                  onClick={() => handleDeleteEdital(edital.id)}
                                >
                                  <Trash2 className="h-4 w-4" />
                                </Button>
                              </div>
                            </TableCell>
                          </motion.tr>
                        ))
                      ) : (
                        <motion.tr
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          exit={{ opacity: 0 }}
                        >
                          <TableCell colSpan={6} className="text-center py-10">
                            <div className="flex flex-col items-center justify-center">
                              <FileText className="h-12 w-12 text-muted-foreground mb-2" />
                              <p className="text-lg font-medium">Nenhum edital encontrado</p>
                              <p className="text-sm text-muted-foreground">
                                {searchTerm ? 'Tente outros termos de busca' : 'Adicione seu primeiro edital'}
                              </p>
                            </div>
                          </TableCell>
                        </motion.tr>
                      )}
                    </AnimatePresence>
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </motion.div>
        </TabsContent>
        
        <TabsContent value="active" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Editais Ativos</CardTitle>
              <CardDescription>
                Editais com prazos em aberto e em andamento.
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center py-10">
              <FileText className="h-12 w-12 mx-auto text-muted-foreground mb-2" />
              <p className="text-lg font-medium">Funcionalidade em desenvolvimento</p>
              <p className="text-sm text-muted-foreground mb-6">
                Esta funcionalidade estará disponível em breve.
              </p>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="archived" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Editais Arquivados</CardTitle>
              <CardDescription>
                Editais finalizados e histórico de participações.
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center py-10">
              <FileText className="h-12 w-12 mx-auto text-muted-foreground mb-2" />
              <p className="text-lg font-medium">Funcionalidade em desenvolvimento</p>
              <p className="text-sm text-muted-foreground mb-6">
                Esta funcionalidade estará disponível em breve.
              </p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </motion.div>
  );
};

export default EditaisPage;
