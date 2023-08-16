from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import CustomUser, UserProfile


@receiver(post_save, sender=CustomUser)
def create_userprofile(sender, instance, created, **kwargs):
    user = instance
    if created:
        UserProfile.objects.create(username=user.username, owner=user, email=user.email)


@receiver(post_delete, sender=UserProfile)
def delete_user(sender, instance, *args, **kwargs):
    user = instance.owner
    user.delete()
