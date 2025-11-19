# 📁 Estrutura do Projeto

## Organização de Arquivos e Pastas

```
projetoia/
│
├── 📄 README.md                    # Documentação principal
├── 📄 QUICKSTART.md               # Guia rápido de início
├── 📄 SECURITY.md                 # Guia de segurança
├── 📄 DASHBOARD.md                # Documentação do dashboard
├── 📄 PROJECT_STRUCTURE.md        # Este arquivo
│
├── 📄 requirements.txt            # Dependências Python
├── 📄 .env                        # Variáveis de ambiente (NÃO commitar)
├── 📄 .env.example               # Template de variáveis
├── 📄 .gitignore                 # Arquivos ignorados pelo Git
│
├── 🐍 Python Backend/
│   ├── app.py                    # Aplicação Flask principal
│   ├── config.py                 # Configurações da aplicação
│   ├── models.py                 # Modelos do banco de dados
│   ├── utils.py                  # Funções utilitárias
│   ├── agente_ia.py             # Classe do agente de IA
│   ├── setup.py                  # Script de configuração
│   ├── test_setup.py            # Testes de validação
│   └── testar_conexao.py        # Teste de conexão OpenAI
│
├── 🌐 Frontend/
│   ├── templates/                # Templates HTML
│   │   ├── index.html           # Página principal (chat)
│   │   └── dashboard.html       # Dashboard avançado
│   │
│   └── static/                   # Arquivos estáticos
│       ├── css/                  # Folhas de estilo
│       │   └── dashboard.css    # Estilos do dashboard
│       │
│       ├── js/                   # JavaScript
│       │   └── dashboard.js     # Lógica do dashboard
│       │
│       └── assets/               # Assets (imagens, ícones, etc)
│           └── (vazio por enquanto)
│
└── 🗄️ Database/
    └── contratos.db              # Banco SQLite (gerado automaticamente)
```

## 📋 Descrição dos Arquivos

### Documentação

| Arquivo | Descrição |
|---------|-----------|
| `README.md` | Documentação completa do projeto |
| `QUICKSTART.md` | Guia rápido para começar |
| `SECURITY.md` | Práticas de segurança |
| `DASHBOARD.md` | Documentação do dashboard |
| `PROJECT_STRUCTURE.md` | Estrutura de arquivos |

### Configuração

| Arquivo | Descrição |
|---------|-----------|
| `requirements.txt` | Dependências Python |
| `.env` | Variáveis de ambiente (secreto) |
| `.env.example` | Template de configuração |
| `.gitignore` | Arquivos ignorados |
| `config.py` | Configurações da app |

### Backend Python

| Arquivo | Descrição | Responsabilidade |
|---------|-----------|------------------|
| `app.py` | Aplicação Flask | Rotas, endpoints, servidor |
| `models.py` | Modelos de dados | Estrutura do banco de dados |
| `utils.py` | Utilitários | Funções auxiliares, mock data |
| `agente_ia.py` | Agente de IA | Integração com OpenAI |
| `setup.py` | Setup inicial | Configuração automatizada |
| `test_setup.py` | Testes | Validação da instalação |

### Frontend

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| `templates/index.html` | HTML | Página principal com chat |
| `templates/dashboard.html` | HTML | Dashboard avançado |
| `static/css/dashboard.css` | CSS | Estilos do dashboard |
| `static/js/dashboard.js` | JavaScript | Lógica do dashboard |

## 🎯 Separação de Responsabilidades

### Backend (Python)
- ✅ Lógica de negócio
- ✅ Integração com APIs externas
- ✅ Gerenciamento de banco de dados
- ✅ Autenticação e autorização
- ✅ Geração de dados mock

### Frontend (HTML/CSS/JS)
- ✅ Interface do usuário
- ✅ Visualização de dados
- ✅ Interatividade
- ✅ Gráficos e dashboards
- ✅ Responsividade

## 📦 Convenções de Nomenclatura

### Python
- **Arquivos**: `snake_case.py`
- **Classes**: `PascalCase`
- **Funções**: `snake_case()`
- **Constantes**: `UPPER_SNAKE_CASE`

### Frontend
- **Arquivos HTML**: `kebab-case.html`
- **Arquivos CSS**: `kebab-case.css`
- **Arquivos JS**: `kebab-case.js`
- **Classes CSS**: `kebab-case`
- **IDs**: `camelCase`
- **Funções JS**: `camelCase()`

## 🔄 Fluxo de Dados

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       │ HTTP Request
       ↓
┌─────────────┐
│  Flask App  │ ← app.py
└──────┬──────┘
       │
       ├─→ Templates (HTML)
       │   └─→ Static (CSS/JS)
       │
       ├─→ Models (Database)
       │
       ├─→ Utils (Data)
       │
       └─→ Agente IA (OpenAI)
```

## 🛠️ Melhores Práticas Implementadas

### Organização
- ✅ Separação clara entre backend e frontend
- ✅ Arquivos CSS e JS externos (não inline)
- ✅ Estrutura modular e escalável
- ✅ Documentação completa

### Código
- ✅ Comentários descritivos
- ✅ Funções pequenas e focadas
- ✅ Nomes descritivos
- ✅ Type hints em Python
- ✅ JSDoc em JavaScript

### Segurança
- ✅ Variáveis de ambiente
- ✅ .gitignore configurado
- ✅ Validação de entrada
- ✅ Sanitização de dados

### Performance
- ✅ Lazy loading
- ✅ Caching quando apropriado
- ✅ Minificação (produção)
- ✅ Otimização de assets

## 📝 Como Adicionar Novos Recursos

### Nova Página HTML
1. Criar arquivo em `templates/nova-pagina.html`
2. Criar CSS em `static/css/nova-pagina.css`
3. Criar JS em `static/js/nova-pagina.js`
4. Adicionar rota em `app.py`

### Novo Endpoint API
1. Adicionar função em `app.py`
2. Adicionar lógica de dados em `utils.py`
3. Documentar no README.md

### Novo Modelo de Dados
1. Adicionar classe em `models.py`
2. Criar migração (se necessário)
3. Atualizar `utils.py` com mock data

## 🔍 Localização Rápida

**Precisa modificar:**

- **Estilos do dashboard?** → `static/css/dashboard.css`
- **Lógica dos gráficos?** → `static/js/dashboard.js`
- **Layout do dashboard?** → `templates/dashboard.html`
- **Dados mock?** → `utils.py`
- **Rotas/endpoints?** → `app.py`
- **Configurações?** → `config.py`
- **Agente de IA?** → `agente_ia.py`

## 🚀 Próximos Passos de Organização

- [ ] Adicionar TypeScript para type safety
- [ ] Implementar build process (webpack/vite)
- [ ] Adicionar testes unitários
- [ ] Implementar CI/CD
- [ ] Adicionar linting (ESLint, Pylint)
- [ ] Adicionar formatação (Prettier, Black)
- [ ] Criar componentes reutilizáveis
- [ ] Implementar lazy loading de módulos

## 📚 Recursos Adicionais

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [Python Best Practices](https://docs.python-guide.org/)
- [JavaScript Best Practices](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)

---

**Última atualização**: 2024  
**Versão da estrutura**: 1.0.0