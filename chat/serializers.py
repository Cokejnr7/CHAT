from rest_framework import serializers
from .models import GroupChat


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = "__all__"
