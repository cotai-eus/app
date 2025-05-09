
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Import translations
import ptBR from './locales/pt-BR';

// Configure i18next
i18n
  .use(initReactI18next)
  .init({
    resources: {
      'pt-BR': ptBR,
    },
    lng: 'pt-BR',
    fallbackLng: 'pt-BR',
    interpolation: {
      escapeValue: false, // React already escapes values
    },
  });

export default i18n;
