from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConvocacaoViewSet

router = DefaultRouter()
router.register(r'convocacoes', ConvocacaoViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
