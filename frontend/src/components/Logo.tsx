import { Orbit } from 'lucide-react';

export function Logo({ compact = false }: { compact?: boolean }) {
  return (
    <div className="brand" aria-label="LRA-26">
      <span className="brand-mark"><Orbit size={24} /></span>
      {!compact && <span><strong>LRA</strong><em>26</em></span>}
    </div>
  );
}
