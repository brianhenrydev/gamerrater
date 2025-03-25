from django.db import models
from gamerraterapi.models.category import Category
from django.utils import timezone
from gamerraterapi.models.game import Game
from django.contrib.auth.models import User


class GameCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
