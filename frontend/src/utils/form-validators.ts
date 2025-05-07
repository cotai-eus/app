
/**
 * Utilitários para formatação e validação de formulários
 * 
 * Este arquivo contém funções para formatar e validar campos comuns
 * em formulários brasileiros, como CPF, CNPJ, telefones, etc.
 */

/**
 * Formata um CPF inserindo as máscaras
 * @param cpf CPF sem formatação
 * @returns CPF formatado (000.000.000-00)
 */
export const formatCpf = (cpf: string): string => {
  const numbers = cpf.replace(/\D/g, '').slice(0, 11);
  if (numbers.length <= 3) return numbers;
  if (numbers.length <= 6) return `${numbers.slice(0, 3)}.${numbers.slice(3)}`;
  if (numbers.length <= 9) return `${numbers.slice(0, 3)}.${numbers.slice(3, 6)}.${numbers.slice(6)}`;
  return `${numbers.slice(0, 3)}.${numbers.slice(3, 6)}.${numbers.slice(6, 9)}-${numbers.slice(9, 11)}`;
};

/**
 * Formata um CNPJ inserindo as máscaras
 * @param cnpj CNPJ sem formatação
 * @returns CNPJ formatado (00.000.000/0000-00)
 */
export const formatCnpj = (cnpj: string): string => {
  const numbers = cnpj.replace(/\D/g, '').slice(0, 14);
  if (numbers.length <= 2) return numbers;
  if (numbers.length <= 5) return `${numbers.slice(0, 2)}.${numbers.slice(2)}`;
  if (numbers.length <= 8) return `${numbers.slice(0, 2)}.${numbers.slice(2, 5)}.${numbers.slice(5)}`;
  if (numbers.length <= 12) return `${numbers.slice(0, 2)}.${numbers.slice(2, 5)}.${numbers.slice(5, 8)}/${numbers.slice(8)}`;
  return `${numbers.slice(0, 2)}.${numbers.slice(2, 5)}.${numbers.slice(5, 8)}/${numbers.slice(8, 12)}-${numbers.slice(12, 14)}`;
};

/**
 * Formata um telefone inserindo as máscaras
 * @param telefone Telefone sem formatação
 * @returns Telefone formatado ((00) 00000-0000)
 */
export const formatTelefone = (telefone: string): string => {
  const numbers = telefone.replace(/\D/g, '').slice(0, 11);
  if (numbers.length <= 2) return `(${numbers}`;
  if (numbers.length <= 7) return `(${numbers.slice(0, 2)}) ${numbers.slice(2)}`;
  return `(${numbers.slice(0, 2)}) ${numbers.slice(2, 7)}-${numbers.slice(7)}`;
};

/**
 * Valida um CPF
 * @param cpf CPF com ou sem formatação
 * @returns true se o CPF é válido, false caso contrário
 */
export const validarCpf = (cpf: string): boolean => {
  const cleaned = cpf.replace(/\D/g, '');
  
  if (cleaned.length !== 11) return false;
  
  // Verificar se todos os dígitos são iguais
  if (/^(\d)\1+$/.test(cleaned)) return false;
  
  // Validar dígitos verificadores
  let sum = 0;
  for (let i = 0; i < 9; i++) {
    sum += parseInt(cleaned.charAt(i)) * (10 - i);
  }
  
  let remainder = sum % 11;
  const digit1 = remainder < 2 ? 0 : 11 - remainder;
  
  if (parseInt(cleaned.charAt(9)) !== digit1) return false;
  
  sum = 0;
  for (let i = 0; i < 10; i++) {
    sum += parseInt(cleaned.charAt(i)) * (11 - i);
  }
  
  remainder = sum % 11;
  const digit2 = remainder < 2 ? 0 : 11 - remainder;
  
  return parseInt(cleaned.charAt(10)) === digit2;
};

/**
 * Valida um CNPJ
 * @param cnpj CNPJ com ou sem formatação
 * @returns true se o CNPJ é válido, false caso contrário
 */
export const validarCnpj = (cnpj: string): boolean => {
  const cleaned = cnpj.replace(/\D/g, '');
  
  if (cleaned.length !== 14) return false;
  
  // Verificar se todos os dígitos são iguais
  if (/^(\d)\1+$/.test(cleaned)) return false;
  
  // Cálculo do primeiro dígito verificador
  let sum = 0;
  let weight = 5;
  for (let i = 0; i < 12; i++) {
    sum += parseInt(cleaned.charAt(i)) * weight;
    weight = weight === 2 ? 9 : weight - 1;
  }
  
  let remainder = sum % 11;
  const digit1 = remainder < 2 ? 0 : 11 - remainder;
  
  if (parseInt(cleaned.charAt(12)) !== digit1) return false;
  
  // Cálculo do segundo dígito verificador
  sum = 0;
  weight = 6;
  for (let i = 0; i < 13; i++) {
    sum += parseInt(cleaned.charAt(i)) * weight;
    weight = weight === 2 ? 9 : weight - 1;
  }
  
  remainder = sum % 11;
  const digit2 = remainder < 2 ? 0 : 11 - remainder;
  
  return parseInt(cleaned.charAt(13)) === digit2;
};

/**
 * Formata a data para o formato brasileiro
 * @param date Data a ser formatada
 * @returns Data formatada (DD/MM/YYYY)
 */
export const formatDateBR = (date: Date): string => {
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(date);
};

/**
 * Formata a data e hora para o formato brasileiro
 * @param date Data a ser formatada
 * @returns Data e hora formatadas (DD/MM/YYYY HH:mm)
 */
export const formatDateTimeBR = (date: Date): string => {
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

/**
 * Formata um valor monetário para o formato brasileiro
 * @param value Valor a ser formatado
 * @returns Valor formatado (R$ 0.000,00)
 */
export const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);
};
