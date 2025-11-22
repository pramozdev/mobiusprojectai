"""
Testes unitários dos modelos
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal

from app.models import User, Client, Contract, Notification
from app import db

class TestUser:
    """Testes do modelo User"""
    
    def test_create_user(self, app):
        """Testa criação de usuário"""
        with app.app_context():
            user = User(
                username='testuser',
                email='test@example.com',
                is_admin=True
            )
            user.set_password('testpass')
            
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.username == 'testuser'
            assert user.email == 'test@example.com'
            assert user.is_admin is True
            assert user.is_active is True
            assert user.created_at is not None
            assert user.check_password('testpass') is True
            assert user.check_password('wrongpass') is False
    
    def test_user_password_hashing(self, app):
        """Testa hash de senha"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpass')
            
            # Senha não deve ser armazenada em texto plano
            assert 'testpass' not in user.password_hash
            assert user.password_hash.startswith('pbkdf2:sha256:')
    
    def test_user_to_dict(self, app, sample_user):
        """Testa conversão para dicionário"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.commit()
            
            user_dict = sample_user.to_dict()
            
            assert 'id' in user_dict
            assert user_dict['username'] == 'testuser'
            assert user_dict['email'] == 'test@example.com'
            assert user_dict['is_admin'] is True
            assert 'created_at' in user_dict
            assert 'clients_count' in user_dict
            assert 'contracts_count' in user_dict
    
    def test_user_update_last_login(self, app, sample_user):
        """Testa atualização de último login"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.commit()
            
            original_login = sample_user.last_login
            sample_user.update_last_login()
            
            assert sample_user.last_login != original_login
            assert sample_user.last_login is not None

class TestClient:
    """Testes do modelo Client"""
    
    def test_create_client(self, app, sample_user):
        """Testa criação de cliente"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.commit()
            
            client = Client(
                name='Test Client',
                email='client@test.com',
                phone='11999999999',
                document='12345678901',
                created_by=sample_user.id
            )
            
            db.session.add(client)
            db.session.commit()
            
            assert client.id is not None
            assert client.name == 'Test Client'
            assert client.email == 'client@test.com'
            assert client.created_by == sample_user.id
            assert client.is_active is True
            assert client.created_at is not None
    
    def test_client_properties(self, app, sample_user, sample_client):
        """Testa propriedades do cliente"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.commit()
            
            sample_client.created_by = sample_user.id
            db.session.add(sample_client)
            db.session.commit()
            
            # Sem contratos
            assert sample_client.contracts_count == 0
            assert sample_client.active_contracts_count == 0
            assert sample_client.total_contract_value == 0.0
            assert sample_client.average_contract_value == 0.0
    
    def test_client_with_contracts(self, app, sample_user, sample_client):
        """Testa cliente com contratos"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.commit()
            
            sample_client.created_by = sample_user.id
            db.session.add(sample_client)
            db.session.commit()
            
            # Adicionar contratos
            contract1 = Contract(
                title='Contract 1',
                client_id=sample_client.id,
                value=1000.00,
                start_date=date.today(),
                end_date=date(2024, 12, 31),
                status='ativo',
                created_by=sample_user.id
            )
            
            contract2 = Contract(
                title='Contract 2',
                client_id=sample_client.id,
                value=2000.00,
                start_date=date.today(),
                end_date=date(2024, 12, 31),
                status='concluído',
                created_by=sample_user.id
            )
            
            db.session.add(contract1)
            db.session.add(contract2)
            db.session.commit()
            
            # Verificar propriedades
            assert sample_client.contracts_count == 2
            assert sample_client.active_contracts_count == 1
            assert sample_client.total_contract_value == 3000.0
            assert sample_client.average_contract_value == 1500.0
    
    def test_client_to_dict(self, app, sample_user, sample_client):
        """Testa conversão para dicionário"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.commit()
            
            sample_client.created_by = sample_user.id
            db.session.add(sample_client)
            db.session.commit()
            
            client_dict = sample_client.to_dict()
            
            assert 'id' in client_dict
            assert client_dict['name'] == 'Cliente Teste'
            assert client_dict['email'] == 'cliente@teste.com'
            assert 'contracts_count' in client_dict
            assert 'total_contract_value' in client_dict
    
    def test_client_search(self, app, sample_user):
        """Testa busca de clientes"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.commit()
            
            # Criar clientes
            clients = [
                Client(name='Client A', email='a@test.com', created_by=sample_user.id),
                Client(name='Client B', email='b@test.com', created_by=sample_user.id),
                Client(name='Client C', email='c@test.com', created_by=sample_user.id)
            ]
            
            for client in clients:
                db.session.add(client)
            
            db.session.commit()
            
            # Buscar por nome
            results = Client.search('Client A')
            assert len(results) == 1
            assert results[0].name == 'Client A'
            
            # Buscar por email
            results = Client.search('b@test.com')
            assert len(results) == 1
            assert results[0].email == 'b@test.com'
            
            # Busca parcial
            results = Client.search('Client')
            assert len(results) == 3

class TestContract:
    """Testes do modelo Contract"""
    
    def test_create_contract(self, app, sample_user, sample_client):
        """Testa criação de contrato"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.add(sample_client)
            db.session.commit()
            
            contract = Contract(
                title='Test Contract',
                client_id=sample_client.id,
                value=10000.00,
                start_date=date.today(),
                end_date=date(2024, 12, 31),
                status='ativo',
                created_by=sample_user.id
            )
            
            db.session.add(contract)
            db.session.commit()
            
            assert contract.id is not None
            assert contract.title == 'Test Contract'
            assert contract.client_id == sample_client.id
            assert float(contract.value) == 10000.00
            assert contract.status == 'ativo'
            assert contract.created_by == sample_user.id
    
    def test_contract_properties(self, app, sample_user, sample_client, sample_contract):
        """Testa propriedades do contrato"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.add(sample_client)
            db.session.commit()
            
            sample_contract.client_id = sample_client.id
            sample_contract.created_by = sample_user.id
            db.session.add(sample_contract)
            db.session.commit()
            
            # Duração
            assert sample_contract.duration_days > 0
            
            # Status
            assert sample_contract.get_status_display() == 'Ativo'
            
            # Valor mensal
            assert sample_contract.monthly_value > 0
    
    def test_contract_expiration(self, app, sample_user, sample_client):
        """Testa verificação de expiração"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.add(sample_client)
            db.session.commit()
            
            # Contrato vencido
            expired_contract = Contract(
                title='Expired Contract',
                client_id=sample_client.id,
                value=1000.00,
                start_date=date(2023, 1, 1),
                end_date=date(2023, 12, 31),
                status='ativo',
                created_by=sample_user.id
            )
            
            # Contrato ativo
            active_contract = Contract(
                title='Active Contract',
                client_id=sample_client.id,
                value=1000.00,
                start_date=date.today(),
                end_date=date.today() + timedelta(days=365),
                status='ativo',
                created_by=sample_user.id
            )
            
            db.session.add(expired_contract)
            db.session.add(active_contract)
            db.session.commit()
            
            assert expired_contract.is_expired is True
            assert active_contract.is_expired is False
            
            # Contrato expirando em breve
            expiring_contract = Contract(
                title='Expiring Contract',
                client_id=sample_client.id,
                value=1000.00,
                start_date=date.today(),
                end_date=date.today() + timedelta(days=15),
                auto_renew=True,
                renewal_days=30,
                status='ativo',
                created_by=sample_user.id
            )
            
            db.session.add(expiring_contract)
            db.session.commit()
            
            assert expiring_contract.is_expiring_soon() is True
            assert expiring_contract.can_renew() is True
    
    def test_contract_status_changes(self, app, sample_user, sample_client):
        """Testa mudanças de status do contrato"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.add(sample_client)
            db.session.commit()
            
            contract = Contract(
                title='Test Contract',
                client_id=sample_client.id,
                value=1000.00,
                start_date=date.today(),
                end_date=date(2024, 12, 31),
                status='rascunho',
                created_by=sample_user.id
            )
            
            db.session.add(contract)
            db.session.commit()
            
            # Ativar contrato
            assert contract.activate() is True
            assert contract.status == 'ativo'
            assert contract.signature_date is not None
            
            # Tentar ativar novamente
            assert contract.activate() is False
            
            # Cancelar contrato
            contract.cancel('Test cancellation')
            assert contract.status == 'cancelado'
            assert 'Test cancellation' in contract.notes
    
    def test_contract_to_dict(self, app, sample_user, sample_client, sample_contract):
        """Testa conversão para dicionário"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.add(sample_client)
            db.session.commit()
            
            sample_contract.client_id = sample_client.id
            sample_contract.created_by = sample_user.id
            db.session.add(sample_contract)
            db.session.commit()
            
            contract_dict = sample_contract.to_dict()
            
            assert 'id' in contract_dict
            assert contract_dict['title'] == 'Contrato Teste'
            assert contract_dict['value'] == 25000.0
            assert 'client' in contract_dict
            assert contract_dict['duration_days'] > 0
            assert 'is_expired' in contract_dict
            assert 'monthly_value' in contract_dict

class TestNotification:
    """Testes do modelo Notification"""
    
    def test_create_notification(self, app, sample_user):
        """Testa criação de notificação"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.commit()
            
            notification = Notification(
                title='Test Notification',
                message='Test message',
                notification_type='info',
                user_id=sample_user.id
            )
            
            db.session.add(notification)
            db.session.commit()
            
            assert notification.id is not None
            assert notification.title == 'Test Notification'
            assert notification.user_id == sample_user.id
            assert notification.is_read is False
            assert notification.is_active is True
    
    def test_notification_read_status(self, app, sample_user, sample_notification):
        """Testa status de leitura"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.commit()
            
            sample_notification.user_id = sample_user.id
            db.session.add(sample_notification)
            db.session.commit()
            
            # Marcar como lida
            sample_notification.mark_as_read()
            assert sample_notification.is_read is True
            assert sample_notification.read_at is not None
            
            # Marcar como não lida
            sample_notification.mark_as_unread()
            assert sample_notification.is_read is False
            assert sample_notification.read_at is None
    
    def test_notification_to_dict(self, app, sample_user, sample_notification):
        """Testa conversão para dicionário"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.commit()
            
            sample_notification.user_id = sample_user.id
            db.session.add(sample_notification)
            db.session.commit()
            
            notification_dict = sample_notification.to_dict()
            
            assert 'id' in notification_dict
            assert notification_dict['title'] == 'Test Notification'
            assert notification_dict['notification_type'] == 'info'
            assert 'is_read' in notification_dict
            assert 'created_at' in notification_dict
    
    def test_contract_notifications(self, app, sample_user, sample_client):
        """Testa criação de notificações de contrato"""
        with app.app_context():
            db.session.add(sample_user)
            db.session.add(sample_client)
            db.session.commit()
            
            contract = Contract(
                title='Test Contract',
                client_id=sample_client.id,
                value=1000.00,
                start_date=date.today(),
                end_date=date.today() + timedelta(days=15),
                status='ativo',
                created_by=sample_user.id
            )
            
            db.session.add(contract)
            db.session.commit()
            
            # Criar notificação de vencimento
            notification = Notification.create_contract_notification(
                sample_user.id,
                contract,
                'warning',
                'Contrato expirando em breve'
            )
            
            assert notification.id is not None
            assert notification.category == 'contract'
            assert notification.action_url == f'/contracts/{contract.id}'
            assert notification.action_text == 'Ver Contrato'
