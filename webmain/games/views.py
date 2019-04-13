from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import GameForm
from .models import Game
from django.contrib import messages
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
            print(new_game)
            print(request.FILES['file'])
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            messages.success(request, "You made a new game")
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        print('fooaof\n\n\n\n\n')
        form = GameForm()
    print(form)
    return render(request, 'games/viewGroup.html', {'form': form})


def viewAll(request):
    games_list = Game.objects.all()

    return render(request, 'games/viewAll.html', {'games':games_list})

def viewGame(request, game_id=None):
    game = None
    if game_id:
        game = Game.objects.get(pk=game_id)
    return render(request, 'games/viewGame.html', {'game':game})
