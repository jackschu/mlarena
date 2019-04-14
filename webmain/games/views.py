import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import GameForm
from .models import Game
from django.contrib import messages
from django.urls import reverse
from gcp.views import create_cloudfunction
# Create your views here.


def addGame(request):
    # a = "dataeihfjoqiej"
    # return render(request, 'games/viewGroup.html')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GameForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            new_game = form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            with open(new_game.file.path, 'rb') as fp:
                print(fp)
                create_cloudfunction(fp, str(new_game.id), "game")
                
            messages.success(request, "You made a new game")
            return HttpResponseRedirect(reverse('gcp:test_cloudfunction'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GameForm()
    return render(request, 'games/viewGroup.html', {'form': form})


def viewAll(request):
    games_list = Game.objects.all()

    return render(request, 'games/viewAll.html', {'games':games_list})

def viewGame(request, game_id=None):
    game = None
    if game_id:
        game = Game.objects.get(pk=game_id)
    return render(request, 'games/viewGame.html', {'game':game})


