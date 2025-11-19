import os
import logging
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgenteIA:
    def __init__(self, nome: str = "Assistente", max_historico: int = 20):
        """
        Inicializa o agente de IA com um nome e configura a API da OpenAI.
        
        Args:
            nome: Nome do assistente
            max_historico: Número máximo de mensagens a manter no histórico
        """
        self.nome = nome
        self.historico = []
        self.exemplos_treinamento = []
        self.client: Optional[OpenAI] = None
        self.max_historico = max_historico
        self._configurar_ambiente()
        self._carregar_contexto_inicial()
        
    def _carregar_contexto_inicial(self):
        """Carrega o contexto inicial do assistente."""
        self.contexto_inicial = f"""Você é um assistente útil chamado {self.nome} que ajuda com gerenciamento de contratos e integração com o Spotify. 
Siga estas diretrizes:
1. Seja conciso e objetivo nas respostas
2. Mantenha o foco nas tarefas relacionadas a contratos e música
3. Use emojis relevantes quando apropriado
4. Sempre verifique os dados antes de responder sobre prazos ou valores

Exemplos de interações:"""
        
    def adicionar_exemplo_treinamento(self, pergunta, resposta):
        """
        Adiciona um exemplo de treinamento personalizado.
        
        Args:
            pergunta (str): Exemplo de pergunta do usuário
            resposta (str): Resposta desejada para a pergunta
        """
        self.exemplos_treinamento.append({
            'pergunta': pergunta,
            'resposta': resposta
        })
        return f"Exemplo de treinamento adicionado: {pergunta[:50]}..."
        
    def obter_contexto_treinamento(self):
        """Retorna o contexto de treinamento formatado."""
        contexto = self.contexto_inicial + "\n\n"
        for exemplo in self.exemplos_treinamento[-5:]:  # Usa apenas os 5 exemplos mais recentes
            contexto += f"\nUsuário: {exemplo['pergunta']}\n"
            contexto += f"{self.nome}: {exemplo['resposta']}\n"
        return contexto
        
    def _configurar_ambiente(self):
        """Carrega as variáveis de ambiente e configura a API da OpenAI."""
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("Chave da API da OpenAI não encontrada. Crie um arquivo .env com OPENAI_API_KEY=sua_chave_aqui")
        self.client = OpenAI(api_key=api_key)
    
    def processar_mensagem(self, mensagem: str) -> str:
        """
        Processa uma mensagem do usuário e retorna a resposta do assistente.
        
        Args:
            mensagem: Mensagem do usuário
            
        Returns:
            Resposta do assistente
        """
        try:
            # Adiciona a mensagem ao histórico
            self.historico.append({"role": "user", "content": mensagem})
            
            # Limita o tamanho do histórico
            if len(self.historico) > self.max_historico:
                self.historico = self.historico[-self.max_historico:]
            
            # Prepara o contexto da conversa
            mensagens = [
                {"role": "system", "content": self.obter_contexto_treinamento()}
            ]
            mensagens.extend(self.historico[-5:])  # Mantém apenas as últimas 5 mensagens
            
            # Chama a API da OpenAI
            modelo = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
            resposta = self.client.chat.completions.create(
                model=modelo,
                messages=mensagens,
                temperature=0.7,
                max_tokens=500
            )
            
            # Extrai a resposta
            resposta_texto = resposta.choices[0].message.content
            
            # Adiciona a resposta ao histórico
            self.historico.append({"role": "assistant", "content": resposta_texto})
            
            logger.info(f"Mensagem processada com sucesso. Histórico: {len(self.historico)} mensagens")
            return resposta_texto
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {str(e)}")
            return f"Desculpe, ocorreu um erro ao processar sua mensagem: {str(e)}"

def main():
    # Cria uma instância do agente
    agente = AgenteIA(nome="Aurora")
    
    print(f"{agente.nome}: Olá! Sou o seu assistente de IA. Como posso ajudar? (Digite 'sair' para encerrar)")
    
    # Loop principal de interação
    while True:
        try:
            # Obtém a entrada do usuário
            mensagem = input("Você: ").strip()
            
            # Verifica se o usuário quer sair
            if mensagem.lower() in ['sair', 'exit', 'tchau']:
                print(f"{agente.nome}: Até mais! Foi um prazer ajudar.")
                break
                
            # Processa a mensagem e exibe a resposta
            resposta = agente.processar_mensagem(mensagem)
            print(f"{agente.nome}: {resposta}")
            
        except KeyboardInterrupt:
            print("\nEncerrando o programa...")
            break
        except Exception as e:
            print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()
