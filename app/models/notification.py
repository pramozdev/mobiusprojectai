"""
Model de Notificação - Sistema de alertas
"""

from app.utils.imports import datetime
from app import db

class Notification(db.Model):
    """Model de notificação para usuários"""
    
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), default='info')  # info, warning, error, success
    category = db.Column(db.String(50))  # contract, client, system, etc.
    
    # Relacionamento
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Status
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Links e ações
    action_url = db.Column(db.String(500))
    action_text = db.Column(db.String(100))
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    read_at = db.Column(db.DateTime)
    
    # Relacionamentos
    user = db.relationship('User', backref=db.backref('notifications', lazy='dynamic'))
    
    def mark_as_read(self):
        """Marca notificação como lida"""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()
            db.session.commit()
    
    def mark_as_unread(self):
        """Marca notificação como não lida"""
        if self.is_read:
            self.is_read = False
            self.read_at = None
            db.session.commit()
    
    def to_dict(self):
        """Converte para dicionário (API)"""
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'category': self.category,
            'user_id': self.user_id,
            'is_read': self.is_read,
            'is_active': self.is_active,
            'action_url': self.action_url,
            'action_text': self.action_text,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }
    
    @classmethod
    def create_contract_notification(cls, user_id, contract, notification_type, message):
        """Cria notificação relacionada a contrato"""
        notification = cls(
            title=f'Contrato: {contract.title}',
            message=message,
            notification_type=notification_type,
            category='contract',
            user_id=user_id,
            action_url=f'/contracts/{contract.id}',
            action_text='Ver Contrato'
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @classmethod
    def create_client_notification(cls, user_id, client, notification_type, message):
        """Cria notificação relacionada a cliente"""
        notification = cls(
            title=f'Cliente: {client.name}',
            message=message,
            notification_type=notification_type,
            category='client',
            user_id=user_id,
            action_url=f'/clients/{client.id}',
            action_text='Ver Cliente'
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @classmethod
    def create_system_notification(cls, user_id, title, message, notification_type='info'):
        """Cria notificação do sistema"""
        notification = cls(
            title=title,
            message=message,
            notification_type=notification_type,
            category='system',
            user_id=user_id
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    def __repr__(self):
        return f'<Notification {self.title}>'
