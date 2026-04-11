from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from ..models import Team


class TeamAPITest(APITestCase):
    def setUp(self):
        self.team_data = {
            "name": "API Team",
            "trainer": "API Trainer",
            "score": 50,
        }
        self.team = Team.objects.create(**self.team_data)

    def test_list_teams(self):
        response = self.client.get(reverse("team-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "API Team")

    def test_create_team(self):
        response = self.client.post(reverse("team-list"), self.team_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)

    def test_update_team(self):
        response = self.client.patch(
            reverse("team-detail", kwargs={"pk": self.team.pk}),
            {"score": 75},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.team.refresh_from_db()
        self.assertEqual(self.team.score, 75)