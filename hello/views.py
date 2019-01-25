from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Game, Score, GameState, Purchases
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#def save_game(request, game_id):
#    return HttpResponse("You have called save_game function")

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

class DeveloperView(generic.View):

    def get(self, request):
        testlist = ['test1', 'test2', 'test3']
        context = {'dict': testlist}
        template_name = 'hello/developer.html'
        return render(request, template_name, context)

class HighScoreView(generic.ListView):
    template_name = 'hello/highscores.html'
    model = Score

class ShopView(generic.ListView):
    template_name = 'hello/shop.html'
    model = Game

class GameDetailView(generic.DetailView):
    """Generic view for a single game."""
    model = Game
    template_name = 'hello/gamedetail.html'

    def save_game(self, **kwargs):
        return HttpResponse("You have called in class save_game function " + str(self.request.user))

class GameSaveView(generic.DetailView):
    """Generic view for a single game."""
    model = Game
    template_name = 'hello/gamedetail.html'

    def post(self, *args, **kwargs):
        
        return HttpResponse("You have called in class save_game function " +str(kwargs) + str(self.request.user))


class ScoreDetailView(generic.DetailView):
    model = Score
    template_name = 'hello/scoredetail.html'

class LoginView(generic.View):
    def login(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        template_name = 'hello/login.html'
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponse("Login succesful")
        else:
            # Return an 'invalid login' error message.
            return HttpResponse("Invalid login")

class LogoutView(generic.View):
    def logout_view(self, request):
        logout(request)
        # Redirect to a success page.
        return HttpResponse("Logout succesful")
