from django.db import models
from authentication.models import CustomUser
from .managers import ThreadManager

# Create your models here.


class GroupChat(models.Model):
    icon = models.ImageField(upload_to="groups/images/")
    name = models.CharField(max_length=150)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        CustomUser, related_name="groups_created", on_delete=models.CASCADE
    )
    participants = models.ManyToManyField(
        CustomUser,
        related_name="groups_in",
    )
    admins = models.ManyToManyField(CustomUser, related_name="admin_in")

    def __str__(self) -> str:
        return self.name


THREAD_TYPES = (("p", "personal"), ("g", "group"))


class Thread(models.Model):
    thread_type = models.CharField(
        max_length=30,
        choices=THREAD_TYPES,
    )
    users = models.ManyToManyField(CustomUser)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = ThreadManager()


class Message(models.Model):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
