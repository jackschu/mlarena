from math import pow
from random import random
from django.urls import reverse, reverse_lazy
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

def get_match(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    rankdiff = int(5 / pow(random() , 0.65))
    bot_list = Bot.objects.filter(game=game).order_by("-last_played")
    match = Match()
    match.game= game
    match.bot1= bot_list[0]
    bot1_id = bot_list[0].id
    bot_list.order_by("-score")
    print(bot_list)
    opp_list = []
    for i in range(len(bot_list)):
        if bot_list[i].id == bot1_id:
            print(i, len(bot_list))
            opp_list += (bot_list[max(i-rankdiff,0):i])
            if(i+1 < len(bot_list)):
                opp_list += (bot_list[i+1:min(i+rankdiff, len(bot_list))])
            break
    bot1_rate = Rating(mu=match.bot1.mu, sigma=match.bot1.sigma)
    print(opp_list)
    opp_list = sorted(opp_list, key= lambda x: (
        x.games_played, -quality_1vs1(Rating(mu=x.mu,sigma=x.sigma), bot1_rate)))
    print(opp_list)
    return HttpResponseRedirect('/')

                
        

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
    print(rate_1, rate_2)
    record.match.bot1.mu = rate_1.mu
    record.match.bot1.sigma = rate_1.sigma
    record.match.bot1.score = rate_1.mu - 3*rate_1.sigma
    record.match.bot1.games_played = record.match.bot1.games_played + 1
    
    record.match.bot2.mu = rate_2.mu
    record.match.bot2.sigma = rate_2.sigma
    record.match.bot2.score = rate_2.mu - 3*rate_2.sigma
    record.match.bot2.games_played = record.match.bot2.games_played + 1
    record.match.bot1.save()
    record.match.bot2.save()    
    return HttpResponseRedirect(reverse('board:viewBoard',kwargs={'game_id':match.game.id}))
