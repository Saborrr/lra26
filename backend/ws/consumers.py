"""WebSocket consumers для real-time рейтинга."""

import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from apps.teams.models import Team


class LeaderboardConsumer(AsyncWebsocketConsumer):
    """Consumer для real-time обновлений рейтинга."""

    async def connect(self):
        """Подключение к группе leaderboard."""
        await self.channel_layer.group_add("leaderboard", self.channel_name)
        await self.accept()
        # Отправляем текущий рейтинг при подключении
        await self.send(
            text_data=json.dumps(
                {"type": "connected", "teams": await self.get_leaderboard()}
            )
        )

    async def disconnect(self, close_code):
        """Отключение от группы."""
        await self.channel_layer.group_discard("leaderboard", self.channel_name)

    async def receive(self, text_data):
        """Обработка входящих сообщений."""
        try:
            data = json.loads(text_data)
            if data.get("type") == "ping":
                await self.send(text_data=json.dumps({"type": "pong"}))
            elif data.get("type") == "get_leaderboard":
                await self.send(
                    text_data=json.dumps(
                        {"type": "leaderboard", "teams": await self.get_leaderboard()}
                    )
                )
        except json.JSONDecodeError:
            await self.send(
                text_data=json.dumps({"type": "error", "message": "Invalid JSON"})
            )

    async def score_update(self, event):
        """Обработка события обновления очков."""
        await self.send(
            text_data=json.dumps(
                {"type": "score_update", "teams": await self.get_leaderboard()}
            )
        )

    @database_sync_to_async
    def get_leaderboard(self):
        """Получение рейтинга команд из БД."""
        teams = Team.objects.select_related("trainer").all()
        # Сортируем по итоговому баллу
        teams = sorted(teams, key=lambda t: t.score - t.penalty, reverse=True)
        return [
            {
                "id": team.id,
                "name": team.name,
                "trainer_name": team.trainer.name if team.trainer else None,
                "score": team.score,
                "penalty": team.penalty,
                "total_score": team.score - team.penalty,
                "color": team.color,
                "position": idx + 1,
            }
            for idx, team in enumerate(teams)
        ]