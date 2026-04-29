import { useState, useEffect } from 'react';
import { api } from '../../services/api';

export function QuestsPage() {
  const [quests, setQuests] = useState<any[]>([]);
  useEffect(() => {
    api.get('/api/quests/').then(r => {
      const data = r.data?.results || r.data || [];
      setQuests(Array.isArray(data) ? data : []);
    }).catch(() => {});
  }, []);

  return (
    <div>
      <h2 style={{ color: '#00ffff', marginBottom: 20 }}>📋 Квесты</h2>
      <div style={card}>
        <table style={table}>
          <thead>
            <tr>
              <th style={th}>Название</th>
              <th style={th}>Баллы</th>
              <th style={th}>Категория</th>
              <th style={th}>Активен</th>
              <th style={th}>Действия</th>
            </tr>
          </thead>
          <tbody>
            {quests.map((q, i) => (
              <tr key={q.id || i}>
                <td style={{...td, color: '#00ff88'}}>{q.title}</td>
                <td style={{...td, color: '#ffaa00'}}>{q.points}</td>
                <td style={td}>{q.category || '—'}</td>
                <td style={td}>{q.active ? '✅' : '❌'}</td>
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
