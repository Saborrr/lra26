import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../../services/api';

type Stats = { teams: number; trainers: number; quests: number; scores: number };

export function DashboardPage() {
  const [stats, setStats] = useState<Stats>({ teams: 0, trainers: 0, quests: 0, scores: 0 });

  useEffect(() => {
    Promise.all([
      api.get('/api/teams/'), api.get('/api/trainers/'),
      api.get('/api/quests/'), api.get('/api/scores/'),
    ]).then(([t, tr, q, s]) => {
      const count = (r: any) => r.data?.count || r.data?.length || 0;
      setStats({ teams: count(t), trainers: count(tr), quests: count(q), scores: count(s) });
    }).catch(() => setStats({ teams: 0, trainers: 0, quests: 0, scores: 0 }));
  }, []);

  const cards = [
    { label: 'Команды', value: stats.teams, icon: '👥', color: '#00ffff' },
    { label: 'Тренеры', value: stats.trainers, icon: '🎓', color: '#ff00ff' },
    { label: 'Квесты', value: stats.quests, icon: '📋', color: '#ffff00' },
    { label: 'Результаты', value: stats.scores, icon: '🏆', color: '#00ff88' },
  ];

  return (
    <div>
      <h2 style={{ color: '#00ffff', marginBottom: 25, fontSize: '1.5em' }}>📊 Панель управления</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 20, marginBottom: 30 }}>
        {cards.map(c => (
          <div key={c.label} style={{
            background: 'rgba(10,10,30,0.85)', backdropFilter: 'blur(30px)',
            border: `1px solid ${c.color}40`, borderRadius: 20, padding: 25, textAlign: 'center',
          }}>
            <div style={{ fontSize: '2.5em', fontWeight: 800, color: c.color, textShadow: `0 0 20px ${c.color}` }}>
              {c.value}
            </div>
            <div style={{ color: 'rgba(255,255,255,0.7)', marginTop: 8 }}>{c.icon} {c.label}</div>
          </div>
        ))}
      </div>

      <div style={{
        background: 'rgba(10,10,30,0.85)', backdropFilter: 'blur(30px)',
        border: '1px solid rgba(0,255,255,0.3)', borderRadius: 20, padding: 25,
      }}>
        <h3 style={{ color: '#00ffff', marginBottom: 15 }}>ℹ️ Информация о мероприятии</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {[
            ['📅 Даты', '27-29 мая 2026'],
            ['🏠 Место', 'ЭФКО'],
            ['👥 Участники', `${stats.teams} команд, ${stats.trainers} тренеров`],
            ['🔗 Сайт', <a href="/" style={{ color: '#00ff88' }}>gofaraway.mooo.com/lra26</a>],
          ].map(([label, value]) => (
            <div key={String(label)} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
              <span style={{ color: 'rgba(255,255,255,0.6)' }}>{label}</span>
              <span style={{ color: '#00ff88', fontWeight: 600 }}>{value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
