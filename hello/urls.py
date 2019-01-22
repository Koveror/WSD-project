from django.urls import path

from . import views

app_name = 'hello'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('home', views.HomeView.as_view(), name='home'),
    path('shop', views.ShopView.as_view(), name='shop'),
    path('gamelist', views.GameListView.as_view(), name='gamelist'),
    path('shop', views.ShopView.as_view(), name='shop'),
    path('developer', views.DeveloperView.as_view(), name='developer'),
    path('highscores', views.HighScoreView.as_view(), name='highscores'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='gamedetail'),
    path('score/<int:pk>/', views.ScoreDetailView.as_view(), name='scoredetail')
]
