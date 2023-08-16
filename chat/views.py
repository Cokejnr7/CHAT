from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializers import GroupSerializer
from .models import GroupChat

# Create your views here.


def lobby(request):
    return render(request, "chat/lobby.html")


# class GroupListCreateAPIView(GenericAPIView):
#     parser_classes = [MultiPartParser, FormParser]

#     def get(self, request, *args, **kwargs):
#         user = request.user
#         groups = GroupChat.objects.filter(= )
#         serializer = GroupSerializer()

#     def post(self, request):
#         print(request.data)
#         return Response("")
