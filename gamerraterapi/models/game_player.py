from django.db import models
from django.utils import timezone
from gamerraterapi.models.game import Game
from django.contrib.auth.models import User


class GamePlayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
