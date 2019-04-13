from django.urls import path, re_path
from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'users'
urlpatterns = [
        path('login/', views.my_login, name='login'),
]
