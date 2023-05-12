from django.db import models
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser,BaseUserManager
from django.utils.translation import gettext_lazy as _



class CustomManager(BaseUserManager):
    
    def create_user(self,username,email,password,**other_fields):
        
        if not username:
            raise ValueError(_("username must be provided"))
        
        if not email:
            raise ValueError(_("email must be provided"))
        
        email = self.normalize_email(email)
        
        user = self.model(username=username,email=email,**other_fields)
        
        user.set_password(password)
        
        user.save()
        
        return user
    
    def create_superuser(self,username,email,password,**other_fields):
        
        other_fields.setdefault('is_staff', True)  
        other_fields.setdefault('is_superuser', True)  
        other_fields.setdefault('is_active', True) 
        
        if other_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
            
        if other_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        
        return self.create_user(username,email,password,**other_fields)




class CustomUser(AbstractBaseUser,PermissionsMixin):
    username:str = models.CharField(max_length=150,unique=True)
    email:str = models.EmailField()
    is_active:bool = models.BooleanField(default=True)
    is_superuser:bool = models.BooleanField(default=False)
    is_staff:bool = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    objects = CustomManager()
    
    def __str__(self) -> str:
        return self.username
    

# Create your models here.
class UserProfile(models.Model):
    owner = models.OneToOneField(CustomUser,related_name="profile",on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profiles/images/")
    username= models.CharField(max_length=150)
    email = models.EmailField()
    bio = models.TextField()
    