
import React from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { AspectRatio } from "@/components/ui/aspect-ratio";
import { Button } from "@/components/ui/button";
import { Award, TrendingUp, ImagePlus, Users } from "lucide-react";

const AboutSection: React.FC = () => {
  return (
    <section className="py-16 px-6 bg-muted">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="overflow-hidden rounded-lg shadow-lg"
          >
            <AspectRatio ratio={4/3}>
              <img
                src="/images/quem-somos.jpg"
                alt="Equipe CotAi"
                className="w-full h-full object-cover"
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.src = "https://placehold.co/800x600/3f3f46/FFFFFF?text=Nossa+Equipe";
                }}
              />
            </AspectRatio>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <h2 className="text-3xl font-bold mb-6">Quem Somos</h2>
            <p className="text-lg mb-6">
              A CotAi é uma empresa especializada em soluções de inteligência artificial para o setor 
              de licitações públicas. Nossa missão é democratizar o acesso às oportunidades de 
              negócios com o setor público, fornecendo ferramentas avançadas que simplificam processos 
              complexos e aumentam as chances de sucesso de empresas de todos os portes.
            </p>
            
            <div className="grid grid-cols-2 gap-4 mb-8">
              <div className="flex items-center gap-2">
                <Award className="h-5 w-5 text-primary" />
                <span>+500 clientes</span>
              </div>
              <div className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-primary" />
                <span>+30% taxa de sucesso</span>
              </div>
              <div className="flex items-center gap-2">
                <ImagePlus className="h-5 w-5 text-primary" />
                <span>+5000 editais analisados</span>
              </div>
              <div className="flex items-center gap-2">
                <Users className="h-5 w-5 text-primary" />
                <span>Equipe especializada</span>
              </div>
            </div>
            
            <Button variant="outline" asChild>
              <Link to="/sobre">Saiba Mais</Link>
            </Button>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
