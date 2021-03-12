import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from .models import Users




class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None
        prefix, token = auth_data.decode('utf-8').split(' ')
        try:
            tag = ('@')
            payload = jwt.decode(token, settings.JWT_SECRET_KEY)
            username = tag + payload('username')
            user = Users.objects.get(username=username)
            return (user, token)
        except jwt.ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed(
        'Your token is invalid, Login!'
        )
        except jwt.DecodeError as e:
            raise exceptions.AuthenticationFailed(
                'Your token is expired, Login!'
            )
