
import React from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const DashboardPage = () => {
  // Dados de exemplo para o dashboard
  const licitacoes = [
    { 
      id: "ED-2023-1234", 
      titulo: "Aquisição de Equipamentos de Informática", 
      orgao: "Secretaria de Tecnologia", 
      dataLimite: "2025-05-15", 
      status: "Em andamento" 
    },
    { 
      id: "ED-2023-1235", 
      titulo: "Contratação de Serviços de Limpeza", 
      orgao: "Secretaria de Administração", 
      dataLimite: "2025-05-20", 
      status: "Em análise" 
    },
    { 
      id: "ED-2023-1236", 
      titulo: "Fornecimento de Material de Escritório", 
      orgao: "Secretaria de Educação", 
      dataLimite: "2025-05-10", 
      status: "Concluído" 
    },
    { 
      id: "ED-2023-1237", 
      titulo: "Manutenção de Ar Condicionado", 
      orgao: "Secretaria de Infraestrutura", 
      dataLimite: "2025-06-01", 
      status: "Em andamento" 
    },
  ];

  const resumo = {
    total: 12,
    emAndamento: 5,
    emAnalise: 3,
    concluidos: 4,
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="container mx-auto py-6"
    >
      <h1 className="text-3xl font-bold mb-6 text-bluenight-800 dark:text-perola-50">Dashboard de Licitações</h1>

      {/* Cards de resumo */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Total de Licitações
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{resumo.total}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Em Andamento
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">{resumo.emAndamento}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Em Análise
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-amber-600 dark:text-amber-400">{resumo.emAnalise}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Concluídos
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-600 dark:text-green-400">{resumo.concluidos}</div>
          </CardContent>
        </Card>
      </div>

      {/* Lista de licitações recentes */}
      <Card>
        <CardHeader>
          <CardTitle>Licitações Recentes</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4">ID</th>
                  <th className="text-left py-3 px-4">Título</th>
                  <th className="text-left py-3 px-4">Órgão</th>
                  <th className="text-left py-3 px-4">Data Limite</th>
                  <th className="text-left py-3 px-4">Status</th>
                </tr>
              </thead>
              <tbody>
                {licitacoes.map((licitacao) => (
                  <tr key={licitacao.id} className="border-b hover:bg-muted/50">
                    <td className="py-3 px-4">{licitacao.id}</td>
                    <td className="py-3 px-4">{licitacao.titulo}</td>
                    <td className="py-3 px-4">{licitacao.orgao}</td>
                    <td className="py-3 px-4">
                      {new Date(licitacao.dataLimite).toLocaleDateString('pt-BR')}
                    </td>
                    <td className="py-3 px-4">
                      <Badge 
                        variant="outline"
                        className={`
                          ${licitacao.status === "Em andamento" 
                            ? "bg-blue-100 text-blue-800 hover:bg-blue-200 dark:bg-blue-900 dark:text-blue-300 border-blue-400" 
                            : licitacao.status === "Concluído" 
                            ? "bg-green-100 text-green-800 hover:bg-green-200 dark:bg-green-900 dark:text-green-300 border-green-400"
                            : "bg-amber-100 text-amber-800 hover:bg-amber-200 dark:bg-amber-900 dark:text-amber-300 border-amber-400"
                          }
                        `}
                      >
                        {licitacao.status}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default DashboardPage;
