from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Game, Score, GameState, Purchases
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


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

        def is_member(user):
            return user.groups.filter(name='Developer').exists()

        def make_developer(user):
            my_group = Group.objects.get(name='Developer')
            my_group.user_set.add(user)

        context = {'is_a_developer': is_member(request.user)}
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
    def get(self, request):
        context = {'msg': "Please enter a username and a password"}
        template_name = 'hello/login.html'
        return render(request, template_name, context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        template_name = 'hello/login.html'
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            context = {'msg': "Login succesful"}
            return render(request, 'hello/home.html', context)
        else:
            # Return an 'invalid login' error message.
            context = {'msg': "Invalid login"}
            return render(request, 'hello/login.html', context)

class LogoutView(generic.View):

    def get(self, request):
        logout(request)
        # Redirect to a success page.
        context = {'msg': "This is not used for anything"}
        return render(request, 'hello/logout.html', context)

class RegisterView(generic.View):

    def get(self, request):
        context = {'msg': "Please enter a username and a password"}
        template_name = 'hello/register.html'
        return render(request, template_name, context)
