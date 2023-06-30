from django.db import models
from authentication.models import CustomUser

# Create your models here.


class Group(models.Model):
    icon = models.ImageField(upload_to="groups/images/")
    name = models.CharField(max_length=150)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser,related_name="groups_created",on_delete=models.CASCADE)
    participants = models.ManyToManyField(CustomUser,related_name="groups_in")
    admins = models.ManyToManyField(CustomUser,related_name="admin_in")
    
    
    def __str__(self) -> str:
        return self.name