import jwt
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, exceptions
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from .token import generate_access_token, generate_refresh_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings

# Create your views here.


User = get_user_model()


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if email is None:
            raise exceptions.AuthenticationFailed("email must be provided")
        elif password is None:
            raise exceptions.AuthenticationFailed("password must be provided")

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed("no user with that email")

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("wrong password")

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        serializer = UserSerializer(user)

        response = Response(
            {"user": serializer.data, "token": access_token}, status=status.HTTP_200_OK
        )

        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        return response


@api_view(["POST"])
def refresh_token(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            "Authentication credentials were not provided"
        )

    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

    except jwt.DecodeError:
        raise exceptions.AuthenticationFailed("invalid token.")

    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            "refresh token expired login please login again."
        )

    user = User.objects.get(email=payload["email"])
    access_token = generate_access_token(user)

    return Response(
        {"access_token": access_token},
        status=status.HTTP_202_ACCEPTED,
    )
