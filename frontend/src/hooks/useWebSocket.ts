import { useEffect, useRef } from 'react';
import { useQueryClient } from '@tanstack/react-query';

/**
 * Хук для WebSocket-соединения с leaderboard.
 * URL определяется автоматически на основе текущего location.
 */
export function useLeaderboardWS() {
  const queryClient = useQueryClient();
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // В dev-режиме подключаемся напрямую к Django (фиксит IPv6 proxy баг)
    const wsUrl = import.meta.env.DEV
      ? 'ws://127.0.0.1:8000/ws/leaderboard/'
      : `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws/leaderboard/`;

    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => console.log('WS connected');
    ws.onclose = () => console.log('WS disconnected');
    ws.onerror = (err) => console.error('WS error:', err);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'score_update' || data.type === 'connected') {
          queryClient.invalidateQueries({ queryKey: ['leaderboard'] });
          console.log('Leaderboard updated via WS');
        }
      } catch {
        console.error('WS: failed to parse message');
      }
    };

    // Пинг для поддержания соединения
    const pingInterval = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'ping' }));
      }
    }, 30000);

    return () => {
      clearInterval(pingInterval);
      ws.close();
      wsRef.current = null;
    };
  }, [queryClient]);
}