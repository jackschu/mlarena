from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from games.models import Game, Match, MatchRecord
from bots.models import Bot

from trueskill import Rating, quality_1vs1, rate_1vs1
# Create your views here.

def view(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    
    bots_list = Bot.objects.filter(game=game).order_by('-score')
    return render(request, 'leaderboards/view.html', {'bots':bots_list}) 

def update_board(request, winner=None, match_pk=None):
    if winner==None or match_pk==None:
        messages.error(request, 'Resource not found for update_board')
        return HttpResponseRedirect('/')
    match = get_object_or_404(Match, pk=match_pk)
    record = MatchRecord()
    record.match = match
    record.did_bot1_win = (winner==1)
    record.save()
    rate_1 = Rating(mu=match.bot1.mu, sigma=match.bot1.sigma)
    rate_2 = Rating(mu=match.bot2.mu, sigma=match.bot2.sigma)
    if record.did_bot1_win:
        rate_1,rate_2 = rate_1vs1(rate_1, rate_2)
    else:
        rate_2,rate_1 = rate_1vs1(rate_2, rate_1)

    record.match.bot1.mu = rate_1.mu
    record.match.bot1.sigma = rate_1.sigma
    record.match.bot1.score = rate_1.mu - 3*rate_1.sigma
    record.match.bot1.games_played = record.match.bot1.games_played + 1
    
    record.match.bot2.mu = rate_2.mu
    record.match.bot2.sigma = rate_2.sigma
    record.match.bot2.score = rate_2.mu - 3*rate_2.sigma
    record.match.bot2.games_played = record.match.bot2.games_played + 1
