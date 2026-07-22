import { LayoutDashboard, LogIn, LogOut, Rocket, Shield, Trophy, UserRound } from 'lucide-react';
import { NavLink, Outlet } from 'react-router-dom';

import { useAuth } from '../contexts/AuthContext';
import { CosmicBackground } from './CosmicBackground';
import { Logo } from './Logo';

export function AppShell() {
  const { user, logout } = useAuth();
  return (
    <div className="app-shell">
      <CosmicBackground />
      <header className="topbar glass">
        <NavLink to="/" className="logo-link"><Logo /></NavLink>
        <nav aria-label="Главная навигация">
          <NavLink to="/" end><Trophy size={18} /> <span>Рейтинг</span></NavLink>
          {user && <NavLink to="/app"><UserRound size={18} /> <span>Кабинет</span></NavLink>}
          {user && user.role !== 'participant' && <NavLink to="/admin"><LayoutDashboard size={18} /> <span>Управление</span></NavLink>}
          {user?.role === 'superadmin' && <NavLink to="/superadmin"><Shield size={18} /> <span>Система</span></NavLink>}
        </nav>
        <div className="topbar-actions">
          {user ? (
            <button className="icon-button" onClick={() => void logout()} title="Выйти"><LogOut size={19} /></button>
          ) : (
            <NavLink className="button button-small" to="/login"><LogIn size={17} /> Войти</NavLink>
          )}
        </div>
      </header>
      <main><Outlet /></main>
      <footer>
        <Rocket size={15} /> LRA-26 · © 2026&nbsp;
        <a href="https://github.com/Saborrr/lra26" target="_blank" rel="noreferrer">Aleksandr Fadeev</a>
      </footer>
    </div>
  );
}
