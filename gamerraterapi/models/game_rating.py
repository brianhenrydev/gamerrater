from django.db import models
from gamerraterapi.models.game import Game
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class GameRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rating")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(
        default=1, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    class Meta:
        unique_together = ["user", "game"]
