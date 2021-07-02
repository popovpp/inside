# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('room/', views.room, name='room'),
    path('get-token/', views.get_token, name='get_token'),
]
