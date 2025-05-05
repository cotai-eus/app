import { useToast } from "@/hooks/use-toast";

// No componente
const { toast } = useToast();

// Para mostrar uma notificação
toast({
  title: "Sucesso",
  description: "Operação realizada com sucesso",
});