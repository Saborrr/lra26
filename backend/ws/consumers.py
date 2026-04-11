import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from teams.models import Team


class LeaderboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("leaderboard", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("leaderboard", self.channel_name)

    async def score_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "score_update",
            "teams": await self.get_leaderboard(),
        }))

    @database_sync_to_async
    def get_leaderboard(self):
        teams = Team.objects.order_by("-score")[:10]  # top 10
        return [
            {
                "id": team.id,
                "name": team.name,
                "trainer": team.trainer,
                "score": team.score,
                "position": team.position,
            }
            for team in teams
        ]