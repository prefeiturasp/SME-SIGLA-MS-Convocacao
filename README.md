# SME-SIGLA-MS-Convocacao

Microserviço para gerenciamento de convocações do sistema SME-SIGLA.

## Descrição

Este microserviço é responsável pelo gerenciamento de convocações, incluindo concursos públicos, processos seletivos, chamadas públicas e editais.

## Funcionalidades

- ✅ CRUD completo de convocações
- ✅ API REST com Django REST Framework
- ✅ Filtros e busca avançada
- ✅ Auditoria de alterações
- ✅ Interface administrativa
- ✅ Testes automatizados
- ✅ Docker e Docker Compose
- ✅ Comandos de management para dados de exemplo

## Tecnologias

- **Backend**: Django 5.2.5
- **API**: Django REST Framework 3.15.2
- **Banco de Dados**: PostgreSQL / SQLite
- **Auditoria**: django-auditlog
- **Containerização**: Docker
- **Testes**: pytest

## Estrutura do Projeto

```
SME-SIGLA-MS-Convocacao/
├── config/                 # Configurações do Django
├── convocacoes/           # App principal
│   ├── models/            # Modelos de dados
│   ├── views.py           # Views da API
│   ├── serializers.py     # Serializers
│   ├── urls.py            # URLs da API
│   ├── admin.py           # Interface administrativa
│   ├── management/        # Comandos customizados
│   └── tests/             # Testes
├── requirements/          # Dependências Python
├── docker-compose.yml     # Orquestração de containers
├── Dockerfile            # Imagem Docker
└── manage.py             # Script de gerenciamento Django
```

## Instalação e Configuração

### Pré-requisitos

- Python 3.12+
- Docker e Docker Compose (opcional)
- PostgreSQL (opcional, SQLite por padrão)

### Instalação Local

1. Clone o repositório:
```bash
git clone <repository-url>
cd SME-SIGLA-MS-Convocacao
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements/local.txt
```

4. Configure as variáveis de ambiente:
```bash
cp env.example .env
# Edite o arquivo .env conforme necessário
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Execute o servidor:
```bash
python manage.py runserver
```

### Instalação com Docker

1. Clone o repositório e configure o ambiente:
```bash
git clone <repository-url>
cd SME-SIGLA-MS-Convocacao
cp env.example .env
```

2. Execute com Docker Compose:
```bash
docker-compose up --build
```

## Uso

### API Endpoints

- **Listar convocações**: `GET /api/v1/convocacoes/`
- **Criar convocação**: `POST /api/v1/convocacoes/`
- **Detalhar convocação**: `GET /api/v1/convocacoes/{id}/`
- **Atualizar convocação**: `PUT/PATCH /api/v1/convocacoes/{id}/`
- **Excluir convocação**: `DELETE /api/v1/convocacoes/{id}/`

### Filtros Disponíveis

- `status`: Filtrar por status da convocação
- `tipo`: Filtrar por tipo (concurso, processo_seletivo, etc.)
- `data_publicacao`: Filtrar por data de publicação
- `search`: Busca por título, número ou descrição

### Comandos de Management

#### Criar dados de exemplo:
```bash
python manage.py criar_convocacoes --count 20
```

#### Limpar todos os dados:
```bash
python manage.py limpar_convocacoes --confirm
```

### Interface Administrativa

Acesse `/admin/` para gerenciar as convocações através da interface administrativa do Django.

## Desenvolvimento

### Executar Testes

```bash
# Todos os testes
pytest

# Testes específicos
pytest convocacoes/tests/

# Com cobertura
pytest --cov=convocacoes
```

### Estrutura de Dados

#### Convocacao

- `titulo`: Título da convocação
- `numero`: Número único da convocação
- `tipo`: Tipo (concurso, processo_seletivo, chamada_publica, edital)
- `descricao`: Descrição detalhada
- `data_publicacao`: Data de publicação
- `data_inicio_inscricoes`: Data de início das inscrições
- `data_fim_inscricoes`: Data de fim das inscrições
- `data_inicio_provas`: Data de início das provas
- `data_fim_provas`: Data de fim das provas
- `data_resultado`: Data de publicação do resultado
- `status`: Status atual (rascunho, publicada, em_andamento, finalizada, cancelada)
- `vagas_disponiveis`: Número de vagas disponíveis
- `requisitos`: Requisitos para participação
- `documentos_necessarios`: Documentos necessários
- `observacoes`: Observações adicionais

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.