
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2 } from 'lucide-react';

const loginSchema = z.object({
  email: z.string().email({ message: 'E-mail inválido' }),
  password: z.string().min(6, { message: 'A senha deve ter pelo menos 6 caracteres' }),
});

type LoginFormValues = z.infer<typeof loginSchema>;

/**
 * Login form component with validation and submission
 */
export const LoginForm = () => {
  const { login, isLoading, error, clearError } = useAuthStore();
  const navigate = useNavigate();
  const [showDemoAccounts, setShowDemoAccounts] = useState(false);
  
  const form = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });
  
  const onSubmit = async (data: LoginFormValues) => {
    clearError();
    await login(data.email, data.password);
    navigate('/app/dashboard');
  };
  
  const useDemoAccount = (type: 'admin' | 'user') => {
    form.setValue('email', type === 'admin' ? 'admin@example.com' : 'user@example.com');
    form.setValue('password', 'password');
    form.handleSubmit(onSubmit)();
  };
  
  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl text-center">Portal de Licitações</CardTitle>
        <CardDescription className="text-center">Entre com suas credenciais para acessar</CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
            
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>E-mail</FormLabel>
                  <FormControl>
                    <Input placeholder="seu@email.com" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Senha</FormLabel>
                  <FormControl>
                    <Input type="password" placeholder="******" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Entrando...
                </>
              ) : (
                'Entrar'
              )}
            </Button>
          </form>
        </Form>
        
        <div className="mt-4 text-center">
          <Button variant="link" onClick={() => setShowDemoAccounts(!showDemoAccounts)}>
            {showDemoAccounts ? 'Ocultar contas demo' : 'Mostrar contas demo'}
          </Button>
          
          {showDemoAccounts && (
            <div className="mt-2 space-y-2">
              <Button variant="outline" size="sm" className="w-full" onClick={() => useDemoAccount('admin')}>
                Acessar como Administrador
              </Button>
              <Button variant="outline" size="sm" className="w-full" onClick={() => useDemoAccount('user')}>
                Acessar como Usuário
              </Button>
            </div>
          )}
        </div>
      </CardContent>
      <CardFooter className="flex flex-col space-y-2">
        <div className="text-center text-sm">
          <Link to="/forgot-password" className="text-primary hover:underline">
            Esqueceu sua senha?
          </Link>
        </div>
        <div className="text-center text-sm">
          Não tem uma conta?{' '}
          <Link to="/signup" className="text-primary hover:underline">
            Cadastre-se
          </Link>
        </div>
        <div className="text-center text-sm">
          <Link to="/demo" className="text-primary hover:underline">
            Ver demonstração
          </Link>
        </div>
      </CardFooter>
    </Card>
  );
};
