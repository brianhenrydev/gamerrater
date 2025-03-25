from django.db import models
from django.utils import timezone

from gamerraterapi.models.game import Game
from django.contrib.auth.models import User


class GameReview(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ["user", "game"]
