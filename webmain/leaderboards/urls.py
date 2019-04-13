from django.urls import path, re_path
from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'board'
urlpatterns = [
        path('view/<int:game_id>/', views.view, name='viewBoard'),
    path('matchup/<int:game_id>/', views.get_match, name='matchup'),    
        path('update/<int:match_pk>/<int:winner>/', views.update_board, name='matchUpdate'),    
]
