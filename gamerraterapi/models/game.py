from django.utils import timezone
from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_user")
    title = models.TextField(unique=True)
    description = models.TextField()
    designer = models.TextField()
    release_year = models.DateField()
    players = models.ManyToManyField(User, through="GamePlayer", related_name="user")
    time_to_complete_estimate = models.IntegerField()
    recommended_age = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def average_rating(self):
        average = self.ratings.aggregate(Avg("rating"))["rating__avg"]
        return average if average is not None else 0
