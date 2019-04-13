from django.urls import path, re_path
from django.conf.urls import url
from django.contrib import admin
from gcp import views

app_name = 'games'
urlpatterns = [
        path('test/cloudfunction', views.test_cloudfunction, name='test_cloudfunction'),
]


