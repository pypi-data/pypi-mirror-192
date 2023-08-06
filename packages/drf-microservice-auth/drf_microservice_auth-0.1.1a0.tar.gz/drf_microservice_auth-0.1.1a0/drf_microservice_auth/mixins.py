from django.db import IntegrityError, transaction

from drf_microservice_auth.models import MicroserviceUser


class MicroserviceUserCreateMixin:
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = MicroserviceUser.objects.create_user(**validated_data)
        return user
