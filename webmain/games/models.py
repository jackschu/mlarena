
from django.db import models
from django.utils import timezone


class Game(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True, null=True)
    file = models.FileField(null=True)

class Match(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    bot1 = models.ForeignKey('bots.Bot', on_delete=models.PROTECT, related_name='bot1')
    bot2 = models.ForeignKey('bots.Bot', on_delete=models.PROTECT, related_name='bot2')
    state = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    
class MatchRecord(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    did_bot1_win =  models.BooleanField()

class GameFrame(models.Model):
    frame_num = models.IntegerField()
    state = models.TextField()
    match_record = models.ForeignKey(MatchRecord, on_delete=models.CASCADE)


