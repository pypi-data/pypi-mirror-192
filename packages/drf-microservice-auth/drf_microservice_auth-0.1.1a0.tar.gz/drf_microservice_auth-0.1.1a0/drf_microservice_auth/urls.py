from rest_framework import routers

from drf_microservice_auth import views

router = routers.DefaultRouter()
router.register(r"users", views.MicroserviceUserViewSet)
router.register(r"groups", views.MicroserviceGroupViewSet)

urlpatterns = router.urls
