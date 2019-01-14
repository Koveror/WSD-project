from django.test import TestCase
from django.utils import timezone
import datetime
from .models import User, Game, Score, GameState, Purchases
from django.contrib.auth.models import User

class GameModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        Game.objects.create(gameid=1000, name="lion", developerid=user, price=2.0, numberSold=0, 
        genre="roar", dateCreated=timezone.now())

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

    def test_game_genre(self):
        lion = Game.objects.get(name="lion")
        self.assertEqual(lion.genre, "roar")


class GameLimitValueTests(TestCase):
    def test_game_number_sold_negative(self):
        newgame = Game(numberSold = -1)
        self.assertEqual(newgame.numberSold, 0)

    def test_new_game_number_sold_too_much(self):
        newgame = Game(numberSold = 1)
        self.assertEqual(newgame.numberSold, 0)

    def test_new_game_date_created_too_much(self):
        time = timezone.now()
        futuretime = timezone.now() + datetime.timedelta(days=30)
        newgame = Game(dateCreated = futuretime)
        self.assertEqual(newgame.dateCreated, time)

''' Test score '''
class ScoreModelTest(TestCase):
    def test_game_id(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        lion = Game.objects.create(gameid=1000, name="lion", developerid=user, price=2.0, numberSold=0, 
        genre="roar", dateCreated=timezone.now())
        score = Score.objects.create(userid=user, gameid=lion, score=0, timestamp=timezone.now())
        self.assertEqual(score.gameid, lion)

    def test_user_id(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        lion = Game.objects.create(gameid=1000, name="lion", developerid=user, price=2.0, numberSold=0, 
        genre="roar", dateCreated=timezone.now())
        score = Score.objects.create(userid=user, gameid=lion, score=0, timestamp=timezone.now())
        self.assertEqual(score.userid, user)

    def test_score(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        lion = Game.objects.create(gameid=1000, name="lion", developerid=user, price=2.0, numberSold=0, 
        genre="roar", dateCreated=timezone.now())
        score = Score.objects.create(userid=user, gameid=lion, score=0, timestamp=timezone.now())
        self.assertEqual(score.score, 0)

class ScoreLimitValueTests(TestCase):
    def test_game_number_sold_negative(self):
        newscore = Score(score = -1)
        self.assertEqual(newscore.score, 0)
    


