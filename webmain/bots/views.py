from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import BotForm
from .models import Bot
from django.contrib import messages
from gcp.views import create_cloudfunction
from games.models import Game

# Create your views here.

def addBot(request, game_id=None):
    game = Game.objects.get(pk=game_id)
    form = BotForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            new_bot = form.save(game=game)
            with open(new_bot.file.path, 'rb') as fp:
                create_cloudfunction(fp, "bot" + str(new_bot.id), "bot")
                
            messages.success(request, 'You made a new bot')
            return HttpResponseRedirect('/')
    else:
        form = BotForm()
        
    return render(request, 'bots/botForm.html', {'form': form, 'game':game})

def viewBot(request, bot_id=None):
    bot = None
    if bot_id:
        bot = Bot.objects.get(pk=bot_id)
    return render(request, 'bots/viewBot.html', {'bot':bot})
