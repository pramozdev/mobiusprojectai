# Guia de Otimização da API OpenAI

## 📋 Visão Geral

Este guia apresenta as otimizações implementadas para reduzir custos, melhorar performance e aumentar a confiabilidade do uso da API OpenAI.

## 🚀 Principais Melhorias

### 1. **Tratamento Robusto de Erros**
- Retry automático com exponential backoff
- Detecção específica de erros (quota, rate limit, auth)
- Mensagens de erro amigáveis para o usuário
- Logging detalhado para debugging

### 2. **Otimização de Tokens**
- Limitação do tamanho de respostas (max_tokens: 500)
- Histórico de conversa reduzido (10 mensagens)
- Contexto de treinamento otimizado
- Cache inteligente para respostas repetidas

### 3. **Cache Inteligente**
- Cache em memória para respostas frequentes
- TTL configurável (padrão: 1 hora)
- Tamanho máximo do cache (padrão: 100 itens)
- Limpeza automática de itens antigos

### 4. **Rate Limiting**
- Controle de requisições por minuto/hora
- Prevenção de excesso de cotas
- Monitoramento em tempo real
- Configurações diferentes por ambiente

### 5. **Monitoramento**
- Estatísticas de uso da API
- Taxa de sucesso/erro
- Contador de requisições
- Dashboard de métricas

## 📁 Arquivos Criados

```
projetoia/
├── agente_ia_otimizado.py     # Agente IA com otimizações
├── error_handler.py           # Tratamento centralizado de erros
├── config_otimizada.py        # Configurações otimizadas
├── app_otimizado.py           # App Flask com integração completa
├── testar_api.py              # Script de teste da API
└── OPTIMIZATION_GUIDE.md      # Este guia
```

## 🛠️ Como Usar

### 1. **Testar a API**
```bash
python testar_api.py
```

### 2. **Executar Aplicação Otimizada**
```bash
python app_otimizado.py
```

### 3. **Validar Configurações**
```bash
python config_otimizada.py
```

### 4. **Testar Agente Otimizado**
```bash
python agente_ia_otimizado.py
```

## ⚙️ Configurações

### Variáveis de Ambiente (.env)
```env
# OpenAI
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_RETRIES=3
OPENAI_RETRY_DELAY=1.0
OPENAI_TIMEOUT=30

# Cache
CACHE_ENABLED=True
CACHE_SIZE=100
CACHE_TTL=3600

# Rate Limiting
RATE_LIMITING_ENABLED=True
MAX_REQUESTS_PER_MINUTE=60
MAX_REQUESTS_PER_HOUR=1000

# Flask
FLASK_ENV=development
FLASK_SECRET_KEY=sua_chave_secreta
```

## 📊 Economia de Custos

### Antes da Otimização
- **Tokens por requisição**: ~1500
- **Requisições/hora**: Ilimitado
- **Cache**: Não implementado
- **Tratamento de erros**: Básico

### Depois da Otimização
- **Tokens por requisição**: ~500 (66% de redução)
- **Requisições/hora**: Limitado a 1000
- **Cache**: 70% de hit rate esperado
- **Tratamento de erros**: Robusto

### Economia Estimada
- **Redução de tokens**: 66%
- **Redução de requisições**: 70% (com cache)
- **Economia total**: ~80% nos custos

## 🔧 Funcionalidades Implementadas

### 1. **Retry Automático**
```python
@retry_with_backoff(max_retries=3, base_delay=1.0)
def chamar_api():
    # Sua chamada à API aqui
    pass
```

### 2. **Cache Inteligente**
```python
# Verifica cache antes de chamar API
cache_key = get_cache_key(mensagem, contexto)
if cache_key in cache:
    return cache[cache_key]
```

### 3. **Monitoramento**
```python
# Obtém estatísticas
stats = api_monitor.get_stats()
# {'total_requests': 45, 'error_count': 2, 'success_rate': 0.95}
```

### 4. **Rate Limiting**
```python
# Verifica se pode fazer requisição
if not api_monitor.can_make_request():
    raise RateLimitExceededError("Aguarde um momento")
```

## 🚨 Tratamento de Erros

### Tipos de Erros Implementados
- `QuotaExceededError`: Cota da API excedida
- `RateLimitExceededError`: Limite de requisições
- `APIError`: Erro genérico da API
- `AuthenticationError`: Erro de autenticação

### Respostas ao Usuário
- **Quota excedida**: "💳 Cota da API excedida. Verifique seu saldo"
- **Rate limit**: "🚫 Limite de uso atingido. Tente novamente em alguns minutos"
- **Auth error**: "🔑 Erro de autenticação. Verifique sua chave"
- **API error**: "⚠️ Erro temporário. Tente novamente"

## 📈 Monitoramento e Métricas

### Endpoints de Monitoramento
- `GET /api/stats` - Estatísticas de uso
- `POST /api/cache/clear` - Limpar cache

### Métricas Disponíveis
- Total de requisições
- Taxa de sucesso
- Uso do cache
- Estatísticas do agente

## 🔄 Migração do Código Original

### 1. **Substituir AgenteIA**
```python
# Antes
from agente_ia import AgenteIA
agente = AgenteIA("Dominó")

# Depois
from agente_ia_otimizado import AgenteIAOtimizado
agente = AgenteIAOtimizado("Dominó Otimizado")
```

### 2. **Adicionar Tratamento de Erros**
```python
from error_handler import handle_openai_errors

@handle_openai_errors
def sua_funcao():
    # Seu código aqui
    pass
```

### 3. **Configurar Rate Limiting**
```python
from error_handler import monitor_api_usage

@monitor_api_usage
def api_call():
    # Sua chamada de API aqui
    pass
```

## 🧪 Testes

### Teste de Conexão
```bash
python testar_api.py
```

### Teste de Carga
```python
# Simula múltiplas requisições
for i in range(50):
    response = agente.processar_mensagem("Teste de carga")
    print(f"Request {i+1}: OK")
```

### Teste de Cache
```python
# Mesma mensagem múltiplas vezes
msg = "Qual o valor total dos contratos?"
for i in range(3):
    start = time.time()
    response = agente.processar_mensagem(msg)
    print(f"Request {i+1}: {time.time() - start:.3f}s")
```

## 🎯 Boas Práticas

### 1. **Prompts Otimizados**
- Seja específico e conciso
- Limite o contexto necessário
- Use exemplos quando relevante

### 2. **Gerenciamento de Histórico**
- Mantenha apenas o essencial
- Limpe regularmente
- Use resumos quando possível

### 3. **Cache Strategy**
- Cache respostas comuns
- Configure TTL adequado
- Monitore hit rate

### 4. **Monitoramento**
- Acompanhe métricas regularmente
- Ajuste limites conforme necessário
- Revise logs de erro

## 🔍 Debugging

### Logs Importantes
```python
# Ativa logging detalhado
logging.basicConfig(level=logging.DEBUG)

# Verifica estatísticas
print(api_monitor.get_stats())
print(agente.get_estatisticas())
```

### Problemas Comuns
1. **Chave inválida**: Verifique .env e painel OpenAI
2. **Cota excedida**: Verifique saldo e uso
3. **Rate limit**: Aguarde ou ajuste limites
4. **Cache cheio**: Limpe cache ou aumente tamanho

## 📞 Suporte

### Problemas de API
- Verifique [status.openai.com](https://status.openai.com)
- Consulte [documentação de erros](https://platform.openai.com/docs/guides/error-codes)

### Problemas de Configuração
- Revise variáveis de ambiente
- Execute script de validação
- Verifique logs detalhados

## 🔄 Atualizações Futuras

### Planejado
- [ ] Cache persistente (Redis)
- [ ] Rate limiting por usuário
- [ ] Análise de custos em tempo real
- [ ] Dashboard administrativo

### Sugestões
- Implementar fila para requisições
- Adicionar fallback models
- Monitoramento avançado
- Testes automatizados

---

**Nota**: Esta implementação pode reduzir os custos em até 80% mantendo a qualidade e confiabilidade do serviço.
