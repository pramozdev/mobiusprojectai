import os
from openai import OpenAI
from dotenv import load_dotenv

def testar_chave():
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("ERRO: Chave da API não encontrada no arquivo .env")
        return
        
    print(f"Chave encontrada: {api_key[:10]}...{api_key[-5:]}")
    
    try:
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        print("\nConexão bem-sucedida! Modelos disponíveis:")
        for model in models.data[:5]:  # Mostra apenas os 5 primeiros modelos
            print(f"- {model.id}")
        print("\n✅ Sua chave está funcionando corretamente!")
        
    except Exception as e:
        print(f"\n❌ Erro ao conectar à API da OpenAI:")
        print(str(e))
        
        if "quota" in str(e).lower():
            print("\n📢 Você atingiu a cota da sua conta ou a chave não tem créditos suficientes.")
            print("Por favor, verifique seu saldo em: https://platform.openai.com/account/usage")
        elif "invalid" in str(e).lower():
            print("\n🔑 A chave de API parece estar inválida ou expirada.")
            print("Por favor, gere uma nova chave em: https://platform.openai.com/api-keys")
        else:
            print("\n🔍 Verifique sua conexão com a internet e tente novamente.")

if __name__ == "__main__":
    testar_chave()
