import jwt
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

User = get_user_model()


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, recieve, send):
        user = await self.get_user(scope, send)
        scope["user"] = user
        return await super().__call__(scope, recieve, send)

    async def send_authentication_error(self, send, error):
        await send(
            {
                "type": "websocket.close",
                "code": 4101,
                "text": str(error),
            }
        )

    async def get_user(self, scope, send):
        try:
            token = scope["query_string"].decode("utf8").split("=")[1]
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[
                    settings.ALGORITHM,
                ],
            )
            user = await database_sync_to_async(User.objects.get)(
                email=payload["email"]
            )

        except (IndexError, jwt.DecodeError):
            await self.send_authentication_error(send, "Invalid token")
        except jwt.ExpiredSignatureError:
            await self.send_authentication_error(send, "token expired")
        else:
            return user
