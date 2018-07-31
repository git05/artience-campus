from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('new/', views.new_post, name='new_post'),
]
