from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Game, Score, GameState, Purchases

class IndexView(generic.View):

    def get(self, request):
        return HttpResponse("Hello, world. You're at the hello index.")

class HomeView(generic.View):

    def get(self, request):    
        testlist = ['test1', 'test2', 'test3']
        context = {'dict': testlist}
        template_name = 'hello/home.html'
        return render(request, template_name, context)

class GameListView(generic.ListView):
    """Generic view for the list of games.
    It creates a context called object_list to be used in templates."""
    template_name = 'hello/gamelist.html'
    model = Game

class GameDetailView(generic.DetailView):
    """Generic view for a single game."""
    model = Game
    template_name = 'hello/gamedetail.html'

class ScoreDetailView(generic.DetailView):
    model = Score
    template_name = 'hello/scoredetail.html'

