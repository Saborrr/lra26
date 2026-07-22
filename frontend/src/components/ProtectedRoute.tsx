import type { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';

import { useAuth } from '../contexts/AuthContext';
import type { Role } from '../types';

const roleWeight: Record<Role, number> = { participant: 1, admin: 2, superadmin: 3 };

export function ProtectedRoute({ children, minimum = 'participant' }: { children: ReactNode; minimum?: Role }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="page centered"><span className="loader" /> Проверяем доступ…</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (roleWeight[user.role] < roleWeight[minimum]) return <Navigate to="/app" replace />;
  return children;
}
