import datetime

import jwt
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core import exceptions as django_exceptions
from rest_framework.exceptions import ValidationError

from drf_microservice_auth.mixins import MicroserviceUserCreateMixin
from drf_microservice_auth.models import MicroserviceUser, MicroserviceGroup


class MicroserviceUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MicroserviceUser
        exclude = ["password"]
        read_only_fields = [
            "last_login",
            "is_staff",
            "is_active",
            "is_superuser",
            "groups",
            "user_permissions",
            "date_joined",
        ]


class MicroserviceCreateUserSerializer(
    MicroserviceUserCreateMixin, serializers.ModelSerializer
):
    password = serializers.CharField(
        style={"input_type": "password"},
    )

    class Meta:
        model = MicroserviceUser
        fields = ["username", "password", "first_name", "last_name", "email"]

    def validate(self, attrs):
        user = MicroserviceUser(**attrs)
        password = attrs.get("password")

        if password:
            try:
                validate_password(password, user)
            except django_exceptions.ValidationError as e:
                raise serializers.ValidationError(e)
        return attrs


class MicroserviceUserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255, help_text="Username")
    password = serializers.CharField(
        help_text="Password",
        style={"input_type": "password", "placeholder": "Password"},
    )

    def validate(self, attrs):
        try:
            user = MicroserviceUser.objects.get(username=attrs["username"])
        except MicroserviceUser.DoesNotExist:
            raise ValidationError(
                f"User with username {attrs['username']} does not exist."
            )

        if not check_password(attrs["password"], user.password):
            raise ValidationError(f"Incorrect password for user {attrs['username']}.")

        attrs["microservice_user"] = user

        return attrs

    def get_tokens(self):

        if not self.validated_data:
            self.is_valid(raise_exception=True)

        microservice_user = self.validated_data["microservice_user"]

        user_dict = {
            "username": microservice_user.username,
            "first_name": microservice_user.first_name,
            "last_name": microservice_user.last_name,
            "email": microservice_user.email,
            "is_staff": microservice_user.is_staff,
            "groups": [group.name for group in microservice_user.groups.all()],
            "is_superuser": microservice_user.is_superuser,
            "is_active": microservice_user.is_active,
            "exp": datetime.datetime.now()
            + settings.DRF_MICROSERVICE_AUTH["ACCESS_TOKEN_LIFETIME"],
            "token_type": "access",
        }

        access_token_dict = user_dict.copy()
        access_token_dict["token_type"] = "access"

        encoded = jwt.encode(
            user_dict, settings.DRF_MICROSERVICE_AUTH["PRIVATE_KEY"], algorithm="EdDSA"
        )
        refresh_token = {
            "token_type": "refresh",
            "exp": datetime.datetime.now()
            + settings.DRF_MICROSERVICE_AUTH["REFRESH_TOKEN_LIFETIME"],
        }
        refresh = jwt.encode(
            refresh_token,
            settings.DRF_MICROSERVICE_AUTH["PRIVATE_KEY"],
            algorithm="EdDSA",
        )
        return {"access": encoded, "refresh": refresh}


class MicroserviceValidationSerializer(serializers.Serializer):

    token = serializers.CharField(max_length=None, help_text="Token to validate.")

    def validate(self, attrs):
        try:
            jwt.decode(
                attrs["token"],
                settings.DRF_MICROSERVICE_AUTH["PUBLIC_KEY"],
                algorithms=["EdDSA"],
            )
        except jwt.ExpiredSignatureError:
            raise ValidationError("Token has expired.")
        except jwt.InvalidSignatureError:
            raise ValidationError("Invalid Signature for token.")
        return attrs


class MicroserviceRefreshSerializer(serializers.Serializer):

    token = serializers.CharField(max_length=None, help_text="Refresh token.")

    def create(self, validated_data):
        raise NotImplemented

    def update(self, instance, validated_data):
        raise NotImplemented

    def validate(self, attrs):
        try:
            jwt.decode(
                attrs["token"],
                settings.DRF_MICROSERVICE_AUTH["PUBLIC_KEY"],
                algorithms=["EdDSA"],
            )
        except jwt.ExpiredSignatureError:
            raise ValidationError("Token has expired.")
        except jwt.InvalidSignatureError:
            raise ValidationError("Invalid Signature for token.")
        return attrs


class MicroserviceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroserviceGroup
        fields = "__all__"

    def validate(self, attrs):
        user = MicroserviceUser(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(e)
        return attrs
