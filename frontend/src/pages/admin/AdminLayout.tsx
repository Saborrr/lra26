import { useState, useEffect, ReactNode } from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';

const navItems = [
  { path: '/admin', icon: '📊', label: 'Главная', exact: true },
  { path: '/admin/teams', icon: '👥', label: 'Команды' },
  { path: '/admin/scores', icon: '🏆', label: 'Результаты' },
  { path: '/admin/quests', icon: '📋', label: 'Квесты' },
  { path: '/admin/trainers', icon: '🎓', label: 'Тренеры' },
  { path: '/admin/marks', icon: '⚫', label: 'Метки' },
];

export function AdminLayout() {
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div style={styles.container}>
      {/* Stars background */}
      <canvas id="stars-bg" style={styles.stars}></canvas>
      <div style={styles.nebula}></div>

      {/* Header */}
      <header style={styles.header}>
        <button style={styles.burger} onClick={() => setSidebarOpen(!sidebarOpen)}>
          ☰
        </button>
        <h1 style={styles.logo}>🚀 ЛРА-2026</h1>
        <a href="/" style={styles.exitBtn}>На сайт →</a>
      </header>

      <div style={styles.body}>
        {/* Sidebar */}
        <nav style={{...styles.sidebar, ...(sidebarOpen ? styles.sidebarOpen : {})}}>
          {navItems.map(item => {
            const isActive = item.exact
              ? location.pathname === item.path
              : location.pathname.startsWith(item.path);
            return (
              <Link
                key={item.path}
                to={item.path}
                style={{...styles.navItem, ...(isActive ? styles.navItemActive : {})}}
                onClick={() => setSidebarOpen(false)}
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Content */}
        <main style={styles.content}>
          <Outlet />
        </main>
      </div>

      {/* Stars animation */}
      <script dangerouslySetInnerHTML={{__html: `
        const c=document.getElementById('stars-bg');
        if(c) {
          const ctx=c.getContext('2d');
          c.width=window.innerWidth; c.height=window.innerHeight;
          const s=Array.from({length:150},()=>({x:Math.random()*c.width,y:Math.random()*c.height,r:Math.random()*1.2+0.5,o:Math.random()*0.8+0.2}));
          function d(){ctx.clearRect(0,0,c.width,c.height);s.forEach(st=>{st.y+=0.02;if(st.y>c.height)st.y=0;ctx.beginPath();ctx.arc(st.x,st.y,st.r,0,Math.PI*2);ctx.fillStyle='rgba(255,255,255,'+st.o+')';ctx.fill()});requestAnimationFrame(d)}d();
        }
      `}} />
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { minHeight: '100vh', fontFamily: "'Exo 2', sans-serif", color: '#fff', position: 'relative' },
  stars: { position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', zIndex: 0, pointerEvents: 'none' },
  nebula: { position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', zIndex: 0, background: 'radial-gradient(circle at 50% 50%, transparent 40%, rgba(20,40,80,0.8) 70%, rgba(0,0,20,1) 100%)', pointerEvents: 'none' },
  header: {
    position: 'relative', zIndex: 10,
    background: 'rgba(10,10,30,0.9)', backdropFilter: 'blur(25px)',
    borderBottom: '1px solid rgba(100,200,255,0.3)',
    padding: '15px 20px', display: 'flex', alignItems: 'center', gap: '15px',
  },
  burger: { background: 'none', border: 'none', color: '#00ffff', fontSize: '1.5em', cursor: 'pointer', display: 'none' },
  logo: { flex: 1, fontSize: '1.3em', background: 'linear-gradient(135deg, #00ffff, #ff00ff)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' },
  exitBtn: { color: '#00ff88', textDecoration: 'none', fontSize: '0.9em' },
  body: { display: 'flex', position: 'relative', zIndex: 5, minHeight: 'calc(100vh - 60px)' },
  sidebar: {
    width: '220px', background: 'rgba(10,10,30,0.85)', backdropFilter: 'blur(30px)',
    borderRight: '1px solid rgba(0,255,255,0.2)', padding: '15px 0',
    transition: '0.3s', flexShrink: 0,
  },
  sidebarOpen: {},
  navItem: {
    display: 'flex', alignItems: 'center', gap: '10px', padding: '12px 20px',
    color: 'rgba(255,255,255,0.7)', textDecoration: 'none', fontSize: '0.95em',
    transition: '0.2s', borderLeft: '3px solid transparent',
  },
  navItemActive: { color: '#00ffff', background: 'rgba(0,255,255,0.05)', borderLeftColor: '#00ffff' },
  content: { flex: 1, padding: '25px', overflow: 'auto' },
};

// Mobile styles are injected via CSS
const styleMobile = document.createElement('style');
styleMobile.textContent = `
  @media (max-width: 768px) {
    .admin-header button { display: block !important; }
    nav { position: fixed; left: -220px; top: 60px; bottom: 0; z-index: 100; }
    nav.open { left: 0; }
    main { padding: 15px !important; }
  }
`;
document.head.appendChild(styleMobile);
