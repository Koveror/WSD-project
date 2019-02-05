from django.test import TestCase
from django.utils import timezone
import datetime
from .models import User, Game, Score, GameState, Purchases
from django.contrib.auth.models import User
import json
import sys
from django.core.serializers.json import DjangoJSONEncoder

class GameModelTest(TestCase):
    
    def setUp(self):
        user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword'
        )
        game = Game.objects.create(
            gameid=1000,
            name="lion",
            developerid=user,
            price=2.0,
            numberSold=0, 
            primarygenre="roar",
            secondarygenre="meow",
            dateCreated=timezone.now(),
            URL="URL",
            description="Game about lions"
        )

    """Test if a game object is created correctly"""
    def test_game_id(self):
        lion = Game.objects.get(name="lion")
        self.assertEqual(lion.gameid, 1000)

    def test_game_price(self):
        lion = Game.objects.get(name="lion")
        self.assertEqual(lion.price, 2.0)

    def test_game_numberSold(self):
        lion = Game.objects.get(name="lion")
        self.assertEqual(lion.numberSold, 0)

    def test_game_primarygenre(self):
        lion = Game.objects.get(name="lion")
        self.assertEqual(lion.primarygenre, "roar")


class GameLimitValueTests(TestCase):

    def setUp(self):
        pass

    def test_game_number_sold_negative(self):
        newgame = Game(numberSold = -1)
        self.assertEqual(newgame.numberSold, 0)

    def test_new_game_number_sold_too_much(self):
        newgame = Game(numberSold = 1)
        self.assertEqual(newgame.numberSold, 1)

    def test_new_game_date_created_too_much(self):
        time = timezone.now()
        futuretime = timezone.now() + datetime.timedelta(days=30)
        newgame = Game(dateCreated = futuretime)
        self.assertEqual(newgame.dateCreated, time)

''' Test score '''
class ScoreModelTest(TestCase):
    
    def setUp(self):
        user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword'
        )
        game = Game.objects.create(
            gameid=1000,
            name="lion",
            developerid=user,
            price=2.0,
            numberSold=0, 
            primarygenre="roar",
            secondarygenre="meow",
            dateCreated=timezone.now(),
            URL="URL",
            description="Game about lions"
        )
        score = Score.objects.create(
            userid=user,
            gameid=game,
            score=0,
            timestamp=timezone.now()
        )

    
    def test_game_id(self):
        user = User.objects.get(username='john')
        game = Game.objects.get(name='lion')
        score = Score.objects.get(userid=user)
        self.assertEqual(score.gameid, game)

    def test_user_id(self):
        user = User.objects.get(username='john')
        game = Game.objects.get(name='lion')
        score = Score.objects.get(gameid=game)
        self.assertEqual(score.userid, user)

    def test_score(self):
        user = User.objects.get(username='john')
        score = Score.objects.get(userid = user)
        self.assertEqual(score.score, 0)

class ScoreLimitValueTests(TestCase):
    def test_game_score_not_negative(self):
        newscore = Score(score = -1)
        self.assertEqual(newscore.score, 0)
    

''' Test gamestate '''
class GameStateModelTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword'
        )
        game = Game.objects.create(
            gameid=1000,
            name="lion",
            developerid=user,
            price=2.0,
            numberSold=0, 
            primarygenre="roar",
            secondarygenre="meow",
            dateCreated=timezone.now(),
            URL="URL",
            description="Game about lions"
        )
        gameState = gameState = GameState.objects.create(
            userid=user,
            gameid=game,
            gameState='{ x: 5, y: 6 }',
            timestamp=timezone.now()
        )

    def test_game_id(self):
        user = User.objects.get(username = 'john')
        game = Game.objects.get(gameid=1000)
        gameState = GameState.objects.get(userid = user)
        self.assertEqual(gameState.gameid, game)

    def test_user_id(self):
        user = User.objects.get(username = 'john')
        gameState = GameState.objects.get(userid = user)
        self.assertEqual(gameState.userid, user)

    def test_game_state(self):
        user = User.objects.get(username = 'john')
        gameState = GameState.objects.get(userid = user)
        self.assertEqual(gameState.gameState, '{ x: 5, y: 6 }')


class GameStateLimitValueTests(TestCase):

    def setUp(self):
        pass

    def test_game_number_sold_negative(self):
        newgamestate = GameState(gameState = '{ "x": 5, "y": 6 }')
        self.assertEqual((json.loads(newgamestate.gameState)), ({"x":5,"y":6}))


''' Test purchases '''
class PurchaseModelTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword'
        )
        game = Game.objects.create(
            gameid=1000,
            name="lion",
            developerid=user,
            price=2.0,
            numberSold=0, 
            primarygenre="roar",
            secondarygenre="meow",
            dateCreated=timezone.now(),
            URL="URL",
            description="Game about lions"
        )
        purchase = Purchases.objects.create(userid=user, gameid=game)

    def test_game_id(self):
        game = Game.objects.get(gameid=1000)
        purchase = Purchases.objects.get(gameid=game)
        self.assertEqual(purchase.gameid, game)

    def test_user_id(self):
        user = User.objects.get(username = 'john')
        purchase = Purchases.objects.get(userid=user)
        self.assertEqual(purchase.userid, user)