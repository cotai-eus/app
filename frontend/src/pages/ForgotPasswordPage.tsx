
import { ForgotPasswordForm } from '@/components/auth/ForgotPasswordForm';
import { motion } from 'framer-motion';

/**
 * Forgot password page component
 */
const ForgotPasswordPage = () => {
  return (
    <motion.div 
      className="min-h-screen flex flex-col items-center justify-center p-4 bg-background"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      <ForgotPasswordForm />
    </motion.div>
  );
};

export default ForgotPasswordPage;
