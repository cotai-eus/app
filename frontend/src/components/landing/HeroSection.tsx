
import React from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from "@/components/ui/carousel";
import { AspectRatio } from "@/components/ui/aspect-ratio";
import { Card } from "@/components/ui/card";

interface StepProps {
  id: string;
  title: string;
  icon: React.ReactNode;
}

const processSteps: StepProps[] = [
  { id: "01", title: "Em andamento", icon: <LineChart className="h-6 w-6" /> },
  { id: "02", title: "Análise de editais", icon: <FileText className="h-6 w-6" /> },
  { id: "03", title: "Extração de requisitos", icon: <Brain className="h-6 w-6" /> },
  { id: "04", title: "Geração de proposta", icon: <Send className="h-6 w-6" /> },
  { id: "05", title: "Submissão da documentação", icon: <CheckCircle className="h-6 w-6" /> },
];

const heroImages = [
  "/images/hero-1.jpg",
  "/images/hero-2.jpg",
  "/images/hero-3.jpg",
];

import { LineChart, FileText, Brain, Send, CheckCircle } from "lucide-react";

const HeroSection: React.FC = () => {
  return (
    <section className="bg-background py-16 px-6">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-left"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
            Transforme sua gestão de licitações com IA CotAi
          </h1>
          <p className="text-xl text-muted-foreground mb-8">
            Licitação Hub automatiza a análise de editais e geração de propostas, economizando seu tempo e maximizando suas chances de sucesso.
          </p>
          <div className="flex flex-wrap gap-4">
            <Button asChild size="lg" className="hover-glow">
              <Link to="/demo/dashboard">
                Ver Demonstração
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button variant="outline" asChild size="lg">
              <Link to="/signup">Criar Conta</Link>
            </Button>
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="space-y-6"
        >
          <Carousel className="w-full">
            <CarouselContent>
              {heroImages.map((image, index) => (
                <CarouselItem key={index}>
                  <div className="p-1">
                    <Card className="overflow-hidden border border-border">
                      <AspectRatio ratio={16/9}>
                        <div className="bg-muted/30 w-full h-full flex items-center justify-center">
                          <img
                            src={image}
                            alt={`Exemplo de uso da plataforma ${index + 1}`}
                            className="w-full h-full object-cover"
                            onError={(e) => {
                              const target = e.target as HTMLImageElement;
                              target.src = "https://placehold.co/600x400/3f3f46/FFFFFF?text=CotAi+Licitação+Hub";
                            }}
                          />
                        </div>
                      </AspectRatio>
                    </Card>
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious className="lg:left-2 -left-4" />
            <CarouselNext className="lg:right-2 -right-4" />
          </Carousel>

          <div className="bg-card p-6 rounded-xl shadow-lg border border-border">
            <h3 className="text-xl font-semibold mb-4 text-center">Dashboard de Licitações</h3>
            <div className="space-y-4">
              {processSteps.map((step) => (
                <div key={step.id} className="flex items-center p-3 bg-muted/50 rounded-lg">
                  <div className="flex items-center justify-center h-10 w-10 rounded-full bg-primary/10 text-primary mr-4">
                    {step.icon}
                  </div>
                  <div>
                    <p className="font-medium">{step.title}</p>
                    <p className="text-sm text-muted-foreground">{step.id}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default HeroSection;
