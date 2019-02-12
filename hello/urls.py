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
    path('become_developer', views.BecomeDeveloperView.as_view(), name='become_developer'),
    path('modify_game/<int:pk>', views.ModifyGameView.as_view(), name='modify_game'),
    path('highscores', views.HighScoreView.as_view(), name='highscores'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('register', views.SignupView.as_view(), name='register'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='gamedetail'),
    path('save_game/<int:pk>/', views.GameSaveView.as_view(), name='save_game'),
    path('score/<int:pk>/', views.ScoreDetailView.as_view(), name='scoredetail'),
    path('submit_score/<int:pk>/', views.SubmitScoreView.as_view(), name='submit_score'),
    path('buy_game/<int:pk>/', views.BuyGameView.as_view(), name='buy_game'),
    path('payment_success/<int:pk>', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('payment_cancel/<int:pk>', views.PaymentCancelView.as_view(), name='payment_cancel'),
    path('payment_error/<int:pk>', views.PaymentErrorView.as_view(), name='payment_error'),
]
