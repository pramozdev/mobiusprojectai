"""
Configurações profissionais da aplicação Flask
Ambientes: development, testing, production
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuração base"""
    
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    
    # Configurações de banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Configurações de segurança
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 horas
    
    # Configurações de CORS
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
    
    # Configurações de upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    # Configurações de email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Configurações de API
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Configurações de cache
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Configurações de rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    
    @staticmethod
    def init_app(app):
        """Inicialização específica da configuração"""
        # Criar diretório de uploads se não existir
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = False
    
    # CORS mais permissivo para desenvolvimento
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000', 
                   'http://127.0.0.1:3000', 'http://127.0.0.1:5000']

class TestingConfig(Config):
    """Configuração de testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost:5000'

class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SESSION_COOKIE_SECURE = True
    
    # CORS restrito para produção
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    
    # Cache Redis para produção
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Rate limiting com Redis
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/1')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Logging para produção
        import logging
        from logging.handlers import RotatingFileHandler, SMTPHandler
        
        if not app.debug and not app.testing:
            # Logging em arquivo
            if not os.path.exists('logs'):
                os.mkdir('logs')
            
            file_handler = RotatingFileHandler(
                'logs/app.log', 
                maxBytes=10240000,  # 10MB
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            
            # Logging por email para erros críticos
            if app.config.get('MAIL_SERVER'):
                auth = None
                if app.config.get('MAIL_USERNAME') and app.config.get('MAIL_PASSWORD'):
                    auth = (app.config.get('MAIL_USERNAME'), app.config.get('MAIL_PASSWORD'))
                
                secure = None
                if app.config.get('MAIL_USE_TLS'):
                    secure = ()
                
                mail_handler = SMTPHandler(
                    mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                    fromaddr=app.config['MAIL_USERNAME'],
                    toaddrs=['admin@' + app.config['MAIL_SERVER'].split('@')[1]],
                    subject='Application Error',
                    credentials=auth,
                    secure=secure
                )
                mail_handler.setLevel(logging.ERROR)
                app.logger.addHandler(mail_handler)
            
            app.logger.setLevel(logging.INFO)
            app.logger.info('Aplicação em produção')

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Validação de configuração
def validate_config():
    """Valida configurações críticas"""
    issues = []
    
    current_config = config[os.getenv('FLASK_ENV', 'default')]
    
    # Verificar SECRET_KEY
    if not current_config.SECRET_KEY or len(current_config.SECRET_KEY) < 32:
        issues.append("SECRET_KEY não configurado ou muito curto")
    
    # Verificar configuração de banco
    if not current_config.SQLALCHEMY_DATABASE_URI:
        issues.append("DATABASE_URL não configurado")
    
    # Verificar configuração de produção
    if os.getenv('FLASK_ENV') == 'production':
        if current_config.DEBUG:
            issues.append("DEBUG=True em ambiente de produção")
        
        if not current_config.SESSION_COOKIE_SECURE:
            issues.append("SESSION_COOKIE_SECURE=False em produção")
    
    return issues
