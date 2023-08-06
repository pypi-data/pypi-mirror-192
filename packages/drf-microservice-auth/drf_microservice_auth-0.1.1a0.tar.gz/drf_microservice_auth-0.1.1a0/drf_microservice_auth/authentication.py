import datetime

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication


class DrfMicroserviceAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        print(request.COOKIES)

        raw_token = (
            request.COOKIES.get(settings.DRF_MICROSERVICE_AUTH["AUTH_COOKIE"]) or None
        )
        print(f"Raw token: {raw_token}")
        try:
            decoded = jwt.decode(
                raw_token,
                settings.DRF_MICROSERVICE_AUTH["PUBLIC_KEY"],
                algorithms=["EdDSA"],
            )
        except Exception as ee:
            print(f"Exception {ee}")
            return None

        user_model = get_user_model()

        print(f"Decoded: {decoded}")
        user, _ = user_model.objects.get_or_create(username=decoded["username"])
        user.first_name = decoded["first_name"]
        user.last_name = decoded["last_name"]
        user.email = decoded["email"]
        user.is_staff = decoded["is_staff"]
        user.is_superuser = decoded["is_superuser"]
        user.is_active = decoded["is_active"]
        user.last_login = datetime.datetime.now()
        user.save()
        return user, None
