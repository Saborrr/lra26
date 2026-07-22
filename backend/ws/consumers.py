from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class LeaderboardConsumer(AsyncJsonWebsocketConsumer):
    group_name = "leaderboard"

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_leaderboard()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def score_update(self, event):
        await self.send_json({"type": "leaderboard.updated", "teams": event["teams"]})

    async def send_leaderboard(self):
        await self.send_json({"type": "leaderboard.updated", "teams": await self.get_teams()})

    @database_sync_to_async
    def get_teams(self):
        from api.views import leaderboard_teams
        from apps.teams.serializers import TeamLeaderboardSerializer

        return TeamLeaderboardSerializer(leaderboard_teams(), many=True).data
