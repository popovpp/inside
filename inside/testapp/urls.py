from django.urls import path

from . import views

urlpatterns = [
    path('client/', views.chat_client, name='chat_client'),
]
