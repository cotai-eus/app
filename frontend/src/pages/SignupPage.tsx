
import { RegisterForm } from '@/components/auth/RegisterForm';
import { motion } from 'framer-motion';

/**
 * Signup page component
 */
const SignupPage = () => {
  return (
    <motion.div 
      className="min-h-screen flex flex-col items-center justify-center p-4 bg-background"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      <RegisterForm />
    </motion.div>
  );
};

export default SignupPage;
