"""
Tests for convocacoes views.
"""
import pytest
import json
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.test import APIClient
from convocacoes.models import Convocacao

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    """Fixture for API client"""
    return APIClient()


@pytest.fixture
def convocacao_data():
    """Fixture with test data for convocacao"""
    return {
        'titulo': 'Concurso Público para Professor',
        'numero': 'CONV-2024-001',
        'tipo': 'concurso',
        'descricao': 'Concurso público para professor de matemática',
        'data_publicacao': timezone.now().isoformat(),
        'data_inicio_inscricoes': (timezone.now() + timedelta(days=1)).isoformat(),
        'data_fim_inscricoes': (timezone.now() + timedelta(days=30)).isoformat(),
        'data_inicio_provas': (timezone.now() + timedelta(days=45)).isoformat(),
        'data_fim_provas': (timezone.now() + timedelta(days=47)).isoformat(),
        'data_resultado': (timezone.now() + timedelta(days=60)).isoformat(),
        'status': 'rascunho',
        'vagas_disponiveis': 10,
        'requisitos': 'Ensino superior completo',
        'documentos_necessarios': 'RG, CPF, diploma',
        'observacoes': 'Convocação de teste'
    }


@pytest.fixture
def sample_convocacao():
    """Fixture with a sample convocacao instance"""
    return Convocacao.objects.create(
        titulo='Concurso Público para Professor',
        numero='CONV-2024-001',
        tipo='concurso',
        descricao='Concurso público para professor de matemática',
        data_publicacao=timezone.now(),
        data_inicio_inscricoes=timezone.now() + timedelta(days=1),
        data_fim_inscricoes=timezone.now() + timedelta(days=30),
        data_inicio_provas=timezone.now() + timedelta(days=45),
        data_fim_provas=timezone.now() + timedelta(days=47),
        data_resultado=timezone.now() + timedelta(days=60),
        status='rascunho',
        vagas_disponiveis=10,
        requisitos='Ensino superior completo',
        documentos_necessarios='RG, CPF, diploma',
        observacoes='Convocação de teste'
    )


@pytest.fixture
def multiple_convocacoes():
    """Fixture with multiple convocacao instances"""
    convocacoes = []
    
    # Create convocacoes with different statuses and types
    convocacoes.append(Convocacao.objects.create(
        titulo='Concurso Público para Professor',
        numero='CONV-2024-001',
        tipo='concurso',
        descricao='Concurso público para professor de matemática',
        data_publicacao=timezone.now() - timedelta(days=2),
        status='publicada',
        vagas_disponiveis=10
    ))
    
    convocacoes.append(Convocacao.objects.create(
        titulo='Processo Seletivo para Técnico',
        numero='CONV-2024-002',
        tipo='processo_seletivo',
        descricao='Processo seletivo para técnico administrativo',
        data_publicacao=timezone.now() - timedelta(days=1),
        status='em_andamento',
        vagas_disponiveis=5
    ))
    
    convocacoes.append(Convocacao.objects.create(
        titulo='Chamada Pública para Estagiário',
        numero='CONV-2024-003',
        tipo='chamada_publica',
        descricao='Chamada pública para estagiário',
        data_publicacao=timezone.now(),
        status='finalizada',
        vagas_disponiveis=3
    ))
    
    return convocacoes


class TestConvocacaoViewSet:
    """Test cases for ConvocacaoViewSet"""

    def test_list_convocacoes(self, api_client, multiple_convocacoes):
        """Test listing all convocacoes"""
        url = reverse('convocacao-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
        assert response.data['count'] == 3

    def test_retrieve_convocacao(self, api_client, sample_convocacao):
        """Test retrieving a specific convocacao"""
        url = reverse('convocacao-detail', kwargs={'pk': sample_convocacao.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['titulo'] == sample_convocacao.titulo
        assert response.data['numero'] == sample_convocacao.numero
        assert response.data['tipo'] == sample_convocacao.tipo

    def test_create_convocacao(self, api_client, convocacao_data):
        """Test creating a new convocacao"""
        url = reverse('convocacao-list')
        response = api_client.post(url, convocacao_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['titulo'] == convocacao_data['titulo']
        assert response.data['numero'] == convocacao_data['numero']
        assert response.data['tipo'] == convocacao_data['tipo']
        
        # Verify the convocacao was created in the database
        assert Convocacao.objects.filter(numero=convocacao_data['numero']).exists()

    def test_create_convocacao_invalid_data(self, api_client):
        """Test creating convocacao with invalid data"""
        url = reverse('convocacao-list')
        invalid_data = {
            'titulo': '',  # Empty title should be invalid
            'numero': 'CONV-2024-001',
            'tipo': 'invalid_type',  # Invalid choice
        }
        response = api_client.post(url, invalid_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'titulo' in response.data
        assert 'tipo' in response.data

    def test_create_convocacao_duplicate_number(self, api_client, sample_convocacao, convocacao_data):
        """Test creating convocacao with duplicate number"""
        url = reverse('convocacao-list')
        convocacao_data['numero'] = sample_convocacao.numero  # Use existing number
        response = api_client.post(url, convocacao_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'numero' in response.data

    def test_update_convocacao(self, api_client, sample_convocacao):
        """Test updating a convocacao"""
        url = reverse('convocacao-detail', kwargs={'pk': sample_convocacao.pk})
        update_data = {
            'titulo': 'Concurso Público Atualizado',
            'status': 'publicada',
            'vagas_disponiveis': 15
        }
        response = api_client.patch(url, update_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['titulo'] == update_data['titulo']
        assert response.data['status'] == update_data['status']
        assert response.data['vagas_disponiveis'] == update_data['vagas_disponiveis']
        
        # Verify the update in the database
        sample_convocacao.refresh_from_db()
        assert sample_convocacao.titulo == update_data['titulo']
        assert sample_convocacao.status == update_data['status']

    def test_delete_convocacao(self, api_client, sample_convocacao):
        """Test deleting a convocacao"""
        url = reverse('convocacao-detail', kwargs={'pk': sample_convocacao.pk})
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Convocacao.objects.filter(pk=sample_convocacao.pk).exists()

    def test_filter_by_status(self, api_client, multiple_convocacoes):
        """Test filtering convocacoes by status"""
        url = reverse('convocacao-list')
        response = api_client.get(url, {'status': 'publicada'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['status'] == 'publicada'

    def test_filter_by_tipo(self, api_client, multiple_convocacoes):
        """Test filtering convocacoes by tipo"""
        url = reverse('convocacao-list')
        response = api_client.get(url, {'tipo': 'concurso'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['tipo'] == 'concurso'

    def test_search_by_titulo(self, api_client, multiple_convocacoes):
        """Test searching convocacoes by titulo"""
        url = reverse('convocacao-list')
        response = api_client.get(url, {'search': 'Professor'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert 'Professor' in response.data['results'][0]['titulo']

    def test_search_by_numero(self, api_client, multiple_convocacoes):
        """Test searching convocacoes by numero"""
        url = reverse('convocacao-list')
        response = api_client.get(url, {'search': 'CONV-2024-002'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['numero'] == 'CONV-2024-002'

    def test_ordering_by_titulo(self, api_client, multiple_convocacoes):
        """Test ordering convocacoes by titulo"""
        url = reverse('convocacao-list')
        response = api_client.get(url, {'ordering': 'titulo'})
        
        assert response.status_code == status.HTTP_200_OK
        titulos = [item['titulo'] for item in response.data['results']]
        assert titulos == sorted(titulos)

    def test_ordering_by_titulo_desc(self, api_client, multiple_convocacoes):
        """Test ordering convocacoes by titulo descending"""
        url = reverse('convocacao-list')
        response = api_client.get(url, {'ordering': '-titulo'})
        
        assert response.status_code == status.HTTP_200_OK
        titulos = [item['titulo'] for item in response.data['results']]
        assert titulos == sorted(titulos, reverse=True)

    def test_ordering_by_data_publicacao(self, api_client, multiple_convocacoes):
        """Test ordering convocacoes by data_publicacao"""
        url = reverse('convocacao-list')
        response = api_client.get(url, {'ordering': 'data_publicacao'})
        
        assert response.status_code == status.HTTP_200_OK
        # Should be ordered by data_publicacao ascending
        datas = [item['data_publicacao'] for item in response.data['results']]
        assert datas == sorted(datas)

    def test_default_ordering(self, api_client, multiple_convocacoes):
        """Test default ordering (most recent first)"""
        url = reverse('convocacao-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Default ordering should be by -data_publicacao, titulo
        # The most recent should be first
        assert response.data['results'][0]['numero'] == 'CONV-2024-003'  # Most recent

    def test_combined_filters(self, api_client, multiple_convocacoes):
        """Test combining multiple filters"""
        url = reverse('convocacao-list')
        response = api_client.get(url, {
            'status': 'em_andamento',
            'tipo': 'processo_seletivo'
        })
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        result = response.data['results'][0]
        assert result['status'] == 'em_andamento'
        assert result['tipo'] == 'processo_seletivo'

    def test_serializer_read_only_fields(self, api_client, sample_convocacao):
        """Test that read-only fields are not writable"""
        url = reverse('convocacao-detail', kwargs={'pk': sample_convocacao.pk})
        original_created_at = sample_convocacao.created_at
        original_updated_at = sample_convocacao.updated_at
        
        update_data = {
            'created_at': timezone.now().isoformat(),
            'updated_at': timezone.now().isoformat(),
            'titulo': 'Updated Title'
        }
        response = api_client.patch(url, update_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['titulo'] == 'Updated Title'
        
        # Verify read-only fields were not updated
        sample_convocacao.refresh_from_db()
        assert sample_convocacao.created_at == original_created_at
        # updated_at should be different (automatically updated by the model)
        assert sample_convocacao.updated_at != original_updated_at

    def test_serializer_computed_fields(self, api_client, sample_convocacao):
        """Test that computed fields are present in response"""
        url = reverse('convocacao-detail', kwargs={'pk': sample_convocacao.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'dias_para_inscricao' in response.data
        assert 'dias_para_prova' in response.data

    def test_pagination(self, api_client):
        """Test pagination functionality"""
        # Create more than one page of convocacoes
        for i in range(25):
            Convocacao.objects.create(
                titulo=f'Convocacao {i}',
                numero=f'CONV-2024-{i:03d}',
                tipo='concurso',
                descricao=f'Descrição {i}',
                status='rascunho'
            )
        
        url = reverse('convocacao-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'count' in response.data
        assert 'next' in response.data
        assert 'previous' in response.data
        assert 'results' in response.data
        assert response.data['count'] == 25
