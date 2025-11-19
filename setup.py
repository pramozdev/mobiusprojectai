"""
Script de configuração inicial do projeto
"""
import os
import secrets
import sys


def gerar_chave_secreta():
    """Gera uma chave secreta segura"""
    return secrets.token_hex(32)


def verificar_arquivo_env():
    """Verifica se o arquivo .env existe"""
    return os.path.exists('.env')


def criar_arquivo_env():
    """Cria o arquivo .env com valores padrão"""
    chave_secreta = gerar_chave_secreta()
    
    conteudo = f"""# Chave de API da OpenAI
# ATENÇÃO: Esta chave deve ser mantida em segredo
# Obtenha sua chave em: https://platform.openai.com/api-keys
OPENAI_API_KEY=sua_chave_aqui

# Flask Configuration
# Chave gerada automaticamente - NÃO compartilhe!
FLASK_SECRET_KEY={chave_secreta}

# Database Configuration
DATABASE_URL=sqlite:///contratos.db

# OpenAI Model (opcional)
OPENAI_MODEL=gpt-3.5-turbo

# Server Configuration
PORT=5000
DEBUG=True
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print("✅ Arquivo .env criado com sucesso!")
    print(f"✅ Chave secreta gerada: {chave_secreta[:20]}...")
    print("\n⚠️  IMPORTANTE: Adicione sua chave da OpenAI no arquivo .env")


def main():
    print("=" * 60)
    print("🚀 Configuração Inicial do Projeto - Agente de IA")
    print("=" * 60)
    print()
    
    # Verifica se .env existe
    if verificar_arquivo_env():
        resposta = input("⚠️  Arquivo .env já existe. Deseja sobrescrever? (s/N): ")
        if resposta.lower() != 's':
            print("❌ Configuração cancelada.")
            return
    
    # Cria arquivo .env
    criar_arquivo_env()
    
    print("\n" + "=" * 60)
    print("📝 Próximos passos:")
    print("=" * 60)
    print("1. Edite o arquivo .env e adicione sua chave da OpenAI")
    print("2. Instale as dependências: pip install -r requirements.txt")
    print("3. Execute o servidor: python app.py")
    print("4. Acesse: http://localhost:5000")
    print("\n✨ Pronto para começar!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Configuração cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro durante a configuração: {str(e)}")
        sys.exit(1)