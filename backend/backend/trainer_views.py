"""Views для интерфейса тренера — выставление оценок."""

import json
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.teams.models import Team
from apps.quests.models import Quest
from apps.scores.models import Score
from apps.penalties.models import BlackMark


class TrainerPanelView(TemplateView):
    """Страница тренерской — выбор квеста и выставление оценок."""
    template_name = "trainer.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["teams"] = list(
            Team.objects.select_related("trainer").all().values(
                "id", "name", "color", "score", "penalty",
                trainer_name="trainer__name",
            )
        )
        ctx["quests"] = list(
            Quest.objects.filter(active=True).order_by("order").values(
                "id", "title", "points", "category",
            )
        )
        # Существующие оценки
        scores = Score.objects.select_related("team", "quest").all()
        ctx["scores_json"] = json.dumps({
            f"{s.team_id}:{s.quest_id}": s.points for s in scores
        })
        return ctx


@method_decorator(csrf_exempt, name="dispatch")
class SaveScoresView(View):
    """API для сохранения оценок (без JWT, для тренерской)."""

    def post(self, request):
        try:
            data = json.loads(request.body)
            scores = data.get("scores", [])
            updated = 0

            for item in scores:
                team_id = item.get("team_id")
                quest_id = item.get("quest_id")
                points = item.get("points", 0)

                if not team_id or not quest_id:
                    continue

                score, created = Score.objects.update_or_create(
                    team_id=team_id,
                    quest_id=quest_id,
                    defaults={"points": points},
                )
                updated += 1

            # Оповещаем WebSocket
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync

            try:
                layer = get_channel_layer()
                if layer:
                    async_to_sync(layer.group_send)(
                        "leaderboard",
                        {"type": "score_update"},
                    )
            except Exception:
                pass

            return JsonResponse({"status": "ok", "updated": updated})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class AddBlackMarkView(View):
    """API для добавления чёрной метки."""

    def post(self, request):
        try:
            data = json.loads(request.body)
            team_id = data.get("team_id")
            reason = data.get("reason", "")
            penalty = data.get("penalty", 10)

            BlackMark.objects.create(
                team_id=team_id,
                reason=reason,
                penalty=penalty,
            )

            # Оповещаем WebSocket
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync

            try:
                layer = get_channel_layer()
                if layer:
                    async_to_sync(layer.group_send)(
                        "leaderboard",
                        {"type": "score_update"},
                    )
            except Exception:
                pass

            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)