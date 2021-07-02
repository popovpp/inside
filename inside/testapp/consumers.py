import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
from channels.db import database_sync_to_async
from django.conf import settings
import asyncio

from testapp.models import Message


@database_sync_to_async
def get_user(username=None):
    return get_object_or_404(User, username=username)


@database_sync_to_async
def save_message_db(username=None, message=None):
    user = get_object_or_404(User, username=username)
    message_instance = Message.objects.create(user=user, message=message)
    message_instance.save()
    return message_instance


@database_sync_to_async
def read_db(amount_of_records=None):
    items_list = list(Message.objects.all().order_by('-pk'))
    length = len(items_list)
    if length < amount_of_records:
        return items_list[:length]
    else:
        return items_list[:amount_of_records]


@database_sync_to_async
def get_username(message_instance=None):
    return message_instance.user.username


@database_sync_to_async
def get_message(message_instance=None):
    return message_instance.message


class AsyncIteratorWrapper():
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value


class ChatConsumer(AsyncWebsocketConsumer):
    
    chanels_dict = {}

    async def send_message_to_channel(self, channel_name=None, message=None):
        await self.channel_layer.send(
                      channel_name,
                      {
                      'type': 'chat_message',
                      'username': self.room_group_name,
                      'message': message
                      }
                )

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send_message_to_channel(channel_name=self.channel_name, message='connect')

    async def disconnect(self, close_code):
        # Leave room group
        await self.send_message_to_channel(channel_name=self.channel_name, 
                                           message="disconnect")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json['username'].strip()
        message = text_data_json['message']

        send_message = True
        not_history = True
        send_list =[]
        message_instance = Message

    # Processing message with token
        if message[:4] == 'auth':
            send_message = False
            try:
                username_in_token = (jwt.decode(message[4:], 
                                     settings.SECRET_KEY, algorithms=["HS256"]))['username']
                if username == username_in_token:
                    user = await get_user(username=username)
                    if user.is_authenticated:
                        self.chanels_dict[self.channel_name] = user.username
                        await self.channel_layer.send(
                              self.channel_name,
                              {
                              'type': 'chat_message',
                              'username': username,
                              'message': 'can send message'
                              }
                        )
                else:
                    await self.send_message_to_channel(channel_name=self.channel_name, 
                                                       message="credentals are invalid")
            except Exception as e:
                print('error:', e)
                await self.send_message_to_channel(channel_name=self.channel_name, 
                                                   message="credentals are invalid")

    # Processing message with "history"
        if 'history' in message[:7]:
            send_message = False
            str_list = message.split()
            amount_of_records = int(str_list[1])
            send_list = await read_db(amount_of_records=amount_of_records)
            if ((self.channel_name in self.chanels_dict) and 
                (username == self.chanels_dict[self.channel_name])):
                async for message_instance in AsyncIteratorWrapper(send_list): 
                    await self.channel_layer.send(
                          self.channel_name,
                          {
                          'type': 'chat_message',
                          'username': await get_username(message_instance),
                          'message': await get_message(message_instance)
                          }
                    )
            else:
                await self.send_message_to_channel(channel_name=self.channel_name, 
                                                   message="can't send history message")
        

        # Send message to room group
        if ((self.channel_name in self.chanels_dict) and 
            (username == self.chanels_dict[self.channel_name])):
            if send_message:
                message_instance = await save_message_db(username=username, message=message)                    
                await self.channel_layer.group_send(
                      self.room_group_name,
                      {
                      'type': 'chat_message',
                      'username': username,
                      'message': message
                      }
                )
        else:
            await self.send_message_to_channel(channel_name=self.channel_name, 
                                               message="can't send message")

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'username': username,
            'message': message
        }))
        