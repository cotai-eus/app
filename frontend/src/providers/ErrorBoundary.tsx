
import { ReactNode } from 'react';
import * as Sentry from '@sentry/react';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertTriangle } from 'lucide-react';

interface FallbackProps {
  error: Error;
  eventId: string;
  resetError(): void;
}

const ErrorFallback = ({ error, resetError }: FallbackProps) => {
  return (
    <Alert variant="destructive" className="m-4">
      <AlertTriangle className="h-4 w-4" />
      <AlertTitle>Algo deu errado!</AlertTitle>
      <AlertDescription className="mt-2">
        <p className="text-sm text-muted-foreground mb-4">
          {error.message || 'Ocorreu um erro inesperado na aplicação.'}
        </p>
        <div className="flex justify-end">
          <Button onClick={resetError} variant="outline">
            Tentar novamente
          </Button>
        </div>
      </AlertDescription>
    </Alert>
  );
};

interface ErrorBoundaryProps {
  children: ReactNode;
}

export const ErrorBoundaryProvider = ({ children }: ErrorBoundaryProps) => {
  return (
    <Sentry.ErrorBoundary fallback={ErrorFallback}>
      {children}
    </Sentry.ErrorBoundary>
  );
};

/**
 * Initializes error tracking and reporting
 */
export const initErrorTracking = () => {
  // In production, use your actual Sentry DSN
  const SENTRY_DSN = import.meta.env.VITE_SENTRY_DSN || '';
  
  if (SENTRY_DSN) {
    Sentry.init({
      dsn: SENTRY_DSN,
      integrations: [
        new Sentry.BrowserTracing(),
        // Optional performance monitoring
        new Sentry.Replay({
          // Replay options
          maskAllText: true,
          blockAllMedia: true,
        }),
      ],
      // Performance Monitoring
      tracesSampleRate: 0.1, // Capture 10% of the transactions
      // Session Replay
      replaysSessionSampleRate: 0.1, // Sample rate for all sessions
      replaysOnErrorSampleRate: 1.0, // Sample rate for sessions with errors
    });
  }
};

/**
 * Utility for tracking errors manually
 */
export const trackError = (error: unknown, context?: Record<string, any>) => {
  console.error(error);
  Sentry.captureException(error, { extra: context });
};

/**
 * Utility for tracking user actions and events
 */
export const trackEvent = (name: string, data?: Record<string, any>) => {
  Sentry.captureMessage(name, {
    level: 'info',
    extra: data,
  });
};

/**
 * Set user information for better error context
 */
export const setUserContext = (user: { id: string; email?: string; role?: string }) => {
  Sentry.setUser({
    id: user.id,
    email: user.email,
    role: user.role,
  });
};

/**
 * Clear user context on logout
 */
export const clearUserContext = () => {
  Sentry.setUser(null);
};
