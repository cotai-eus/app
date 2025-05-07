
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Calendar, LayoutDashboard, FileText, Mail, CheckCircle, Users } from 'lucide-react';
import { ThemeToggle } from '@/components/theme/ThemeToggle';

/**
 * Landing page component
 */
const LandingPage = () => {
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
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border">
        <div className="container mx-auto py-4 px-4 md:px-6 lg:px-8 flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold">
            Portal Licitações
          </Link>
          
          <div className="flex items-center gap-4">
            <ThemeToggle />
            <Link to="/login">
              <Button variant="outline">Entrar</Button>
            </Link>
            <Link to="/signup">
              <Button>Cadastre-se</Button>
            </Link>
          </div>
        </div>
      </header>
      
      {/* Hero section */}
      <motion.section 
        className="py-16 md:py-24 container mx-auto px-4 md:px-6 lg:px-8"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6 }}
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div>
            <motion.h1 
              className="text-4xl md:text-5xl font-bold leading-tight"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
            >
              Gerencie suas licitações com eficiência e organização
            </motion.h1>
            <motion.p 
              className="text-xl text-muted-foreground mt-4 mb-8"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              Plataforma completa para empresas brasileiras gerenciarem todo o ciclo de licitações públicas.
            </motion.p>
            <motion.div 
              className="flex flex-wrap gap-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              <Link to="/signup">
                <Button size="lg">Comece Agora</Button>
              </Link>
              <Link to="/demo">
                <Button variant="outline" size="lg">Ver Demonstração</Button>
              </Link>
            </motion.div>
          </div>
          
          <motion.div
            className="relative"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="aspect-video border border-border rounded-xl overflow-hidden shadow-lg bg-card">
              <div className="grid grid-cols-3 h-full">
                <div className="col-span-1 bg-primary/10 border-r border-border flex items-center justify-center">
                  <div className="flex flex-col items-center space-y-6 p-4">
                    <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center">
                      <LayoutDashboard className="h-6 w-6 text-primary" />
                    </div>
                    <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center">
                      <FileText className="h-6 w-6 text-primary" />
                    </div>
                    <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center">
                      <Calendar className="h-6 w-6 text-primary" />
                    </div>
                    <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center">
                      <Mail className="h-6 w-6 text-primary" />
                    </div>
                  </div>
                </div>
                <div className="col-span-2 p-4 flex flex-col">
                  <div className="text-xl font-semibold mb-4">Dashboard</div>
                  <div className="grid grid-cols-2 gap-3 mb-4">
                    <div className="bg-muted rounded-md p-3">
                      <div className="text-sm font-medium">Licitações</div>
                      <div className="text-2xl font-bold">24</div>
                    </div>
                    <div className="bg-muted rounded-md p-3">
                      <div className="text-sm font-medium">Editais</div>
                      <div className="text-2xl font-bold">12</div>
                    </div>
                    <div className="bg-muted rounded-md p-3">
                      <div className="text-sm font-medium">Prazos</div>
                      <div className="text-2xl font-bold">8</div>
                    </div>
                    <div className="bg-muted rounded-md p-3">
                      <div className="text-sm font-medium">Sucesso</div>
                      <div className="text-2xl font-bold">64%</div>
                    </div>
                  </div>
                  <div className="flex-1 bg-muted rounded-md p-3">
                    <div className="h-20 flex items-center justify-center">
                      <div className="w-full bg-primary/20 h-8 rounded-md" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="absolute -bottom-5 -right-5 bg-primary text-primary-foreground px-4 py-2 rounded-lg shadow-lg">
              Interface intuitiva e moderna
            </div>
          </motion.div>
        </div>
      </motion.section>
      
      {/* Features section */}
      <motion.section 
        className="py-16 bg-muted/50"
        variants={container}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true }}
      >
        <div className="container mx-auto px-4 md:px-6 lg:px-8">
          <motion.h2 
            className="text-3xl font-bold text-center mb-12"
            variants={item}
          >
            Funcionalidades Principais
          </motion.h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <motion.div variants={item}>
              <Card className="h-full">
                <CardHeader>
                  <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                    <LayoutDashboard className="h-6 w-6 text-primary" />
                  </div>
                  <CardTitle>Dashboard Completo</CardTitle>
                  <CardDescription>
                    Visualize todas as métricas importantes em um só lugar.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    <li className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-primary mr-2" />
                      <span className="text-sm">Indicadores de performance</span>
                    </li>
                    <li className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-primary mr-2" />
                      <span className="text-sm">Gráficos interativos</span>
                    </li>
                    <li className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-primary mr-2" />
                      <span className="text-sm">Resumo de atividades</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
            </motion.div>
            
            <motion.div variants={item}>
              <Card className="h-full">
                <CardHeader>
                  <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                    <FileText className="h-6 w-6 text-primary" />
                  </div>
                  <CardTitle>Gestão de Editais</CardTitle>
                  <CardDescription>
                    Organize e acompanhe todos os editais e documentos.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    <li className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-primary mr-2" />
                      <span className="text-sm">Upload de documentos</span>
                    </li>
                    <li className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-primary mr-2" />
                      <span className="text-sm">Versionamento de arquivos</span>
                    </li>
                    <li className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-primary mr-2" />
                      <span className="text-sm">Categorização inteligente</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
            </motion.div>
            
            <motion.div variants={item}>
              <Card className="h-full">
                <CardHeader>
                  <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                    <Calendar className="h-6 w-6 text-primary" />
                  </div>
                  <CardTitle>Calendário de Prazos</CardTitle>
                  <CardDescription>
                    Nunca perca um prazo importante novamente.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    <li className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-primary mr-2" />
                      <span className="text-sm">Notificações automáticas</span>
                    </li>
                    <li className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-primary mr-2" />
                      <span className="text-sm">Visualização mensal e semanal</span>
                    </li>
                    <li className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-primary mr-2" />
                      <span className="text-sm">Priorização por importância</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
            </motion.div>
            
            <motion.div variants={item}>
              <Card className="h-full">
                <CardHeader>
                  <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                    <Mail className="h-6 w-6 text-primary" />
                  </div>
                  <CardTitle>Mensagens Internas</CardTitle>
                  <CardDescription>
                    Comunique-se com sua equipe de forma eficiente.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    <li className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-primary mr-2" />
                      <span className="text-sm">Chat em tempo real</span>
                    </li>
                    <li className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-primary mr-2" />
                      <span className="text-sm">Compartilhamento de arquivos</span>
                    </li>
                    <li className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-primary mr-2" />
                      <span className="text-sm">Grupos por projeto ou tema</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </motion.section>
      
      {/* CTA section */}
      <motion.section 
        className="py-16 md:py-24 container mx-auto px-4 md:px-6 lg:px-8"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
      >
        <div className="bg-primary-foreground rounded-2xl p-8 md:p-12">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Pronto para simplificar sua gestão de licitações?
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Comece agora mesmo a organizar seus processos e aumente suas chances de sucesso em licitações.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link to="/signup">
                <Button size="lg">Criar Conta Grátis</Button>
              </Link>
              <Link to="/demo">
                <Button variant="outline" size="lg">Ver Demonstração</Button>
              </Link>
            </div>
          </div>
        </div>
      </motion.section>
      
      {/* Testimonials section */}
      <motion.section 
        className="py-16 bg-muted/50"
        variants={container}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true }}
      >
        <div className="container mx-auto px-4 md:px-6 lg:px-8">
          <motion.h2 
            className="text-3xl font-bold text-center mb-12"
            variants={item}
          >
            O que nossos clientes dizem
          </motion.h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <motion.div variants={item}>
              <Card className="h-full">
                <CardContent className="pt-6">
                  <div className="flex items-center mb-4">
                    <div className="mr-4">
                      <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center">
                        <Users className="h-6 w-6 text-primary" />
                      </div>
                    </div>
                    <div>
                      <p className="font-medium">Maria Silva</p>
                      <p className="text-sm text-muted-foreground">Construtora ABC</p>
                    </div>
                  </div>
                  <p className="italic">
                    "O Portal de Licitações revolucionou a forma como gerenciamos nossos processos. Economizamos tempo e aumentamos nossa eficiência significativamente."
                  </p>
                </CardContent>
              </Card>
            </motion.div>
            
            <motion.div variants={item}>
              <Card className="h-full">
                <CardContent className="pt-6">
                  <div className="flex items-center mb-4">
                    <div className="mr-4">
                      <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center">
                        <Users className="h-6 w-6 text-primary" />
                      </div>
                    </div>
                    <div>
                      <p className="font-medium">João Costa</p>
                      <p className="text-sm text-muted-foreground">Tech Solutions</p>
                    </div>
                  </div>
                  <p className="italic">
                    "O sistema de calendário e notificações nos ajudou a nunca mais perder um prazo importante. A interface é intuitiva e fácil de usar."
                  </p>
                </CardContent>
              </Card>
            </motion.div>
            
            <motion.div variants={item}>
              <Card className="h-full">
                <CardContent className="pt-6">
                  <div className="flex items-center mb-4">
                    <div className="mr-4">
                      <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center">
                        <Users className="h-6 w-6 text-primary" />
                      </div>
                    </div>
                    <div>
                      <p className="font-medium">Ana Oliveira</p>
                      <p className="text-sm text-muted-foreground">Suprimentos SA</p>
                    </div>
                  </div>
                  <p className="italic">
                    "Desde que começamos a utilizar o Portal de Licitações, nossa taxa de sucesso em licitações públicas aumentou em mais de 30%."
                  </p>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </motion.section>
      
      {/* Footer */}
      <footer className="border-t border-border py-12">
        <div className="container mx-auto px-4 md:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-lg font-bold mb-4">Portal Licitações</h3>
              <p className="text-muted-foreground">
                Plataforma completa para gestão de licitações públicas para empresas brasileiras.
              </p>
            </div>
            
            <div>
              <h4 className="font-medium mb-4">Recursos</h4>
              <ul className="space-y-2">
                <li>
                  <Link to="/demo" className="text-muted-foreground hover:text-foreground transition-colors">
                    Demonstração
                  </Link>
                </li>
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-colors">
                    Funcionalidades
                  </Link>
                </li>
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-colors">
                    Planos
                  </Link>
                </li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium mb-4">Suporte</h4>
              <ul className="space-y-2">
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-colors">
                    FAQ
                  </Link>
                </li>
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-colors">
                    Contato
                  </Link>
                </li>
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-colors">
                    Tutoriais
                  </Link>
                </li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium mb-4">Legal</h4>
              <ul className="space-y-2">
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-colors">
                    Termos de Uso
                  </Link>
                </li>
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-colors">
                    Política de Privacidade
                  </Link>
                </li>
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-colors">
                    Segurança
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-border mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-muted-foreground">
              © 2023 Portal Licitações. Todos os direitos reservados.
            </p>
            <div className="flex items-center mt-4 md:mt-0">
              <ThemeToggle />
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
