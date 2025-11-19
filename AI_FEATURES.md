# 🤖 Funcionalidades de IA - Documentação

## Visão Geral

O sistema agora possui integração completa com Inteligência Artificial para análise preditiva, geração de insights e alertas inteligentes sobre os dados de contratos.

## 🎯 Funcionalidades Implementadas

### 1. Alertas Inteligentes 🚨

**Descrição**: Sistema de monitoramento contínuo que detecta automaticamente situações que requerem atenção.

**Tipos de Alertas**:
- **Inadimplência Alta**: Quando taxa > 5%
- **Taxa de Renovação Baixa**: Quando < 75%
- **Crescimento Negativo**: Quando há queda mensal
- **Concentração de Vencimentos**: Muitos contratos vencendo no mesmo período

**Características**:
- ✅ Severidade classificada (Alta/Média/Baixa)
- ✅ Ações sugeridas específicas
- ✅ Ícones visuais para identificação rápida
- ✅ Atualização automática

**Exemplo de Alerta**:
```json
{
  "tipo": "inadimplencia",
  "severidade": "Alta",
  "titulo": "Inadimplência Acima do Ideal",
  "mensagem": "Taxa de inadimplência em 7.5%...",
  "acao_sugerida": "Revisar processos de cobrança",
  "icone": "⚠️"
}
```

### 2. Score de Risco 📊

**Descrição**: Pontuação de 0-100 que avalia o risco geral do portfólio de contratos.

**Fatores Analisados**:
1. **Inadimplência** (peso 40%)
2. **Taxa de Renovação** (peso 35%)
3. **Crescimento** (peso 25%)

**Classificações**:
- **0-30**: Risco Baixo (verde)
- **30-60**: Risco Médio (amarelo)
- **60-100**: Risco Alto (vermelho)

**Visualização**:
- Score numérico grande
- Barras de progresso por fator
- Recomendação personalizada
- Cores dinâmicas

### 3. Análise Inteligente de Métricas 🧠

**Descrição**: IA analisa as métricas principais e gera insights acionáveis.

**Fornece**:
- Análise geral da saúde do portfólio
- Pontos de atenção específicos
- Recomendações práticas
- Nível de risco calculado

**Exemplo de Análise**:
```
Análise Geral:
"O portfólio apresenta saúde financeira sólida com 120 contratos ativos 
e valor total de R$ 1.5M. A taxa de renovação de 85% está acima da média 
do mercado."

Pontos de Atenção:
- Inadimplência em 6.2% requer monitoramento
- Crescimento desacelerou nos últimos 2 meses

Recomendações:
- Implementar programa de fidelização
- Revisar política de crédito
- Diversificar base de clientes
```

### 4. Previsões e Tendências 🔮

**Descrição**: Análise preditiva baseada em dados históricos.

**Previsões Geradas**:
- Valor esperado próximo mês
- Quantidade de vencimentos
- Tendência (crescente/decrescente/estável)
- Nível de confiança

**Algoritmo**:
- Análise de séries temporais
- Média móvel
- Detecção de padrões sazonais

**Exemplo**:
```json
{
  "tendencia_valor": "crescente",
  "tendencia_quantidade": "estável",
  "previsao_proximo_mes": {
    "valor": 125000.50,
    "quantidade": 18
  },
  "confianca": "Média",
  "observacao": "Baseado nos últimos 6 períodos"
}
```

### 5. Detecção de Anomalias 🔍

**Descrição**: Identifica padrões incomuns nos dados automaticamente.

**Detecta**:
- Desvios significativos da média (>30%)
- Picos ou quedas abruptas
- Padrões atípicos

**Severidade**:
- **Alta**: Desvio > 50%
- **Média**: Desvio 30-50%

**Exemplo de Anomalia**:
```json
{
  "tipo": "desvio_valor",
  "periodo": "Jan/24",
  "valor": 180000,
  "media": 120000,
  "desvio_percentual": 50,
  "severidade": "Alta",
  "descricao": "Valor 50% acima da média"
}
```

### 6. Análise de Gráficos com IA 📈

**Descrição**: Botão "Analisar com IA" em cada gráfico para insights específicos.

**Funcionalidade**:
- Clique no botão "🤖 Analisar com IA"
- IA analisa os dados do gráfico
- Gera insights em linguagem natural
- Mostra em modal

**Insights Fornecidos**:
- Principal padrão observado
- Tendências identificadas
- Recomendações práticas

### 7. Perguntas em Linguagem Natural 💬

**Descrição**: Interface para fazer perguntas sobre os dados em português.

**Como Usar**:
1. Digite sua pergunta na caixa de texto
2. Pressione Enter ou clique em "Perguntar"
3. IA processa e responde baseada nos dados reais

**Exemplos de Perguntas**:
- "Qual setor tem maior inadimplência?"
- "Quantos contratos vencem este mês?"
- "Qual a tendência de crescimento?"
- "Quais regiões têm melhor performance?"

**Características**:
- Respostas baseadas em dados reais
- Contexto completo do dashboard
- Histórico de perguntas e respostas
- Processamento em tempo real

## 🔧 Arquitetura Técnica

### Backend (Python)

**Arquivo**: `ai_analytics.py`

**Classe Principal**: `AIAnalytics`

**Métodos**:
```python
- analisar_metricas(metricas) -> Dict
- detectar_anomalias(dados_historicos) -> List
- gerar_alertas(dados_completos) -> List
- calcular_score_risco(dados_completos) -> Dict
- prever_tendencias(timeline) -> Dict
- analisar_grafico(tipo, dados) -> str
- responder_pergunta_dados(pergunta, contexto) -> str
```

### Frontend (JavaScript)

**Arquivo**: `static/js/dashboard.js`

**Funções Principais**:
```javascript
- criarSecaoAlertas(alertas)
- criarScoreRisco(scoreData)
- criarInsightsIA(analise)
- criarPrevisoes(tendencias)
- analisarGrafico(tipo, dados)
- perguntarDados()
```

### API Endpoints

#### GET `/api/dashboard`
Retorna dados completos incluindo análises de IA

**Response**:
```json
{
  "metricas": {...},
  "distribuicao_status": [...],
  "ai_insights": {
    "analise_metricas": {...},
    "alertas": [...],
    "score_risco": {...},
    "tendencias": {...},
    "anomalias": [...]
  }
}
```

#### POST `/api/analisar-grafico`
Analisa um gráfico específico

**Request**:
```json
{
  "tipo": "Distribuição por Status",
  "dados": [...]
}
```

**Response**:
```json
{
  "analise": "O gráfico mostra predominância de contratos ativos..."
}
```

#### POST `/api/perguntar-dados`
Responde perguntas sobre os dados

**Request**:
```json
{
  "pergunta": "Qual setor tem maior inadimplência?"
}
```

**Response**:
```json
{
  "resposta": "Com base nos dados, o setor de Comércio..."
}
```

## 📊 Fluxo de Dados

```
┌─────────────┐
│  Dashboard  │
└──────┬──────┘
       │
       │ GET /api/dashboard
       ↓
┌─────────────┐
│  Flask App  │
└──────┬──────┘
       │
       ├─→ Gera dados mock (utils.py)
       │
       ├─→ AIAnalytics.analisar_metricas()
       ├─→ AIAnalytics.gerar_alertas()
       ├─→ AIAnalytics.calcular_score_risco()
       ├─→ AIAnalytics.prever_tendencias()
       ├─→ AIAnalytics.detectar_anomalias()
       │
       ↓
┌─────────────┐
│  OpenAI API │
└──────┬──────┘
       │
       │ Análise de IA
       ↓
┌─────────────┐
│  Response   │
└─────────────┘
```

## 🎨 Interface do Usuário

### Seções Adicionadas

1. **Alertas Inteligentes** (topo do dashboard)
   - Cards coloridos por severidade
   - Ícones visuais
   - Ações sugeridas

2. **Score de Risco** (grid 2 colunas)
   - Score grande e destacado
   - Barras de progresso por fator
   - Recomendação

3. **Insights de IA** (grid 2 colunas)
   - Análise geral
   - Pontos de atenção
   - Recomendações

4. **Previsões** (seção dedicada)
   - Cards de previsão
   - Indicadores de tendência
   - Nota de confiança

5. **Interface de Perguntas** (seção interativa)
   - Input de texto
   - Histórico de Q&A
   - Respostas em tempo real

## 🚀 Como Usar

### 1. Visualizar Alertas
- Alertas aparecem automaticamente no topo
- Verifique severidade e ações sugeridas
- Atualize para ver novos alertas

### 2. Consultar Score de Risco
- Veja o score geral (0-100)
- Analise fatores individuais
- Leia a recomendação

### 3. Ler Insights
- Seção "Análise Inteligente"
- Pontos de atenção destacados
- Recomendações acionáveis

### 4. Ver Previsões
- Seção "Previsões e Tendências"
- Valores previstos para próximo mês
- Tendências identificadas

### 5. Analisar Gráficos
- Clique em "🤖 Analisar com IA"
- Leia análise no modal
- Feche clicando no X

### 6. Fazer Perguntas
- Digite pergunta em português
- Pressione Enter ou clique "Perguntar"
- Veja resposta baseada em dados reais

## ⚙️ Configuração

### Variáveis de Ambiente

```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-3.5-turbo  # ou gpt-4
```

### Dependências

```bash
pip install openai>=1.0.0
```

## 🎯 Casos de Uso

### Gestor Financeiro
- Monitora alertas de inadimplência
- Acompanha score de risco
- Toma decisões baseadas em previsões

### Analista de Contratos
- Analisa gráficos com IA
- Faz perguntas sobre dados
- Identifica anomalias

### Diretor Comercial
- Visualiza insights estratégicos
- Acompanha tendências
- Planeja ações corretivas

## 📈 Benefícios

1. **Proatividade**: Alertas antes de problemas se agravarem
2. **Precisão**: Análises baseadas em IA
3. **Eficiência**: Insights automáticos
4. **Acessibilidade**: Perguntas em linguagem natural
5. **Previsibilidade**: Tendências futuras

## 🔒 Segurança

- Dados nunca saem do contexto da aplicação
- API key protegida em variáveis de ambiente
- Análises processadas em tempo real
- Sem armazenamento de histórico sensível

## 🐛 Troubleshooting

### Alertas não aparecem
- Verifique se há dados suficientes
- Confirme thresholds de alerta

### Score de risco não calcula
- Verifique métricas disponíveis
- Confirme fórmulas de cálculo

### IA não responde perguntas
- Verifique OPENAI_API_KEY
- Confirme créditos disponíveis
- Veja logs do servidor

### Previsões imprecisas
- Necessário mais dados históricos (mínimo 3 períodos)
- Tendências baseadas em média simples

## 🔮 Melhorias Futuras

- [ ] Machine Learning para previsões mais precisas
- [ ] Análise de sentimento em feedbacks
- [ ] Recomendações personalizadas por usuário
- [ ] Exportação de relatórios de IA
- [ ] Integração com mais fontes de dados
- [ ] Alertas via email/SMS
- [ ] Dashboard personalizado por IA
- [ ] Análise comparativa com mercado

---

**Versão**: 1.0.0  
**Última atualização**: 2024  
**Desenvolvido com** 🤖 **IA para análise inteligente de contratos**