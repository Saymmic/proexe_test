from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from proexe.dynamic_tables.api.views import DynamicTableViewSet
from proexe.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("table", DynamicTableViewSet)

app_name = "api"
urlpatterns = router.urls
