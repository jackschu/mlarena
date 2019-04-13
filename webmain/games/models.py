from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True, null=True)
    file = models.FileField()
