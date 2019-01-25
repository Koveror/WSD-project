from django.urls import path

from . import views

#FIXME: Slugs for urls

app_name = 'hello'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('home', views.HomeView.as_view(), name='home'),
    path('shop', views.ShopView.as_view(), name='shop'),
    path('gamelist', views.GameListView.as_view(), name='gamelist'),
    path('shop', views.ShopView.as_view(), name='shop'),
    path('developer', views.DeveloperView.as_view(), name='developer'),
    path('highscores', views.HighScoreView.as_view(), name='highscores'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='gamedetail'),
    path('save_game/<int:pk>/', views.GameSaveView.as_view(), name='save_game'),
    path('score/<int:pk>/', views.ScoreDetailView.as_view(), name='scoredetail')
]
