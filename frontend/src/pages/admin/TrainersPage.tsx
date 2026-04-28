import { useState, useEffect } from 'react';
import { api } from '../../services/api';

export function TrainersPage() {
  const [trainers, setTrainers] = useState<any[]>([]);
  useEffect(() => {
    api.get('/api/trainers/').then(r => {
      const data = r.data?.results || r.data || [];
      setTrainers(Array.isArray(data) ? data : []);
    }).catch(() => {});
  }, []);

  return (
    <div>
      <h2 style={{ color: '#00ffff', marginBottom: 20 }}>🎓 Тренеры</h2>
      <div style={card}>
        <table style={table}>
          <thead>
            <tr>
              <th style={th}>Имя</th>
              <th style={th}>Команда</th>
              <th style={th}>Telegram</th>
              <th style={th}>Действия</th>
            </tr>
          </thead>
          <tbody>
            {trainers.map((t, i) => (
              <tr key={t.id || i}>
                <td style={{...td, color: '#00ff88'}}>{t.name}</td>
                <td style={td}>{t.team_name || t.team || '—'}</td>
                <td style={td}>{t.telegram_id ? '✅' : '❌'}</td>
                <td style={td}><button style={actionBtn}>✏️</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const card: React.CSSProperties = {
  background: 'rgba(10,10,30,0.85)', backdropFilter: 'blur(30px)',
  border: '1px solid rgba(0,255,255,0.3)', borderRadius: 20, overflow: 'hidden',
};
const table: React.CSSProperties = { width: '100%', borderCollapse: 'collapse', color: '#fff' };
const th: React.CSSProperties = { padding: '15px', textAlign: 'left', color: '#00ffff', borderBottom: '1px solid rgba(0,255,255,0.2)' };
const td: React.CSSProperties = { padding: '12px 15px', borderBottom: '1px solid rgba(255,255,255,0.05)' };
const actionBtn: React.CSSProperties = { background: 'none', border: 'none', cursor: 'pointer', color: '#00ffff', fontSize: '1em' };
