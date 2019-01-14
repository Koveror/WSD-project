from django.contrib import admin
from .models import Game, GameState, Score, Purchases

# Register your models here.
admin.site.register(Game)
admin.site.register(GameState)
admin.site.register(Score)
admin.site.register(Purchases)