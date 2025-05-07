
import { LoginForm } from '@/components/auth/LoginForm';
import { motion } from 'framer-motion';

/**
 * Login page component
 */
const LoginPage = () => {
  return (
    <motion.div 
      className="min-h-screen flex flex-col items-center justify-center p-4 bg-background"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      <LoginForm />
    </motion.div>
  );
};

export default LoginPage;
