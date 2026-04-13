import { useQuery } from '@tanstack/react-query';

const API_BASE = '/api';

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