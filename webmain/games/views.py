from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import GameForm
from django.contrib import messages
# Create your views here.


def addGame(request):
    # a = "dataeihfjoqiej"
    # return render(request, 'games/viewGroup.html')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_game = form.save()
            print(new_game)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            messages.success(request, "You made a new game")
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GameForm()
    print(form)
    return render(request, 'games/viewGroup.html', {'form': form})


def viewGame(request, game_id=None):
    return HttpResponse('hi' + str(game_id))
