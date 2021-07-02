from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='users',
                                blank=True, null=True)
    message = models.TextField(default='', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
