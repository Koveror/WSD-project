from django.db import models
from django.contrib.auth.models import User



class Game(models.Model):
    gameid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    developerid = models.ForeignKey(User, on_delete= models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    numberSold = models.IntegerField()
    genre = models.CharField(max_length=200)
    dateCreated = models.DateTimeField()
    def __str__(self):
        return self.name

class Score(models.Model):
    userid = models.ForeignKey(User, on_delete= models.CASCADE)
    gameid = models.ForeignKey(Game, on_delete= models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField()
    def __str__(self):
        return '{}, {}, {}'.format(self.gameid, self.userid, self.score)

class GameState(models.Model):
    gameid = models.ForeignKey(Game, on_delete= models.CASCADE)
    userid = models.ForeignKey(User, on_delete= models.CASCADE)
    gameState = models.TextField()
    timestamp = models.DateTimeField()
    def __str__(self):
        return '{}, {}, {}'.format(self.gameid, self.userid, self.gameState)

class Purchases(models.Model):
    gameid = models.ForeignKey(Game, on_delete= models.CASCADE)
    userid = models.ForeignKey(User, on_delete= models.CASCADE)
    def __str__(self):
        return '{}, {}'.format(self.gameid, self.userid)