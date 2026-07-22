import { Award, BookOpenCheck, CircleGauge, ShieldAlert, Sparkles, UserRound } from 'lucide-react';
import { useEffect, useState } from 'react';

import { Leaderboard } from '../components/Leaderboard';
import { useAuth } from '../contexts/AuthContext';
import { api, listData } from '../services/api';
import type { Quest, Team } from '../types';

export function ParticipantPage() {
  const { user } = useAuth();
  const [teams, setTeams] = useState<Team[]>([]);
  const [quests, setQuests] = useState<Quest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    void Promise.all([
      api.get<Team[]>('my-team/').then(response => setTeams(response.data)).catch(() => setTeams([])),
      api.get<Quest[] | { results: Quest[] }>('quests/').then(response => setQuests(listData(response.data))),
    ]).finally(() => setLoading(false));
  }, []);

  const team = teams[0];
  return (
    <div className="page dashboard-page">
      <section className="dashboard-hero">
        <div><span className="eyebrow">Participant console</span><h1>Добро пожаловать, {user?.first_name || user?.username}</h1><p>Пульс вашей команды и все активные задания в одном месте.</p></div>
        <div className="role-chip"><UserRound size={17} /> Участник</div>
      </section>
      {loading ? <div className="empty-state glass"><span className="loader" /> Загружаем данные…</div> : team ? (
        <section className="metric-grid">
          <article className="metric-card glass accent-cyan"><CircleGauge /><span>Баллы</span><strong>{team.score}</strong></article>
          <article className="metric-card glass accent-pink"><ShieldAlert /><span>Штраф</span><strong>{team.penalty}</strong></article>
          <article className="metric-card glass accent-gold"><Award /><span>Итого</span><strong>{team.total_score}</strong></article>
          <article className="team-identity glass"><span className="team-avatar fallback" style={{ '--team-color': team.color } as React.CSSProperties}>{team.name.slice(0, 2)}</span><div><small>Ваш экипаж</small><h2>{team.name}</h2><p>{team.trainer_name || 'Наставник не назначен'}</p></div></article>
        </section>
      ) : <div className="empty-state glass"><Sparkles /> Аккаунт создан. Администратор ещё не привязал к нему команду.</div>}
      <section className="content-grid">
        <div className="quest-panel glass">
          <div className="section-heading"><div><span className="eyebrow">Mission map</span><h2>Активные задания</h2></div><BookOpenCheck /></div>
          <div className="quest-list">
            {quests.map(quest => <article key={quest.id}><span>{String(quest.order + 1).padStart(2, '0')}</span><div><strong>{quest.title}</strong><p>{quest.description || quest.category || 'Описание появится перед стартом.'}</p></div><b>+{quest.points}</b></article>)}
          </div>
        </div>
        <Leaderboard compact />
      </section>
    </div>
  );
}
