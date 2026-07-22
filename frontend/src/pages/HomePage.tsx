import { ArrowRight, Bot, Globe2, ShieldCheck, Smartphone } from 'lucide-react';
import { Link } from 'react-router-dom';

import { Leaderboard } from '../components/Leaderboard';
import { useAuth } from '../contexts/AuthContext';

export function HomePage() {
  const { user } = useAuth();
  return (
    <div className="page home-page">
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow"><span className="pulse-dot" /> Миссия 27–29 мая 2026</span>
          <h1>Ваша команда.<br /><span>Ваша орбита.</span></h1>
          <p>Live-рейтинг Слёта лидеров рабочего актива. Следите за движением экипажей, заданиями и личным прогрессом в одном приложении.</p>
          <div className="hero-actions">
            <Link className="button" to={user ? '/app' : '/login'}>{user ? 'Открыть кабинет' : 'Войти в миссию'} <ArrowRight size={18} /></Link>
            <a className="button button-ghost" href="#ranking">Смотреть рейтинг</a>
          </div>
          <div className="platform-strip">
            <span><Globe2 /> Web</span><span><Smartphone /> iOS · Android</span><span><Bot /> Telegram · VK</span><span><ShieldCheck /> Защищено</span>
          </div>
        </div>
        <div className="planet-stage" aria-hidden="true">
          <div className="planet"><span className="planet-grid" /></div>
          <div className="planet-ring" />
          <div className="satellite">26</div>
        </div>
      </section>
      <div id="ranking"><Leaderboard /></div>
    </div>
  );
}
