# chat/views.py
from django.shortcuts import render
import requests
from django.contrib.auth import authenticate, login
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


def index(request):
    return render(request, 'chat/index.html')


def room(request):
    return render(request, 'chat/room.html', {
        'room_name': 'room'
    })


def get_token(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], 
                                     password=request.POST['password'])
        if user is not None:
            login(request, user)
        else:
            return render(request, 'chat/get_token.html', {'token': 'Username or password is not valid',
            	                                           'room_name': 'room'})

        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        payload = jwt_payload_handler(user)
        jwt_token = jwt_encode_handler(payload)
        return render(request, 'chat/get_token.html', {'token': f'jwt_token: {jwt_token}',
        	                                           'room_name': 'room', 'username': user.username})

    return render(request, 'chat/get_token.html', {'room_name': 'room'})
