
import { useAuthStore } from '@/store/authStore';

// Define permission types
export type Permission = 
  | 'dashboard:view'
  | 'kanban:view' | 'kanban:edit'
  | 'editais:view' | 'editais:edit' | 'editais:delete'
  | 'mensagens:view' | 'mensagens:send'
  | 'calendario:view' | 'calendario:edit'
  | 'users:view' | 'users:edit'
  | 'settings:view' | 'settings:edit'
  | 'api:generate';

// Permission mapping for each role
const rolePermissionMap: Record<string, Permission[]> = {
  admin: [
    'dashboard:view',
    'kanban:view', 'kanban:edit',
    'editais:view', 'editais:edit', 'editais:delete',
    'mensagens:view', 'mensagens:send',
    'calendario:view', 'calendario:edit',
    'users:view', 'users:edit',
    'settings:view', 'settings:edit',
    'api:generate'
  ],
  user: [
    'dashboard:view',
    'kanban:view',
    'editais:view',
    'mensagens:view', 'mensagens:send',
    'calendario:view',
    'settings:view'
  ]
};

export function usePermissions() {
  const { user } = useAuthStore();
  
  const role = user?.role || 'user';
  const permissions = rolePermissionMap[role] || [];
  
  const hasPermission = (permission: Permission): boolean => {
    return permissions.includes(permission);
  };
  
  const hasAnyPermission = (requiredPermissions: Permission[]): boolean => {
    return requiredPermissions.some(permission => permissions.includes(permission));
  };
  
  const hasAllPermissions = (requiredPermissions: Permission[]): boolean => {
    return requiredPermissions.every(permission => permissions.includes(permission));
  };
  
  return {
    permissions,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    role
  };
}
