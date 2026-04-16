import { useQuery } from '@tanstack/react-query';

// В dev-режиме ходим напрямую в Django (фиксит IPv6 proxy баг Node 18.13)
const API_BASE = import.meta.env.DEV 
  ? 'http://127.0.0.1:8000/api' 
  : '/api';

interface Team {
  id: number;
  name: string;
  trainer_name: string | null;
  score: number;
  penalty: number;
  total_score: number;
  color: string;
  position: number | null;
}

export function useLeaderboard() {
  return useQuery<Team[]>({
    queryKey: ['leaderboard'],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/leaderboard/`);
      if (!res.ok) throw new Error('Failed to fetch leaderboard');
      return res.json();
    },
  });
}