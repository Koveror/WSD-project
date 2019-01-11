from django.shortcuts import render
from django.http import HttpResponse
from .models import Game, Score, GameState, Purchases

def index(request):
    return HttpResponse("Hello, world. You're at the hello index.")

def home(request):
    return HttpResponse("Hello, this is home page.")

def gamelist(request):
    games = Game.objects.all()
    str = ''
    for game in games:
        str = str + game.name + ' '
    return HttpResponse(str)

def score(request, gameId, userId):
    scoreObject = Score.objects.get(gameid = gameId, userid = userId)
    return HttpResponse(scoreObject.score)

def purchases(request, userId):
    usersPurchases = Purchases.objects.filter(userid = userId)
    str = ''
    for buy in purchases:
        str = str + buy.gameid + ' '
    return HttpResponse(str)

def gamestate(request, userId, gameId):
    state = GameState.objects.get(gameid = gameId, userid = userId)
    return HtppResponse(state.gameState)