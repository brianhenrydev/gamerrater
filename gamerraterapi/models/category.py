from django.db import models
from django.utils import timezone


class Category(models.Model):
    label = models.TextField(max_length=120)
    created_at = models.DateTimeField(default=timezone.now)
