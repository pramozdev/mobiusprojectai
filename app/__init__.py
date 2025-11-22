"""
Aplicação Flask com Factory Pattern
Configuração profissional com blueprints e injeção de dependências
"""

from app.utils.imports import (
    os, logging, RotatingFileHandler,
    Flask, CORS, SQLAlchemy
)

# Inicializar extensões
db = SQLAlchemy()

def create_app(config_name='development'):
    """
    Factory pattern para criação da aplicação Flask
    
    Args:
        config_name: Nome da configuração (development, testing, production)
    
    Returns:
        Flask: Instância da aplicação configurada
    """
    # Template e static folders
    template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    
    # Configuração
    from config import config
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    
    # Configurar CORS seguro
    CORS(app, 
         origins=app.config.get('CORS_ORIGINS', ['http://localhost:5000']),
         methods=['GET', 'POST', 'PUT', 'DELETE'],
         allow_headers=['Content-Type', 'Authorization'])
    
    # Configurar logging
    setup_logging(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Configurar error handlers
    register_error_handlers(app)
    
    # Configurar CLI commands
    register_cli_commands(app)
    
    return app

def setup_logging(app):
    """Configura sistema de logging profissional"""
    if not app.debug and not app.testing:
        # Logging para arquivo
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
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Aplicação iniciada')

def register_blueprints(app):
    """Registra todos os blueprints da aplicação"""
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from app.web import bp as web_bp
    app.register_blueprint(web_bp)
    
    # Configurar template context global
    @app.context_processor
    def inject_global_vars():
        """Injeta variáveis globais nos templates"""
        try:
            from app.models import Notification
            user_id = 1  # Temporário até implementar auth
            unread_count = Notification.query.filter_by(
                user_id=user_id, 
                is_read=False
            ).count()
            return {'unread_count': unread_count}
        except:
            return {'unread_count': 0}
    
    # Funções auxiliares para templates
    @app.template_global()
    def get_notification_link(notification):
        """Gera link para notificação baseado no tipo"""
        from flask import url_for
        if notification.type == 'contract' and notification.related_id:
            return url_for('web.contract_detail', contract_id=notification.related_id)
        elif notification.type == 'client' and notification.related_id:
            return url_for('web.client_detail', client_id=notification.related_id)
        return '#'

def register_error_handlers(app):
    """Registra handlers de erro globais"""
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        from flask import jsonify
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': str(e.description)
        }), 429

def register_cli_commands(app):
    """Registra comandos CLI personalizados"""
    @app.cli.command()
    def init_db():
        """Inicializa banco de dados"""
        from app.models import client, contract, user
        db.create_all()
        print('Banco de dados inicializado.')
    
    @app.cli.command()
    def create_admin():
        """Cria usuário administrador"""
        from app.models.user import User
        from werkzeug.security import generate_password_hash
        
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Usuário administrador criado.')
