
import React, { useState, useRef } from "react";
import { motion } from "framer-motion";
import { 
  User, 
  Building2, 
  Mail, 
  Phone, 
  FileText, 
  Calendar, 
  Upload, 
  Copy, 
  Check
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

// Tipos
interface UserProfile {
  nome: string;
  sobrenome: string;
  email: string;
  cpf: string;
  telefone: string;
  dataNascimento: string;
  avatarUrl: string;
}

interface EmpresaData {
  nome: string;
  cnpj: string;
  endereco: string;
  telefone: string;
  cargo: string;
}

// Mock de dados iniciais
const initialUserData: UserProfile = {
  nome: "Carlos",
  sobrenome: "Santos",
  email: "carlos.santos@empresa.com.br",
  cpf: "123.456.789-00",
  telefone: "(11) 98765-4321",
  dataNascimento: "1985-07-15",
  avatarUrl: "",
};

const empresaData: EmpresaData = {
  nome: "TechBids Soluções LTDA",
  cnpj: "12.345.678/0001-90",
  endereco: "Av. Paulista, 1000 - São Paulo, SP",
  telefone: "(11) 3456-7890",
  cargo: "Analista de Licitações",
};

// Helpers para formatação
const formatCPF = (value: string) => {
  return value
    .replace(/\D/g, '')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d{1,2})/, '$1-$2')
    .replace(/(-\d{2})\d+?$/, '$1');
};

const formatPhone = (value: string) => {
  return value
    .replace(/\D/g, '')
    .replace(/(\d{2})(\d)/, '($1) $2')
    .replace(/(\d{5})(\d)/, '$1-$2')
    .replace(/(-\d{4})\d+?$/, '$1');
};

const formatCNPJ = (value: string) => {
  return value
    .replace(/\D/g, '')
    .replace(/(\d{2})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1/$2')
    .replace(/(\d{4})(\d)/, '$1-$2')
    .replace(/(-\d{2})\d+?$/, '$1');
};

export default function PerfilPage() {
  const [userData, setUserData] = useState<UserProfile>(initialUserData);
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [activeTab, setActiveTab] = useState("pessoal");
  const [copied, setCopied] = useState(false);
  const { toast } = useToast();
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handlers
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    
    let formattedValue = value;
    
    // Aplicar máscaras
    if (name === 'cpf') {
      formattedValue = formatCPF(value);
    } else if (name === 'telefone') {
      formattedValue = formatPhone(value);
    }
    
    setUserData(prev => ({ ...prev, [name]: formattedValue }));
  };
  
  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        if (event.target?.result) {
          setUserData(prev => ({ ...prev, avatarUrl: event.target.result as string }));
        }
      };
      reader.readAsDataURL(file);
    }
  };
  
  const handleSave = async () => {
    setIsSaving(true);
    
    // Simulando uma chamada de API
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Salvar no localStorage como fallback
    localStorage.setItem('userProfile', JSON.stringify(userData));
    
    setIsSaving(false);
    setIsEditing(false);
    
    toast({
      title: "Perfil atualizado",
      description: "Suas informações foram salvas com sucesso.",
    });
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
    
    toast({
      title: "CNPJ copiado",
      description: "O CNPJ foi copiado para a área de transferência.",
    });
  };

  // Determinando as iniciais para o avatar fallback
  const getInitials = () => {
    return `${userData.nome.charAt(0)}${userData.sobrenome.charAt(0)}`;
  };

  // Componentes específicos
  const AvatarEditor = () => (
    <div className="flex flex-col items-center mb-6">
      <div className="relative group">
        <Avatar className="w-32 h-32 border-4 border-primary/20">
          <AvatarImage src={userData.avatarUrl} />
          <AvatarFallback className="text-3xl">{getInitials()}</AvatarFallback>
        </Avatar>
        
        {isEditing && (
          <div 
            className="absolute inset-0 flex items-center justify-center bg-black/50 rounded-full opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
            onClick={() => fileInputRef.current?.click()}
          >
            <Upload className="text-white" />
            <input 
              ref={fileInputRef}
              type="file" 
              accept="image/*" 
              className="hidden"
              onChange={handleImageUpload}
            />
          </div>
        )}
      </div>
      
      <h2 className="text-xl font-semibold mt-4">{userData.nome} {userData.sobrenome}</h2>
      <p className="text-muted-foreground">{empresaData.cargo}</p>
      
      {isEditing && (
        <p className="text-xs text-muted-foreground mt-2">
          Clique na imagem para alterar sua foto de perfil
        </p>
      )}
    </div>
  );

  // Renderização principal
  return (
    <div className="container py-8 max-w-5xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="space-y-6"
      >
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">Meu Perfil</h1>
          
          {!isEditing ? (
            <Button onClick={() => setIsEditing(true)}>
              Editar Perfil
            </Button>
          ) : (
            <div className="space-x-2">
              <Button variant="outline" onClick={() => setIsEditing(false)}>
                Cancelar
              </Button>
              <Button 
                onClick={handleSave} 
                disabled={isSaving}
              >
                {isSaving ? "Salvando..." : "Salvar Alterações"}
              </Button>
            </div>
          )}
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full max-w-md grid-cols-2">
            <TabsTrigger value="pessoal">Dados Pessoais</TabsTrigger>
            <TabsTrigger value="empresa">Empresa</TabsTrigger>
          </TabsList>
          
          <TabsContent value="pessoal" className="mt-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <Card className="lg:col-span-1">
                <CardHeader>
                  <CardTitle>Perfil</CardTitle>
                  <CardDescription>
                    Sua foto e informações básicas
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <AvatarEditor />
                </CardContent>
              </Card>
              
              <Card className="lg:col-span-2">
                <CardHeader>
                  <CardTitle>Dados Pessoais</CardTitle>
                  <CardDescription>
                    Informações utilizadas para identificação nos processos licitatórios
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="nome">Nome</Label>
                      <div className="flex">
                        <User className="mr-2 h-4 w-4 opacity-70 mt-3" />
                        <Input
                          id="nome"
                          name="nome"
                          value={userData.nome}
                          onChange={handleInputChange}
                          disabled={!isEditing}
                        />
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="sobrenome">Sobrenome</Label>
                      <div className="flex">
                        <User className="mr-2 h-4 w-4 opacity-70 mt-3" />
                        <Input
                          id="sobrenome"
                          name="sobrenome"
                          value={userData.sobrenome}
                          onChange={handleInputChange}
                          disabled={!isEditing}
                        />
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="email">E-mail</Label>
                      <div className="flex">
                        <Mail className="mr-2 h-4 w-4 opacity-70 mt-3" />
                        <Input
                          id="email"
                          name="email"
                          type="email"
                          value={userData.email}
                          onChange={handleInputChange}
                          disabled={!isEditing}
                        />
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="telefone">Telefone</Label>
                      <div className="flex">
                        <Phone className="mr-2 h-4 w-4 opacity-70 mt-3" />
                        <Input
                          id="telefone"
                          name="telefone"
                          value={userData.telefone}
                          onChange={handleInputChange}
                          disabled={!isEditing}
                          placeholder="(00) 00000-0000"
                        />
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="cpf">CPF</Label>
                      <div className="flex">
                        <FileText className="mr-2 h-4 w-4 opacity-70 mt-3" />
                        <Input
                          id="cpf"
                          name="cpf"
                          value={userData.cpf}
                          onChange={handleInputChange}
                          disabled={!isEditing}
                          placeholder="000.000.000-00"
                        />
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="dataNascimento">Data de Nascimento</Label>
                      <div className="flex">
                        <Calendar className="mr-2 h-4 w-4 opacity-70 mt-3" />
                        <Input
                          id="dataNascimento"
                          name="dataNascimento"
                          type="date"
                          value={userData.dataNascimento}
                          onChange={handleInputChange}
                          disabled={!isEditing}
                        />
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
          
          <TabsContent value="empresa" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Dados da Empresa</CardTitle>
                <CardDescription>
                  Informações da empresa vinculada ao seu perfil
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="empresa-nome">Nome da Empresa</Label>
                    <div className="flex">
                      <Building2 className="mr-2 h-4 w-4 opacity-70 mt-3" />
                      <Input
                        id="empresa-nome"
                        value={empresaData.nome}
                        disabled
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="empresa-cnpj">CNPJ</Label>
                    <div className="flex">
                      <FileText className="mr-2 h-4 w-4 opacity-70 mt-3" />
                      <Input
                        id="empresa-cnpj"
                        value={formatCNPJ(empresaData.cnpj)}
                        disabled
                      />
                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button 
                              variant="ghost" 
                              size="icon"
                              className="ml-2" 
                              onClick={() => copyToClipboard(empresaData.cnpj)}
                            >
                              {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>Copiar CNPJ</p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="empresa-endereco">Endereço</Label>
                    <div className="flex">
                      <Building2 className="mr-2 h-4 w-4 opacity-70 mt-3" />
                      <Input
                        id="empresa-endereco"
                        value={empresaData.endereco}
                        disabled
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="empresa-telefone">Telefone</Label>
                    <div className="flex">
                      <Phone className="mr-2 h-4 w-4 opacity-70 mt-3" />
                      <Input
                        id="empresa-telefone"
                        value={empresaData.telefone}
                        disabled
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="empresa-cargo">Seu Cargo</Label>
                    <div className="flex">
                      <User className="mr-2 h-4 w-4 opacity-70 mt-3" />
                      <Input
                        id="empresa-cargo"
                        value={empresaData.cargo}
                        disabled
                      />
                    </div>
                  </div>
                </div>
                
                <div className="bg-muted/40 p-4 rounded-lg mt-6">
                  <p className="text-sm text-muted-foreground">
                    Para atualizar os dados da empresa, entre em contato com o administrador do sistema através do e-mail <span className="font-medium">suporte@cotai.com.br</span>
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </motion.div>
    </div>
  );
}
