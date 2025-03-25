from django.db import models
from gamerraterapi.models.game import Game
from django.contrib.auth.models import User


class GameRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ["user", "game"]
