import json
from datetime import datetime
from hashlib import md5
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
import django.core.exceptions
from .models import Game, Score, GameState, Purchases
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(generic.View):

    def get(self, request):
        return HttpResponse("Hello, world. You're at the hello index.")

class HomeView(generic.View):

    def get(self, request):
        testlist = ['test1', 'test2', 'test3']
        context = {'dict': testlist}
        template_name = 'hello/home.html'
        return render(request, template_name, context)

class GameListView(LoginRequiredMixin, generic.View):
    login_url = 'hello:login'

    def get(self, request):
        purchases = Purchases.objects.filter(userid=request.user)
        template_name = 'hello/gamelist.html'
        return render(request, template_name, {'purchases': purchases})

class DeveloperView(LoginRequiredMixin, generic.View):
    login_url = 'hello:login'

    #Add the user to the developer-group
    def make_developer(user):
        my_group = Group.objects.get(name='Developer')
        my_group.user_set.add(user)

    def get(self, request):
        #Test if user belongs to developer-group
        is_member = request.user.groups.filter(name='Developer').exists()
        #Generate a list of developer's games
        games = Game.objects.filter(developerid=request.user)

        context = {'is_a_developer': is_member, 'games': games}
        return render(request, 'hello/developer.html', context)

    def post(self, request):
        #Create a new game
        name = request.POST['name']
        price = request.POST['price']
        genre = request.POST['genre']
        URL = request.POST['URL']
        description = request.POST['description']
        newgame = Game.objects.create(name=name,
                       price=price,
                       genre=genre,
                       URL=URL,
                       developerid=request.user,
                       numberSold=0,
                       dateCreated=datetime.now(),
                       description=description
                       )
        #Test if user belongs to developer-group
        is_member = request.user.groups.filter(name='Developer').exists()
        #Generate a list of developer's games
        games = Game.objects.filter(developerid=request.user)
        context = {'is_a_developer': is_member, 'games': games, 'msg': 'You succesfully added a game'}
        return render(request, 'hello/developer.html', context)


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
        try:
            message = json.loads(self.request.body)
            game_state_str = str(message.get('gameState'))

            gameid = self.kwargs['pk']
            game = Game.objects.get(gameid = gameid)

            game_state = GameState(
                userid = self.request.user,
                gameid = game,
                gameState = game_state_str,
                timestamp = datetime.now()
            )

            game_state.save()

            save_message = {'message' : 'Successfully saved'}
            return JsonResponse(save_message)
        except:     #FIXME: Generic exception handler
            save_message = {'message' : 'Something went wrong'}
            return JsonResponse(save_message)

class SubmitScoreView(generic.DetailView):
    model = Score
    template_name = 'hello/scoredetail.html'

    def post(self, *args, **kwargs):

        #FIXME: Check for login here
        #@login_required
        try:
            message = json.loads(self.request.body)
            user_score = message.get('score')

            gameid = self.kwargs['pk']
            game = Game.objects.get(gameid = gameid)

            score = Score(
                userid = self.request.user,
                gameid = game,
                score = user_score,
                timestamp = datetime.now()
            )
            score.save()

            save_message = {'message' : 'Successfully saved'}
            return JsonResponse(save_message)
        except:     #FIXME: Generic exception handler
            save_message = {'message' : 'Something went wrong'}
            return JsonResponse(save_message)

        save_message = {'message' : 'Submit score called successfully'}
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
        template_name = 'hello/register.html'
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

class BuyGameView(generic.View):

    def get(self, *args, **kwargs):
        #Get a page with the form required for payment.
        #Form is automatically submitted and customer is redirected to payment service.

        template_name = "hello/buygame.html"

        #FIXME: Read these from somewhere
        secret_key = "INSERT SECRET KEY"
        sid = "INSERT SID"
        pid = "INSERT PID"
        amount = "INSERT AMOUNT"
        checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
        m = md5(checksumstr.encode("ascii"))
        checksum = m.hexdigest()

        context = {
            'sid' : sid,
            'pid' : pid,
            'amount' : amount,
            'secret_key' : secret_key,
            'checksum' : checksum
        }

        return render(self.request, template_name, context)
