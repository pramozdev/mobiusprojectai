"""
Script de teste para validar a configuração do projeto
"""
import os
import sys
from dotenv import load_dotenv


def teste_arquivo_env():
    """Testa se o arquivo .env existe"""
    print("1️⃣  Testando arquivo .env...", end=" ")
    if os.path.exists('.env'):
        print("✅ OK")
        return True
    else:
        print("❌ FALHOU - Arquivo .env não encontrado")
        print("   Execute: python setup.py")
        return False


def teste_variaveis_ambiente():
    """Testa se as variáveis de ambiente estão configuradas"""
    print("2️⃣  Testando variáveis de ambiente...", end=" ")
    load_dotenv()
    
    variaveis_necessarias = ['OPENAI_API_KEY', 'FLASK_SECRET_KEY']
    faltando = []
    
    for var in variaveis_necessarias:
        valor = os.getenv(var)
        if not valor or valor == 'sua_chave_aqui' or valor == 'sua_chave_secreta_aqui':
            faltando.append(var)
    
    if not faltando:
        print("✅ OK")
        return True
    else:
        print("❌ FALHOU")
        print(f"   Variáveis não configuradas: {', '.join(faltando)}")
        print("   Edite o arquivo .env e adicione os valores corretos")
        return False


def teste_importacoes():
    """Testa se todas as dependências estão instaladas"""
    print("3️⃣  Testando dependências...", end=" ")
    
    dependencias = [
        'flask',
        'flask_cors',
        'flask_sqlalchemy',
        'flask_login',
        'openai',
        'dotenv'
    ]
    
    faltando = []
    for dep in dependencias:
        try:
            __import__(dep)
        except ImportError:
            faltando.append(dep)
    
    if not faltando:
        print("✅ OK")
        return True
    else:
        print("❌ FALHOU")
        print(f"   Dependências não instaladas: {', '.join(faltando)}")
        print("   Execute: pip install -r requirements.txt")
        return False


def teste_conexao_openai():
    """Testa conexão com a API da OpenAI"""
    print("4️⃣  Testando conexão com OpenAI...", end=" ")
    
    try:
        from openai import OpenAI
        load_dotenv()
        
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Faz uma chamada de teste simples
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Teste"}],
            max_tokens=5
        )
        
        print("✅ OK")
        return True
        
    except Exception as e:
        print("❌ FALHOU")
        print(f"   Erro: {str(e)}")
        print("   Verifique:")
        print("   - Chave da API está correta")
        print("   - Você tem créditos disponíveis")
        print("   - Conexão com internet está estável")
        return False


def teste_estrutura_arquivos():
    """Testa se todos os arquivos necessários existem"""
    print("5️⃣  Testando estrutura de arquivos...", end=" ")
    
    arquivos_necessarios = [
        'app.py',
        'agente_ia.py',
        'models.py',
        'utils.py',
        'config.py',
        'requirements.txt',
        'templates/index.html'
    ]
    
    faltando = []
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            faltando.append(arquivo)
    
    if not faltando:
        print("✅ OK")
        return True
    else:
        print("❌ FALHOU")
        print(f"   Arquivos faltando: {', '.join(faltando)}")
        return False


def main():
    print("=" * 60)
    print("🧪 Teste de Configuração do Projeto")
    print("=" * 60)
    print()
    
    testes = [
        teste_arquivo_env,
        teste_variaveis_ambiente,
        teste_estrutura_arquivos,
        teste_importacoes,
        teste_conexao_openai
    ]
    
    resultados = []
    for teste in testes:
        try:
            resultado = teste()
            resultados.append(resultado)
        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            resultados.append(False)
        print()
    
    print("=" * 60)
    print("📊 Resultado Final")
    print("=" * 60)
    
    total = len(resultados)
    passou = sum(resultados)
    
    print(f"Testes passados: {passou}/{total}")
    
    if passou == total:
        print("\n✅ Todos os testes passaram! Projeto configurado corretamente.")
        print("\n🚀 Próximos passos:")
        print("   1. Execute: python app.py")
        print("   2. Acesse: http://localhost:5000")
        return 0
    else:
        print("\n❌ Alguns testes falharam. Corrija os problemas acima.")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Teste cancelado pelo usuário.")
        sys.exit(1)