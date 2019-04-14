from django.urls import path, re_path
from django.conf.urls import url
from django.contrib import admin
from bots import views

app_name = 'bots'
urlpatterns = [
        path('new/<int:game_id>/', views.addBot, name='addBot'),
        path('view/<int:bot_id>/', views.viewBot, name='viewBot'),
    	path('viewMatch/<int:match_id>/', views.viewMatch, name='viewMatch')
]
