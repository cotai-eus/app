
import { useTranslation } from 'react-i18next';
import { format as formatDate } from 'date-fns';
import { ptBR } from 'date-fns/locale';

export const useI18n = () => {
  const { t } = useTranslation();
  
  // Format date according to Brazilian format
  const formatDateBR = (date: Date | string | number): string => {
    const dateObj = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date;
    return formatDate(dateObj, 'dd/MM/yyyy', { locale: ptBR });
  };
  
  // Format date and time according to Brazilian format
  const formatDateTimeBR = (date: Date | string | number): string => {
    const dateObj = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date;
    return formatDate(dateObj, 'dd/MM/yyyy HH:mm', { locale: ptBR });
  };
  
  // Format currency according to Brazilian format
  const formatCurrency = (value: number): string => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value);
  };
  
  return {
    t,
    formatDateBR,
    formatDateTimeBR,
    formatCurrency,
  };
};
