# 🚀 Guia Rápido de Início

## ⚡ Configuração em 3 Passos

### 1. Configure o Projeto

```bash
python setup.py
```

Este comando irá:
- ✅ Criar o arquivo `.env`
- ✅ Gerar uma chave secreta segura
- ✅ Configurar valores padrão

### 2. Adicione sua Chave da OpenAI

Edite o arquivo `.env` e adicione sua chave:

```env
OPENAI_API_KEY=sk-proj-sua_chave_aqui
```

**Onde conseguir a chave:**
1. Acesse: https://platform.openai.com/api-keys
2. Clique em "Create new secret key"
3. Copie a chave gerada
4. Cole no arquivo `.env`

### 3. Instale e Execute

```bash
# Instalar dependências
pip install -r requirements.txt

# Testar configuração
python test_setup.py

# Executar o servidor
python app.py
```

Acesse: **http://localhost:5000**

---

## 📝 Comandos Úteis

### Testar Conexão com OpenAI
```bash
python testar_conexao.py
```

### Usar o Agente em Modo CLI
```bash
python agente_ia.py
```

### Executar Testes de Configuração
```bash
python test_setup.py
```

---

## 🎯 Funcionalidades Principais

### 1. Dashboard de Contratos
- Visualize contratos próximos do vencimento
- Acompanhe estatísticas mensais
- Interface responsiva

### 2. Chat com IA
- Converse com o assistente Dominó
- Perguntas sobre contratos
- Respostas contextualizadas

### 3. API REST
- Endpoint `/api/contratos` - Lista de contratos
- Endpoint `/chat` - Enviar mensagens

---

## 🔧 Configurações Avançadas

### Alterar Modelo da IA

Edite o arquivo `.env`:

```env
OPENAI_MODEL=gpt-4  # ou gpt-3.5-turbo (padrão)
```

### Alterar Porta do Servidor

```env
PORT=8000  # padrão: 5000
```

### Modo de Desenvolvimento/Produção

```env
DEBUG=False  # True para desenvolvimento
```

---

## 🐛 Problemas Comuns

### Erro: "Chave da API não encontrada"

**Solução:**
1. Verifique se o arquivo `.env` existe
2. Confirme que `OPENAI_API_KEY` está definida
3. Execute: `python test_setup.py`

### Erro: "ModuleNotFoundError"

**Solução:**
```bash
pip install -r requirements.txt
```

### Erro de Conexão com OpenAI

**Solução:**
1. Verifique sua internet
2. Confirme se tem créditos na OpenAI
3. Teste com: `python testar_conexao.py`

---

## 📚 Próximos Passos

1. ✅ Explore o dashboard em http://localhost:5000
2. ✅ Teste o chat com a IA
3. ✅ Personalize o agente em `agente_ia.py`
4. ✅ Adicione seus próprios contratos no banco de dados
5. ✅ Leia a documentação completa no `README.md`

---

## 🆘 Precisa de Ajuda?

- 📖 Leia o `README.md` completo
- 🔒 Consulte `SECURITY.md` para segurança
- 🧪 Execute `python test_setup.py` para diagnóstico
- 🐛 Abra uma issue no repositório

---

## ✨ Dica Pro

Para uma experiência completa:

1. Configure webhooks para notificações
2. Integre com seu sistema de contratos
3. Personalize as respostas do agente
4. Adicione autenticação de usuários

**Divirta-se! 🎉**