import { Orbit } from 'lucide-react';
import { Link } from 'react-router-dom';

export function NotFoundPage() {
  return <div className="page centered not-found"><Orbit size={64} /><span className="eyebrow">404 · Lost in space</span><h1>Эта орбита не найдена</h1><Link className="button" to="/">Вернуться к рейтингу</Link></div>;
}
