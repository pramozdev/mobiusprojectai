import logging
import functools
import time
from typing import Callable, Any, Optional
from flask import jsonify
from openai import RateLimitError, APIError as OpenAIAPIError, AuthenticationError

# Configuração de logging
logger = logging.getLogger(__name__)

class APIError(Exception):
    """Erro personalizado para problemas de API"""
    pass

class QuotaExceededError(APIError):
    """Erro específico para cota excedida"""
    pass

class RateLimitExceededError(APIError):
    """Erro específico para limite de taxa"""
    pass

def handle_openai_errors(func: Callable) -> Callable:
    """
    Decorator para tratamento centralizado de erros da OpenAI
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RateLimitError as e:
            logger.error(f"Rate limit exceeded: {e}")
            raise RateLimitExceededError(
                "Limite de requisições atingido. Tente novamente em alguns minutos."
            )
        except AuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            raise APIError(
                "Erro de autenticação. Verifique sua chave de API."
            )
        except OpenAIAPIError as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "billing" in error_msg:
                logger.error(f"Quota exceeded: {e}")
                raise QuotaExceededError(
                    "Cota da API excedida. Verifique seu saldo em platform.openai.com"
                )
            else:
                logger.error(f"API error: {e}")
                raise APIError("Erro temporário da API. Tente novamente.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise APIError("Ocorreu um erro inesperado. Tente novamente.")
    return wrapper

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0
) -> Callable:
    """
    Decorator para retry com exponential backoff
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (RateLimitError, OpenAIAPIError) as e:
                    last_exception = e
                    
                    if attempt == max_retries - 1:
                        break
                    
                    # Calcula delay com exponential backoff
                    delay = min(base_delay * (exponential_base ** attempt), max_delay)
                    logger.warning(
                        f"Tentativa {attempt + 1}/{max_retries} falhou. "
                        f"Aguardando {delay:.2f}s antes de retry..."
                    )
                    time.sleep(delay)
                except Exception as e:
                    # Para outros erros, não faz retry
                    raise e
            
            raise last_exception
        return wrapper
    return decorator

def create_error_response(error_type: str, message: str, status_code: int = 500) -> tuple:
    """
    Cria resposta de erro padronizada para Flask
    """
    return jsonify({
        "error": error_type,
        "message": message,
        "timestamp": time.time()
    }), status_code

def flask_error_handler(app):
    """
    Registra handlers de erro globais para Flask
    """
    @app.errorhandler(QuotaExceededError)
    def handle_quota_exceeded(e):
        return create_error_response(
            "quota_exceeded",
            str(e),
            429
        )
    
    @app.errorhandler(RateLimitExceededError)
    def handle_rate_limit_exceeded(e):
        return create_error_response(
            "rate_limit_exceeded",
            str(e),
            429
        )
    
    @app.errorhandler(APIError)
    def handle_api_error(e):
        return create_error_response(
            "api_error",
            str(e),
            500
        )
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        logger.error(f"Internal server error: {e}")
        return create_error_response(
            "internal_error",
            "Erro interno do servidor. Tente novamente.",
            500
        )
    
    @app.errorhandler(404)
    def handle_not_found(e):
        return create_error_response(
            "not_found",
            "Recurso não encontrado.",
            404
        )

# Classe para monitoramento de uso da API
class APIMonitor:
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = None
        self.rate_limit_window = 60  # segundos
        self.max_requests_per_window = 60
        
    def can_make_request(self) -> bool:
        """Verifica se pode fazer uma requisição baseado no rate limiting"""
        current_time = time.time()
        
        if self.last_request_time is None:
            self.last_request_time = current_time
            return True
        
        # Reseta contador se passou da janela de tempo
        if current_time - self.last_request_time > self.rate_limit_window:
            self.request_count = 0
            self.last_request_time = current_time
            return True
        
        # Verifica se excedeu o limite
        if self.request_count >= self.max_requests_per_window:
            return False
        
        return True
    
    def record_request(self, success: bool = True):
        """Registra uma requisição"""
        self.request_count += 1
        if not success:
            self.error_count += 1
    
    def get_stats(self) -> dict:
        """Retorna estatísticas de uso"""
        return {
            "total_requests": self.request_count,
            "error_count": self.error_count,
            "success_rate": (
                (self.request_count - self.error_count) / self.request_count 
                if self.request_count > 0 else 0
            )
        }

# Monitor global
api_monitor = APIMonitor()

def monitor_api_usage(func: Callable) -> Callable:
    """
    Decorator para monitorar uso da API
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Verifica rate limiting
        if not api_monitor.can_make_request():
            raise RateLimitExceededError(
                "Muitas requisições. Por favor, aguarde um momento."
            )
        
        try:
            result = func(*args, **kwargs)
            api_monitor.record_request(success=True)
            return result
        except Exception as e:
            api_monitor.record_request(success=False)
            raise e
    
    return wrapper
