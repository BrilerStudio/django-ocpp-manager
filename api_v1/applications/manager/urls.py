from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)

router.register(r'ChargePoint', views.ChargePointViewSet)
router.register(r'Location', views.LocationViewSet)
router.register(r'Transaction', views.TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
