import { useState, useEffect } from 'react';
import { api } from '../../services/api';

export function ScoresPage() {
  const [scores, setScores] = useState<any[]>([]);

  useEffect(() => {
    api.get('/api/scores/').then(r => {
      const data = r.data?.results || r.data || [];
      setScores(Array.isArray(data) ? data : []);
    }).catch(() => {});
  }, []);

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 20 }}>
        <h2 style={{ color: '#00ffff' }}>🏆 Результаты</h2>
        <button style={btnStyle}>+ Внести результат</button>
      </div>
      <div style={card}>
        <table style={table}>
          <thead>
            <tr>
              <th style={th}>Команда</th>
              <th style={th}>Квест</th>
              <th style={th}>Баллы</th>
              <th style={th}>Подтверждено</th>
            </tr>
          </thead>
          <tbody>
            {scores.length === 0 && <tr><td colSpan={4} style={{ color: 'rgba(255,255,255,0.4)', textAlign: 'center', padding: 30 }}>Нет результатов</td></tr>}
            {scores.map((s, i) => (
              <tr key={s.id || i}>
                <td style={{...td, color: '#00ff88'}}>{s.team_name || s.team}</td>
                <td style={td}>{s.quest_title || s.quest}</td>
                <td style={{...td, color: '#ffaa00', fontWeight: 700}}>{s.points}</td>
                <td style={td}>{s.verified ? '✅' : '⏳'}</td>
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
  padding: '10px 20px', borderRadius: 15, cursor: 'pointer', fontFamily: "'Exo 2', sans-serif",
};
const card: React.CSSProperties = {
  background: 'rgba(10,10,30,0.85)', backdropFilter: 'blur(30px)',
  border: '1px solid rgba(0,255,255,0.3)', borderRadius: 20, overflow: 'hidden',
};
const table: React.CSSProperties = { width: '100%', borderCollapse: 'collapse', color: '#fff' };
const th: React.CSSProperties = { padding: '15px', textAlign: 'left', color: '#00ffff', borderBottom: '1px solid rgba(0,255,255,0.2)' };
const td: React.CSSProperties = { padding: '12px 15px', borderBottom: '1px solid rgba(255,255,255,0.05)' };
