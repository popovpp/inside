from django.contrib import admin

from testapp.models import Message


class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'message', 'timestamp']
    list_display_links = ['id']

    class Meta:
        model = Message

admin.site.register(Message, MessageModelAdmin)
