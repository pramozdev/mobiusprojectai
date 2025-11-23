"""
Decorators úteis para a aplicação
"""

from functools import wraps
from flask import render_template, flash, current_app, jsonify
from app.utils.imports import request


def handle_route_errors(template_name='errors/error.html', json_response=False):
    """
    Decorator para tratamento padronizado de erros em rotas web
    
    Args:
        template_name (str): Template para renderizar em caso de erro
        json_response (bool): Se True, retorna JSON em vez de template
    
    Usage:
        @handle_route_errors('clients.html')
        @handle_route_errors(json_response=True)  # Para APIs
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                current_app.logger.error(f"Erro em {func.__name__}: {str(e)}")
                
                if json_response or request.is_json:
                    return jsonify({
                        'error': 'Internal Error',
                        'message': 'Erro interno do servidor'
                    }), 500
                else:
                    flash('Erro ao processar solicitação', 'error')
                    return render_template(template_name, error=str(e))
        return wrapper
    return decorator


def validate_json(required_fields=None):
    """
    Decorator para validação de JSON em requisições de API
    
    Args:
        required_fields (list): Campos obrigatórios no JSON
    
    Usage:
        @validate_json(['name', 'email'])
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({
                    'error': 'Bad Request',
                    'message': 'Content-Type deve ser application/json'
                }), 400
            
            data = request.get_json()
            if not data:
                return jsonify({
                    'error': 'Bad Request',
                    'message': 'JSON body é obrigatório'
                }), 400
            
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify({
                        'error': 'Validation Error',
                        'message': f'Campos obrigatórios: {", ".join(missing_fields)}'
                    }), 400
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def cache_response(timeout=300, key_prefix=None):
    """
    Decorator para cache de respostas (simplificado)
    
    Args:
        timeout (int): Tempo em segundos
        key_prefix (str): Prefixo para chave do cache
    
    Usage:
        @cache_response(timeout=60)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Cache simples em memória (em produção, usar Redis)
            cache_key = f"{key_prefix or func.__name__}_{hash(str(args) + str(kwargs))}"
            
            # Implementação básica - substituir por Flask-Caching em produção
            if not hasattr(cache_response, '_cache'):
                cache_response._cache = {}
            
            cached_result = cache_response._cache.get(cache_key)
            if cached_result:
                return cached_result
            
            result = func(*args, **kwargs)
            cache_response._cache[cache_key] = result
            return result
        return wrapper
    return decorator


def rate_limit(max_requests=10, window=60):
    """
    Decorator para rate limiting básico
    
    Args:
        max_requests (int): Máximo de requisições
        window (int): Janela de tempo em segundos
    
    Usage:
        @rate_limit(max_requests=5, window=60)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Implementação básica - substituir por Flask-Limiter em produção
            client_ip = request.remote_addr
            
            if not hasattr(rate_limit, '_requests'):
                rate_limit._requests = {}
            
            now = time.time()
            window_start = now - window
            
            # Limpar requisições antigas
            if client_ip in rate_limit._requests:
                rate_limit._requests[client_ip] = [
                    req_time for req_time in rate_limit._requests[client_ip]
                    if req_time > window_start
                ]
            else:
                rate_limit._requests[client_ip] = []
            
            # Verificar limite
            if len(rate_limit._requests[client_ip]) >= max_requests:
                return jsonify({
                    'error': 'Rate Limit Exceeded',
                    'message': f'Máximo de {max_requests} requisições por {window} segundos'
                }), 429
            
            # Adicionar requisição atual
            rate_limit._requests[client_ip].append(now)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Import necessário para rate_limit
import time
