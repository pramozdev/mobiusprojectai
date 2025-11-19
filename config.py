"""
Configurações da aplicação
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuração base"""
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///contratos.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Servidor
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'


class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True


class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False


# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}