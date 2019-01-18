from django.urls import path

from . import views

app_name = 'hello'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('home', views.HomeView.as_view(), name='home'),
    path('gamelist', views.GameListView.as_view(), name='gamelist'),
    path('shop', views.ShopView.as_view(), name='shop'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='gamedetail'),
    path('score/<int:pk>/', views.ScoreDetailView.as_view(), name='scoredetail')
]
