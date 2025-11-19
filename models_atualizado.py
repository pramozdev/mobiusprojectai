from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    notifications = db.relationship('Notification', backref='user', lazy=True)
    chat_messages = db.relationship('ChatMessage', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    cnpj_cpf = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    sector = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    contracts = db.relationship('Contract', backref='client', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'cnpj_cpf': self.cnpj_cpf,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'sector': self.sector,
            'created_at': self.created_at.strftime('%d/%m/%Y'),
            'updated_at': self.updated_at.strftime('%d/%m/%Y'),
            'contracts_count': len(self.contracts)
        }
    
    def get_total_contract_value(self):
        """Retorna o valor total de todos os contratos do cliente"""
        return sum(contract.value for contract in self.contracts if contract.status == 'Ativo')
    
    def get_active_contracts(self):
        """Retorna contratos ativos do cliente"""
        return [c for c in self.contracts if c.status == 'Ativo']

class Contract(db.Model):
    __tablename__ = 'contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    contract_number = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    value = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(50))
    payment_frequency = db.Column(db.String(20))  # Mensal, Anual, etc.
    status = db.Column(db.String(20), default='Ativo')  # Ativo, Suspenso, Cancelado, Concluído
    renewal_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_name': self.client.name if self.client else 'N/A',
            'contract_number': self.contract_number,
            'description': self.description,
            'value': self.value,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'payment_method': self.payment_method,
            'payment_frequency': self.payment_frequency,
            'status': self.status,
            'renewal_date': self.renewal_date.strftime('%Y-%m-%d') if self.renewal_date else None,
            'days_until_due': (self.end_date - datetime.now().date()).days,
            'days_until_renewal': (self.renewal_date - datetime.now().date()).days if self.renewal_date else None,
            'created_at': self.created_at.strftime('%d/%m/%Y'),
            'updated_at': self.updated_at.strftime('%d/%m/%Y')
        }
    
    def is_overdue(self):
        """Verifica se o contrato está vencido"""
        return datetime.now().date() > self.end_date and self.status == 'Ativo'
    
    def is_renewal_due(self):
        """Verifica se está próximo da data de renovação"""
        if not self.renewal_date:
            return False
        days_until = (self.renewal_date - datetime.now().date()).days
        return 0 <= days_until <= 30  # 30 dias antes da renovação

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'))
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(20), default='info')  # info, warning, error, success
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com contrato
    contract = db.relationship('Contract', backref='notifications')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M'),
            'contract_id': self.contract_id,
            'contract_number': self.contract.contract_number if self.contract else None
        }

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'response': self.response,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M')
        }

# Funções auxiliares para o banco de dados
def init_db():
    """Inicializa o banco de dados com as tabelas"""
    db.create_all()
    print("✅ Banco de dados inicializado com sucesso!")

def create_sample_data():
    """Cria dados de exemplo para teste"""
    from datetime import date, timedelta
    
    # Criar clientes de exemplo
    clients_data = [
        {
            'name': 'Tech Solutions Ltda',
            'email': 'contato@techsolutions.com',
            'phone': '(11) 1234-5678',
            'cnpj_cpf': '12.345.678/0001-90',
            'address': 'Rua das Tecnologias, 123',
            'city': 'São Paulo',
            'state': 'SP',
            'sector': 'Tecnologia'
        },
        {
            'name': 'Consultoria Empresarial S/A',
            'email': 'financeiro@consultoria.com',
            'phone': '(21) 9876-5432',
            'cnpj_cpf': '98.765.432/0001-10',
            'address': 'Avenida Central, 456',
            'city': 'Rio de Janeiro',
            'state': 'RJ',
            'sector': 'Consultoria'
        },
        {
            'name': 'Comércio Varejista ME',
            'email': 'contato@varejo.com',
            'phone': '(31) 5555-9999',
            'cnpj_cpf': '45.678.901/0001-23',
            'address': 'Rua do Comércio, 789',
            'city': 'Belo Horizonte',
            'state': 'MG',
            'sector': 'Varejo'
        }
    ]
    
    clients = []
    for client_data in clients_data:
        client = Client(**client_data)
        db.session.add(client)
        clients.append(client)
    
    db.session.commit()
    
    # Criar contratos de exemplo
    contracts_data = [
        {
            'client': clients[0],
            'contract_number': 'CTR-2024-001',
            'description': 'Desenvolvimento de sistema ERP',
            'value': 150000.00,
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
            'payment_method': 'Transferência Bancária',
            'payment_frequency': 'Mensal',
            'renewal_date': date(2024, 12, 1)
        },
        {
            'client': clients[0],
            'contract_number': 'CTR-2024-002',
            'description': 'Manutenção e suporte técnico',
            'value': 36000.00,
            'start_date': date(2024, 6, 1),
            'end_date': date(2025, 5, 31),
            'payment_method': 'Boleto',
            'payment_frequency': 'Mensal',
            'renewal_date': date(2025, 5, 1)
        },
        {
            'client': clients[1],
            'contract_number': 'CTR-2024-003',
            'description': 'Consultoria em gestão',
            'value': 85000.00,
            'start_date': date(2024, 3, 1),
            'end_date': date(2024, 8, 31),
            'payment_method': 'Transferência Bancária',
            'payment_frequency': 'Trimestral',
            'renewal_date': date(2024, 8, 15),
            'status': 'Concluído'
        },
        {
            'client': clients[2],
            'contract_number': 'CTR-2024-004',
            'description': 'Sistema de gestão de estoque',
            'value': 45000.00,
            'start_date': date(2024, 7, 1),
            'end_date': date(2024, 12, 31),
            'payment_method': 'PIX',
            'payment_frequency': 'Mensal',
            'renewal_date': date(2024, 12, 15)
        }
    ]
    
    for contract_data in contracts_data:
        contract = Contract(**contract_data)
        db.session.add(contract)
    
    db.session.commit()
    
    # Criar notificações de exemplo
    notifications_data = [
        {
            'user_id': 1,
            'contract_id': 1,
            'title': 'Contrato próximo ao vencimento',
            'message': 'O contrato CTR-2024-001 vence em 30 dias',
            'type': 'warning'
        },
        {
            'user_id': 1,
            'contract_id': 2,
            'title': 'Nova renovação disponível',
            'message': 'O contrato CTR-2024-002 pode ser renovado',
            'type': 'info'
        }
    ]
    
    for notif_data in notifications_data:
        notification = Notification(**notif_data)
        db.session.add(notification)
    
    db.session.commit()
    
    print("✅ Dados de exemplo criados com sucesso!")
    print(f"   - {len(clients)} clientes criados")
    print(f"   - {len(contracts_data)} contratos criados")
    print(f"   - {len(notifications_data)} notificações criadas")

if __name__ == "__main__":
    print("🔧 Configurando banco de dados...")
    init_db()
    create_sample_data()
