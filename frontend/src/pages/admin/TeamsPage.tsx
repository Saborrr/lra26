import { useState, useEffect } from 'react';
import { api } from '../../services/api';

export function TeamsPage() {
  const [teams, setTeams] = useState<any[]>([]);

  useEffect(() => {
    api.get('/api/teams/').then(r => {
      const data = r.data?.results || r.data || [];
      setTeams(Array.isArray(data) ? data : []);
    }).catch(() => setTeams([]));
  }, []);

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <h2 style={{ color: '#00ffff' }}>👥 Команды</h2>
        <button style={btnStyle}>+ Добавить команду</button>
      </div>
      <div style={tableWrap}>
        <table style={table}>
          <thead>
            <tr>
              <th style={th}>#</th>
              <th style={th}>Команда</th>
              <th style={th}>Тренер</th>
              <th style={th}>Очки</th>
              <th style={th}>Штраф</th>
              <th style={th}>Итого</th>
              <th style={th}>Действия</th>
            </tr>
          </thead>
          <tbody>
            {teams.length === 0 && <tr><td colSpan={7} style={{ color: 'rgba(255,255,255,0.4)', textAlign: 'center', padding: 30 }}>Загружается...</td></tr>}
            {teams.map((t, i) => (
              <tr key={t.id || i}>
                <td style={td}>{i + 1}</td>
                <td style={{...td, color: '#00ff88', fontWeight: 600}}>{t.name}</td>
                <td style={td}>{t.trainer_name || '—'}</td>
                <td style={td}>{t.score || 0}</td>
                <td style={td}>{t.penalty || 0}</td>
                <td style={{...td, color: '#ffaa00', fontWeight: 700}}>{(t.score || 0) - (t.penalty || 0)}</td>
                <td style={td}>
                  <button style={actionBtn}>✏️</button>
                  <button style={{...actionBtn, color: '#ff4444'}}>🗑️</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const btnStyle: React.CSSProperties = {
  background: 'rgba(0,255,255,0.15)', border: '1px solid #00ffff', color: '#00ffff',
  padding: '10px 20px', borderRadius: 15, cursor: 'pointer', fontFamily: "'Exo 2', sans-serif", fontSize: '0.9em',
};
const tableWrap: React.CSSProperties = {
  background: 'rgba(10,10,30,0.85)', backdropFilter: 'blur(30px)',
  border: '1px solid rgba(0,255,255,0.3)', borderRadius: 20, overflow: 'hidden',
};
const table: React.CSSProperties = { width: '100%', borderCollapse: 'collapse', color: '#fff' };
const th: React.CSSProperties = { padding: '15px', textAlign: 'left', color: '#00ffff', borderBottom: '1px solid rgba(0,255,255,0.2)', fontWeight: 600 };
const td: React.CSSProperties = { padding: '12px 15px', borderBottom: '1px solid rgba(255,255,255,0.05)' };
const actionBtn: React.CSSProperties = { background: 'none', border: 'none', cursor: 'pointer', fontSize: '1em', padding: '2px 5px' };
