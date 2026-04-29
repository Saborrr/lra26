import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || '';

export const api = {
  get: (url: string) => axios.get(`${BASE_URL}${url}`),
  post: (url: string, data: any) => axios.post(`${BASE_URL}${url}`, data),
  put: (url: string, data: any) => axios.put(`${BASE_URL}${url}`, data),
  delete: (url: string) => axios.delete(`${BASE_URL}${url}`),
};

export function getToken(): string | null {
  return localStorage.getItem('jwt_token');
}

export function setToken(token: string) {
  localStorage.setItem('jwt_token', token);
}

export function clearToken() {
  localStorage.removeItem('jwt_token');
}
