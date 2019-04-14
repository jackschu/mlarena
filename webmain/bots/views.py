from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import BotForm
from .models import Bot
from django.contrib import messages
from games.models import Game, Match
from django.db.models import Q

# Create your views here.

def addBot(request, game_id=None):
    game = Game.objects.get(pk=game_id)
    form = BotForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            new_bot = form.save(game=game)
            messages.success(request, 'You made a new bot')
            return HttpResponseRedirect('/')
    else:
        form = BotForm()
        
    return render(request, 'bots/botForm.html', {'form': form, 'game':game})

def viewBot(request, bot_id=None):
    bot = None
    if bot_id:
        bot = Bot.objects.get(pk=bot_id)
    matches = Match.objects.filter((Q(bot1=bot) | Q(bot2=bot)) & Q(state=2))
    return render(request, 'bots/viewBot.html', {'bot':bot, 'matches':matches})

def viewMatch(request, match_id=None):
    match = None
    if match_id:
        pass # TODO something
    return render(request, 'bots/canvas.html', {})
