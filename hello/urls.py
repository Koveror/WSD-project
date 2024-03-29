from django.urls import path, include
from . import views



app_name = 'hello'
urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    path('shop', views.ShopView.as_view(), name='shop'),
    path('gamelist', views.GameListView.as_view(), name='gamelist'),
    path('shop', views.ShopView.as_view(), name='shop'),
    path('developer', views.DeveloperView.as_view(), name='developer'),
    path('become_developer', views.BecomeDeveloperView.as_view(), name='become_developer'),
    path('modify_game/<str:pk>', views.ModifyGameView.as_view(), name='modify_game'),
    path('gamesales/<str:pk>', views.GameSalesView.as_view(), name='gamesales'),
    path('highscores', views.HighScoreView.as_view(), name='highscores'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('register', views.SignupView.as_view(), name='register'),
    path('game/<str:pk>/', views.GameDetailView.as_view(), name='gamedetail'),
    path('load_game/<str:pk>', views.GameLoadView.as_view(), name = 'load_game'),
    path('save_game/<str:pk>/', views.GameSaveView.as_view(), name='save_game'),
    path('score/<str:pk>/', views.ScoreDetailView.as_view(), name='scoredetail'),
    path('submit_score/<str:pk>/', views.SubmitScoreView.as_view(), name='submit_score'),
    path('buy_game/<str:pk>/', views.BuyGameView.as_view(), name='buy_game'),
    path('payment_success/<str:pk>', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('payment_cancel/<str:pk>', views.PaymentCancelView.as_view(), name='payment_cancel'),
    path('payment_error/<str:pk>', views.PaymentErrorView.as_view(), name='payment_error'),
    path('activate/<str:uidb64>/<str:token>', views.ActivateAccountView.as_view(), name='activate'),
    path('game_api', views.game_list, name='game_api'),

]
