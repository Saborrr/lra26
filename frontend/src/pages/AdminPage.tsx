import { ClipboardList, Flag, Gauge, Plus, Save, ShieldAlert, Trash2, UsersRound } from 'lucide-react';
import { type FormEvent, useCallback, useEffect, useMemo, useState } from 'react';

import { useAuth } from '../contexts/AuthContext';
import { api, apiError, listData } from '../services/api';
import type { ParticipantAccount, Penalty, Quest, Score, Team, Trainer } from '../types';

type Tab = 'scores' | 'teams' | 'participants' | 'quests' | 'penalties';

export function AdminPage() {
  const { user } = useAuth();
  const [tab, setTab] = useState<Tab>('scores');
  const [teams, setTeams] = useState<Team[]>([]);
  const [quests, setQuests] = useState<Quest[]>([]);
  const [scores, setScores] = useState<Score[]>([]);
  const [penalties, setPenalties] = useState<Penalty[]>([]);
  const [trainers, setTrainers] = useState<Trainer[]>([]);
  const [participants, setParticipants] = useState<ParticipantAccount[]>([]);
  const [message, setMessage] = useState('');

  const load = useCallback(async () => {
    try {
      const [teamResponse, questResponse, scoreResponse, penaltyResponse, trainerResponse, participantResponse] = await Promise.all([
        api.get<Team[] | { results: Team[] }>('teams/'), api.get<Quest[] | { results: Quest[] }>('quests/'),
        api.get<Score[] | { results: Score[] }>('scores/'), api.get<Penalty[] | { results: Penalty[] }>('marks/'),
        api.get<Trainer[] | { results: Trainer[] }>('trainers/'), api.get<ParticipantAccount[]>('auth/participants/'),
      ]);
      setTeams(listData(teamResponse.data)); setQuests(listData(questResponse.data)); setScores(listData(scoreResponse.data));
      setPenalties(listData(penaltyResponse.data)); setTrainers(listData(trainerResponse.data)); setParticipants(participantResponse.data);
    } catch (error) { setMessage(apiError(error)); }
  }, []);

  useEffect(() => { void load(); }, [load]);

  const submit = async (endpoint: string, payload: Record<string, unknown>, success: string) => {
    setMessage('');
    try { await api.post(endpoint, payload); setMessage(success); await load(); }
    catch (error) { setMessage(apiError(error)); }
  };

  const remove = async (endpoint: string) => {
    if (!window.confirm('Удалить запись? Это действие попадёт в журнал аудита.')) return;
    try { await api.delete(endpoint); await load(); } catch (error) { setMessage(apiError(error)); }
  };

  const total = useMemo(() => teams.reduce((sum, team) => sum + team.total_score, 0), [teams]);
  return (
    <div className="page dashboard-page admin-page">
      <section className="dashboard-hero"><div><span className="eyebrow">Mission control</span><h1>Центр управления</h1><p>Баллы, задания, команды и дисциплина в реальном времени.</p></div><div className="role-chip admin"><Gauge size={17} /> {user?.role === 'superadmin' ? 'Суперадминистратор' : 'Администратор'}</div></section>
      <section className="metric-grid admin-metrics">
        <article className="metric-card glass"><UsersRound /><span>Команды</span><strong>{teams.length}</strong></article>
        <article className="metric-card glass"><ClipboardList /><span>Результаты</span><strong>{scores.length}</strong></article>
        <article className="metric-card glass"><Flag /><span>Общий счёт</span><strong>{total}</strong></article>
        <article className="metric-card glass"><ShieldAlert /><span>Штрафы</span><strong>{penalties.reduce((sum, item) => sum + item.penalty, 0)}</strong></article>
      </section>
      <div className="admin-tabs glass" role="tablist">
        {(['scores', 'teams', 'participants', 'quests', 'penalties'] as Tab[]).map(item => <button key={item} className={tab === item ? 'active' : ''} onClick={() => setTab(item)}>{({ scores: 'Результаты', teams: 'Команды', participants: 'Участники', quests: 'Задания', penalties: 'Штрафы' })[item]}</button>)}
      </div>
      {message && <div className="notice" role="status">{message}</div>}
      {tab === 'scores' && <ScoreAdmin teams={teams} quests={quests} scores={scores} onSubmit={submit} onRemove={remove} />}
      {tab === 'teams' && <TeamAdmin teams={teams} trainers={trainers} onSubmit={submit} onRemove={remove} />}
      {tab === 'participants' && <ParticipantAdmin participants={participants} trainers={trainers} onSubmit={submit} onRemove={remove} />}
      {tab === 'quests' && <QuestAdmin quests={quests} onSubmit={submit} onRemove={remove} />}
      {tab === 'penalties' && <PenaltyAdmin teams={teams} penalties={penalties} onSubmit={submit} onRemove={remove} />}
    </div>
  );
}

function FormCard({ title, children, onSubmit }: { title: string; children: React.ReactNode; onSubmit: (event: FormEvent<HTMLFormElement>) => void }) {
  return <form className="form-card glass" onSubmit={onSubmit}><h2><Plus size={20} /> {title}</h2>{children}<button className="button"><Save size={17} /> Сохранить</button></form>;
}

interface AdminProps { onSubmit: (endpoint: string, payload: Record<string, unknown>, success: string) => Promise<void>; onRemove: (endpoint: string) => Promise<void>; }

function ScoreAdmin({ teams, quests, scores, onSubmit, onRemove }: AdminProps & { teams: Team[]; quests: Quest[]; scores: Score[] }) {
  const [team, setTeam] = useState(''); const [quest, setQuest] = useState(''); const [points, setPoints] = useState('0'); const selected = quests.find(item => item.id === quest);
  return <section className="admin-workspace"><FormCard title="Внести результат" onSubmit={event => { event.preventDefault(); void onSubmit('scores/', { team: Number(team), quest, points: Number(points), verified: true }, 'Результат сохранён'); }}>
    <label><span>Команда</span><select required value={team} onChange={e => setTeam(e.target.value)}><option value="">Выберите</option>{teams.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</select></label>
    <label><span>Задание</span><select required value={quest} onChange={e => { setQuest(e.target.value); setPoints('0'); }}><option value="">Выберите</option>{quests.filter(item => item.active).map(item => <option key={item.id} value={item.id}>{item.title} · max {item.points}</option>)}</select></label>
    <label><span>Баллы</span><input required type="number" min="0" max={selected?.points ?? 0} value={points} onChange={e => setPoints(e.target.value)} /></label>
  </FormCard><DataTable headers={['Команда', 'Задание', 'Баллы', '']} rows={scores.map(item => [item.team_name, item.quest_title, item.points, <button className="table-action danger" onClick={() => void onRemove(`scores/${item.id}/`)}><Trash2 size={15} /></button>])} /></section>;
}

function TeamAdmin({ teams, trainers, onSubmit, onRemove }: AdminProps & { teams: Team[]; trainers: Trainer[] }) {
  const [name, setName] = useState(''); const [trainer, setTrainer] = useState(''); const [color, setColor] = useState('#7c5cff');
  return <section className="admin-workspace"><FormCard title="Добавить команду" onSubmit={event => { event.preventDefault(); void onSubmit('teams/', { name, trainer: trainer ? Number(trainer) : null, color }, 'Команда создана'); setName(''); }}>
    <label><span>Название</span><input required maxLength={100} value={name} onChange={e => setName(e.target.value)} /></label>
    <label><span>Наставник</span><select value={trainer} onChange={e => setTrainer(e.target.value)}><option value="">Не назначен</option>{trainers.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</select></label>
    <label><span>Цвет экипажа</span><input type="color" value={color} onChange={e => setColor(e.target.value)} /></label>
  </FormCard><DataTable headers={['Команда', 'Наставник', 'Итого', '']} rows={teams.map(item => [item.name, item.trainer_name || '—', item.total_score, <button className="table-action danger" onClick={() => void onRemove(`teams/${item.id}/`)}><Trash2 size={15} /></button>])} /></section>;
}

function ParticipantAdmin({ participants, trainers, onSubmit, onRemove }: AdminProps & { participants: ParticipantAccount[]; trainers: Trainer[] }) {
  const [account, setAccount] = useState(''); const [name, setName] = useState(''); const [phone, setPhone] = useState('');
  const available = participants.filter(item => item.is_active && item.trainer_id === null);
  const chooseAccount = (value: string) => {
    setAccount(value);
    const selected = participants.find(item => item.id === Number(value));
    if (selected) setName(selected.display_name);
  };
  return <section className="admin-workspace"><FormCard title="Добавить участника" onSubmit={event => { event.preventDefault(); void onSubmit('trainers/', { user: Number(account), name, phone }, 'Профиль участника создан'); setAccount(''); setName(''); setPhone(''); }}>
    <label><span>Аккаунт</span><select required value={account} onChange={e => chooseAccount(e.target.value)}><option value="">Выберите аккаунт</option>{available.map(item => <option key={item.id} value={item.id}>{item.display_name} · @{item.username}</option>)}</select></label>
    <label><span>Имя в системе</span><input required maxLength={100} value={name} onChange={e => setName(e.target.value)} /></label>
    <label><span>Телефон, необязательно</span><input type="tel" maxLength={20} autoComplete="tel" value={phone} onChange={e => setPhone(e.target.value)} /></label>
    {!available.length && <small className="field-hint">Свободных аккаунтов нет. Суперадминистратор может создать новый аккаунт.</small>}
  </FormCard><DataTable headers={['Участник', 'Аккаунт', 'Команд', '']} rows={trainers.map(item => [item.name, item.username ? `@${item.username}` : 'Без аккаунта', item.teams_count, <button className="table-action danger" onClick={() => void onRemove(`trainers/${item.id}/`)}><Trash2 size={15} /></button>])} /></section>;
}

function QuestAdmin({ quests, onSubmit, onRemove }: AdminProps & { quests: Quest[] }) {
  const [id, setId] = useState(''); const [title, setTitle] = useState(''); const [description, setDescription] = useState(''); const [points, setPoints] = useState('100'); const [category, setCategory] = useState('');
  return <section className="admin-workspace"><FormCard title="Добавить задание" onSubmit={event => { event.preventDefault(); void onSubmit('quests/', { id, title, description, points: Number(points), category, active: true, order: quests.length }, 'Задание создано'); }}>
    <label><span>Код</span><input required pattern="[A-Za-zА-Яа-я0-9_-]+" value={id} onChange={e => setId(e.target.value)} placeholder="Q-01" /></label>
    <label><span>Название</span><input required value={title} onChange={e => setTitle(e.target.value)} /></label>
    <label><span>Описание</span><textarea value={description} onChange={e => setDescription(e.target.value)} /></label>
    <div className="form-row"><label><span>Максимум</span><input required min="1" type="number" value={points} onChange={e => setPoints(e.target.value)} /></label><label><span>Категория</span><input value={category} onChange={e => setCategory(e.target.value)} /></label></div>
  </FormCard><DataTable headers={['Задание', 'Категория', 'Максимум', '']} rows={quests.map(item => [item.title, item.category || '—', item.points, <button className="table-action danger" onClick={() => void onRemove(`quests/${item.id}/`)}><Trash2 size={15} /></button>])} /></section>;
}

function PenaltyAdmin({ teams, penalties, onSubmit, onRemove }: AdminProps & { teams: Team[]; penalties: Penalty[] }) {
  const [team, setTeam] = useState(''); const [reason, setReason] = useState(''); const [penalty, setPenalty] = useState('10');
  return <section className="admin-workspace"><FormCard title="Добавить штраф" onSubmit={event => { event.preventDefault(); void onSubmit('marks/', { team: Number(team), reason, penalty: Number(penalty) }, 'Штраф добавлен'); }}>
    <label><span>Команда</span><select required value={team} onChange={e => setTeam(e.target.value)}><option value="">Выберите</option>{teams.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</select></label>
    <label><span>Причина</span><input required maxLength={200} value={reason} onChange={e => setReason(e.target.value)} /></label>
    <label><span>Штраф</span><input required min="1" max="1000" type="number" value={penalty} onChange={e => setPenalty(e.target.value)} /></label>
  </FormCard><DataTable headers={['Команда', 'Причина', 'Штраф', '']} rows={penalties.map(item => [item.team_name, item.reason, `−${item.penalty}`, <button className="table-action danger" onClick={() => void onRemove(`marks/${item.id}/`)}><Trash2 size={15} /></button>])} /></section>;
}

function DataTable({ headers, rows }: { headers: string[]; rows: React.ReactNode[][] }) {
  return <div className="data-table glass"><table><thead><tr>{headers.map((header, i) => <th key={`${header}-${i}`}>{header}</th>)}</tr></thead><tbody>{rows.map((row, i) => <tr key={i}>{row.map((cell, j) => <td key={j}>{cell}</td>)}</tr>)}</tbody></table>{!rows.length && <div className="empty-state">Записей пока нет.</div>}</div>;
}
