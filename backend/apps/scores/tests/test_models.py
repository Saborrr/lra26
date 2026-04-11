from django.test import TestCase

from teams.models import Team
from ..models import Score


class ScoreModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Test Team")
        self.score = Score.objects.create(
            team=self.team, quest_id="Q1", points=10
        )

    def test_str(self):
        expected = "Test Team - Q1: 10 pts"
        self.assertEqual(str(self.score), expected)

    def test_default_points(self):
        score = Score.objects.create(team=self.team, quest_id="Q2")
        self.assertEqual(score.points, 0)

    def test_ordering(self):
        Score.objects.create(team=self.team, quest_id="Q3", points=20, timestamp=self.score.timestamp)
        scores = list(Score.objects.all())
        self.assertEqual(scores[0].points, 20)