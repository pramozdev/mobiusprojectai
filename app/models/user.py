"""
Model de Usuário - Autenticação e gerenciamento
"""

from app.utils.imports import datetime, generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    """Model de usuário com autenticação"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)
    
    # Relacionamentos
    clients = db.relationship('Client', backref='created_by_user', lazy='dynamic')
    contracts = db.relationship('Contract', backref='created_by_user', lazy='dynamic')
    
    def __init__(self, username, email, **kwargs):
        self.username = username
        self.email = email
        super(User, self).__init__(**kwargs)
    
    def set_password(self, password):
        """Define senha com hash seguro"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica senha"""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Atualiza data do último login"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def get_clients_count(self):
        """Retorna número de clientes criados pelo usuário"""
        return self.clients.count()
    
    def get_contracts_count(self):
        """Retorna número de contratos criados pelo usuário"""
        return self.contracts.count()
    
    def to_dict(self):
        """Converte para dicionário (API)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'clients_count': self.get_clients_count(),
            'contracts_count': self.get_contracts_count()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
