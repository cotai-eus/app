
import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { motion } from 'framer-motion';
import { Activity, BarChart3, Clock, FileText, ArrowUp, ArrowDown } from 'lucide-react';

interface StatsCardProps {
  title: string;
  value: string;
  description: string;
  trend: 'up' | 'down' | 'neutral';
  trendValue: string;
  progress?: number;
  icon: JSX.Element;
}

const StatsCard = ({ title, value, description, trend, trendValue, progress, icon }: StatsCardProps) => (
  <Card>
    <CardHeader className="flex flex-row items-center justify-between pb-2">
      <CardTitle className="text-sm font-medium">{title}</CardTitle>
      {icon}
    </CardHeader>
    <CardContent>
      <div className="text-2xl font-bold">{value}</div>
      <div className="flex items-center text-xs text-muted-foreground">
        {trend === 'up' && <ArrowUp className="mr-1 h-4 w-4 text-green-500" />}
        {trend === 'down' && <ArrowDown className="mr-1 h-4 w-4 text-red-500" />}
        <span className={trend === 'up' ? 'text-green-500' : trend === 'down' ? 'text-red-500' : ''}>
          {trendValue}
        </span>
        <span className="ml-1">{description}</span>
      </div>
      {progress !== undefined && <Progress value={progress} className="h-1 mt-3" />}
    </CardContent>
  </Card>
);

/**
 * Dashboard page component with stats and charts
 */
const DashboardPage = () => {
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Simulate data loading
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);
    
    return () => clearTimeout(timer);
  }, []);
  
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
  
  if (loading) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-160px)]">
        <div className="flex flex-col items-center">
          <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin" />
          <p className="mt-4 text-lg">Carregando dados...</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="space-y-6">
      <div className="flex flex-col space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground">
          Visão geral das licitações, editais e calendário de prazos.
        </p>
      </div>
      
      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Visão Geral</TabsTrigger>
          <TabsTrigger value="analytics">Análises</TabsTrigger>
          <TabsTrigger value="reports">Relatórios</TabsTrigger>
        </TabsList>
        <TabsContent value="overview">
          <motion.div 
            className="grid gap-6 md:grid-cols-2 lg:grid-cols-4"
            variants={container}
            initial="hidden"
            animate="show"
          >
            <motion.div variants={item}>
              <StatsCard
                title="Licitações Ativas"
                value="24"
                description="desde o último mês"
                trend="up"
                trendValue="+8%"
                progress={80}
                icon={<Activity className="h-4 w-4 text-muted-foreground" />}
              />
            </motion.div>
            <motion.div variants={item}>
              <StatsCard
                title="Editais Publicados"
                value="12"
                description="desde o último mês"
                trend="down"
                trendValue="-2%"
                progress={45}
                icon={<FileText className="h-4 w-4 text-muted-foreground" />}
              />
            </motion.div>
            <motion.div variants={item}>
              <StatsCard
                title="Prazos Próximos"
                value="8"
                description="nos próximos 7 dias"
                trend="up"
                trendValue="+3"
                progress={65}
                icon={<Clock className="h-4 w-4 text-muted-foreground" />}
              />
            </motion.div>
            <motion.div variants={item}>
              <StatsCard
                title="Taxa de Sucesso"
                value="64%"
                description="nas licitações"
                trend="up"
                trendValue="+12%"
                progress={64}
                icon={<BarChart3 className="h-4 w-4 text-muted-foreground" />}
              />
            </motion.div>
          </motion.div>
          
          <motion.div 
            className="grid gap-6 md:grid-cols-2 lg:grid-cols-7 mt-6"
            variants={container}
            initial="hidden"
            animate="show"
          >
            <motion.div variants={item} className="col-span-full lg:col-span-4">
              <Card className="h-full">
                <CardHeader>
                  <CardTitle>Visão Geral de Licitações</CardTitle>
                  <CardDescription>
                    Volume de licitações nos últimos 6 meses
                  </CardDescription>
                </CardHeader>
                <CardContent className="pl-2">
                  <div className="h-[300px] flex items-center justify-center">
                    <BarChart3 size={120} className="text-muted-foreground" />
                  </div>
                </CardContent>
              </Card>
            </motion.div>
            <motion.div variants={item} className="col-span-full lg:col-span-3">
              <Card className="h-full">
                <CardHeader>
                  <CardTitle>Resumo de Atividades</CardTitle>
                  <CardDescription>
                    Atividades recentes no sistema
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center">
                      <div className="w-9 h-9 rounded-full bg-primary/10 flex items-center justify-center mr-3">
                        <FileText className="h-5 w-5 text-primary" />
                      </div>
                      <div>
                        <p className="text-sm font-medium">Novo edital publicado</p>
                        <p className="text-xs text-muted-foreground">Há 2 horas</p>
                      </div>
                    </div>
                    <div className="flex items-center">
                      <div className="w-9 h-9 rounded-full bg-primary/10 flex items-center justify-center mr-3">
                        <Clock className="h-5 w-5 text-primary" />
                      </div>
                      <div>
                        <p className="text-sm font-medium">Prazo finalizado</p>
                        <p className="text-xs text-muted-foreground">Há 1 dia</p>
                      </div>
                    </div>
                    <div className="flex items-center">
                      <div className="w-9 h-9 rounded-full bg-primary/10 flex items-center justify-center mr-3">
                        <Activity className="h-5 w-5 text-primary" />
                      </div>
                      <div>
                        <p className="text-sm font-medium">Nova licitação disponível</p>
                        <p className="text-xs text-muted-foreground">Há 3 dias</p>
                      </div>
                    </div>
                    <div className="flex items-center">
                      <div className="w-9 h-9 rounded-full bg-primary/10 flex items-center justify-center mr-3">
                        <FileText className="h-5 w-5 text-primary" />
                      </div>
                      <div>
                        <p className="text-sm font-medium">Documento atualizado</p>
                        <p className="text-xs text-muted-foreground">Há 5 dias</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </motion.div>
        </TabsContent>
        <TabsContent value="analytics" className="h-[400px] flex items-center justify-center">
          <div className="text-center">
            <BarChart3 className="h-16 w-16 mx-auto text-muted-foreground" />
            <h3 className="text-xl font-semibold mt-4">Análises Avançadas</h3>
            <p className="text-muted-foreground max-w-md mx-auto mt-2">
              Módulo de análises detalhadas disponível na versão completa.
            </p>
          </div>
        </TabsContent>
        <TabsContent value="reports" className="h-[400px] flex items-center justify-center">
          <div className="text-center">
            <FileText className="h-16 w-16 mx-auto text-muted-foreground" />
            <h3 className="text-xl font-semibold mt-4">Relatórios</h3>
            <p className="text-muted-foreground max-w-md mx-auto mt-2">
              Geração de relatórios personalizados disponível na versão completa.
            </p>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default DashboardPage;
