# Guia de Segurança

## 🔒 Práticas de Segurança Importantes

### 1. Proteção de Chaves de API

#### ⚠️ NUNCA faça isso:
- ❌ Commitar o arquivo `.env` no Git
- ❌ Compartilhar chaves de API em mensagens, emails ou chat
- ❌ Usar chaves de API em código hardcoded
- ❌ Expor chaves em logs ou mensagens de erro

#### ✅ SEMPRE faça isso:
- ✅ Usar variáveis de ambiente (arquivo `.env`)
- ✅ Adicionar `.env` ao `.gitignore`
- ✅ Usar `.env.example` como template (sem valores reais)
- ✅ Revogar chaves expostas imediatamente

### 2. Revogando Chaves Expostas

Se você acidentalmente expôs sua chave da OpenAI:

1. **Acesse:** https://platform.openai.com/api-keys
2. **Encontre** a chave exposta
3. **Clique** em "Revoke" ou "Delete"
4. **Gere** uma nova chave
5. **Atualize** o arquivo `.env` com a nova chave

### 3. Gerando Chaves Seguras

#### Para Flask Secret Key:

```python
import secrets
print(secrets.token_hex(32))
```

Ou use o script de configuração:

```bash
python setup.py
```

### 4. Configuração do Arquivo .env

**Estrutura correta:**

```env
# Chaves de API
OPENAI_API_KEY=sk-proj-...  # Sua chave real aqui

# Flask
FLASK_SECRET_KEY=<chave-gerada-com-secrets>

# Database
DATABASE_URL=sqlite:///contratos.db
```

### 5. Checklist de Segurança

Antes de fazer commit:

- [ ] Arquivo `.env` está no `.gitignore`?
- [ ] Não há chaves hardcoded no código?
- [ ] `.env.example` não contém valores reais?
- [ ] Chaves antigas foram revogadas?
- [ ] Dependências estão atualizadas?

### 6. Atualizando Dependências

Mantenha as dependências atualizadas para corrigir vulnerabilidades:

```bash
pip install --upgrade -r requirements.txt
```

### 7. Variáveis de Ambiente em Produção

Em produção, configure as variáveis de ambiente diretamente no servidor/plataforma:

**Heroku:**
```bash
heroku config:set OPENAI_API_KEY=sua_chave
```

**Railway:**
Use o painel de configuração de variáveis

**Render:**
Use o painel de Environment Variables

### 8. Rate Limiting

Considere implementar rate limiting para proteger contra abuso:

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)
```

### 9. HTTPS em Produção

**SEMPRE** use HTTPS em produção para proteger dados em trânsito.

### 10. Reportando Vulnerabilidades

Se encontrar uma vulnerabilidade de segurança:

1. **NÃO** abra uma issue pública
2. Entre em contato diretamente com os mantenedores
3. Forneça detalhes sobre a vulnerabilidade
4. Aguarde resposta antes de divulgar publicamente

## 📚 Recursos Adicionais

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security](https://flask.palletsprojects.com/en/2.3.x/security/)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)

## 🆘 Em Caso de Incidente

Se você suspeitar que suas credenciais foram comprometidas:

1. **Revogue** todas as chaves imediatamente
2. **Gere** novas chaves
3. **Revise** logs de acesso
4. **Atualize** todas as instâncias da aplicação
5. **Monitore** atividade suspeita