#!/bin/bash

# Script de Setup do Projeto
# Configura ambiente e dependências para desenvolvimento

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar pré-requisitos
check_prerequisites() {
    log "Verificando pré-requisitos..."
    
    # Python
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version | cut -d' ' -f2)
        log_success "Python $python_version encontrado"
    else
        log_error "Python 3 não encontrado. Instale Python 3.12+"
        exit 1
    fi
    
    # Node.js
    if command -v node &> /dev/null; then
        node_version=$(node --version)
        log_success "Node.js $node_version encontrado"
    else
        log_warning "Node.js não encontrado. Opcional para frontend"
    fi
    
    # npm
    if command -v npm &> /dev/null; then
        npm_version=$(npm --version)
        log_success "npm $npm_version encontrado"
    else
        log_warning "npm não encontrado. Opcional para frontend"
    fi
    
    # Git
    if command -v git &> /dev/null; then
        git_version=$(git --version)
        log_success "Git $git_version encontrado"
    else
        log_warning "Git não encontrado. Recomendado para controle de versão"
    fi
}

# Setup Python
setup_python() {
    log "🐍 Configurando ambiente Python..."
    
    # Criar ambiente virtual
    if [ ! -d "venv" ]; then
        log "Criando ambiente virtual..."
        python3 -m venv venv
        log_success "Ambiente virtual criado"
    else
        log_success "Ambiente virtual já existe"
    fi
    
    # Ativar ambiente virtual
    log "Ativando ambiente virtual..."
    source venv/bin/activate
    
    # Atualizar pip
    log "Atualizando pip..."
    pip install --upgrade pip
    
    # Instalar dependências
    log "Instalando dependências Python..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        log_success "Dependências Python instaladas"
    else
        log_error "requirements.txt não encontrado"
        exit 1
    fi
    
    # Instalar dependências de desenvolvimento
    log "Instalando dependências de desenvolvimento..."
    pip install pytest pytest-cov pytest-mock black flake8 bandit mypy pip-audit
    
    log_success "Ambiente Python configurado"
}

# Setup JavaScript
setup_javascript() {
    if command -v node &> /dev/null && [ -f "package.json" ]; then
        log "📜 Configurando ambiente JavaScript..."
        
        # Instalar dependências
        log "Instalando dependências Node.js..."
        npm install
        
        log_success "Ambiente JavaScript configurado"
    else
        log_warning "Pulando configuração JavaScript (Node.js não encontrado ou sem package.json)"
    fi
}

# Setup Banco de Dados
setup_database() {
    log "🗄️  Configurando banco de dados..."
    
    # Criar diretório instance se não existir
    if [ ! -d "instance" ]; then
        mkdir -p instance
        log_success "Diretório instance criado"
    fi
    
    # Verificar se banco existe
    if [ -f "instance/contratos.db" ]; then
        log_success "Banco de dados já existe"
    else
        log "Inicializando banco de dados..."
        python3 -c "
from app import init_database
try:
    init_database()
    print('Banco de dados inicializado com sucesso')
except Exception as e:
    print(f'Erro ao inicializar banco: {e}')
    exit(1)
"
        log_success "Banco de dados inicializado"
    fi
}

# Setup Configuração
setup_config() {
    log "⚙️  Configurando arquivos de configuração..."
    
    # Criar .env se não existir
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            log_success ".env criado a partir de .env.example"
            log_warning "Edite .env com suas configurações"
        else
            log_warning ".env.example não encontrado. Criando .env básico..."
            cat > .env << EOF
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/contratos.db
EOF
            log_success ".env básico criado"
        fi
    else
        log_success ".env já existe"
    fi
    
    # Criar logs directory
    if [ ! -d "logs" ]; then
        mkdir -p logs
        log_success "Diretório logs criado"
    fi
    
    # Verificar .gitignore
    if [ ! -f ".gitignore" ]; then
        log "Criando .gitignore..."
        cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Flask
instance/
.webassets-cache

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Coverage
.coverage
htmlcov/
.pytest_cache/

# Build
build/
dist/

# Database
*.db
*.sqlite
*.sqlite3

# Temporary files
*.tmp
*.temp
EOF
        log_success ".gitignore criado"
    else
        log_success ".gitignore já existe"
    fi
}

# Setup Git Hooks (se Git estiver disponível)
setup_git_hooks() {
    if command -v git &> /dev/null && [ -d ".git" ]; then
        log "🪝 Configurando Git hooks..."
        
        # Criar pre-commit hook
        cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Pre-commit hook para qualidade de código
echo "🔍 Executando verificações pre-commit..."

# Python formatting check
if command -v black &> /dev/null; then
    if ! black --check . > /dev/null 2>&1; then
        echo "❌ Formatação Python falhou. Execute 'black .' para corrigir."
        exit 1
    fi
fi

# Python linting
if command -v flake8 &> /dev/null; then
    if ! flake8 .; then
        echo "❌ Linting Python falhou."
        exit 1
    fi
fi

# JavaScript checks (se package.json existe)
if [ -f "package.json" ] && command -v npm &> /dev/null; then
    if ! npm run lint > /dev/null 2>&1; then
        echo "❌ Linting JavaScript falhou."
        exit 1
    fi
fi

echo "✅ Verificações pre-commit passaram!"
exit 0
EOF
        
        chmod +x .git/hooks/pre-commit
        log_success "Git hooks configurados"
    else
        log_warning "Git não disponível ou não é um repositório Git"
    fi
}

# Setup Testes
setup_tests() {
    log "🧪 Configurando ambiente de testes..."
    
    # Criar diretório de testes se não existir
    if [ ! -d "tests" ]; then
        mkdir -p tests
        log_success "Diretório tests criado"
    fi
    
    # Criar arquivo de configuração de testes
    cat > pytest.ini << EOF
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=.
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests
EOF
    
    log_success "Configuração de testes criada"
}

# Verificar Setup
verify_setup() {
    log "🔍 Verificando setup..."
    
    # Verificar ambiente virtual
    if [ -d "venv" ]; then
        log_success "Ambiente virtual OK"
    else
        log_error "Ambiente virtual não encontrado"
        return 1
    fi
    
    # Verificar dependências Python
    source venv/bin/activate
    if python -c "import flask, pytest, black, flake8" > /dev/null 2>&1; then
        log_success "Dependências Python OK"
    else
        log_error "Dependências Python com problemas"
        return 1
    fi
    
    # Verificar banco de dados
    if [ -f "instance/contratos.db" ]; then
        log_success "Banco de dados OK"
    else
        log_error "Banco de dados não encontrado"
        return 1
    fi
    
    # Verificar configuração
    if [ -f ".env" ]; then
        log_success "Arquivo .env OK"
    else
        log_error "Arquivo .env não encontrado"
        return 1
    fi
    
    log_success "Setup verificado com sucesso!"
}

# Main
main() {
    log "🚀 Iniciando setup do projeto Dashboard de Contratos..."
    
    check_prerequisites
    setup_python
    setup_javascript
    setup_database
    setup_config
    setup_git_hooks
    setup_tests
    
    if verify_setup; then
        log_success "🎉 Setup concluído com sucesso!"
        log ""
        log "Próximos passos:"
        log "1. Ative o ambiente virtual: source venv/bin/activate"
        log "2. Edite o arquivo .env com suas configurações"
        log "3. Execute o servidor: python app.py"
        log "4. Execute testes: pytest"
        log "5. Execute verificação de qualidade: ./scripts/quality-check.sh"
        log ""
        log "🌐 Acesse o dashboard em: http://localhost:5000/dashboard"
    else
        log_error "Setup falhou. Verifique os erros acima."
        exit 1
    fi
}

# Executar main
main "$@"
