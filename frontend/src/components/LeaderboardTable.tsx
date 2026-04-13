import { LucideIcon } from 'lucide-react';
import { Crown, Users, Award } from 'lucide-react';
import { clsx } from 'clsx';

interface Team {
  id: number;
  name: string;
  trainer_name: string | null;
  score: number;
  penalty: number;
  total_score: number;
  color: string;
  position: number | null;
}

interface LeaderboardTableProps {
  teams: Team[];
}

export function LeaderboardTable({ teams }: LeaderboardTableProps) {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center font-bold neon-text uppercase tracking-wider">
        <div>Позиция</div>
        <div>Команда</div>
        <div>Счёт</div>
        <div>Итог</div>
      </div>
      {teams.map((team, index) => (
        <div key={team.id} className={clsx(
          'glass-card leaderboard-row p-6 flex items-center justify-between md:justify-start md:space-x-6',
          index === 0 && 'border-l-4 border-neon-green shadow-neon-green'
        )}>
          <div className="text-2xl font-bold neon-gold">
            {team.position || index + 1}
            {index === 0 && <Crown className="inline ml-2 w-6 h-6" />}
          </div>
          <div className="flex-1 font-semibold neon-text">
            <div className="text-lg">{team.name}</div>
            <div className="text-sm opacity-75">{team.trainer_name || 'Без тренера'}</div>
          </div>
          <div className="text-right">
            <div className={clsx('font-bold text-2xl', team.color === '#00ff88' ? 'neon-green' : 'neon-purple')}>
              {team.score}
            </div>
            <div className="text-sm opacity-75 -mt-1">-{team.penalty}</div>
          </div>
          <div className="font-bold text-2xl neon-gold">
            {team.total_score}
            <Users className="inline ml-1 w-5 h-5 opacity-75" />
          </div>
        </div>
      ))}
    </div>
  );
}