from django.db import models
from django.contrib.auth.models import User
import uuid

from django.core.exceptions import ValidationError

from django.db.models.signals import post_save
from django.dispatch import receiver

def validate_positive(value):
    if (value < 0) :
        raise ValidationError('%s Value less than zero' % value)


class Game(models.Model):

    gameid = models.CharField(primary_key=True, unique=True, default=uuid.uuid4, max_length=200)
    name = models.CharField(max_length=200, unique=True)
    developerid = models.ForeignKey(User, on_delete= models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=5,validators=[validate_positive])
    numberSold = models.DecimalField(default=0, decimal_places=2, max_digits=5, validators=[validate_positive])
    primarygenre = models.CharField(max_length=200)
    secondarygenre = models.CharField(max_length=200, blank=True)
    dateCreated = models.DateTimeField()
    URL = models.CharField(max_length=200)
    description = models.TextField(max_length=400, default="no description")
    def __str__(self):
        return self.name


class Score(models.Model):
    userid = models.ForeignKey(User, on_delete= models.CASCADE)
    gameid = models.ForeignKey(Game, on_delete= models.CASCADE)
    score = models.DecimalField(default = 0, decimal_places=2, max_digits=5, validators=[validate_positive])
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
    pid = models.CharField(primary_key=True, unique=True, max_length=200)
    gameid = models.ForeignKey(Game, on_delete= models.CASCADE)
    userid = models.ForeignKey(User, on_delete= models.CASCADE)
    def __str__(self):
        return '{}, {}'.format(self.gameid, self.userid)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    # other fields...
