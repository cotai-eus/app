
export default {
  translation: {
    // Common
    common: {
      save: 'Salvar',
      cancel: 'Cancelar',
      edit: 'Editar',
      delete: 'Excluir',
      close: 'Fechar',
      loading: 'Carregando...',
      search: 'Buscar',
      copy: 'Copiar',
      copied: 'Copiado!',
      error: 'Erro',
      success: 'Sucesso',
      required: 'Este campo é obrigatório',
      invalidFormat: 'Formato inválido',
      confirmAction: 'Confirmar ação',
    },
    
    // Auth
    auth: {
      login: 'Entrar',
      logout: 'Sair',
      register: 'Cadastrar',
      email: 'E-mail',
      password: 'Senha',
      forgotPassword: 'Esqueceu a senha?',
      resetPassword: 'Redefinir senha',
      confirmPassword: 'Confirmar senha',
      name: 'Nome',
      loginError: 'E-mail ou senha inválidos',
      invalidEmail: 'E-mail inválido',
      passwordsMustMatch: 'As senhas não coincidem',
      passwordMinLength: 'A senha deve ter no mínimo 6 caracteres',
      resetEmailSent: 'E-mail de redefinição enviado',
    },
    
    // Navigation
    nav: {
      dashboard: 'Dashboard',
      kanban: 'Kanban',
      editais: 'Editais',
      mensagens: 'Mensagens',
      calendario: 'Calendário',
      profile: 'Perfil',
      settings: 'Configurações',
    },
    
    // Profile
    profile: {
      personalInfo: 'Informações Pessoais',
      companyInfo: 'Informações da Empresa',
      updateSuccess: 'Perfil atualizado com sucesso',
      updateFailed: 'Falha ao atualizar perfil',
      cpf: 'CPF',
      cnpj: 'CNPJ',
      phone: 'Telefone',
      address: 'Endereço',
      uploadAvatar: 'Enviar foto',
      changeAvatar: 'Alterar foto',
      removeAvatar: 'Remover foto',
    },
    
    // Settings
    settings: {
      appearance: 'Aparência',
      notifications: 'Notificações',
      security: '2FA e Segurança',
      api: 'API e Integrações',
      theme: {
        title: 'Tema',
        light: 'Claro',
        dark: 'Escuro',
        system: 'Sistema',
      },
      density: {
        title: 'Densidade',
        compact: 'Compacta',
        comfortable: 'Confortável',
      },
      notificationSettings: {
        email: 'Notificações por E-mail',
        push: 'Notificações Push',
        sms: 'Notificações por SMS',
        frequency: 'Frequência',
      },
      securitySettings: {
        twoFactor: 'Autenticação de dois fatores',
        activeSessions: 'Sessões ativas',
        changePassword: 'Alterar senha',
        logoutAllDevices: 'Sair de todos os dispositivos',
      },
      apiSettings: {
        generateKey: 'Gerar chave',
        revokeKey: 'Revogar chave',
        confirmPassword: 'Confirmar senha para gerar chave',
        keyInfo: 'Esta chave só será exibida uma vez. Copie-a agora.',
      },
    },
    
    // Dates and formats
    formats: {
      date: 'DD/MM/YYYY',
      time: 'HH:mm',
      dateTime: 'DD/MM/YYYY HH:mm',
      currency: 'R$ {{value}}',
    },
  },
};
