import os
import logging
import time
import json
from typing import Optional, List, Dict, Any
from functools import wraps
from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError, APIError, AuthenticationError

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações de otimização
CONFIG = {
    'max_retries': 3,
    'retry_delay': 1.0,  # segundos
    'max_historico': 10,  # reduzido para economizar tokens
    'cache_enabled': True,
    'cache_size': 100,
    'model': 'gpt-3.5-turbo',  # modelo mais econômico
    'max_tokens': 500,  # limite de resposta para economizar
    'temperature': 0.7
}

# Cache simples em memória
cache = {}

def retry_on_error(max_retries=3, delay=1.0):
    """Decorator para retry automático em caso de erro de API"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (RateLimitError, APIError) as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        wait_time = delay * (2 ** attempt)  # exponential backoff
                        logger.warning(f"Tentativa {attempt + 1} falhou. Aguardando {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Todas as {max_retries} tentativas falharam")
                except AuthenticationError as e:
                    logger.error(f"Erro de autenticação: {e}")
                    break
                except Exception as e:
                    logger.error(f"Erro inesperado: {e}")
                    break
            raise last_error
        return wrapper
    return decorator

def get_cache_key(mensagem: str, contexto: str) -> str:
    """Gera chave única para cache baseada na mensagem e contexto"""
    import hashlib
    content = f"{mensagem}:{contexto}"
    return hashlib.md5(content.encode()).hexdigest()

class AgenteIAOtimizado:
    def __init__(self, nome: str = "Assistente", config: Dict = None):
        """
        Inicializa o agente de IA com otimizações e tratamento robusto de erros.
        
        Args:
            nome: Nome do assistente
            config: Configurações personalizadas
        """
        self.nome = nome
        self.config = {**CONFIG, **(config or {})}
        self.historico: List[Dict[str, str]] = []
        self.exemplos_treinamento: List[Dict[str, str]] = []
        self.client: Optional[OpenAI] = None
        self._configurar_ambiente()
        self._carregar_contexto_inicial()
        
    def _carregar_contexto_inicial(self):
        """Carrega o contexto inicial do assistente otimizado."""
        self.contexto_inicial = f"""Você é um assistente útil chamado {self.nome} especializado em gerenciamento de contratos.

Diretrizes:
1. Seja conciso e objetivo (máximo 3-4 frases)
2. Forneça apenas informações essenciais
3. Use emojis apenas quando relevante
4. Se não tiver certeza, diga honestamente

Contexto: Você ajuda com análise de contratos, prazos, valores e métricas."""
        
    def _configurar_ambiente(self):
        """Configura o ambiente com tratamento de erros."""
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError("Chave da API da OpenAI não encontrada")
            
        try:
            self.client = OpenAI(api_key=api_key)
            # Testa a conexão
            self.client.models.list()
            logger.info("Conexão com API OpenAI estabelecida com sucesso")
        except Exception as e:
            logger.error(f"Falha ao conectar à API OpenAI: {e}")
            raise
            
    def adicionar_exemplo_treinamento(self, pergunta: str, resposta: str) -> str:
        """Adiciona exemplo de treinamento com validação."""
        if len(pergunta) > 200 or len(resposta) > 200:
            logger.warning("Exemplo de treinamento muito longo, será truncado")
            pergunta = pergunta[:200]
            resposta = resposta[:200]
            
        self.exemplos_treinamento.append({
            'pergunta': pergunta,
            'resposta': resposta
        })
        
        # Limita o número de exemplos para economizar tokens
        if len(self.exemplos_treinamento) > 5:
            self.exemplos_treinamento = self.exemplos_treinamento[-5:]
            
        return f"Exemplo adicionado: {pergunta[:30]}..."
        
    def obter_contexto_treinamento(self) -> str:
        """Retorna contexto otimizado para economizar tokens."""
        contexto = self.contexto_inicial + "\n\n"
        
        # Adiciona apenas exemplos recentes e relevantes
        for exemplo in self.exemplos_treinamento[-3:]:
            contexto += f"Q: {exemplo['pergunta']}\nA: {exemplo['resposta']}\n\n"
            
        return contexto.strip()
        
    def _limpar_historico(self):
        """Mantém o histórico dentro do limite configurado."""
        if len(self.historico) > self.config['max_historico']:
            # Mantém as mensagens mais importantes
            self.historico = self.historico[-self.config['max_historico']:]
            
    @retry_on_error(max_retries=CONFIG['max_retries'], delay=CONFIG['retry_delay'])
    def _chamar_api(self, mensagens: List[Dict[str, str]]) -> str:
        """Faz chamada à API com tratamento de erros e retry."""
        try:
            response = self.client.chat.completions.create(
                model=self.config['model'],
                messages=mensagens,
                max_tokens=self.config['max_tokens'],
                temperature=self.config['temperature']
            )
            return response.choices[0].message.content.strip()
        except RateLimitError as e:
            logger.error(f"Limite de taxa excedido: {e}")
            raise
        except APIError as e:
            logger.error(f"Erro da API: {e}")
            raise
        except AuthenticationError as e:
            logger.error(f"Erro de autenticação: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado na API: {e}")
            raise
            
    def processar_mensagem(self, mensagem: str) -> str:
        """
        Processa mensagem com cache, otimização e tratamento robusto de erros.
        
        Args:
            mensagem: Mensagem do usuário
            
        Returns:
            Resposta do assistente ou mensagem de erro
        """
        # Verifica cache primeiro
        if self.config['cache_enabled']:
            cache_key = get_cache_key(mensagem, self.obter_contexto_treinamento())
            if cache_key in cache:
                logger.info("Resposta encontrada no cache")
                return cache[cache_key]
        
        try:
            # Validação da entrada
            if not mensagem or not mensagem.strip():
                return "Por favor, envie uma mensagem válida."
                
            mensagem = mensagem.strip()
            
            # Adiciona ao histórico
            self.historico.append({"role": "user", "content": mensagem})
            self._limpar_historico()
            
            # Prepara mensagens para a API
            mensagens = [
                {"role": "system", "content": self.obter_contexto_treinamento()},
                *self.historico[-10:]  # Limita histórico para economizar tokens
            ]
            
            # Chama a API
            resposta = self._chamar_api(mensagens)
            
            # Adiciona resposta ao histórico
            self.historico.append({"role": "assistant", "content": resposta})
            
            # Armazena no cache
            if self.config['cache_enabled']:
                if len(cache) < self.config['cache_size']:
                    cache[cache_key] = resposta
                else:
                    # Remove item mais antigo do cache
                    cache.pop(next(iter(cache)))
                    cache[cache_key] = resposta
            
            return resposta
            
        except RateLimitError:
            return "🚫 Limite de uso atingido. Por favor, tente novamente em alguns minutos."
        except AuthenticationError:
            return "🔑 Erro de autenticação. Verifique sua chave de API."
        except APIError as e:
            if "quota" in str(e).lower():
                return "💳 Cota da API excedida. Verifique seu saldo em platform.openai.com"
            return "⚠️ Erro temporário da API. Tente novamente."
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            return "❌ Ocorreu um erro inesperado. Tente novamente."
            
    def limpar_cache(self):
        """Limpa o cache de respostas."""
        global cache
        cache.clear()
        logger.info("Cache limpo")
        
    def get_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso."""
        return {
            'historico_size': len(self.historico),
            'exemplos_size': len(self.exemplos_treinamento),
            'cache_size': len(cache),
            'cache_enabled': self.config['cache_enabled'],
            'model': self.config['model']
        }

# Função de teste
def testar_agente_otimizado():
    """Testa o agente otimizado com vários cenários."""
    agente = AgenteIAOtimizado("Teste")
    
    # Adiciona exemplos de treinamento
    agente.adicionar_exemplo_treinamento(
        "Qual o valor total dos contratos?",
        "O valor total é R$ 1.250.000,00"
    )
    
    # Testa mensagens
    test_messages = [
        "Olá, como você está?",
        "Quantos contratos temos ativos?",
        "Qual o valor médio dos contratos?",
        "Me mostre os contratos que vencem este mês"
    ]
    
    print("🧪 Testando Agente IA Otimizado")
    print("=" * 50)
    
    for i, msg in enumerate(test_messages, 1):
        print(f"\nTeste {i}: {msg}")
        try:
            resposta = agente.processar_mensagem(msg)
            print(f"Resposta: {resposta}")
        except Exception as e:
            print(f"Erro: {e}")
    
    print(f"\n📊 Estatísticas: {agente.get_estatisticas()}")

if __name__ == "__main__":
    testar_agente_otimizado()
