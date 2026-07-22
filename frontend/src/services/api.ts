const BASE_URL = `${import.meta.env.BASE_URL}api/`;
const TOKEN_KEY = 'lra26.access';

let accessToken = sessionStorage.getItem(TOKEN_KEY);
let refreshPromise: Promise<string | null> | null = null;

interface ApiResponse<T> {
  data: T;
  status: number;
}

export class ApiRequestError extends Error {
  status: number;
  data: unknown;

  constructor(status: number, data: unknown) {
    super(`API request failed: ${status}`);
    this.status = status;
    this.data = data;
  }
}

export function setAccessToken(token: string | null) {
  accessToken = token;
  if (token) sessionStorage.setItem(TOKEN_KEY, token);
  else sessionStorage.removeItem(TOKEN_KEY);
}

async function refreshAccessToken() {
  try {
    const response = await request<{ access: string }>('auth/refresh/', { method: 'POST' }, false);
    setAccessToken(response.data.access);
    return response.data.access;
  } catch {
    setAccessToken(null);
    return null;
  }
}

async function request<T>(path: string, init: RequestInit = {}, retry = true): Promise<ApiResponse<T>> {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 15_000);
  const headers = new Headers(init.headers);
  headers.set('Accept', 'application/json');
  if (init.body) headers.set('Content-Type', 'application/json');
  if (accessToken) headers.set('Authorization', `Bearer ${accessToken}`);

  try {
    const response = await fetch(`${BASE_URL}${path}`, {
      ...init,
      headers,
      credentials: 'include',
      signal: controller.signal,
    });
    if (response.status === 401 && retry && !path.startsWith('auth/')) {
      refreshPromise ??= refreshAccessToken().finally(() => { refreshPromise = null; });
      if (await refreshPromise) return request<T>(path, init, false);
    }
    const data = response.status === 204 ? undefined : await response.json().catch(() => undefined);
    if (!response.ok) throw new ApiRequestError(response.status, data);
    return { data: data as T, status: response.status };
  } finally {
    window.clearTimeout(timeout);
  }
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T = unknown>(path: string, data?: unknown) => request<T>(path, { method: 'POST', body: data === undefined ? undefined : JSON.stringify(data) }),
  patch: <T = unknown>(path: string, data: unknown) => request<T>(path, { method: 'PATCH', body: JSON.stringify(data) }),
  put: <T = unknown>(path: string, data: unknown) => request<T>(path, { method: 'PUT', body: JSON.stringify(data) }),
  delete: <T = unknown>(path: string) => request<T>(path, { method: 'DELETE' }),
};

export function apiError(error: unknown) {
  if (error instanceof ApiRequestError) {
    const data = error.data as { detail?: string; [key: string]: unknown } | undefined;
    if (data?.detail) return data.detail;
    if (data) {
      const first = Object.values(data)[0];
      if (Array.isArray(first)) return String(first[0]);
      if (typeof first === 'string') return first;
    }
  }
  if (error instanceof DOMException && error.name === 'AbortError') return 'Сервер не ответил вовремя.';
  return 'Не удалось выполнить запрос. Попробуйте ещё раз.';
}

export function listData<T>(data: T[] | { results: T[] }): T[] {
  return Array.isArray(data) ? data : data.results;
}
