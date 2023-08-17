from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializers import GroupSerializer
from .models import Message
from authentication.models import CustomUser
from .models import Thread

# Create your views here.


def home(request):
    users = CustomUser.objects.all()
    context = {"users": users}
    return render(request, "chat/home.html", context)


def lobby(request, username):
    other_user = CustomUser.objects.get(username=username)
    thread = Thread.objects.get_or_create_personal_thread(request.user, other_user)
    messages = Message.objects.filter(thread=thread)
    context = {"messages": messages}
    return render(request, "chat/lobby.html", context)


class GroupListCreateAPIView(GenericAPIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        user = request.user
        # groups = GroupChat.objects.filter(= )
        serializer = GroupSerializer()
        return Response("")

    def post(self, request):
        print(request.data)
        return Response("")
