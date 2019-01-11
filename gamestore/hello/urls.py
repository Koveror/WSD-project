from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('home', views.home, name='home'),
    path('gamelist', views.gamelist, name='gamelist'),
    path('purchases', views.purchases, name='purchases'),
    path('gamestate', views.gamestate, name='gamestate')
]
