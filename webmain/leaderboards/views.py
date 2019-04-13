from django.shortcuts import render, redirect, get_object_or_404
from games.models import Game
from bots.models import Bot
# Create your views here.

def view(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    
    bots_list = Bot.objects.filter(game=game).order_by('-score')
    return render(request, 'leaderboards/view.html', {'bots':bots_list}) 
