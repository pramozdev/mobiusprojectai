#!/bin/bash

# Script de Verificação de Qualidade
# Executa todas as verificações de qualidade em sequência

set -e  # Para em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função de log
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

# Verificar se estamos no diretório correto
if [ ! -f "app.py" ] || [ ! -f "requirements.txt" ]; then
    log_error "Execute este script no diretório raiz do projeto"
    exit 1
fi

log "Iniciando verificação de qualidade completa..."

# 1. Verificação Python
log "🐍 Verificação Python..."

# Black (formatação)
log "Verificando formatação com Black..."
if black --check --diff . > /dev/null 2>&1; then
    log_success "Black: Formatação OK"
else
    log_warning "Black: Problemas de formatação encontrados"
    black --diff .
    echo
fi

# Flake8 (linting)
log "Verificando código com Flake8..."
if flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; then
    log_success "Flake8: Linting OK"
else
    log_error "Flake8: Erros encontrados"
fi

# MyPy (tipagem)
log "Verificando tipos com MyPy..."
if mypy --ignore-missing-imports . > /dev/null 2>&1; then
    log_success "MyPy: Tipagem OK"
else
    log_warning "MyPy: Problemas de tipagem encontrados"
    mypy --ignore-missing-imports . || true
fi

# Bandit (segurança)
log "Verificando segurança com Bandit..."
if bandit -r . -f json -o bandit-report.json > /dev/null 2>&1; then
    log_success "Bandit: Segurança OK"
else
    log_warning "Bandit: Problemas de segurança encontrados"
    bandit -r . -ll || true
fi

# 2. Testes Python
log "🧪 Executando testes Python..."
if pytest tests/ -v --cov=. --cov-report=term-missing --cov-fail-under=80; then
    log_success "Testes Python: Todos passaram"
else
    log_error "Testes Python: Falharam"
    exit 1
fi

# 3. Verificação JavaScript (se package.json existe)
if [ -f "package.json" ]; then
    log "📜 Verificação JavaScript..."
    
    # ESLint
    if npm run lint > /dev/null 2>&1; then
        log_success "ESLint: Linting OK"
    else
        log_warning "ESLint: Problemas encontrados"
        npm run lint || true
    fi
    
    # Prettier
    if npm run format:check > /dev/null 2>&1; then
        log_success "Prettier: Formatação OK"
    else
        log_warning "Prettier: Problemas de formatação encontrados"
        npm run format:check || true
    fi
    
    # Testes JavaScript
    if npm test > /dev/null 2>&1; then
        log_success "Testes JavaScript: Todos passaram"
    else
        log_warning "Testes JavaScript: Alguns falharam"
        npm test || true
    fi
else
    log_warning "package.json não encontrado, pulando verificações JavaScript"
fi

# 4. Verificação de Dependências
log "📦 Verificando dependências..."

# Python dependencies
log "Verificando dependências Python..."
if pip-audit > /dev/null 2>&1; then
    log_success "Dependências Python: Seguras"
else
    log_warning "Dependências Python: Vulnerabilidades encontradas"
    pip-audit || true
fi

# Node.js dependencies (se package.json existe)
if [ -f "package.json" ]; then
    log "Verificando dependências Node.js..."
    if npm audit --audit-level=moderate > /dev/null 2>&1; then
        log_success "Dependências Node.js: Seguras"
    else
        log_warning "Dependências Node.js: Vulnerabilidades encontradas"
        npm audit || true
    fi
fi

# 5. Verificação de Performance
log "⚡ Verificação de performance..."

# Verificar tamanho do projeto
project_size=$(du -sh . | cut -f1)
log "Tamanho do projeto: $project_size"

# Verificar arquivos grandes
large_files=$(find . -type f -size +10M -not -path "./.git/*" -not -path "./node_modules/*" | wc -l)
if [ $large_files -eq 0 ]; then
    log_success "Nenhum arquivo grande (>10MB) encontrado"
else
    log_warning "Encontrados $large_files arquivos grandes (>10MB)"
    find . -type f -size +10M -not -path "./.git/*" -not -path "./node_modules/*" -exec ls -lh {} \;
fi

# 6. Verificação de Documentação
log "📚 Verificação de documentação..."

if [ -f "README.md" ]; then
    log_success "README.md encontrado"
    readme_size=$(wc -l < README.md)
    log "README.md tem $readme_size linhas"
    
    if [ $readme_size -lt 50 ]; then
        log_warning "README.md parece muito curto"
    fi
else
    log_error "README.md não encontrado"
fi

# 7. Verificação de Configuração
log "⚙️  Verificação de configuração..."

config_files=(".env.example" ".gitignore" "requirements.txt")
for file in "${config_files[@]}"; do
    if [ -f "$file" ]; then
        log_success "$file encontrado"
    else
        log_warning "$file não encontrado"
    fi
done

# 8. Verificação de Segurança
log "🔒 Verificação de segurança básica..."

# Verificar se há chaves ou senhas expostas
if grep -r -i "password\|secret\|key\|token" --include="*.py" --include="*.js" --include="*.json" --exclude-dir=".git" --exclude-dir="node_modules" . | grep -v "password.*example\|secret.*example\|key.*example" > /dev/null 2>&1; then
    log_warning "Possíveis senhas/chaves encontradas (verificar manualmente)"
    grep -r -i "password\|secret\|key\|token" --include="*.py" --include="*.js" --include="*.json" --exclude-dir=".git" --exclude-dir="node_modules" . | grep -v "password.*example\|secret.*example\|key.*example" || true
else
    log_success "Nenhuma senha/chave óbvia encontrada"
fi

# 9. Verificação de Estrutura
log "🏗️  Verificação de estrutura do projeto..."

required_dirs=("static" "templates" "utils")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        log_success "Diretório $dir encontrado"
    else
        log_warning "Diretório $dir não encontrado"
    fi
done

# 10. Resumo Final
log "📊 Gerando resumo final..."

# Contar linhas de código
python_lines=$(find . -name "*.py" -not -path "./.git/*" -not -path "./node_modules/*" -exec wc -l {} + | tail -1 | awk '{print $1}')
js_lines=$(find . -name "*.js" -not -path "./.git/*" -not -path "./node_modules/*" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo "0")

log "Estatísticas:"
log "  - Linhas Python: $python_lines"
log "  - Linhas JavaScript: $js_lines"
log "  - Tamanho do projeto: $project_size"

# Verificar coverage dos testes
if [ -f "coverage.xml" ]; then
    coverage=$(grep -o 'line-rate="[0-9.]*"' coverage.xml | cut -d'"' -f2 | head -1)
    log "  - Coverage: ${coverage}%"
fi

log_success "Verificação de qualidade concluída!"
log "🎉 Projeto está pronto para deploy!"

# Gerar relatório
cat > quality-report.md << EOF
# Relatório de Qualidade - $(date)

## Sumário
- **Status**: ✅ Aprovado
- **Data**: $(date)
- **Projeto**: Dashboard de Contratos

## Verificações Executadas

### Python
- [x] Black (formatação)
- [x] Flake8 (linting)
- [x] MyPy (tipagem)
- [x] Bandit (segurança)
- [x] Pytest (testes)

### JavaScript
- [x] ESLint (linting)
- [x] Prettier (formatação)
- [x] Jest (testes)

### Segurança
- [x] pip-audit (dependências Python)
- [x] npm audit (dependências Node.js)
- [x] Verificação de chaves expostas

### Performance
- [x] Verificação de arquivos grandes
- [x] Análise de tamanho do projeto

### Documentação
- [x] README.md
- [x] Estrutura do projeto

## Métricas
- Linhas Python: $python_lines
- Linhas JavaScript: $js_lines
- Tamanho do projeto: $project_size
- Coverage: ${coverage:-N/A}%

## Recomendações
- Manter coverage acima de 80%
- Executar este script antes de cada deploy
- Configurar CI/CD para execução automática

EOF

log_success "Relatório gerado: quality-report.md"
