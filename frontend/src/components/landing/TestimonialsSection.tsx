
import React from "react";
import { motion } from "framer-motion";
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from "@/components/ui/carousel";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Star } from "lucide-react";

interface TestimonialProps {
  id: number;
  name: string;
  quote: string;
  image: string;
  stars: number;
}

const testimonials: TestimonialProps[] = [
  {
    id: 1,
    name: "Construtora Silva Ltda.",
    quote: "Aumentamos nossa taxa de sucesso em licitações em 45% após começar a usar o CotAi.",
    image: "/images/construtora.jpg",
    stars: 5,
  },
  {
    id: 2,
    name: "Tecnologia Futuro S.A.",
    quote: "A análise automática de editais nos permite participar de 3x mais licitações com a mesma equipe.",
    image: "/images/tecnologia.jpg",
    stars: 5,
  },
  {
    id: 3,
    name: "Serviços Integrados ME",
    quote: "O suporte da equipe CotAi fez toda a diferença na nossa adaptação ao sistema de licitações eletrônicas.",
    image: "/images/servicos.jpg",
    stars: 4,
  },
];

const TestimonialsSection: React.FC = () => {
  return (
    <section className="py-16 px-6 bg-background">
      <div className="max-w-7xl mx-auto">
        <motion.h2
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-3xl font-bold text-center mb-12"
        >
          Casos de Sucesso
        </motion.h2>

        <Carousel className="w-full">
          <CarouselContent>
            {testimonials.map((testimonial) => (
              <CarouselItem key={testimonial.id} className="md:basis-1/2 lg:basis-1/3">
                <div className="p-1 h-full">
                  <Card className="h-full flex flex-col">
                    <div className="relative w-full h-48">
                      <img
                        src={testimonial.image}
                        alt={testimonial.name}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          const target = e.target as HTMLImageElement;
                          target.src = `https://placehold.co/600x200/3f3f46/FFFFFF?text=${testimonial.name.replace(/ /g, '+')}`;
                        }}
                      />
                      <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black to-transparent h-1/2" />
                    </div>
                    <CardHeader>
                      <CardTitle className="text-xl">{testimonial.name}</CardTitle>
                      <div className="flex">
                        {Array(testimonial.stars).fill(0).map((_, i) => (
                          <Star key={i} className="h-4 w-4 fill-primary text-primary" />
                        ))}
                      </div>
                    </CardHeader>
                    <CardContent className="flex-grow">
                      <p className="italic">"{testimonial.quote}"</p>
                    </CardContent>
                    <CardFooter>
                      <Button variant="outline" size="sm" className="w-full">
                        Ver Caso Completo
                      </Button>
                    </CardFooter>
                  </Card>
                </div>
              </CarouselItem>
            ))}
          </CarouselContent>
          <CarouselPrevious className="left-2 -translate-y-1/2" />
          <CarouselNext className="right-2 -translate-y-1/2" />
        </Carousel>
      </div>
    </section>
  );
};

export default TestimonialsSection;
