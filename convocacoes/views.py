from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Convocacao
from .serializers import (
    ConvocacaoSerializer, 
)


class ConvocacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing convocations
    """
    queryset = Convocacao.objects.all()
    serializer_class = ConvocacaoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'tipo', 'data_publicacao']
    search_fields = ['titulo', 'numero', 'descricao']
    ordering_fields = ['titulo', 'data_publicacao', 'data_inicio_inscricoes', 'created_at']
    ordering = ['-data_publicacao', 'titulo']
