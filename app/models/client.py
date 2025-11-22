"""
Model de Cliente - Gestão de clientes
"""

from app.utils.imports import datetime, Index
from app import db

class Client(db.Model):
    """Model de cliente com validações e relacionamentos"""
    
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True)
    phone = db.Column(db.String(20))
    document = db.Column(db.String(20), unique=True, index=True)  # CPF/CNPJ
    address = db.Column(db.Text)
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    postal_code = db.Column(db.String(10))
    country = db.Column(db.String(50), default='Brasil')
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relacionamentos
    contracts = db.relationship('Contract', backref='client', lazy='dynamic', cascade='all, delete-orphan')
    
    # Índices compostos
    __table_args__ = (
        Index('idx_client_name_active', 'name', 'is_active'),
        Index('idx_client_created_by', 'created_by'),
    )
    
    def __init__(self, name, email, created_by, **kwargs):
        self.name = name
        self.email = email.lower() if email else None
        self.created_by = created_by
        super(Client, self).__init__(**kwargs)
    
    @property
    def contracts_count(self):
        """Retorna número de contratos do cliente"""
        return self.contracts.count()
    
    @property
    def active_contracts_count(self):
        """Retorna número de contratos ativos"""
        return self.contracts.filter_by(status='ativo').count()
    
    @property
    def total_contract_value(self):
        """Retorna valor total de todos os contratos"""
        result = db.session.query(db.func.sum(Contract.value)).filter(
            Contract.client_id == self.id
        ).scalar()
        return float(result) if result else 0.0
    
    @property
    def average_contract_value(self):
        """Retorna valor médio dos contratos"""
        count = self.contracts_count
        if count == 0:
            return 0.0
        return self.total_contract_value / count
    
    def get_contracts_by_status(self, status):
        """Retorna contratos por status"""
        return self.contracts.filter_by(status=status).all()
    
    def get_expired_contracts(self):
        """Retorna contratos vencidos"""
        from datetime import date
        return self.contracts.filter(
            Contract.end_date < date.today()
        ).all()
    
    def get_expiring_contracts(self, days=30):
        """Retorna contratos que vencem em X dias"""
        from datetime import date, timedelta
        limit_date = date.today() + timedelta(days=days)
        return self.contracts.filter(
            Contract.end_date <= limit_date,
            Contract.end_date >= date.today(),
            Contract.status == 'ativo'
        ).all()
    
    def to_dict(self, include_contracts=False):
        """Converte para dicionário (API)"""
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'document': self.document,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'contracts_count': self.contracts_count,
            'active_contracts_count': self.active_contracts_count,
            'total_contract_value': self.total_contract_value,
            'average_contract_value': self.average_contract_value
        }
        
        if include_contracts:
            data['contracts'] = [contract.to_dict() for contract in self.contracts]
        
        return data
    
    def update_from_dict(self, data):
        """Atualiza cliente a partir de dicionário"""
        allowed_fields = ['name', 'email', 'phone', 'document', 'address', 
                         'city', 'state', 'postal_code', 'country', 'is_active']
        
        for field in allowed_fields:
            if field in data:
                if field == 'email' and data[field]:
                    setattr(self, field, data[field].lower())
                else:
                    setattr(self, field, data[field])
        
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def search(cls, query, user_id=None):
        """Busca clientes por nome, email ou documento"""
        search_filter = cls.name.ilike(f'%{query}%') | \
                        cls.email.ilike(f'%{query}%') | \
                        cls.document.ilike(f'%{query}%')
        
        base_query = cls.query.filter(search_filter)
        
        if user_id:
            base_query = base_query.filter_by(created_by=user_id)
        
        return base_query.all()
    
    def __repr__(self):
        return f'<Client {self.name}>'
