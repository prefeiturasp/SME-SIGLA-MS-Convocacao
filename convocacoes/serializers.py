from rest_framework import serializers
from django.utils import timezone
from .models import Convocacao


class ConvocacaoSerializer(serializers.ModelSerializer):
    dias_para_inscricao = serializers.SerializerMethodField()
    dias_para_prova = serializers.SerializerMethodField()
    
    class Meta:
        model = Convocacao
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_dias_para_inscricao(self, obj):
        """Calculate days until registration deadline"""
        if obj.data_fim_inscricoes:
            delta = obj.data_fim_inscricoes - timezone.now()
            return max(0, delta.days)
        return None
    
    def get_dias_para_prova(self, obj):
        """Calculate days until exam date"""
        if obj.data_inicio_provas:
            delta = obj.data_inicio_provas - timezone.now()
            return max(0, delta.days)
        return None
