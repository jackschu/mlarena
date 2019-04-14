from django.db import models
from datetime import datetime
from games.models import Game

class Bot(models.Model):
    name = models.CharField(max_length=50)
    mu = models.FloatField(default=25.)
    sigma = models.FloatField(default=25/3)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    w = models.IntegerField(default=0)
    l = models.IntegerField(default=0)
    d = models.IntegerField(default=0)        
    score = models.FloatField(default=0)
    games_played = models.IntegerField(default=0)
    last_played = models.DateTimeField(default=datetime(2009, 12, 20, 0, 0))
    file = models.FileField(null=True)
    
    def __str__(self):
        return self.name
