from django.urls import path, re_path
from django.conf.urls import url
from django.contrib import admin
from bots import views

app_name = 'bots'
urlpatterns = [
        path('new/<int:game_id>/', views.addBot, name='addBot'),
#    	path('view-all/<int:game_id>/', views.viewAll, name='viewAll'),
#       path('view/<int:game_id>/<int:bot_id>/', views.viewBot, name='viewBot'),
]
