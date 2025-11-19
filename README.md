# 🚀 Sistema Completo de Gestão de Clientes e Contratos com IA

> ⚠️ **AVISO DE SEGURANÇA IMPORTANTE**  
> Se você expôs acidentalmente sua chave da OpenAI, **REVOGUE IMEDIATAMENTE** em:  
> https://platform.openai.com/api-keys e gere uma nova chave.  
> Consulte `SECURITY.md` para mais informações.

Sistema web completo para gerenciamento de clientes e contratos com assistente de IA integrado, dashboard avançado e chat interativo.

---

## 🎯 **NOVIDADE: Sistema de Gestão de Clientes e Contratos**

### 🏢 **Gestão de Clientes** 
- ✅ **CRUD Completo**: Cadastre, edite, visualize e exclua clientes
- ✅ **Campos Detalhados**: Nome, email, telefone, CNPJ/CPF, endereço completo, setor
- ✅ **Busca Inteligente**: Encontre clientes rapidamente por qualquer campo
- ✅ **Validação Automática**: Email único, CNPJ/CPF único, campos obrigatórios

### 📄 **Gestão de Contratos**
- ✅ **CRUD Completo**: Gerencie contratos do início ao fim
- ✅ **Relacionamento Cliente-Contrato**: Cada contrato vinculado a um cliente
- ✅ **Campos Avançados**: Número do contrato, descrição, valor, datas, método e frequência de pagamento
- ✅ **Status Inteligente**: Ativo, Suspenso, Concluído, Cancelado
- ✅ **Alertas Automáticos**: Contratos vencidos e próximos ao vencimento
- ✅ **Sistema de Renovação**: Data de renovação e contratos para renovar

### 📊 **Dashboard de Gestão**
- ✅ **Estatísticas em Tempo Real**: Total de clientes, contratos, valor total
- ✅ **Indicadores Chave**: Contratos ativos, vencidos, para renovação
- ✅ **Top Clientes**: Clientes com maior valor em contratos
- ✅ **Interface Moderna**: Design responsivo com Bootstrap 5

---

## 🚀 Início Rápido

**Quer começar rapidamente?** Leia o [QUICKSTART.md](QUICKSTART.md)

```bash
# 1. Configure o projeto
python setup.py

# 2. Adicione sua chave OpenAI no arquivo .env

# 3. Instale e execute
pip install -r requirements.txt
python app.py

# 4. Para o sistema de gestão (NOVO!)
python gestao_clientes.py
```

---

## 🚀 Funcionalidades Completas

### 🎯 **Sistema de Gestão (NOVO!)**
- ✅ **Gestão de Clientes**: Cadastro completo com validação de dados
- ✅ **Gestão de Contratos**: Ciclo de vida completo dos contratos
- ✅ **Dashboard Integrado**: Estatísticas e métricas em tempo real
- ✅ **API REST**: Endpoints completos para integração
- ✅ **Busca Avançada**: Filtros inteligentes e pesquisa rápida
- ✅ **Validação Robusta**: Prevenção de dados duplicados e inválidos

### Chat Inteligente
- ✅ Chat com assistente de IA (OpenAI GPT)
- ✅ Processamento de linguagem natural
- ✅ Contexto de conversação mantido
- ✅ Interface amigável e responsiva

### Dashboard Avançado 📊
- ✅ **Métricas em Tempo Real**: Total de contratos, valor total, taxa de renovação, inadimplência
- ✅ **Gráficos Interativos**: 
  - Distribuição por status (rosca)
  - Top 5 clientes (barras)
  - Valor por setor (pizza)
  - Valor por região (barras)
  - Timeline de vencimentos (linha dupla)
- ✅ **Indicadores de Mercado**: Taxa Selic, IPCA, IGPM, CDI, Dólar, Ibovespa
- ✅ **Comparação por Setor**: Análise detalhada de performance
- ✅ **Atualização Automática**: Dados atualizados a cada 30 segundos
- ✅ **Design Moderno**: Tema escuro, animações suaves, totalmente responsivo

### Funcionalidades de IA 🤖 **NOVO!**
- ✅ **Alertas Inteligentes**: Monitoramento contínuo com alertas automáticos
- ✅ **Score de Risco**: Pontuação 0-100 do portfólio com análise de fatores
- ✅ **Análise de Métricas**: IA analisa dados e gera insights acionáveis
- ✅ **Previsões**: Tendências futuras baseadas em dados históricos
- ✅ **Detecção de Anomalias**: Identifica padrões incomuns automaticamente
- ✅ **Análise de Gráficos**: Botão "Analisar com IA" em cada gráfico
- ✅ **Perguntas em Linguagem Natural**: Faça perguntas sobre seus dados

### Outros Recursos
- ✅ Gerenciamento de vencimentos
- ✅ Banco de dados SQLite com migração automática
- ✅ Sistema de autenticação (em desenvolvimento)
- ✅ API REST completa
- ✅ Sistema de notificações
- ✅ Backup automático do banco de dados

---

## 🛠️ **Arquivos Principais**

### Sistema de Gestão
```bash
gestao_clientes.py          # Servidor Flask do sistema de gestão
models_atualizado.py        # Modelos de dados atualizados
templates/gestao.html       # Interface web de gestão
migrar_banco.py            # Script de migração de dados
testar_gestao.py           # Script de testes da API
```

### Sistema Original
```bash
app.py                     # Aplicação Flask principal
agente_ia.py              # Agente de IA
models.py                 # Modelos de dados originais
templates/index.html      # Interface original
```

---

## 📋 **Como Usar o Sistema de Gestão**

### 1. Migração de Dados (se necessário)
```bash
python migrar_banco.py
```

### 2. Iniciar o Servidor
```bash
python gestao_clientes.py
```

### 3. Acessar a Interface
- **Web Interface**: http://localhost:5000
- **API Endpoints**: http://localhost:5000/api/

### 4. Testar a API
```bash
python testar_gestao.py
```

---

## 📚 **Documentação da API**

### Clientes
- `GET /api/clients` - Listar todos os clientes
- `POST /api/clients` - Criar novo cliente
- `GET /api/clients/<id>` - Buscar cliente específico
- `PUT /api/clients/<id>` - Atualizar cliente
- `DELETE /api/clients/<id>` - Excluir cliente
- `GET /api/clients/search?q=<termo>` - Buscar clientes

### Contratos
- `GET /api/contracts` - Listar todos os contratos
- `POST /api/contracts` - Criar novo contrato
- `GET /api/contracts/<id>` - Buscar contrato específico
- `PUT /api/contracts/<id>` - Atualizar contrato
- `DELETE /api/contracts/<id>` - Excluir contrato
- `GET /api/contracts/search?q=<termo>` - Buscar contratos
- `GET /api/contracts/overdue` - Contratos vencidos
- `GET /api/contracts/renewal-due` - Contratos para renovação

### Dashboard
- `GET /api/dashboard/stats` - Estatísticas do sistema

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta na OpenAI (para obter uma chave de API)
- Node.js (opcional, para desenvolvimento frontend)

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd projetoia
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edite o arquivo `.env` e adicione suas credenciais:

```env
# Obtenha sua chave em: https://platform.openai.com/api-keys
OPENAI_API_KEY=sua_chave_aqui

# Gere uma chave segura com: python -c "import secrets; print(secrets.token_hex(32))"
FLASK_SECRET_KEY=sua_chave_secreta_aqui

# Configuração do banco de dados
DATABASE_URL=sqlite:///contratos.db
```

### 5. Inicialize o banco de dados

```bash
python app.py
```

O banco de dados será criado automaticamente na primeira execução.

## 🎯 Como usar

### Executar o servidor

```bash
python app.py
```

O servidor estará disponível em: `http://localhost:5000`

### Testar a conexão com OpenAI

```bash
python testar_conexao.py
```

### Usar o agente em modo CLI

```bash
python agente_ia.py
```

## 📁 Estrutura do Projeto

```
projetoia/
├── app.py                 # Aplicação Flask principal
├── agente_ia.py          # Classe do agente de IA
├── models.py             # Modelos do banco de dados
├── utils.py              # Funções utilitárias
├── testar_conexao.py     # Script de teste da API
├── requirements.txt      # Dependências do projeto
├── .env                  # Variáveis de ambiente (não commitar!)
├── .env.example          # Exemplo de variáveis de ambiente
├── .gitignore           # Arquivos ignorados pelo Git
└── templates/
    └── index.html        # Interface web

```

## 🔒 Segurança

⚠️ **IMPORTANTE:**

1. **NUNCA** faça commit do arquivo `.env` no Git
2. Revogue chaves de API antigas se foram expostas
3. Use chaves secretas fortes para o Flask
4. Mantenha as dependências atualizadas

### Gerar chave secreta segura

```python
import secrets
print(secrets.token_hex(32))
```

## 🛠️ Desenvolvimento

### Adicionar novos exemplos de treinamento

```python
from agente_ia import AgenteIA

agente = AgenteIA(nome="Dominó")
agente.adicionar_exemplo_treinamento(
    pergunta="Quantos contratos vencem este mês?",
    resposta="Deixe-me verificar os contratos para você..."
)
```

### Personalizar o modelo de IA

Edite o arquivo `.env`:

```env
OPENAI_MODEL=gpt-4  # ou gpt-3.5-turbo
```

## 📊 API Endpoints

### GET `/`
Página principal com chat e resumo de contratos

### GET `/dashboard`
Dashboard avançado com visualizações e análises

### GET `/api/contratos`
Retorna lista de contratos em JSON

**Response:**
```json
{
  "resumo": {...},
  "contratos": [...]
}
```

### GET `/api/dashboard`
Retorna todos os dados do dashboard avançado

**Response:**
```json
{
  "metricas": {...},
  "distribuicao_status": [...],
  "top_clientes": [...],
  "valor_por_setor": [...],
  "valor_por_regiao": [...],
  "timeline_vencimentos": [...],
  "mapa_calor": [...],
  "indicadores_mercado": {...},
  "comparacao_setores": [...]
}
```

### POST `/chat`
Envia mensagem para o assistente de IA

**Body:**
```json
{
  "mensagem": "Olá, como você pode me ajudar?"
}
```

**Response:**
```json
{
  "resposta": "Olá! Posso ajudar com..."
}
```

📖 **Documentação completa do Dashboard**: Veja [DASHBOARD.md](DASHBOARD.md)  
## 🤖 **Documentação das Funcionalidades de IA**: Veja [AI_FEATURES.md](AI_FEATURES.md)

## 🐛 Troubleshooting

### Erro: "Banco de dados não encontrado"
- Execute: `python gestao_clientes.py` (cria automaticamente)
- Ou: `python migrar_banco.py` (para migração)

### Erro: "Chave da API da OpenAI não encontrada"
- Verifique se o arquivo `.env` existe
- Confirme que `OPENAI_API_KEY` está definida
- Certifique-se de que a chave é válida

### Erro: "ModuleNotFoundError"
- Execute: `pip install -r requirements.txt`
- Ative o ambiente virtual

### Erro de conexão com OpenAI
- Verifique sua conexão com a internet
- Confirme se você tem créditos na conta OpenAI
- Teste com: `python testar_conexao.py`

### Erro: "Servidor não responde"
- Verifique se a porta 5000 está livre
- Reinicie o servidor: `python gestao_clientes.py`
- Teste a API: `python testar_gestao.py`

## 📝 TODO - Próximas Melhorias

### 🎯 Sistema de Gestão
- [ ] Sistema de autenticação e multi-usuários
- [ ] Relatórios em PDF/Excel
- [ ] Sistema de faturas e pagamentos
- [ ] Calendário de vencimentos
- [ ] Notificações por e-mail
- [ ] Upload de documentos
- [ ] Histórico de alterações

### 🤖 Funcionalidades de IA
- [ ] Análise preditiva de renovação
- [ ] Score de crédito automático
- [ ] Insights personalizados por cliente
- [ ] Chatbots para atendimento

### 🛠️ Técnico
- [ ] Deploy em produção (Docker)
- [ ] Testes unitários automatizados
- [ ] Sistema de logs avançado
- [ ] Backup automático em nuvem
- [ ] API rate limiting
- [ ] WebSockets para tempo real

## 📄 Licença

Este projeto está licenciado sob a licença MIT.

## 👥 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.