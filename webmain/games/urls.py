from django.urls import path, re_path
from django.conf.urls import url
from django.contrib import admin
from games import views

app_name = 'games'
urlpatterns = [
        path('new/', views.addGame, name='addGame'),
        path('view/<int:game_id>/', views.viewGame, name='viewGame'),
]
