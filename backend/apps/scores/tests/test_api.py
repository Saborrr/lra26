from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from teams.models import Team
from ..models import Score


class ScoreAPITest(APITestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Test Team")
        self.score_data = {
            "team": self.team.id,
            "quest_id": "Q1",
            "points": 10,
        }
        self.score = Score.objects.create(**self.score_data)

    def test_list_scores(self):
        response = self.client.get(reverse("score-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_score(self):
        response = self.client.post(reverse("score-list"), self.score_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Score.objects.count(), 2)