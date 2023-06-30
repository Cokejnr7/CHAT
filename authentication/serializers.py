from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import exceptions

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8,max_length=60,write_only=True)
    
    
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8,max_length=60,write_only=True)
    class Meta:
        model = User
        fields = ['__all__']
        
    def validate(self,attrs):
        email = attrs.get('email')
        
        if User.objects.get(email=email).exists():
            raise exceptions.ValidationError("user with that email already exists.")
        
        super().validate(attrs)