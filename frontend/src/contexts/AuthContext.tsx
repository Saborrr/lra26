import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';

import type { CurrentUser } from '../types';
import { api, apiError, setAccessToken } from '../services/api';
import { detectPlatform, type PlatformPayload } from '../services/platform';

interface AuthContextValue {
  user: CurrentUser | null;
  loading: boolean;
  error: string;
  platformNeedsLink: boolean;
  login: (username: string, password: string) => Promise<void>;
  linkPlatform: (code: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [platform, setPlatform] = useState<PlatformPayload | null>(null);
  const [platformNeedsLink, setPlatformNeedsLink] = useState(false);

  const acceptAuth = useCallback((data: { access: string; user: CurrentUser }) => {
    setAccessToken(data.access);
    setUser(data.user);
    setPlatformNeedsLink(false);
    setError('');
  }, []);

  const authenticatePlatform = useCallback(async (payload: PlatformPayload, linkCode?: string) => {
    const endpoint = payload.provider === 'telegram' ? 'auth/telegram/' : 'auth/vk/';
    const body = { ...payload, provider: undefined, link_code: linkCode || undefined };
    try {
      const response = await api.post<{ access: string; user: CurrentUser }>(endpoint, body);
      acceptAuth(response.data);
    } catch (requestError) {
      const status = (requestError as { status?: number }).status;
      if (status === 400) setPlatformNeedsLink(true);
      else setError(apiError(requestError));
    }
  }, [acceptAuth]);

  useEffect(() => {
    let active = true;
    void (async () => {
      try {
        const detected = await detectPlatform();
        if (!active) return;
        setPlatform(detected);
        if (detected) {
          await authenticatePlatform(detected);
          return;
        }
        try {
          const me = await api.get<CurrentUser>('auth/me/');
          if (active) setUser(me.data);
        } catch {
          try {
            const refreshed = await api.post<{ access: string; user: CurrentUser }>('auth/refresh/');
            if (active) acceptAuth(refreshed.data);
          } catch {
            setAccessToken(null);
          }
        }
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, [acceptAuth, authenticatePlatform]);

  const login = useCallback(async (username: string, password: string) => {
    setError('');
    try {
      const response = await api.post<{ access: string; user: CurrentUser }>('auth/login/', { username, password });
      acceptAuth(response.data);
    } catch (requestError) {
      const message = apiError(requestError);
      setError(message);
      throw new Error(message);
    }
  }, [acceptAuth]);

  const linkPlatform = useCallback(async (code: string) => {
    if (!platform) return;
    await authenticatePlatform(platform, code);
  }, [authenticatePlatform, platform]);

  const logout = useCallback(async () => {
    try { await api.post('auth/logout/'); } finally {
      setAccessToken(null);
      setUser(null);
    }
  }, []);

  const value = useMemo(() => ({ user, loading, error, platformNeedsLink, login, linkPlatform, logout }), [user, loading, error, platformNeedsLink, login, linkPlatform, logout]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error('useAuth must be used within AuthProvider');
  return value;
}
