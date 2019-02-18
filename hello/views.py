import json
import os
import uuid
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
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django import forms
from django.core.mail import send_mail


#Homepage view that displays messages and has links to other views
class HomeView(generic.View):

    def get(self, request):
        context = {'message': ''}
        return render(request, 'hello/home.html', context)

#List of users own games
class GameListView(LoginRequiredMixin, generic.View):
    login_url = 'hello:login'

    def get(self, request):
        purchases = Purchases.objects.filter(userid=request.user)
        return render(request, 'hello/gamelist.html', {'purchases': purchases})

#View used to add users to developer group
class BecomeDeveloperView(LoginRequiredMixin, generic.View):
    login_url = 'hello:login'

    #Add the user to the developer-group which can be assumed exists
    def post(self, request):
        Group.objects.get(name='Developer').user_set.add(request.user)
        messages.success(request, 'You succesfully became a developer')
        return redirect('hello:home')

#Developer view for managing games
class DeveloperView(LoginRequiredMixin, generic.View):
    login_url = 'hello:login'

    def get(self, request):
        #Test if user belongs to developer-group
        is_member = request.user.groups.filter(name='Developer').exists()
        #Generate a list of developer's games
        games = Game.objects.filter(developerid=request.user)

        purchases = Purchases.objects.filter(gameid__in=games)
        ordering = ['gameid', '-timestamp']

        context = {'is_a_developer': is_member, 'games': games}
        return render(request, 'hello/developer.html', context)

    def post(self, request):
        #Test if user belongs to developer-group
        is_member = request.user.groups.filter(name='Developer').exists()
        #Generate a list of developer's games
        games = Game.objects.filter(developerid=request.user)

        #Create a new game
        try:
            name = request.POST['name']
            price = request.POST['price']
            URL = request.POST['URL']
            description = request.POST['description']
            primarygenre = request.POST['primarygenre']
            secondarygenre = request.POST['secondarygenre']
            image = request.POST['imageToUpload']
            newgame = Game.objects.create(name=name,
                       price=price,
                       URL=URL,
                       developerid=request.user,
                       numberSold=0,
                       dateCreated=datetime.now(),
                       description=description,
                       primarygenre=primarygenre,
                       secondarygenre=secondarygenre,
                       image=image
                       )
            context = {'is_a_developer': is_member, 'games': games}
            messages.success(request, 'You succesfully added a game')
            return render(request, 'hello/developer.html', context)
        except KeyError:
            context = {'is_a_developer': is_member, 'games': games}
            messages.add_message(request, messages.ERROR, 'Something went wrong')
            return render(request, 'hello/developer.html', context)

class ModifyGameView(LoginRequiredMixin, generic.DetailView):
    model = Game
    template_name = 'hello/modifygame.html'
    login_url = 'hello:login'

    def post(self, request, *args, **kwargs):
        #Test if user belongs to developer-group
        is_member = request.user.groups.filter(name='Developer').exists()
        #Generate a list of developer's games
        games = Game.objects.filter(developerid=request.user)
        #To-be-modified game's id
        gameid = self.kwargs['pk']
        #Check if the developer is the owner of the game
        if Game.objects.filter(developerid=request.user, gameid=gameid).exists():
            #Overwrite old values
            try:
                name = request.POST['name']
                price = request.POST['price']
                URL = request.POST['URL']
                description = request.POST['description']
                primarygenre = request.POST['primarygenre']
                secondarygenre = request.POST['secondarygenre']
                newgame = Game.objects.filter(pk=gameid).update(name=name,
                    price=price,
                    URL=URL,
                    developerid=request.user,
                    numberSold=0,
                    dateCreated=datetime.now(),
                    description=description,
                    primarygenre=primarygenre,
                    secondarygenre=secondarygenre
                    )
            except KeyError:
                messages.add_message(request, messages.ERROR, '''You don't have permission to modify this game''')
                return redirect('hello:developer')

            context = {'is_a_developer': is_member, 'games': games}
            messages.success(request, 'You succesfully modified a game')
            return redirect('hello:developer')

class GameSalesView(LoginRequiredMixin, generic.DetailView):
    login_url = 'hello:login'
    template_name = 'hello/gamesales.html'
    model = Purchases
    ordering = ['-timestamp']
    def get(self, request, *args, **kwargs):

        gameid = self.kwargs['pk']
        #game = Game.objects.get(gameid = gameid)
        #developerid = game.developerid
        if Purchases.objects.filter( gameid=gameid, developerid=request.user).exists():
            context = {'purchases': Purchases.objects.filter(gameid = gameid)}
            return render(request, 'hello/gamesales.html', context)
        else:
            messages.add_message(request, messages.INFO, 'No sales for this one yet')
            return redirect('hello:developer')

class HighScoreView(generic.ListView):
    template_name = 'hello/highscores.html'
    model = Score
    ordering = ['gameid', '-score']

class ShopView(generic.ListView):
    template_name = 'hello/shop.html'
    model = Game

#Generic view for a single game
class GameDetailView(LoginRequiredMixin, generic.View):

    login_url = 'hello:login'

    def get(self, request, *args, **kwargs):
        #Test if the user has bought the game
        gameid = self.kwargs['pk']
        if Purchases.objects.filter(userid=request.user, gameid=gameid).exists():
            context = {'game': Game.objects.get(gameid = gameid)}
            return render(request, 'hello/gamedetail.html', context)
        else:
            messages.add_message(request, messages.INFO, 'Access denied')
            return redirect('hello:home')

#View for saving gamestates. The save message is posted to this view using ajax
class GameSaveView(LoginRequiredMixin, generic.DetailView):

    model = Game
    template_name = 'hello/gamedetail.html'
    login_url = 'hello:login'

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
        except KeyError:    #FIXME: Add more error handling
            save_message = {'message' : 'Something went wrong'}
            return JsonResponse(save_message)

#View for submitting scores. The score is posted using ajax.
class SubmitScoreView(LoginRequiredMixin, generic.DetailView):
    model = Score
    template_name = 'hello/scoredetail.html'
    login_url = 'hello:login'

    def post(self, *args, **kwargs):
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
        except KeyError:
            save_message = {'message' : 'Something went wrong'}
            return JsonResponse(save_message)

        save_message = {'message' : 'Submit score called successfully'}
        return JsonResponse(save_message)

#View details for a single score
class ScoreDetailView(generic.DetailView):
    model = Score
    template_name = 'hello/scoredetail.html'

#View for logging in
class LoginView(generic.View):

    def get(self, request):
        if not request.user.is_authenticated:
            context = {'msg': "Please enter a username and a password"}
            return render(request, 'hello/login.html', context)
        else:
            messages.add_message(request, messages.INFO, 'You are already logged in')
            return redirect('hello:home')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, 'You are now logged in')
            return redirect('hello:home')
        else:
            # Return an 'invalid login' error message.
            messages.add_message(request, messages.INFO, 'Invalid username or password')
            return redirect('hello:login')

#View for logging out
class LogoutView(generic.View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            # Redirect to a success page.
            messages.success(request, 'You succesfully logged out')
            return redirect('hello:home')
        else:
            messages.add_message(request, messages.INFO, 'You are not logged in')
            return redirect('hello:home')

#Custom signup form for email confirmation
class EmailSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SignupView(generic.View):

    def get(self, request):
        return render(request, 'hello/register.html', {'form': EmailSignupForm()})

    def post(self, request):
        form = EmailSignupForm(request.POST)
        if form.is_valid():
            #Email authentication here
            message = self.create_confirmation_email(request, form)

            mail_subject = 'Please activate you gamestore account'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            if request.POST.get("developer", "") == 'Yes':
                dev_group = Group.objects.get(name='Developer')
                dev_group.user_set.add(User.objects.get(username=request.POST['username']))
            messages.success(request, 'Please confirm your email address to login.')
            #Since no SMTP server is configured, give the link
            messages.add_message(request, messages.INFO, 'Since we do not have a smtp server, the confirmation email is also here.')
            messages.add_message(request, messages.INFO, message)
            return redirect('hello:login')
        else:
            return render(request, 'hello/register.html', {'form': form})

    def create_confirmation_email(self, request, form):
        
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        message = render_to_string('hello/email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token':account_activation_token.make_token(user),
        })
        return message


class ActivateAccountView(generic.View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Thank you for your email confirmation. You are now logged in.')
            return redirect('hello:home')
        else:   
            messages.add_message(request, messages.ERROR, 'Activation link is invalid!')
            return redirect('hello:home')

#A form for buying a specific game. Displayed before moving to payment service.
#FIXME: What if game is bought twice
class BuyGameView(LoginRequiredMixin, generic.DetailView):

    template_name = 'hello/buygame.html'
    login_url = 'hello:login'

    def get(self, *args, **kwargs):
        #Get a page with the form required for payment.
        template_name = "hello/buygame.html"

        try:
            gameid = self.kwargs['pk']
            game = Game.objects.get(gameid = gameid)

            #Secret values are read from enviromental variables.
            #Set up your own variables by running on the command line:
            #MY_VARIABLE=something
            #export MY_VARIABLE
            secret_key = os.environ['WSD_SECRET_KEY']
            sid = os.environ['WSD_SID']

            pid = uuid.uuid1().hex
            amount = game.price
            developerid = game.developerid

            checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
            m = md5(checksumstr.encode("ascii"))
            checksum = m.hexdigest()

            success_url = self.request.build_absolute_uri('/payment_success')
            cancel_url = self.request.build_absolute_uri('/payment_cancel')
            error_url = self.request.build_absolute_uri('/payment_error')

            context = {
                'sid' : sid,
                'pid' : pid,
                'amount' : amount,
                'secret_key' : secret_key,
                'checksum' : checksum,
                'gameid' : gameid,
                'game' : game,
                'success_url' : success_url,
                'cancel_url' : cancel_url,
                'error_url' : error_url,
                'developerid' : developerid,
            }

            return render(self.request, template_name, context)

        except KeyError as e:
            return HttpResponse("The server is incorrectly set up: {}".format(e))

#User is redirected to this view after succesfully interacting with the payment service.
class PaymentSuccessView(LoginRequiredMixin, generic.View):
    login_url = 'hello:login'
    def get(self, *args, **kwargs):

        checksum = ""
        try:
            game = Game.objects.get(gameid = self.kwargs['pk'])
            user = self.request.user
            pid = self.request.GET.get('pid', '')
            parameter_checksum = self.request.GET.get('checksum', '')
            checksum = self.calculate_checksum(self.request)
        except KeyError:
            checksum = "ERROR"

        #The purchase is authenticated by matching a given checksum with the one we calculated
        if checksum == parameter_checksum:
            self.save_purchase(game, user, pid)
            messages.success(self.request, "Payment successfull. Go to your gamelist to play your games.")
            return redirect('hello:home')
        else:
            #If checksum doesn't match on our end, continue to payment error
            return redirect('hello:payment_error')

    #Helper function for calculating a checksum
    def calculate_checksum(self, request):

        #The payment service gives data in url parameters.
        #They can be accessed like this
        pid = request.GET.get('pid', '')
        ref = request.GET.get('ref', '')
        result = request.GET.get('result', '')
        secret_key = os.environ['WSD_SECRET_KEY']

        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
        m = md5(checksumstr.encode("ascii"))
        checksum = m.hexdigest()

        return checksum

    #Helper function for saving a purchase to the database
    def save_purchase(self, game, user, pid):
        p = Purchases(pid = pid, gameid = game, userid = user, timestamp = datetime.now())
        p.save()


#User is redirected to this view is payment is cancelled in the payment service.
class PaymentCancelView(generic.View):

    def get(self, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, "Payment has been cancelled.")
        return redirect("hello:home")


#User is redirected here if there is an error with the payment service.
class PaymentErrorView(generic.View):

    def get(self, *args, **kwargs):
        messages.add_message(self.request, messages.ERROR, "There was an error in handling your payment.")
        return redirect("hello:home")
