"""
Constantes da aplicação - Centralização de configurações
"""

# Cache
CACHE_TIMEOUT = 300  # 5 minutos
CACHE_SIZE_DEFAULT = 32
CACHE_SIZE_SMALL = 16
CACHE_SIZE_LARGE = 100

# Paginação
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Rate Limiting
DEFAULT_RATE_LIMIT = 100  # requisições por minuto
API_RATE_LIMIT = 10       # requisições por minuto

# Contratos
DEFAULT_RENEWAL_DAYS = 30
CONTRACT_STATUSES = ['rascunho', 'ativo', 'suspenso', 'concluído', 'cancelado']
CONTRACT_TYPES = ['serviço', 'produto', 'licença', 'consultoria']

# Upload
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

# API
API_VERSION = 'v1'
DEFAULT_API_RESPONSE = {
    'error': 'Internal Error',
    'message': 'Erro interno do servidor'
}

# Log
LOG_MAX_BYTES = 10240000  # 10MB
LOG_BACKUP_COUNT = 10

# AI/Analytics
AI_MAX_TOKENS = 500
AI_TEMPERATURE = 0.7
AI_MAX_HISTORY = 10

# Validações
MIN_PASSWORD_LENGTH = 8
MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 120
MAX_DOCUMENT_LENGTH = 20

# Datas
DEFAULT_EXPIRY_DAYS = 30
UPCOMING_EXPIRY_DAYS = [30, 60, 90]

# Formatos
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
CURRENCY = 'BRL'

# Mensagens
FLASH_MESSAGES = {
    'error_default': 'Erro ao processar solicitação',
    'success_save': 'Salvo com sucesso',
    'success_delete': 'Excluído com sucesso',
    'error_not_found': 'Recurso não encontrado',
    'error_validation': 'Dados inválidos'
}

# Templates
ERROR_TEMPLATES = {
    'default': 'errors/error.html',
    '404': 'errors/404.html',
    '500': 'errors/500.html'
}

# Configurações de ambiente
ENVIRONMENTS = ['development', 'testing', 'production']
DEFAULT_ENV = 'development'
