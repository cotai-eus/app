
import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { motion } from "framer-motion";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { Upload, FileText, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { toast } from "sonner";
import { useToast } from "@/hooks/use-toast";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

interface EditalFormValues {
  codigo: string;
  ua: string;
  titulo: string;
  orgao: string;
  numero: string;
  dataPublicacao: Date;
  dataLimite: Date;
  descricao: string;
}

// Risk analysis data
const riskData = [
  { name: 'Baixo', value: 30, color: '#10B981' },
  { name: 'Médio', value: 45, color: '#F59E0B' },
  { name: 'Alto', value: 25, color: '#EF4444' },
];

const NovaLicitacaoPage = () => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const { toast } = useToast();
  
  const form = useForm<EditalFormValues>({
    defaultValues: {
      codigo: "ED-" + Math.floor(1000 + Math.random() * 9000),
      ua: "",
      titulo: "",
      orgao: "",
      numero: "",
      descricao: "",
    },
  });

  const onSubmit = (data: EditalFormValues) => {
    if (!uploadedFile) {
      toast({
        title: "Erro",
        description: "Por favor, faça upload do arquivo do edital.",
        variant: "destructive",
      });
      return;
    }
    
    console.log("Dados do formulário:", data);
    console.log("Arquivo:", uploadedFile);
    
    toast({
      title: "Sucesso",
      description: "Edital cadastrado com sucesso!",
    });
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      toast({
        title: "Arquivo carregado",
        description: `${file.name} foi carregado com sucesso.`,
      });
    }
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    
    const file = event.dataTransfer.files?.[0];
    if (file) {
      setUploadedFile(file);
      toast({
        title: "Arquivo carregado",
        description: `${file.name} foi carregado com sucesso.`,
      });
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="container mx-auto py-6"
    >
      <h1 className="text-3xl font-bold mb-6">Nova Licitação</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Área de Upload */}
        <Card>
          <CardHeader>
            <CardTitle>Upload do Edital</CardTitle>
            <CardDescription>
              Faça upload do arquivo do edital nos formatos PDF, DOCX, XLS ou ODS.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div 
              className="border-2 border-dashed border-border rounded-lg p-6 flex flex-col items-center justify-center space-y-4 h-80"
              onDrop={handleDrop}
              onDragOver={handleDragOver}
            >
              <Upload className="h-16 w-16 text-muted-foreground" />
              <p className="text-center text-muted-foreground">
                Arraste e solte o edital aqui ou clique para procurar
              </p>
              
              <Input
                id="file-upload"
                type="file"
                className="hidden"
                accept=".pdf,.docx,.xls,.xlsx,.ods"
                onChange={handleFileUpload}
              />
              
              <Button
                variant="outline" 
                onClick={() => document.getElementById("file-upload")?.click()}
              >
                <FileText className="mr-2 h-4 w-4" />
                Selecionar Arquivo
              </Button>
              
              {uploadedFile && (
                <div className="mt-4 p-3 bg-secondary/50 rounded-md">
                  <p className="font-medium">Arquivo carregado:</p>
                  <p className="text-sm">{uploadedFile.name}</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
        
        {/* Formulário de Dados */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Dados do Edital</CardTitle>
              <CardDescription>
                Preencha as informações sobre o edital.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <FormField
                      control={form.control}
                      name="codigo"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Código Interno</FormLabel>
                          <FormControl>
                            <Input placeholder="Ex: ED-1234" {...field} readOnly />
                          </FormControl>
                        </FormItem>
                      )}
                    />
                    
                    <FormField
                      control={form.control}
                      name="ua"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>UA</FormLabel>
                          <FormControl>
                            <Input placeholder="Identificador UA" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                  
                  <FormField
                    control={form.control}
                    name="titulo"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Título</FormLabel>
                        <FormControl>
                          <Input placeholder="Título do edital" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  <div className="grid grid-cols-2 gap-4">
                    <FormField
                      control={form.control}
                      name="orgao"
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
                      name="numero"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Número</FormLabel>
                          <FormControl>
                            <Input placeholder="Nº do edital" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <FormField
                      control={form.control}
                      name="dataPublicacao"
                      render={({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel>Data de Publicação</FormLabel>
                          <Popover>
                            <PopoverTrigger asChild>
                              <FormControl>
                                <Button
                                  variant="outline"
                                  className="w-full pl-3 text-left font-normal"
                                >
                                  {field.value ? (
                                    format(field.value, "P", { locale: ptBR })
                                  ) : (
                                    <span className="text-muted-foreground">
                                      Selecione uma data
                                    </span>
                                  )}
                                </Button>
                              </FormControl>
                            </PopoverTrigger>
                            <PopoverContent className="w-auto p-0 pointer-events-auto">
                              <Calendar
                                mode="single"
                                selected={field.value}
                                onSelect={field.onChange}
                                locale={ptBR}
                                className="p-3 pointer-events-auto"
                              />
                            </PopoverContent>
                          </Popover>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <FormField
                      control={form.control}
                      name="dataLimite"
                      render={({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel>Data Limite</FormLabel>
                          <Popover>
                            <PopoverTrigger asChild>
                              <FormControl>
                                <Button
                                  variant="outline"
                                  className="w-full pl-3 text-left font-normal"
                                >
                                  {field.value ? (
                                    format(field.value, "P", { locale: ptBR })
                                  ) : (
                                    <span className="text-muted-foreground">
                                      Selecione uma data
                                    </span>
                                  )}
                                </Button>
                              </FormControl>
                            </PopoverTrigger>
                            <PopoverContent className="w-auto p-0 pointer-events-auto">
                              <Calendar
                                mode="single"
                                selected={field.value}
                                onSelect={field.onChange}
                                locale={ptBR}
                                className="p-3 pointer-events-auto"
                              />
                            </PopoverContent>
                          </Popover>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                  
                  <FormField
                    control={form.control}
                    name="descricao"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Descrição</FormLabel>
                        <FormControl>
                          <Textarea
                            placeholder="Descreva os detalhes do edital"
                            className="min-h-32"
                            {...field}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  <Button type="submit" className="w-full hover-glow">
                    Cadastrar Edital
                  </Button>
                </form>
              </Form>
            </CardContent>
          </Card>

          {/* Risk Analysis Section */}
          <Card>
            <CardHeader className="space-y-0 pb-2">
              <CardTitle className="text-md flex items-center">
                <AlertCircle className="h-4 w-4 mr-2" />
                Análise de Risco
              </CardTitle>
              <CardDescription>
                Análise preliminar baseada no texto do edital
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-48">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={riskData}
                      cx="50%"
                      cy="50%"
                      innerRadius={40}
                      outerRadius={80}
                      fill="#8884d8"
                      paddingAngle={2}
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {riskData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => `${value}%`} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <p className="text-xs text-muted-foreground text-center mt-2">
                * Esta é uma análise automática preliminar. Os dados podem ser revisados manualmente.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </motion.div>
  );
};

export default NovaLicitacaoPage;
