from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def addGame(request):
    a = "dataeihfjoqiej"
    return render(request, 'games/viewGroup.html')

    
def viewGame(request, game_id=None):
    return HttpResponse('hi' + str(game_id))
