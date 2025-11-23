# 🏗️ Documentação de Arquitetura

## 📋 **Visão Geral**

Este documento descreve a arquitetura do Sistema de Gestão de Contratos com IA Analytics, destacando as decisões de design, padrões utilizados e otimizações implementadas.

## 🏛️ **Arquitetura Geral**

### **Padrão Arquitetural**
- **MVC (Model-View-Controller)** com Flask
- **Service Layer** para lógica de negócio
- **Repository Pattern** para acesso a dados
- **Factory Pattern** para criação da aplicação

### **Tecnologias**
```python
# Backend
Flask 2.3+          # Web Framework
SQLAlchemy 3.1+     # ORM
SQLite 3            # Database (dev) / PostgreSQL (prod)
Redis 5.0+          # Cache (planejado)

# Frontend
Bootstrap 5         # CSS Framework
Chart.js            # Gráficos
Jinja2              # Templates

# Analytics & IA
OpenAI API          # IA Analytics (opcional)
Pandas 2.1+         # Data Analysis
NumPy 1.25+         # Computação Numérica
```

## 📁 **Estrutura de Diretórios**

```
projetoia/
├── 📁 app/                        # Aplicação principal
│   ├── 📄 __init__.py             # Factory pattern & configuração
│   ├── 📁 api/                    # API REST endpoints
│   │   ├── 📄 __init__.py         # Blueprint API
│   │   └── 📄 routes.py           # Endpoints REST
│   ├── 📁 web/                    # Web interface
│   │   ├── 📄 __init__.py         # Blueprint Web
│   │   └── 📄 routes.py           # Páginas web
│   ├── 📁 models/                 # Models SQLAlchemy
│   │   ├── 📄 __init__.py
│   │   ├── 📄 client.py           # Model Cliente
│   │   ├── 📄 contract.py         # Model Contrato
│   │   ├── 📄 user.py             # Model Usuário
│   │   └── 📄 notification.py     # Model Notificação
│   ├── 📁 services/               # Lógica de negócio
│   │   ├── 📄 dashboard_service.py # Dashboard otimizado
│   │   ├── 📄 agente_ia.py        # IA Analytics
│   │   ├── 📄 ai_analytics.py     # Analytics avançados
│   │   └── 📄 relatorios.py       # Geração de relatórios
│   ├── 📁 utils/                  # Utilitários
│   │   ├── 📄 decorators.py       # Decorators reutilizáveis
│   │   ├── 📄 helpers.py          # Funções auxiliares
│   │   ├── 📄 imports.py          # Imports centralizados
│   │   └── 📄 error_handler.py    # Tratamento de erros
│   └── 📄 constants.py            # Constantes centralizadas
├── 📁 static/                     # Assets frontend
├── 📁 templates/                  # Templates Jinja2
├── 📁 migrations/                 # Migrações DB
├── 📁 tests/                      # Testes automatizados
├── 📁 scripts/                    # Scripts utilitários
├── 📄 config.py                   # Configurações
├── 📄 requirements.txt            # Dependências
└── 📄 run.py                      # Entry point
```

## 🔄 **Fluxo de Dados**

### **Request Flow**
```
Client Request
    ↓
Flask App (Factory Pattern)
    ↓
Blueprint (api/web)
    ↓
Decorator (@handle_route_errors)
    ↓
Service Layer (DashboardService)
    ↓
Repository (SQLAlchemy ORM)
    ↓
Database (SQLite/PostgreSQL)
```

### **Cache Strategy**
```python
# LRU Cache para dados frequentes
@lru_cache(maxsize=CACHE_SIZE_DEFAULT)
def get_basic_stats_cached():
    # Query otimizada com cache
    
# Planejado: Redis para cache distribuído
@cache_response(timeout=300)
def expensive_operation():
    # Cache em Redis
```

## 🚀 **Otimizações de Performance**

### **1. Query Optimization**
```python
# Antes: Múltiplas queries
clients_count = Client.query.count()
contracts_count = Contract.query.count()
active_contracts = Contract.query.filter_by(status='ativo').count()

# Depois: Query única otimizada
results = db.session.execute(text("""
    SELECT 
        COUNT(*) as total_clients,
        (SELECT COUNT(*) FROM contracts) as total_contracts,
        (SELECT COUNT(*) FROM contracts WHERE status = 'ativo') as active_contracts
    FROM clients
""")).fetchone()
```

### **2. Database Indexes**
```sql
-- Índices para performance
CREATE INDEX idx_clients_email ON clients(email);
CREATE INDEX idx_contracts_status ON contracts(status);
CREATE INDEX idx_contracts_client_id ON contracts(client_id);
CREATE INDEX idx_contracts_status_end_date ON contracts(status, end_date);
```

### **3. Cache Intelligence**
```python
# Cache hierárquico
CACHE_SIZE_DEFAULT = 32  # Dados frequentes
CACHE_SIZE_SMALL = 16    # Métricas
CACHE_SIZE_LARGE = 100   # Relatórios pesados
```

## 🎯 **Design Patterns**

### **1. Factory Pattern**
```python
# app/__init__.py
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_blueprints(app)
    register_error_handlers(app)
    return app
```

### **2. Service Layer**
```python
# app/services/dashboard_service.py
class DashboardService:
    @staticmethod
    @lru_cache(maxsize=CACHE_SIZE_DEFAULT)
    def get_basic_stats():
        # Lógica centralizada
```

### **3. Decorator Pattern**
```python
# app/utils/decorators.py
@handle_route_errors('dashboard.html')
def dashboard():
    # Tratamento automático de erros
```

## 🔧 **Configuration Management**

### **Environment-based Config**
```python
# config.py
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
```

### **Constants Centralization**
```python
# app/constants.py
CACHE_TIMEOUT = 300
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
CONTRACT_STATUSES = ['rascunho', 'ativo', 'suspenso', 'concluído', 'cancelado']
```

## 🛡️ **Security Measures**

### **Implemented**
- 🔐 CSRF Protection via Flask-WTF
- 🚦 Rate limiting básico
- 🔒 Input validation
- 📝 SQL injection protection via ORM
- 🔐 Secure headers

### **Planned**
- 🚦 Redis-based rate limiting
- 🔐 JWT authentication
- 🛡️ CORS configuration
- 🔐 Audit logging

## 📊 **Monitoring & Logging**

### **Current Implementation**
```python
# Structured logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# Error tracking
current_app.logger.error(f"Erro em {func.__name__}: {str(e)}")
```

### **Planned**
- 📊 Sentry integration
- 📈 Performance metrics
- 📊 Database query logging
- 📈 API response time tracking

## 🧪 **Testing Strategy**

### **Current Status**
- 🧪 Manual testing
- 🔧 Basic integration tests

### **Planned Implementation**
```python
# tests/test_dashboard_service.py
def test_get_basic_stats():
    with app.test_request_context():
        stats = DashboardService.get_basic_stats()
        assert 'total_clients' in stats
        assert isinstance(stats['total_clients'], int)
```

### **Coverage Goals**
- 🎯 Unit tests: >80%
- 🔧 Integration tests: >60%
- 📊 E2E tests: >40%

## 🚀 **Scaling Considerations**

### **Current Limitations**
- 🗄️ SQLite for development only
- 🧠 In-memory cache
- 📦 Single instance deployment

### **Scaling Path**
1. **Database**: PostgreSQL with read replicas
2. **Cache**: Redis cluster
3. **Application**: Load balancer + multiple instances
4. **Files**: CDN for static assets
5. **Monitoring**: Full observability stack

## 🔄 **Future Enhancements**

### **Short Term (v2.1.0)**
- 🧪 Comprehensive test suite
- 📚 API documentation
- 🔄 Redis cache implementation

### **Medium Term (v2.2.0)**
- 🚀 Microservices architecture
- 📊 Advanced analytics
- 🔐 Enhanced security

### **Long Term (v3.0.0)**
- 🌐 Multi-tenant support
- 🤖 Advanced AI features
- 📱 Mobile app API

---

## 📞 **Contact & Support**

Para questões sobre arquitetura:
- 📧 Email: [team@example.com]
- 📋 Issues: [GitHub Issues]
- 📚 Documentation: [Wiki]

---

*Última atualização: 23/11/2025*
