from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from drf_microservice_auth.models import MicroserviceUser, MicroserviceGroup

from drf_microservice_auth.serializers import (
    MicroserviceUserSerializer,
    MicroserviceUserLoginSerializer,
    MicroserviceGroupSerializer,
    MicroserviceValidationSerializer,
    MicroserviceRefreshSerializer,
    MicroserviceCreateUserSerializer,
)


class MicroserviceUserViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """

    queryset = MicroserviceUser.objects.all()
    serializer_class = MicroserviceUserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "login":
            return MicroserviceUserLoginSerializer
        elif self.action == "validate":
            return MicroserviceValidationSerializer
        elif self.action == "refresh":
            return MicroserviceRefreshSerializer
        elif self.action == "create":
            return MicroserviceCreateUserSerializer
        return MicroserviceUserSerializer

    @action(detail=False, methods=["post"])
    def login(self, request, *args, **kwargs):
        response = Response()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.get_tokens()
        response.set_cookie(
            key=settings.DRF_MICROSERVICE_AUTH["AUTH_COOKIE"],
            value=tokens["access"],
            max_age=settings.DRF_MICROSERVICE_AUTH["ACCESS_TOKEN_LIFETIME"],
            secure=settings.DRF_MICROSERVICE_AUTH["AUTH_COOKIE_SECURE"],
            httponly=settings.DRF_MICROSERVICE_AUTH["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.DRF_MICROSERVICE_AUTH["AUTH_COOKIE_SAMESITE"],
        )
        response.set_cookie(
            key=settings.DRF_MICROSERVICE_AUTH["REFRESH_COOKIE"],
            value=tokens["refresh"],
            max_age=settings.DRF_MICROSERVICE_AUTH["REFRESH_TOKEN_LIFETIME"],
            secure=settings.DRF_MICROSERVICE_AUTH["AUTH_COOKIE_SECURE"],
            httponly=settings.DRF_MICROSERVICE_AUTH["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.DRF_MICROSERVICE_AUTH["AUTH_COOKIE_SAMESITE"],
        )
        response.data = tokens
        response.status_code = 200
        return response

    @action(detail=False, methods=["post"])
    def validate(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(True, 200)

    @action(detail=False, methods=["post"])
    def refresh(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(True, 200)

    @action(detail=False, methods=["GET"])
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.request.user)
        return Response(serializer.data, 200)


class MicroserviceGroupViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """

    queryset = MicroserviceGroup.objects.all()
    serializer_class = MicroserviceGroupSerializer
    permission_classes = [IsAuthenticated]
