import { ReactNode } from 'react';
import { usePermissions, Permission } from '@/hooks/usePermissions';

interface PermissionGateProps {
  children: ReactNode;
  permissions?: Permission[];
  anyPermission?: Permission[];
  fallback?: ReactNode;
}

export const PermissionGate = ({ 
  children, 
  permissions = [], 
  anyPermission = [],
  fallback = null 
}: PermissionGateProps) => {
  const { hasPermission, hasAnyPermission } = usePermissions();
  
  // If no permissions are required, render children
  if (permissions.length === 0 && anyPermission.length === 0) {
    return <>{children}</>;
  }
  
  // Check if user has all required permissions
  const hasRequired = permissions.length > 0 ? 
    permissions.every(permission => hasPermission(permission)) : true;
  
  // Check if user has any of the alternative permissions
  const hasAny = anyPermission.length > 0 ? 
    hasAnyPermission(anyPermission) : true;
  
  // If user has required permissions or any alternative, render children
  if (hasRequired && hasAny) {
    return <>{children}</>;
  }
  
  // Otherwise render fallback
  return <>{fallback}</>;
};
