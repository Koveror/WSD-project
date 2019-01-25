import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from .models import Game, Score, GameState, Purchases
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

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

    @login_required
    @user_passes_test(lambda u: u.groups.filter(name='Developer').count() == 0, login_url='/hello/denied/')
    def not_in_developer_group(self, user):
        if user:
            return user.groups.filter(name='Developer').count() == 0
        return False

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

class GameSaveView(generic.DetailView):
    """View for saving gamestates. The save message is posted to this view using ajax."""
    model = Game
    template_name = 'hello/gamedetail.html'

    #FIXME: Check for login
    #@login_required
    def post(self, *args, **kwargs):
        """Method for saving data"""
        message = json.loads(self.request.body)
        game_state_str = str(message.get('gameState'))

        #FIXME: Find correct user and game!
        #FIXME: Try-catch here
        user = User.objects.get(id = 1)
        game = Game.objects.get(gameid = 1)

        game_state = GameState(
            userid = user,
            gameid = game,
            gameState = game_state_str,
            timestamp = datetime.now()
        )

        game_state.save()

        save_message = {'message' : 'Successfully saved'}
        return JsonResponse(save_message)


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
        context = {'msg': "Logout succesful"}
        return render(request, 'hello/logout.html', context)


class SignupView(generic.View):
    def signup(self, request):
        template_name = 'hello/signup.html'
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
