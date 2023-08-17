from django.contrib import admin
from .models import GroupChat, Message, Thread

# Register your models here.


admin.site.register(GroupChat)
admin.site.register(Message)
admin.site.register(Thread)
