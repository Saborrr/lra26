import { Crown, Medal, Minus, Radio } from 'lucide-react';
import { useEffect, useMemo, useRef, useState } from 'react';

import { api } from '../services/api';
import type { Team } from '../types';

function TeamAvatar({ team }: { team: Team }) {
  if (team.logo) return <img src={team.logo} alt="" className="team-avatar" />;
  return <span className="team-avatar fallback" style={{ '--team-color': team.color } as React.CSSProperties}>{team.name.slice(0, 2).toUpperCase()}</span>;
}

export function Leaderboard({ compact = false }: { compact?: boolean }) {
  const [teams, setTeams] = useState<Team[]>([]);
  const [connected, setConnected] = useState(false);
  const [loading, setLoading] = useState(true);
  const reconnectRef = useRef<number | undefined>(undefined);
  const connectedRef = useRef(false);

  useEffect(() => {
    let active = true;
    let socket: WebSocket | null = null;
    let attempts = 0;
    const load = async () => {
      try {
        const response = await api.get<Team[]>('leaderboard/');
        if (active) setTeams(response.data);
      } finally {
        if (active) setLoading(false);
      }
    };
    const connect = () => {
      if (!active) return;
      const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
      socket = new WebSocket(`${protocol}//${location.host}${import.meta.env.BASE_URL}ws/leaderboard/`);
      socket.onopen = () => { attempts = 0; connectedRef.current = true; setConnected(true); };
      socket.onmessage = event => {
        const message = JSON.parse(event.data) as { teams?: Team[] };
        if (message.teams) setTeams(message.teams);
      };
      socket.onerror = () => socket?.close();
      socket.onclose = () => {
        connectedRef.current = false;
        setConnected(false);
        if (active) {
          attempts += 1;
          const delay = Math.min(30_000, 1_000 * 2 ** attempts) + Math.random() * 700;
          reconnectRef.current = window.setTimeout(connect, delay);
        }
      };
    };
    void load();
    connect();
    const fallback = window.setInterval(() => { if (!connectedRef.current) void load(); }, 30_000);
    return () => {
      active = false;
      socket?.close();
      window.clearTimeout(reconnectRef.current);
      window.clearInterval(fallback);
    };
  }, []);

  const leader = teams[0];
  const rows = useMemo(() => compact ? teams.slice(0, 5) : teams, [compact, teams]);

  if (loading) return <div className="empty-state"><span className="loader" /> Синхронизируем орбиту…</div>;
  return (
    <section className="leaderboard glass">
      <div className="section-heading">
        <div><span className="eyebrow">Live telemetry</span><h2>Рейтинг экипажей</h2></div>
        <span className={`live-status ${connected ? 'online' : ''}`}><Radio size={15} /> {connected ? 'В эфире' : 'Резервный режим'}</span>
      </div>
      {leader && !compact && (
        <div className="leader-card">
          <div className="leader-glow" style={{ '--team-color': leader.color } as React.CSSProperties} />
          <Crown size={28} />
          <TeamAvatar team={leader} />
          <div><span>Лидер миссии</span><strong>{leader.name}</strong><small>{leader.trainer_name || 'Экипаж'}</small></div>
          <b>{leader.total_score}<small> очков</small></b>
        </div>
      )}
      <div className="ranking-list">
        {rows.map((team, index) => (
          <article className="ranking-row" key={team.id}>
            <span className={`rank rank-${index + 1}`}>{index < 3 ? <Medal size={19} /> : team.position || index + 1}</span>
            <TeamAvatar team={team} />
            <div className="team-copy"><strong>{team.name}</strong><small>{team.trainer_name || 'Без наставника'}</small></div>
            <div className="score-breakdown"><span>{team.score}</span>{team.penalty > 0 && <small><Minus size={12} />{team.penalty}</small>}</div>
            <strong className="total-score">{team.total_score}</strong>
          </article>
        ))}
        {!rows.length && <div className="empty-state">Команды появятся перед стартом миссии.</div>}
      </div>
    </section>
  );
}
