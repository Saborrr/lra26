import { GlassCard } from '../components/GlassCard';
import { StarField } from '../components/StarField';
import { LeaderboardTable } from '../components/LeaderboardTable';
import { useLeaderboard } from '../services/api';
import { useLeaderboardWS } from '../hooks/useWebSocket';

export function LeaderboardPage() {
  const { data: teams = [], isLoading, isError, error } = useLeaderboard();
  useLeaderboardWS();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="neon-text text-2xl animate-pulse">Загрузка рейтинга...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen relative overflow-hidden">
      <StarField />
      <div className="relative z-10 pt-20 pb-10 px-4 md:px-8 max-w-6xl mx-auto">
        <GlassCard className="text-center mb-12">
          <h1 className="neon-text text-5xl md:text-6xl font-bold mb-4">
            🚀 LRA-26 Лидерборд
          </h1>
          <p className="opacity-75 text-lg">Live рейтинг команд Слёта Лидеров Рабочего Актива</p>
        </GlassCard>

        {isError && (
          <GlassCard className="text-center mb-8 border-red-500/50">
            <p className="text-red-400 text-lg">
              ⚠️ Ошибка загрузки данных: {error instanceof Error ? error.message : 'Неизвестная ошибка'}
            </p>
            <p className="opacity-60 mt-2">Попробуйте обновить страницу</p>
          </GlassCard>
        )}

        {!isError && teams.length === 0 && (
          <GlassCard className="text-center">
            <p className="neon-text text-xl">Команды пока не добавлены</p>
            <p className="opacity-60 mt-2">Данные появятся, когда будут созданы команды</p>
          </GlassCard>
        )}

        {teams.length > 0 && (
          <GlassCard padding="p-2 md:p-8">
            <LeaderboardTable teams={teams} />
          </GlassCard>
        )}
      </div>
    </div>
  );
}
