import { useState, useEffect } from 'react';
import { api } from '../../services/api';

export function MarksPage() {
  const [marks, setMarks] = useState<any[]>([]);
  useEffect(() => {
    api.get('/api/marks/').then(r => {
      const data = r.data?.results || r.data || [];
      setMarks(Array.isArray(data) ? data : []);
    }).catch(() => {});
  }, []);

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 20 }}>
        <h2 style={{ color: '#00ffff' }}>⚫ Чёрные метки</h2>
        <button style={btnStyle}>+ Добавить метку</button>
      </div>
      <div style={card}>
        <table style={table}>
          <thead>
            <tr>
              <th style={th}>Команда</th>
              <th style={th}>Причина</th>
              <th style={th}>Штраф</th>
              <th style={th}>Дата</th>
              <th style={th}>Действия</th>
            </tr>
          </thead>
          <tbody>
            {marks.length === 0 && <tr><td colSpan={5} style={{ color: 'rgba(255,255,255,0.4)', textAlign: 'center', padding: 30 }}>Нет меток</td></tr>}
            {marks.map((m, i) => (
              <tr key={m.id || i}>
                <td style={{...td, color: '#00ff88'}}>{m.team_name || m.team}</td>
                <td style={td}>{m.reason}</td>
                <td style={{...td, color: '#ff4444', fontWeight: 700}}>-{m.penalty}</td>
                <td style={td}>{m.created_at?.slice(0,10) || '—'}</td>
                <td style={td}><button style={{...actionBtn, color: '#ff4444'}}>🗑️</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const btnStyle: React.CSSProperties = {
  background: 'rgba(255,50,50,0.15)', border: '1px solid #ff4444', color: '#ff4444',
  padding: '10px 20px', borderRadius: 15, cursor: 'pointer', fontFamily: "'Exo 2', sans-serif",
};
const card: React.CSSProperties = {
  background: 'rgba(10,10,30,0.85)', backdropFilter: 'blur(30px)',
  border: '1px solid rgba(0,255,255,0.3)', borderRadius: 20, overflow: 'hidden',
};
const table: React.CSSProperties = { width: '100%', borderCollapse: 'collapse', color: '#fff' };
const th: React.CSSProperties = { padding: '15px', textAlign: 'left', color: '#00ffff', borderBottom: '1px solid rgba(0,255,255,0.2)' };
const td: React.CSSProperties = { padding: '12px 15px', borderBottom: '1px solid rgba(255,255,255,0.05)' };
const actionBtn: React.CSSProperties = { background: 'none', border: 'none', cursor: 'pointer', fontSize: '1em' };
