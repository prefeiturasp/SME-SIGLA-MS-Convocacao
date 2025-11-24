from django.contrib import admin
from .models import Convocacao

@admin.register(Convocacao)
class ConvocacaoAdmin(admin.ModelAdmin):
    """Admin configuration for Convocacao model"""
    list_display = ['numero', 'titulo', 'tipo', 'status', 'data_publicacao', 'vagas_disponiveis', 'created_at']
    list_filter = ['status', 'tipo', 'data_publicacao', 'created_at', 'is_active']
    search_fields = ['titulo', 'numero', 'descricao']
    readonly_fields = ['created_at', 'updated_at', 'is_active']
    date_hierarchy = 'data_publicacao'
    list_per_page = 25
    list_editable = ['status']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'numero', 'tipo', 'descricao')
        }),
        ('Datas e Prazos', {
            'fields': ('data_publicacao', 'data_inicio_inscricoes', 'data_fim_inscricoes', 
                      'data_inicio_provas', 'data_fim_provas', 'data_resultado')
        }),
        ('Status e Vagas', {
            'fields': ('status', 'vagas_disponiveis')
        }),
        ('Requisitos e Documentos', {
            'fields': ('requisitos', 'documentos_necessarios', 'observacoes')
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at', 'is_active'),
            'classes': ('collapse',)
        }),
    )
