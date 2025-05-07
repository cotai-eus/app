
import React from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FileText, Brain, LineChart, Clock } from "lucide-react";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2,
    },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

interface FeatureProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  image: string;
}

const features: FeatureProps[] = [
  {
    title: "Análise Rápida de Editais",
    description: "Nossa IA analisa os editais em segundos, extraindo todos os requisitos e informações importantes.",
    icon: <FileText className="h-8 w-8 text-primary" />,
    image: "/images/analise-editais.jpg",
  },
  {
    title: "Geração Inteligente de Propostas",
    description: "Propostas personalizadas que atendem a todos os requisitos do edital, aumentando suas chances de sucesso.",
    icon: <Brain className="h-8 w-8 text-primary" />,
    image: "/images/proposta-inteligente.jpg",
  },
  {
    title: "Monitoramento Proativo",
    description: "Acompanhamento em tempo real dos prazos e status de cada licitação em andamento.",
    icon: <LineChart className="h-8 w-8 text-primary" />,
    image: "/images/monitoramento.jpg",
  },
  {
    title: "Economia de Tempo",
    description: "Reduza em até 70% o tempo gasto na análise de editais e preparação de propostas.",
    icon: <Clock className="h-8 w-8 text-primary" />,
    image: "/images/economia-tempo.jpg",
  },
];

const FeaturesSection: React.FC = () => {
  return (
    <section className="bg-muted py-16 px-6">
      <div className="max-w-7xl mx-auto">
        <motion.h2
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-3xl font-bold text-center mb-12"
        >
          Recursos que Transformam sua Participação em Licitações
        </motion.h2>

        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 md:grid-cols-2 gap-8"
        >
          {features.map((feature, index) => (
            <motion.div
              key={index}
              variants={item}
              className="hover-scale"
            >
              <Card className="h-full overflow-hidden">
                <div className="relative w-full h-48">
                  <img
                    src={feature.image}
                    alt={feature.title}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.src = `https://placehold.co/600x200/3f3f46/FFFFFF?text=${feature.title.replace(/ /g, '+')}`;
                    }}
                  />
                  <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-t from-black/50 to-transparent" />
                </div>
                <CardHeader>
                  <div className="mb-4">{feature.icon}</div>
                  <CardTitle>{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>{feature.description}</p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default FeaturesSection;
