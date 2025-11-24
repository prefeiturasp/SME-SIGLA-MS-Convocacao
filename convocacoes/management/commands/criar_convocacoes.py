"""
Django management command to create sample convocacoes.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from convocacoes.models import Convocacao
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Cria convocações de exemplo para desenvolvimento'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Número de convocações a serem criadas (padrão: 10)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        self.stdout.write(
            self.style.SUCCESS(f'Criando {count} convocações...')
        )
        
        # Dados de exemplo
        titulos = [
            'Concurso Público para Professor de Matemática',
            'Processo Seletivo para Técnico Administrativo',
            'Chamada Pública para Médico Clínico Geral',
            'Edital para Enfermeiro',
            'Concurso Público para Pedagogo',
            'Processo Seletivo para Assistente Social',
            'Chamada Pública para Psicólogo',
            'Edital para Nutricionista',
            'Concurso Público para Fisioterapeuta',
            'Processo Seletivo para Fonoaudiólogo',
            'Chamada Pública para Terapeuta Ocupacional',
            'Edital para Educador Físico',
            'Concurso Público para Bibliotecário',
            'Processo Seletivo para Contador',
            'Chamada Pública para Engenheiro Civil'
        ]
        
        tipos = ['concurso', 'processo_seletivo', 'chamada_publica', 'edital']
        status_choices = ['rascunho', 'publicada', 'em_andamento', 'finalizada']
        
        convocacoes_criadas = []
        
        for i in range(count):
            # Gerar número único
            numero = f'CONV-{2024}-{str(i+1).zfill(3)}'
            
            # Verificar se número já existe
            while Convocacao.objects.filter(numero=numero).exists():
                numero = f'CONV-{2024}-{str(i+1).zfill(3)}-{random.randint(1, 999)}'
            
            # Gerar datas
            hoje = timezone.now()
            data_publicacao = hoje - timedelta(days=random.randint(1, 30))
            data_inicio_inscricoes = data_publicacao + timedelta(days=random.randint(1, 7))
            data_fim_inscricoes = data_inicio_inscricoes + timedelta(days=random.randint(15, 30))
            data_inicio_provas = data_fim_inscricoes + timedelta(days=random.randint(7, 14))
            data_fim_provas = data_inicio_provas + timedelta(days=random.randint(1, 3))
            data_resultado = data_fim_provas + timedelta(days=random.randint(7, 15))
            
            convocacao = Convocacao.objects.create(
                titulo=titulos[i % len(titulos)],
                numero=numero,
                tipo=random.choice(tipos),
                descricao=f'Descrição detalhada da convocação {numero}. Esta é uma convocação de exemplo para desenvolvimento e testes do sistema.',
                data_publicacao=data_publicacao,
                data_inicio_inscricoes=data_inicio_inscricoes,
                data_fim_inscricoes=data_fim_inscricoes,
                data_inicio_provas=data_inicio_provas,
                data_fim_provas=data_fim_provas,
                data_resultado=data_resultado,
                status=random.choice(status_choices),
                vagas_disponiveis=random.randint(1, 50),
                requisitos=f'Requisitos para a convocação {numero}:\n- Ensino superior completo\n- Experiência na área\n- Disponibilidade para trabalhar em horário comercial',
                documentos_necessarios=f'Documentos necessários para {numero}:\n- Cópia do RG e CPF\n- Comprovante de residência\n- Currículo atualizado\n- Diplomas e certificados',
                observacoes=f'Convocacao de exemplo {i+1} criada automaticamente'
            )
            
            self.stdout.write(
                f'  ✓ Criada convocação: {convocacao.numero} - {convocacao.titulo}'
            )
            
            convocacoes_criadas.append(convocacao)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ {len(convocacoes_criadas)} convocações criadas com sucesso!'
            )
        )
        
        # Estatísticas
        rascunho = Convocacao.objects.filter(status='rascunho').count()
        publicadas = Convocacao.objects.filter(status='publicada').count()
        em_andamento = Convocacao.objects.filter(status='em_andamento').count()
        finalizadas = Convocacao.objects.filter(status='finalizada').count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'📊 Estatísticas: {rascunho} rascunho, {publicadas} publicadas, {em_andamento} em andamento, {finalizadas} finalizadas'
            )
        )
