import { Activity, KeyRound, ShieldCheck, UserPlus, Users } from 'lucide-react';
import { type FormEvent, useCallback, useEffect, useState } from 'react';

import { api, apiError, listData } from '../services/api';
import type { AuditEvent, ManagedUser } from '../types';

export function SuperAdminPage() {
  const [users, setUsers] = useState<ManagedUser[]>([]);
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [message, setMessage] = useState('');
  const [username, setUsername] = useState(''); const [password, setPassword] = useState(''); const [role, setRole] = useState('participant');

  const load = useCallback(async () => {
    try {
      const [userResponse, auditResponse] = await Promise.all([
        api.get<ManagedUser[] | { results: ManagedUser[] }>('auth/users/'),
        api.get<AuditEvent[] | { results: AuditEvent[] }>('auth/audit/'),
      ]);
      setUsers(listData(userResponse.data)); setEvents(listData(auditResponse.data));
    } catch (error) { setMessage(apiError(error)); }
  }, []);
  useEffect(() => { void load(); }, [load]);

  const createUser = async (event: FormEvent) => {
    event.preventDefault(); setMessage('');
    try { await api.post('auth/users/', { username, password, role }); setUsername(''); setPassword(''); setMessage('Пользователь создан'); await load(); }
    catch (error) { setMessage(apiError(error)); }
  };
  const issueCode = async (userId: number) => {
    try {
      const response = await api.post<{ code: string; expires_at: string }>('auth/link-codes/issue/', { user: userId });
      setMessage(`Одноразовый код: ${response.data.code} · действует 15 минут`);
    } catch (error) { setMessage(apiError(error)); }
  };
  const changeRole = async (user: ManagedUser, nextRole: string) => {
    try { await api.patch(`auth/users/${user.id}/`, { role: nextRole }); await load(); }
    catch (error) { setMessage(apiError(error)); }
  };
  return (
    <div className="page dashboard-page super-page">
      <section className="dashboard-hero"><div><span className="eyebrow">Root command</span><h1>Системный контур</h1><p>Учётные записи, уровни доступа и неизменяемый журнал действий.</p></div><div className="role-chip super"><ShieldCheck size={17} /> Суперадминистратор</div></section>
      {message && <div className="notice code-notice" role="status">{message}</div>}
      <section className="super-grid">
        <form className="form-card glass" onSubmit={event => void createUser(event)}>
          <h2><UserPlus /> Новый пользователь</h2>
          <label><span>Логин</span><input required value={username} onChange={e => setUsername(e.target.value)} autoComplete="off" /></label>
          <label><span>Временный пароль</span><input required minLength={12} type="password" value={password} onChange={e => setPassword(e.target.value)} autoComplete="new-password" /></label>
          <label><span>Роль</span><select value={role} onChange={e => setRole(e.target.value)}><option value="participant">Участник</option><option value="admin">Администратор</option></select></label>
          <button className="button"><UserPlus size={17} /> Создать</button>
        </form>
        <div className="users-panel glass">
          <div className="section-heading"><div><span className="eyebrow">Access matrix</span><h2>Пользователи</h2></div><Users /></div>
          <div className="user-list">
            {users.map(user => <article key={user.id}><span className="user-avatar">{user.username.slice(0, 2).toUpperCase()}</span><div><strong>{user.username}</strong><small>{user.first_name} {user.last_name}</small></div><select value={user.current_role} onChange={e => void changeRole(user, e.target.value)}><option value="participant">Участник</option><option value="admin">Администратор</option></select><button className="icon-button" title="Выдать код привязки" onClick={() => void issueCode(user.id)}><KeyRound size={17} /></button></article>)}
          </div>
        </div>
      </section>
      <section className="audit-panel glass">
        <div className="section-heading"><div><span className="eyebrow">Immutable trail</span><h2>Последние действия</h2></div><Activity /></div>
        <div className="audit-list">{events.slice(0, 50).map(event => <article key={event.id}><span>{new Date(event.created_at).toLocaleString('ru')}</span><strong>{event.action}</strong><small>{event.actor_name || 'system'} · {event.target_type} {event.target_id}</small></article>)}</div>
      </section>
    </div>
  );
}
