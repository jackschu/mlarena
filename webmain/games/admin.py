from django.contrib import admin
from .models import Game, Match, MatchRecord
# Register your models here.
admin.site.register(Game)
admin.site.register(Match)
admin.site.register(MatchRecord)
