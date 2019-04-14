from django.urls import path, re_path
from django.conf.urls import url
from django.contrib import admin
from gcp import views

app_name = 'games'
urlpatterns = [
        path('test/cloudfunction', views.test_cloudfunction, name='test_cloudfunction'),
        path('test/cloudfunction/run', views.test_cloudfunction_run, name='test_cloudfunction_run'),
        path('match/start', views.start_match, name='start_match'),
]


