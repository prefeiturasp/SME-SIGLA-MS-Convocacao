"""
Django management command to clear all convocacoes.
"""
from django.core.management.base import BaseCommand
from django.db import connection
from convocacoes.models import Convocacao


class Command(BaseCommand):
    help = 'Remove todos os registros da tabela de convocações'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirma a exclusão de todas as convocações'
        )

    def handle(self, *args, **options):
        confirm = options['confirm']
        
        # Contar registros existentes
        total_registros = Convocacao.objects.count()
        
        if total_registros == 0:
            self.stdout.write(
                self.style.WARNING('⚠️  Não há convocações para remover.')
            )
            return
        
        if not confirm:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  Você está prestes a remover {total_registros} convocações!'
                )
            )
            self.stdout.write(
                'Use --confirm para confirmar a operação.'
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(f'Removendo {total_registros} convocações...')
        )
        
        try:
            # Método 1: Usando delete() em queryset (mais seguro)
            Convocacao.objects.all().delete()
            
            # Método 2: Usando SQL direto (mais rápido, mas menos seguro)
            # with connection.cursor() as cursor:
            #     cursor.execute("DELETE FROM convocacoes_convocacao")
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ {total_registros} convocações removidas com sucesso!')
            )
            
            # Verificar se realmente foi limpo
            registros_restantes = Convocacao.objects.count()
            if registros_restantes == 0:
                self.stdout.write(
                    self.style.SUCCESS('✅ Tabela completamente limpa!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Ainda restam {registros_restantes} convocações.')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao remover convocações: {e}')
            )
