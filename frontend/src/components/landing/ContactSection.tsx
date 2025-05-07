
import React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { MessageSquare, Calendar } from "lucide-react";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from "@/components/ui/form";
import { useForm } from "react-hook-form";

type ContactFormValues = {
  name: string;
  email: string;
  message: string;
};

const ContactSection: React.FC = () => {
  const form = useForm<ContactFormValues>();

  const onSubmit = (data: ContactFormValues) => {
    console.log(data);
    // Here would go the contact form submission logic
  };

  return (
    <section className="bg-background py-16 px-6">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12">
        <div>
          <h2 className="text-3xl font-bold mb-6">Entre em Contato</h2>
          <p className="mb-8">
            Estamos aqui para responder suas dúvidas e ajudar sua empresa a conquistar mais contratos públicos.
          </p>
          
          <div className="space-y-4">
            <div className="flex items-center">
              <MessageSquare className="h-5 w-5 mr-3" />
              <a href="https://telegram.org" target="_blank" rel="noreferrer" className="hover:underline">
                Telegram: @CotAiLicitacoes
              </a>
            </div>
            <div className="flex items-center">
              <MessageSquare className="h-5 w-5 mr-3" />
              <a href="https://whatsapp.com" target="_blank" rel="noreferrer" className="hover:underline">
                WhatsApp: +55 11 98765-4321
              </a>
            </div>
            <div className="flex items-center">
              <Calendar className="h-5 w-5 mr-3" />
              <a href="mailto:contato@cotai.com.br" className="hover:underline">
                Email: contato@cotai.com.br
              </a>
            </div>
          </div>
        </div>
        
        <div>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Nome</FormLabel>
                    <FormControl>
                      <Input placeholder="Seu nome" {...field} />
                    </FormControl>
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
                      <Input placeholder="seu-email@exemplo.com" {...field} />
                    </FormControl>
                  </FormItem>
                )}
              />
              
              <FormField
                control={form.control}
                name="message"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Mensagem</FormLabel>
                    <FormControl>
                      <Textarea placeholder="Como podemos ajudar?" {...field} className="min-h-[120px]" />
                    </FormControl>
                  </FormItem>
                )}
              />
              
              <Button type="submit" className="w-full hover-glow">Enviar Mensagem</Button>
            </form>
          </Form>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;
