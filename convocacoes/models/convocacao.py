from django.db import models
from .base import BaseModel
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog


class Convocacao(BaseModel):
    """
    Model for managing convocations
    """
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('publicada', 'Publicada'),
        ('em_andamento', 'Em Andamento'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    TIPO_CHOICES = [
        ('concurso', 'Concurso Público'),
        ('processo_seletivo', 'Processo Seletivo'),
        ('chamada_publica', 'Chamada Pública'),
        ('edital', 'Edital'),
    ]

    titulo = models.CharField(max_length=200)
    numero = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField()
    data_publicacao = models.DateTimeField(null=True, blank=True)
    data_inicio_inscricoes = models.DateTimeField(null=True, blank=True)
    data_fim_inscricoes = models.DateTimeField(null=True, blank=True)
    data_inicio_provas = models.DateTimeField(null=True, blank=True)
    data_fim_provas = models.DateTimeField(null=True, blank=True)
    data_resultado = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='rascunho')
    vagas_disponiveis = models.PositiveIntegerField(default=0)
    requisitos = models.TextField(blank=True)
    documentos_necessarios = models.TextField(blank=True)
    observacoes = models.TextField(blank=True)
    history = AuditlogHistoryField()

    class Meta:
        verbose_name = 'Convocação'
        verbose_name_plural = 'Convocações'
        ordering = ['-data_publicacao', 'titulo']

    def __str__(self):
        return f"{self.numero} - {self.titulo}"
    
auditlog.register(Convocacao)
