from math import pow
from django.db.models import Count
from django.utils import timezone
from random import random, randrange, shuffle
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from games.models import Game, Match, MatchRecord
from bots.models import Bot
from gcp.views import run_match

from trueskill import Rating, quality_1vs1, rate_1vs1
# Create your views here.

def view(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    
    bots_list = Bot.objects.filter(game=game).order_by('-score')
    return render(request, 'leaderboards/view.html', {'bots':bots_list, 'game':game}) 

def get_match_all_games():
    preid = Game.objects.annotate(toys_num=Count('bot')).filter(toys_num__gt=1).distinct()

    shuffle(list(preid))
    id = preid[0].id
    return _get_match(id)

def get_match(request, game_id):
    match = _get_match(game_id)
    return run_match(match)
    return HttpResponseRedirect(reverse('board:viewBoard',kwargs={'game_id':match.game.id}))
                
def _get_match(game_id):
    game = get_object_or_404(Game, pk=game_id)
    rankdiff = int(5 / pow(random() , 0.65))
    bot_list = Bot.objects.filter(game=game).order_by("last_played")
    print(bot_list)
    match = Match()
    match.game= game
    match.bot1= bot_list[0]
    bot1_id = bot_list[0].id
    bot_list.order_by("-score")
    print(match.bot1)
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
    match.bot2 = opp_list[0]
    match.state = 1
    match.save()
    return match

def update_match_winner(match, winner):
    return HttpResponseRedirect(reverse('board:matchUpdate',
                                        kwargs={'match_pk':match.id, 'winner':winner}))
        

def update_board(request, winner=None, match_pk=None):
    if winner==None or match_pk==None:
        messages.error(request, 'Resource not found for update_board')
        return HttpResponseRedirect('/')
    match = get_object_or_404(Match, pk=match_pk)
    match.state = 2;
    match.save()
    record = MatchRecord()
    record.match = match
    record.winner_number = winner
    record.save()
    rate_1 = Rating(mu=match.bot1.mu, sigma=match.bot1.sigma)
    rate_2 = Rating(mu=match.bot2.mu, sigma=match.bot2.sigma)
    if record.winner_number == 1:
        record.match.bot1.w +=1
        record.match.bot2.l +=1
        rate_1,rate_2 = rate_1vs1(rate_1, rate_2)
    elif record.winner_number == 2:
        record.match.bot2.w +=1
        record.match.bot1.l +=1
        rate_2,rate_1 = rate_1vs1(rate_2, rate_1)
    else:
        record.match.bot1.d +=1
        record.match.bot2.d +=1        
        rate_1,rate_2 = rate_1vs1(rate_1, rate_2, drawn=True)
    print(rate_1, rate_2)
    record.match.bot1.mu = rate_1.mu
    record.match.bot1.sigma = rate_1.sigma
    record.match.bot1.score = rate_1.mu - 3*rate_1.sigma
    record.match.bot1.games_played = record.match.bot1.games_played + 1
    
    record.match.bot2.mu = rate_2.mu
    record.match.bot2.sigma = rate_2.sigma
    record.match.bot2.score = rate_2.mu - 3*rate_2.sigma
    record.match.bot2.games_played = record.match.bot2.games_played + 1
    record.match.bot1.last_played = timezone.now()
    record.match.bot2.last_played = timezone.now()  
    record.match.bot1.save()
    record.match.bot2.save()    
    return HttpResponseRedirect(reverse('board:viewBoard',kwargs={'game_id':match.game.id}))
