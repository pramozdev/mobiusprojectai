"""
Model de Contrato - Gestão de contratos
"""

from app.utils.imports import datetime, date, Decimal, Index, CheckConstraint
from app import db

class Contract(db.Model):
    """Model de contrato com validações e relacionamentos"""
    
    __tablename__ = 'contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Relacionamento com cliente
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    # Informações do contrato
    contract_number = db.Column(db.String(50), unique=True, index=True)
    value = db.Column(db.Numeric(15, 2), nullable=False)
    currency = db.Column(db.String(3), default='BRL')
    
    # Datas
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    signature_date = db.Column(db.Date)
    
    # Status e tipo
    status = db.Column(db.String(20), default='rascunho', nullable=False)  # rascunho, ativo, suspenso, concluído, cancelado
    contract_type = db.Column(db.String(50), default='serviço')  # serviço, produto, licença, etc.
    
    # Renovação
    auto_renew = db.Column(db.Boolean, default=False)
    renewal_days = db.Column(db.Integer, default=30)
    
    # Pagamento
    payment_method = db.Column(db.String(50))  # boleto, transferência, cartão, etc.
    payment_frequency = db.Column(db.String(20))  # mensal, trimestral, anual, etc.
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Campos de auditoria
    notes = db.Column(db.Text)
    attachments = db.Column(db.Text)  # JSON com lista de anexos
    
    # Constraints
    __table_args__ = (
        CheckConstraint('value > 0', name='check_contract_value_positive'),
        CheckConstraint('end_date >= start_date', name='check_contract_dates'),
        CheckConstraint("status IN ('rascunho', 'ativo', 'suspenso', 'concluído', 'cancelado')", 
                       name='check_contract_status'),
        Index('idx_contract_client_status', 'client_id', 'status'),
        Index('idx_contract_dates', 'start_date', 'end_date'),
        Index('idx_contract_value', 'value'),
        Index('idx_contract_created_by', 'created_by'),
    )
    
    def __init__(self, title, client_id, value, start_date, end_date, created_by, **kwargs):
        self.title = title
        self.client_id = client_id
        self.value = Decimal(str(value))
        self.start_date = start_date
        self.end_date = end_date
        self.created_by = created_by
        super(Contract, self).__init__(**kwargs)
    
    @property
    def duration_days(self):
        """Retorna duração do contrato em dias"""
        return (self.end_date - self.start_date).days + 1
    
    @property
    def days_until_expiration(self):
        """Retorna dias até o vencimento"""
        today = date.today()
        if self.end_date < today:
            return -(today - self.end_date).days
        return (self.end_date - today).days
    
    @property
    def is_expired(self):
        """Verifica se contrato está vencido"""
        return self.end_date < date.today()
    
    @property
    def is_expiring_soon(self, days=30):
        """Verifica se contrato vence em breve"""
        if self.status != 'ativo':
            return False
        return 0 <= self.days_until_expiration <= days
    
    @property
    def monthly_value(self):
        """Retorna valor mensal aproximado"""
        if self.duration_days == 0:
            return float(self.value)
        return float(self.value * Decimal(30) / Decimal(self.duration_days))
    
    def get_status_display(self):
        """Retorna descrição do status"""
        status_map = {
            'rascunho': 'Rascunho',
            'ativo': 'Ativo',
            'suspension': 'Suspenso',
            'concluído': 'Concluído',
            'cancelado': 'Cancelado'
        }
        return status_map.get(self.status, self.status.title())
    
    def can_renew(self):
        """Verifica se contrato pode ser renovado"""
        return (
            self.status == 'ativo' and 
            self.days_until_expiration <= self.renewal_days and
            self.auto_renew
        )
    
    def renew(self, days=365):
        """Renova contrato por X dias"""
        if not self.can_renew():
            return False
        
        new_end_date = self.end_date + datetime.timedelta(days=days)
        self.end_date = new_end_date
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return True
    
    def cancel(self, reason=''):
        """Cancela contrato"""
        self.status = 'cancelado'
        self.notes = f"Cancelado em {datetime.now().strftime('%d/%m/%Y')}: {reason}"
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def activate(self):
        """Ativa contrato"""
        if self.status == 'rascunho':
            self.status = 'ativo'
            self.signature_date = date.today()
            self.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        return False
    
    def to_dict(self, include_client=False):
        """Converte para dicionário (API)"""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'client_id': self.client_id,
            'contract_number': self.contract_number,
            'value': float(self.value),
            'currency': self.currency,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'signature_date': self.signature_date.isoformat() if self.signature_date else None,
            'status': self.status,
            'status_display': self.get_status_display(),
            'contract_type': self.contract_type,
            'auto_renew': self.auto_renew,
            'renewal_days': self.renewal_days,
            'payment_method': self.payment_method,
            'payment_frequency': self.payment_frequency,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'notes': self.notes,
            'duration_days': self.duration_days,
            'days_until_expiration': self.days_until_expiration,
            'is_expired': self.is_expired,
            'is_expiring_soon': self.is_expiring_soon,
            'monthly_value': self.monthly_value
        }
        
        if include_client and self.client:
            data['client'] = self.client.to_dict()
        
        return data
    
    def update_from_dict(self, data):
        """Atualiza contrato a partir de dicionário"""
        allowed_fields = [
            'title', 'description', 'contract_number', 'value', 'currency',
            'start_date', 'end_date', 'signature_date', 'status', 'contract_type',
            'auto_renew', 'renewal_days', 'payment_method', 'payment_frequency',
            'notes', 'attachments'
        ]
        
        for field in allowed_fields:
            if field in data:
                if field in ['value'] and data[field]:
                    setattr(self, field, Decimal(str(data[field])))
                elif field in ['start_date', 'end_date', 'signature_date'] and data[field]:
                    if isinstance(data[field], str):
                        setattr(self, field, datetime.strptime(data[field], '%Y-%m-%d').date())
                    else:
                        setattr(self, field, data[field])
                else:
                    setattr(self, field, data[field])
        
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def search(cls, query, user_id=None):
        """Busca contratos por título ou número"""
        search_filter = cls.title.ilike(f'%{query}%') | \
                        cls.contract_number.ilike(f'%{query}%')
        
        base_query = cls.query.filter(search_filter)
        
        if user_id:
            base_query = base_query.filter_by(created_by=user_id)
        
        return base_query.all()
    
    @classmethod
    def get_expiring_contracts(cls, days=30, user_id=None):
        """Retorna contratos que vencem em X dias"""
        from datetime import date, timedelta
        limit_date = date.today() + timedelta(days=days)
        
        base_query = cls.query.filter(
            cls.end_date <= limit_date,
            cls.end_date >= date.today(),
            cls.status == 'ativo'
        )
        
        if user_id:
            base_query = base_query.filter_by(created_by=user_id)
        
        return base_query.all()
    
    @classmethod
    def get_expired_contracts(cls, user_id=None):
        """Retorna contratos vencidos"""
        base_query = cls.query.filter(
            cls.end_date < date.today(),
            cls.status == 'ativo'
        )
        
        if user_id:
            base_query = base_query.filter_by(created_by=user_id)
        
        return base_query.all()
    
    def __repr__(self):
        return f'<Contract {self.title}>'
