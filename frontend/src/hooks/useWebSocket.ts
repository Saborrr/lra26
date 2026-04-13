import { useEffect, useCallback } from 'react';
import { useQueryClient } from '@tanstack/react-query';

export function useLeaderboardWS() {
  const queryClient = useQueryClient();

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/leaderboard/');

    ws.onopen = () => console.log('WS connected');
    ws.onclose = () => console.log('WS disconnected');
    ws.onerror = (err) => console.error('WS error:', err);

    ws.onmessage = useCallback((event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'score_update') {
        queryClient.invalidateQueries({ queryKey: ['leaderboard'] });
        console.log('Leaderboard updated via WS');
      }
    }, [queryClient]);

    return () => {
      ws.close();
    };
  }, [queryClient]);
}