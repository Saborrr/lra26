from django.test import TestCase

from ..models import Team


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            name="Test Team",
            trainer="Test Trainer",
            score=100,
        )

    def test_str(self):
        self.assertEqual(str(self.team), "Test Team (100 pts)")

    def test_default_score(self):
        team = Team.objects.create(name="No Score")
        self.assertEqual(team.score, 0)

    def test_ordering(self):
        Team.objects.create(name="High Score", score=200)
        teams = list(Team.objects.order_by("-score"))
        self.assertEqual(teams[0].score, 200)