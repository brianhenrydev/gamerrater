from django.db import models
from django.utils import timezone

from gamerraterapi.models.game import Game
from django.contrib.auth.models import User


class GameImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, related_name="pictures")
    image = models.ImageField(
        upload_to="game_images/",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
