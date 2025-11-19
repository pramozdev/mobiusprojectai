"""
Configurações otimizadas para a aplicação com foco em eficiência de API
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

# Configurações de otimização da API
API_CONFIG = {
    'openai': {
        'model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
        'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '500')),
        'temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.7')),
        'max_retries': int(os.getenv('OPENAI_MAX_RETRIES', '3')),
        'retry_delay': float(os.getenv('OPENAI_RETRY_DELAY', '1.0')),
        'timeout': int(os.getenv('OPENAI_TIMEOUT', '30')),
    },
    'cache': {
        'enabled': os.getenv('CACHE_ENABLED', 'True').lower() == 'true',
        'size': int(os.getenv('CACHE_SIZE', '100')),
        'ttl': int(os.getenv('CACHE_TTL', '3600')),  # 1 hora
    },
    'rate_limiting': {
        'enabled': os.getenv('RATE_LIMITING_ENABLED', 'True').lower() == 'true',
        'max_requests_per_minute': int(os.getenv('MAX_REQUESTS_PER_MINUTE', '60')),
        'max_requests_per_hour': int(os.getenv('MAX_REQUESTS_PER_HOUR', '1000')),
    }
}

# Configurações da aplicação
class Config:
    """Configuração base otimizada"""
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///contratos.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI otimizado
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_CONFIG = API_CONFIG['openai']
    
    # Cache
    CACHE_CONFIG = API_CONFIG['cache']
    
    # Rate limiting
    RATE_LIMIT_CONFIG = API_CONFIG['rate_limiting']
    
    # Servidor
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Otimizações
    JSONIFY_PRETTYPRINT_REGULAR = False  # Melhora performance
    JSON_SORT_KEYS = False  # Melhora performance
    TEMPLATES_AUTO_RELOAD = False  # Melhora performance em produção

class DevelopmentConfig(Config):
    """Configuração de desenvolvimento com otimizações"""
    DEBUG = True
    # Em desenvolvimento, usamos limites mais altos para testes
    RATE_LIMIT_CONFIG = {
        **Config.RATE_LIMIT_CONFIG,
        'max_requests_per_minute': 120,
        'max_requests_per_hour': 2000,
    }
    # Cache menor em desenvolvimento
    CACHE_CONFIG = {
        **Config.CACHE_CONFIG,
        'size': 50,
        'ttl': 1800,  # 30 minutos
    }

class ProductionConfig(Config):
    """Configuração de produção com otimizações máximas"""
    DEBUG = False
    # Em produção, limites mais restritos
    RATE_LIMIT_CONFIG = {
        **Config.RATE_LIMIT_CONFIG,
        'max_requests_per_minute': 30,
        'max_requests_per_hour': 500,
    }
    # Cache maior em produção
    CACHE_CONFIG = {
        **Config.CACHE_CONFIG,
        'size': 200,
        'ttl': 7200,  # 2 horas
    }
    # Tokens mais conservadores em produção
    OPENAI_CONFIG = {
        **Config.OPENAI_CONFIG,
        'max_tokens': 300,
        'temperature': 0.5,
    }

class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    DEBUG = True
    # Em testes, usamos mock ou limites muito baixos
    OPENAI_CONFIG = {
        **Config.OPENAI_CONFIG,
        'max_tokens': 100,
        'max_retries': 1,
    }
    RATE_LIMIT_CONFIG = {
        **Config.RATE_LIMIT_CONFIG,
        'max_requests_per_minute': 10,
        'max_requests_per_hour': 50,
    }
    CACHE_CONFIG = {
        **Config.CACHE_CONFIG,
        'enabled': False,  # Cache desabilitado em testes
    }

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config() -> Config:
    """Retorna a configuração baseada no ambiente"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])

def validate_config() -> Dict[str, Any]:
    """
    Valida as configurações e retorna status
    """
    issues = []
    warnings = []
    
    current_config = get_config()
    
    # Validações críticas
    if not current_config.OPENAI_API_KEY:
        issues.append("OPENAI_API_KEY não configurada")
    
    if not current_config.SECRET_KEY:
        issues.append("FLASK_SECRET_KEY não configurada")
    
    # Avisos de otimização
    if current_config.OPENAI_CONFIG['max_tokens'] > 1000:
        warnings.append("max_tokens muito alto pode aumentar custos")
    
    if current_config.CACHE_CONFIG['enabled'] and current_config.CACHE_CONFIG['size'] > 500:
        warnings.append("Cache muito grande pode consumir muita memória")
    
    if current_config.RATE_LIMIT_CONFIG['max_requests_per_minute'] > 100:
        warnings.append("Rate limit muito alto pode exceder cotas da API")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': warnings,
        'config_summary': {
            'environment': os.getenv('FLASK_ENV', 'development'),
            'cache_enabled': current_config.CACHE_CONFIG['enabled'],
            'rate_limiting_enabled': current_config.RATE_LIMIT_CONFIG['enabled'],
            'openai_model': current_config.OPENAI_CONFIG['model'],
            'max_tokens': current_config.OPENAI_CONFIG['max_tokens'],
        }
    }

# Função para imprimir configurações atuais (debug)
def print_config_summary():
    """Imprime um resumo das configurações atuais"""
    validation = validate_config()
    
    print("🔧 Resumo das Configurações:")
    print("=" * 40)
    
    for key, value in validation['config_summary'].items():
        print(f"{key}: {value}")
    
    if validation['issues']:
        print("\n❌ Problemas:")
        for issue in validation['issues']:
            print(f"  - {issue}")
    
    if validation['warnings']:
        print("\n⚠️ Avisos:")
        for warning in validation['warnings']:
            print(f"  - {warning}")
    
    if validation['valid']:
        print("\n✅ Configuração válida!")
    else:
        print("\n❌ Configuração inválida!")

if __name__ == "__main__":
    print_config_summary()
