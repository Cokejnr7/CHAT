import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

User = get_user_model()


@database_sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[
                settings.ALGORITHM,
            ],
        )

        user = User.objects.get(email=payload["email"])

    except jwt.DecodeError:
        user = AnonymousUser()

    except jwt.ExpiredSignatureError:
        user = AnonymousUser()

    except User.DoesNotExist:
        user = AnonymousUser()

    return user


class TokenAuthMiddleware:
    def __init__(self, inner):
        pass

    def __call__(self, *args):
        pass
