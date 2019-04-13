from django.db import models
from games.models import Game

class Bot(models.Model):
    name = models.CharField(max_length=50)
    mu = models.FloatField(default=25.)
    sigma = models.FloatField(default=25/3)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    games_played = models.IntegerField(default=0)
    def __str__(self):
        return self.name
