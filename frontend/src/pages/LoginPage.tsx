import { KeyRound, LockKeyhole, Send, Sparkles } from 'lucide-react';
import { type FormEvent, useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';

import { useAuth } from '../contexts/AuthContext';

export function LoginPage() {
  const { user, error, login, linkPlatform, platformNeedsLink } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [code, setCode] = useState('');
  const [busy, setBusy] = useState(false);

  if (user) return <Navigate to="/app" replace />;

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setBusy(true);
    try {
      if (platformNeedsLink) await linkPlatform(code);
      else await login(username, password);
      navigate('/app');
    } catch { /* message is rendered from context */ } finally { setBusy(false); }
  };

  return (
    <div className="page auth-page centered">
      <section className="auth-card glass">
        <div className="auth-orb"><Sparkles /></div>
        <span className="eyebrow">Secure access</span>
        <h1>{platformNeedsLink ? 'Привязка к миссии' : 'Вход в систему'}</h1>
        <p>{platformNeedsLink ? 'Введите одноразовый код, который выдал администратор. Код действует 15 минут.' : 'Используйте учётную запись участника или администратора.'}</p>
        <form onSubmit={event => void submit(event)}>
          {platformNeedsLink ? (
            <label><span><KeyRound size={16} /> Одноразовый код</span><input autoFocus required value={code} onChange={event => setCode(event.target.value.toUpperCase())} placeholder="AB12-CD34-EF56" autoComplete="one-time-code" /></label>
          ) : (
            <>
              <label><span><Send size={16} /> Логин</span><input required value={username} onChange={event => setUsername(event.target.value)} autoComplete="username" /></label>
              <label><span><LockKeyhole size={16} /> Пароль</span><input required type="password" value={password} onChange={event => setPassword(event.target.value)} autoComplete="current-password" /></label>
            </>
          )}
          {error && <div className="form-error" role="alert">{error}</div>}
          <button className="button full-width" disabled={busy}>{busy ? 'Проверяем…' : platformNeedsLink ? 'Привязать аккаунт' : 'Войти'}</button>
        </form>
        <small className="security-note"><LockKeyhole size={13} /> Пароль и platform-токены не сохраняются в браузере.</small>
      </section>
    </div>
  );
}
