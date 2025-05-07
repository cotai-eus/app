
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, BarChart, FileText, Calendar, Bell } from 'lucide-react';

/**
 * Demo page component showing a limited version of the dashboard
 */
const DemoPage = () => {
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
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="container mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-2">
            <Link to="/">
              <Button variant="ghost" size="icon">
                <ArrowLeft className="h-5 w-5" />
              </Button>
            </Link>
            <h1 className="text-2xl font-bold">Demonstração do Portal de Licitações</h1>
          </div>
          <div>
            <Link to="/login">
              <Button>Acessar Portal Completo</Button>
            </Link>
          </div>
        </div>

        <Tabs defaultValue="overview" className="mb-6">
          <TabsList>
            <TabsTrigger value="overview">Visão Geral</TabsTrigger>
            <TabsTrigger value="licitacoes">Licitações</TabsTrigger>
            <TabsTrigger value="editais">Editais</TabsTrigger>
          </TabsList>
          <TabsContent value="overview">
            <motion.div 
              variants={container}
              initial="hidden"
              animate="show"
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            >
              <motion.div variants={item}>
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">
                      Licitações Ativas
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold">12</div>
                    <p className="text-xs text-muted-foreground">
                      +2 desde o mês passado
                    </p>
                    <Progress value={45} className="h-1 mt-3" />
                  </CardContent>
                </Card>
              </motion.div>
              <motion.div variants={item}>
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">
                      Editais Disponíveis
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold">8</div>
                    <p className="text-xs text-muted-foreground">
                      +3 desde o mês passado
                    </p>
                    <Progress value={65} className="h-1 mt-3" />
                  </CardContent>
                </Card>
              </motion.div>
              <motion.div variants={item}>
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">
                      Eventos Próximos
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold">4</div>
                    <p className="text-xs text-muted-foreground">
                      Esta semana
                    </p>
                    <Progress value={35} className="h-1 mt-3" />
                  </CardContent>
                </Card>
              </motion.div>

              <motion.div variants={item} className="md:col-span-2">
                <Card>
                  <CardHeader>
                    <CardTitle>Relatório de Atividades</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="h-60 flex items-center justify-center">
                      <BarChart size={120} className="text-muted-foreground" />
                      <p className="text-center text-muted-foreground">
                        Dados detalhados disponíveis na versão completa
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>

              <motion.div variants={item}>
                <Card>
                  <CardHeader>
                    <CardTitle>Notificações</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-start space-x-3">
                      <Bell className="h-4 w-4 text-primary mt-1" />
                      <div>
                        <p className="text-sm font-medium">Novo edital disponível</p>
                        <p className="text-xs text-muted-foreground">10 minutos atrás</p>
                      </div>
                    </div>
                    <div className="flex items-start space-x-3">
                      <Calendar className="h-4 w-4 text-primary mt-1" />
                      <div>
                        <p className="text-sm font-medium">Prazo se aproximando</p>
                        <p className="text-xs text-muted-foreground">3 dias restantes</p>
                      </div>
                    </div>
                    <div className="flex items-start space-x-3">
                      <FileText className="h-4 w-4 text-primary mt-1" />
                      <div>
                        <p className="text-sm font-medium">Documento atualizado</p>
                        <p className="text-xs text-muted-foreground">Ontem</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </motion.div>
          </TabsContent>
          <TabsContent value="licitacoes">
            <Card>
              <CardHeader>
                <CardTitle>Licitações Disponíveis - Demonstração</CardTitle>
              </CardHeader>
              <CardContent className="text-center py-12">
                <FileText size={60} className="mx-auto text-muted-foreground mb-4" />
                <h3 className="text-xl font-semibold mb-2">Acesso Restrito</h3>
                <p className="text-muted-foreground mb-6">
                  Os dados completos de licitações estão disponíveis apenas para usuários autenticados.
                </p>
                <Link to="/login">
                  <Button>Fazer Login para Acessar</Button>
                </Link>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="editais">
            <Card>
              <CardHeader>
                <CardTitle>Editais Públicos - Demonstração</CardTitle>
              </CardHeader>
              <CardContent className="text-center py-12">
                <FileText size={60} className="mx-auto text-muted-foreground mb-4" />
                <h3 className="text-xl font-semibold mb-2">Acesso Restrito</h3>
                <p className="text-muted-foreground mb-6">
                  Os editais completos estão disponíveis apenas para usuários autenticados.
                </p>
                <Link to="/login">
                  <Button>Fazer Login para Acessar</Button>
                </Link>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        <Card className="mt-8 bg-primary-foreground">
          <CardContent className="p-6">
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-2">Desbloqueie Todos os Recursos</h2>
              <p className="text-muted-foreground mb-6">
                Esta é apenas uma demonstração limitada. Registre-se para acessar todas as funcionalidades.
              </p>
              <div className="flex justify-center space-x-4">
                <Link to="/signup">
                  <Button>Criar Conta</Button>
                </Link>
                <Link to="/login">
                  <Button variant="outline">Fazer Login</Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default DemoPage;
