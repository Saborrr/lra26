import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.penalties.models import BlackMark
from apps.quests.models import Quest
from apps.scores.models import Score
from apps.teams.models import Team

User = get_user_model()


@pytest.fixture
def quest():
    return Quest.objects.create(id="Q-01", title="Launch", points=100)


@pytest.fixture
def team():
    return Team.objects.create(name="Aurora")


@pytest.mark.django_db
def test_score_writes_require_admin(team, quest):
    client = APIClient()
    payload = {"team": team.pk, "quest": quest.pk, "points": 50}
    assert client.post("/api/scores/", payload, format="json").status_code == 401

    participant = User.objects.create_user(username="crew", password="long-test-password")
    client.force_authenticate(participant)
    assert client.post("/api/scores/", payload, format="json").status_code == 403

    admin = User.objects.create_user(username="admin", password="long-test-password", is_staff=True)
    client.force_authenticate(admin)
    assert client.post("/api/scores/", payload, format="json").status_code == 201
    team.refresh_from_db()
    assert team.score == 50


@pytest.mark.django_db
def test_score_cannot_exceed_quest_maximum(team, quest):
    admin = User.objects.create_user(username="admin", is_staff=True)
    client = APIClient()
    client.force_authenticate(admin)
    response = client.post(
        "/api/scores/",
        {"team": team.pk, "quest": quest.pk, "points": 101},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_repeated_score_updates_existing_result(team, quest):
    admin = User.objects.create_user(username="admin", is_staff=True)
    client = APIClient()
    client.force_authenticate(admin)
    payload = {"team": team.pk, "quest": quest.pk, "points": 20}
    assert client.post("/api/scores/", payload, format="json").status_code == 201
    payload["points"] = 75
    assert client.post("/api/scores/", payload, format="json").status_code == 200
    assert Score.objects.get(team=team, quest=quest).points == 75
    assert Score.objects.filter(team=team, quest=quest).count() == 1


@pytest.mark.django_db
def test_penalty_must_be_positive(team):
    admin = User.objects.create_user(username="admin", is_staff=True)
    client = APIClient()
    client.force_authenticate(admin)
    response = client.post(
        "/api/marks/",
        {"team": team.pk, "reason": "test", "penalty": -10},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_only_superadmin_can_manage_users():
    staff = User.objects.create_user(username="staff", is_staff=True)
    root = User.objects.create_superuser(username="root", password="long-test-password")
    client = APIClient()
    client.force_authenticate(staff)
    assert client.get("/api/auth/users/").status_code == 403
    client.force_authenticate(root)
    assert client.get("/api/auth/users/").status_code == 200


@pytest.mark.django_db
def test_admin_gets_minimal_participant_directory():
    User.objects.create_user(
        username="participant", first_name="Alex", email="private@example.test"
    )
    admin = User.objects.create_user(username="admin", is_staff=True)
    client = APIClient()
    client.force_authenticate(admin)
    response = client.get("/api/auth/participants/")
    assert response.status_code == 200
    assert response.data[0]["username"] == "participant"
    assert "email" not in response.data[0]


@pytest.mark.django_db
def test_leaderboard_is_public_but_scores_are_not(team, quest):
    client = APIClient()
    assert client.get("/api/leaderboard/").status_code == 200
    assert client.get("/api/scores/").status_code == 401


@pytest.mark.django_db
def test_reassigning_results_updates_both_teams(team, quest):
    other = Team.objects.create(name="Nebula")
    score = Score.objects.create(team=team, quest=quest, points=40)
    mark = BlackMark.objects.create(team=team, reason="Delay", penalty=7)
    team.refresh_from_db()
    assert (team.score, team.penalty) == (40, 7)

    score.team = other
    score.save(update_fields=["team"])
    mark.team = other
    mark.save(update_fields=["team"])
    team.refresh_from_db()
    other.refresh_from_db()
    assert (team.score, team.penalty) == (0, 0)
    assert (other.score, other.penalty) == (40, 7)


@pytest.mark.django_db
def test_penalty_author_cannot_be_reassigned(team):
    admin = User.objects.create_user(username="admin", is_staff=True)
    client = APIClient()
    client.force_authenticate(admin)
    created = client.post(
        "/api/marks/",
        {"team": team.pk, "reason": "Delay", "penalty": 5},
        format="json",
    )
    assert created.status_code == 201
    response = client.patch(
        f"/api/marks/{created.data['id']}/",
        {"given_by": 999999},
        format="json",
    )
    assert response.status_code == 200
    assert response.data["given_by"] is None
