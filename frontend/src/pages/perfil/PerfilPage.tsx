
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { User, Copy, Check, Edit, Save } from 'lucide-react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { toast } from '@/hooks/use-toast';
import { 
  Card, 
  CardHeader, 
  CardTitle, 
  CardDescription, 
  CardContent, 
  CardFooter 
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { useAuthStore } from '@/store/authStore';

// Definição dos tipos
interface UserProfile {
  id: string;
  nome: string;
  email: string;
  cpf: string;
  telefone: string;
  cargo: string;
  departamento: string;
  avatarUrl?: string;
}

interface Company {
  id: string;
  nome: string;
  cnpj: string;
  endereco: string;
  telefone: string;
  site: string;
}

// Schema de validação
const formSchema = z.object({
  nome: z.string().min(3, 'Nome deve ter pelo menos 3 caracteres'),
  email: z.string().email('Email inválido'),
  cpf: z.string()
    .regex(/^\d{3}\.\d{3}\.\d{3}-\d{2}$/, 'CPF inválido (formato: 000.000.000-00)'),
  telefone: z.string()
    .regex(/^\(\d{2}\)\s\d{5}-\d{4}$/, 'Telefone inválido (formato: (00) 00000-0000)'),
  cargo: z.string().min(2, 'Cargo é obrigatório'),
  departamento: z.string().min(2, 'Departamento é obrigatório'),
});

type FormData = z.infer<typeof formSchema>;

/**
 * Formata um CPF inserindo as máscaras
 * @param cpf CPF sem formatação
 * @returns CPF formatado (000.000.000-00)
 */
const formatCpf = (cpf: string): string => {
  const numbers = cpf.replace(/\D/g, '').slice(0, 11);
  if (numbers.length <= 3) return numbers;
  if (numbers.length <= 6) return `${numbers.slice(0, 3)}.${numbers.slice(3)}`;
  if (numbers.length <= 9) return `${numbers.slice(0, 3)}.${numbers.slice(3, 6)}.${numbers.slice(6)}`;
  return `${numbers.slice(0, 3)}.${numbers.slice(3, 6)}.${numbers.slice(6, 9)}-${numbers.slice(9, 11)}`;
};

/**
 * Formata um telefone inserindo as máscaras
 * @param telefone Telefone sem formatação
 * @returns Telefone formatado ((00) 00000-0000)
 */
const formatTelefone = (telefone: string): string => {
  const numbers = telefone.replace(/\D/g, '').slice(0, 11);
  if (numbers.length <= 2) return `(${numbers}`;
  if (numbers.length <= 7) return `(${numbers.slice(0, 2)}) ${numbers.slice(2)}`;
  return `(${numbers.slice(0, 2)}) ${numbers.slice(2, 7)}-${numbers.slice(7)}`;
};

/**
 * Componente de edição de avatar
 */
const AvatarEditor = ({ 
  avatarUrl, 
  onAvatarChange 
}: { 
  avatarUrl?: string, 
  onAvatarChange: (url: string) => void 
}) => {
  const [previewUrl, setPreviewUrl] = useState<string | undefined>(avatarUrl);
  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const url = event.target?.result as string;
        setPreviewUrl(url);
        onAvatarChange(url);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="flex flex-col items-center">
      <Avatar className="h-32 w-32 mb-4">
        <AvatarImage src={previewUrl} alt="Avatar do usuário" />
        <AvatarFallback className="text-4xl">
          <User size={64} />
        </AvatarFallback>
      </Avatar>
      
      <label htmlFor="avatar-upload">
        <Button variant="outline" className="cursor-pointer" type="button">
          Alterar foto
        </Button>
      </label>
      <input 
        id="avatar-upload" 
        type="file" 
        accept="image/*" 
        className="hidden" 
        onChange={handleFileChange} 
      />
    </div>
  );
};

/**
 * Card de dados pessoais
 */
const DadosPessoaisCard = ({ 
  profile, 
  isEditing, 
  onSave,
  onEdit,
  onCancel,
}: { 
  profile: UserProfile, 
  isEditing: boolean,
  onSave: (data: FormData) => void,
  onEdit: () => void,
  onCancel: () => void,
}) => {
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      nome: profile.nome,
      email: profile.email,
      cpf: profile.cpf,
      telefone: profile.telefone,
      cargo: profile.cargo,
      departamento: profile.departamento,
    },
  });

  useEffect(() => {
    if (!isEditing) {
      form.reset({
        nome: profile.nome,
        email: profile.email,
        cpf: profile.cpf,
        telefone: profile.telefone,
        cargo: profile.cargo,
        departamento: profile.departamento,
      });
    }
  }, [isEditing, profile, form]);

  const handleCpfChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const formatted = formatCpf(e.target.value);
    form.setValue('cpf', formatted, { shouldValidate: true });
  };

  const handleTelefoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const formatted = formatTelefone(e.target.value);
    form.setValue('telefone', formatted, { shouldValidate: true });
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center">
          <div>
            <CardTitle>Dados Pessoais</CardTitle>
            <CardDescription>Informações do seu perfil</CardDescription>
          </div>
          {!isEditing ? (
            <Button variant="ghost" size="icon" onClick={onEdit}>
              <Edit className="h-4 w-4" />
            </Button>
          ) : null}
        </div>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSave)} className="space-y-4">
            <FormField
              control={form.control}
              name="nome"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Nome Completo</FormLabel>
                  <FormControl>
                    <Input {...field} disabled={!isEditing} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input {...field} type="email" disabled={!isEditing} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="cpf"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>CPF</FormLabel>
                    <FormControl>
                      <Input 
                        {...field} 
                        disabled={!isEditing}
                        onChange={handleCpfChange}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              
              <FormField
                control={form.control}
                name="telefone"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Telefone</FormLabel>
                    <FormControl>
                      <Input 
                        {...field} 
                        disabled={!isEditing}
                        onChange={handleTelefoneChange}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="cargo"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Cargo</FormLabel>
                    <FormControl>
                      <Input {...field} disabled={!isEditing} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              
              <FormField
                control={form.control}
                name="departamento"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Departamento</FormLabel>
                    <FormControl>
                      <Input {...field} disabled={!isEditing} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            
            {isEditing && (
              <div className="flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={onCancel}>
                  Cancelar
                </Button>
                <Button type="submit">
                  <Save className="mr-2 h-4 w-4" />
                  Salvar
                </Button>
              </div>
            )}
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};

/**
 * Card da empresa
 */
const EmpresaCard = ({ company }: { company: Company }) => {
  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Copiado!",
      description: `${label} copiado para a área de transferência.`,
    });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Dados da Empresa</CardTitle>
        <CardDescription>Informações da empresa vinculada</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <p className="text-sm font-medium">Nome</p>
          <p className="text-muted-foreground">{company.nome}</p>
        </div>
        
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <p className="text-sm font-medium">CNPJ</p>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-5 w-5"
                  onClick={() => copyToClipboard(company.cnpj, "CNPJ")}
                >
                  <Copy className="h-3 w-3" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>Copiar CNPJ</TooltipContent>
            </Tooltip>
          </div>
          <p className="text-muted-foreground">{company.cnpj}</p>
        </div>
        
        <div className="space-y-2">
          <p className="text-sm font-medium">Endereço</p>
          <p className="text-muted-foreground">{company.endereco}</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <p className="text-sm font-medium">Telefone</p>
            <p className="text-muted-foreground">{company.telefone}</p>
          </div>
          
          <div className="space-y-2">
            <p className="text-sm font-medium">Site</p>
            <p className="text-muted-foreground">{company.site}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

/**
 * Página de perfil do usuário
 */
const PerfilPage = () => {
  const { user } = useAuthStore();
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [userProfile, setUserProfile] = useState<UserProfile>({
    id: "1",
    nome: "João da Silva",
    email: "joao.silva@empresa.com.br",
    cpf: "123.456.789-00",
    telefone: "(11) 98765-4321",
    cargo: "Analista de Licitações",
    departamento: "Comercial",
    avatarUrl: "",
  });
  
  const [company, setCompany] = useState<Company>({
    id: "1",
    nome: "Empresa Demonstração Ltda",
    cnpj: "12.345.678/0001-90",
    endereco: "Av. Paulista, 1000, São Paulo - SP",
    telefone: "(11) 3456-7890",
    site: "www.empresademo.com.br",
  });
  
  // Carregamento simulado de dados
  useEffect(() => {
    // Mock de API - Em uma implementação real faria uma chamada axios aqui
    const savedProfile = localStorage.getItem("userProfile");
    if (savedProfile) {
      setUserProfile(JSON.parse(savedProfile));
    }
    
    const savedCompany = localStorage.getItem("company");
    if (savedCompany) {
      setCompany(JSON.parse(savedCompany));
    }
  }, []);

  const handleAvatarChange = (url: string) => {
    setUserProfile(prev => ({ ...prev, avatarUrl: url }));
    
    // Salvar no localStorage
    localStorage.setItem("userProfile", JSON.stringify({ ...userProfile, avatarUrl: url }));
    
    toast({
      title: "Avatar atualizado",
      description: "Sua foto de perfil foi atualizada com sucesso!",
    });
  };
  
  const handleSave = async (data: FormData) => {
    setIsSaving(true);
    
    try {
      // Simulação de API
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const updatedProfile = {
        ...userProfile,
        ...data,
      };
      
      setUserProfile(updatedProfile);
      localStorage.setItem("userProfile", JSON.stringify(updatedProfile));
      
      setIsEditing(false);
      toast({
        title: (
          <div className="flex items-center">
            <Check className="mr-2 h-4 w-4 text-green-500" />
            <span>Dados salvos</span>
          </div>
        ),
        description: "Suas informações foram atualizadas com sucesso!",
      });
    } catch (error) {
      toast({
        title: "Erro ao salvar",
        description: "Ocorreu um erro ao salvar os dados. Tente novamente.",
        variant: "destructive",
      });
    } finally {
      setIsSaving(false);
    }
  };
  
  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold">Perfil</h1>
        <p className="text-muted-foreground mt-2">
          Gerencie seus dados pessoais e informações da empresa
        </p>
      </motion.div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Coluna da esquerda - Avatar */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="lg:col-span-1"
        >
          <Card>
            <CardContent className="pt-6">
              <AvatarEditor 
                avatarUrl={userProfile.avatarUrl} 
                onAvatarChange={handleAvatarChange} 
              />
              
              <div className="mt-6 text-center">
                <h3 className="text-xl font-medium">{userProfile.nome}</h3>
                <p className="text-muted-foreground">{userProfile.cargo}</p>
                <p className="text-xs text-muted-foreground">{userProfile.email}</p>
              </div>
            </CardContent>
          </Card>
        </motion.div>
        
        {/* Coluna da direita - Dados */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="lg:col-span-2 space-y-8"
        >
          {/* Card de dados pessoais */}
          <DadosPessoaisCard 
            profile={userProfile}
            isEditing={isEditing}
            onEdit={() => setIsEditing(true)}
            onCancel={() => setIsEditing(false)}
            onSave={handleSave}
          />
          
          {/* Card da empresa */}
          <EmpresaCard company={company} />
        </motion.div>
      </div>
    </div>
  );
};

export default PerfilPage;
