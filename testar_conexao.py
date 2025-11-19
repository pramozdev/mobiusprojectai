import os
from dotenv import load_dotenv
from openai import OpenAI

def testar_conexao():
    try:
        # Carrega as variáveis de ambiente
        load_dotenv()
        
        # Inicializa o cliente da OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Faz uma chamada de teste simples
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Diga apenas 'Conexão bem-sucedida!'"}],
            max_tokens=10
        )
        
        print("✅ " + resposta.choices[0].message.content)
        print("\n✅ Conexão com a API da OpenAI realizada com sucesso!")
        
    except Exception as e:
        print("❌ Erro ao conectar à API da OpenAI:")
        print(str(e))
        print("\nVerifique se:")
        print("1. Sua chave de API está correta no arquivo .env")
        print("2. Você tem créditos disponíveis na sua conta")
        print("3. Sua conexão com a internet está estável")

if __name__ == "__main__":
    print("Testando conexão com a API da OpenAI...\n")
    testar_conexao()
