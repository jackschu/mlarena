from django.urls import path, re_path
from django.conf.urls import url
from django.contrib import admin
from . import views
from .views import Register

app_name = 'users'
urlpatterns = [
        path('login/', views.my_login, name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', views.my_logout, name ='logout'),    
]
