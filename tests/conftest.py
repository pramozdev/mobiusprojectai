"""
Configuração de testes com pytest
Fixtures e configurações compartilhadas
"""

import pytest
import tempfile
import os
from datetime import datetime, date
from flask import Flask

from app import create_app, db
from app.models import User, Client, Contract, Notification

@pytest.fixture(scope='session')
def app():
    """Cria aplicação de teste"""
    # Criar banco de dados temporário
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope='session')
def client(app):
    """Cliente de teste"""
    return app.test_client()

@pytest.fixture(scope='session')
def runner(app):
    """CLI runner de teste"""
    return app.test_cli_runner()

@pytest.fixture
def auth_headers(client):
    """Headers de autenticação"""
    # Criar usuário de teste
    user = User(username='testuser', email='test@example.com')
    user.set_password('testpass')
    db.session.add(user)
    db.session.commit()
    
    # Login
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    
    token = response.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def sample_user():
    """Usuário de exemplo"""
    user = User(
        username='testuser',
        email='test@example.com',
        is_admin=True
    )
    user.set_password('testpass')
    return user

@pytest.fixture
def sample_client():
    """Cliente de exemplo"""
    return Client(
        name='Cliente Teste',
        email='cliente@teste.com',
        phone='11999999999',
        document='12345678901',
        address='Rua Teste, 123',
        city='São Paulo',
        state='SP',
        postal_code='01234567',
        created_by=1
    )

@pytest.fixture
def sample_contract():
    """Contrato de exemplo"""
    return Contract(
        title='Contrato Teste',
        description='Descrição do contrato teste',
        client_id=1,
        value=10000.00,
        start_date=date.today(),
        end_date=date(2024, 12, 31),
        status='ativo',
        contract_type='serviço',
        created_by=1
    )

@pytest.fixture
def sample_notification():
    """Notificação de exemplo"""
    return Notification(
        title='Test Notification',
        message='Test message',
        notification_type='info',
        user_id=1
    )

@pytest.fixture
def populated_db(app):
    """Banco de dados populado com dados de teste"""
    with app.app_context():
        # Criar usuário
        user = User(
            username='admin',
            email='admin@test.com',
            is_admin=True
        )
        user.set_password('admin123')
        db.session.add(user)
        
        # Criar clientes
        clients = [
            Client(
                name='Cliente A',
                email='clienta@test.com',
                created_by=1
            ),
            Client(
                name='Cliente B',
                email='clientb@test.com',
                created_by=1
            ),
            Client(
                name='Cliente C',
                email='clientc@test.com',
                created_by=1
            )
        ]
        
        for client in clients:
            db.session.add(client)
        
        db.session.commit()
        
        # Criar contratos
        contracts = [
            Contract(
                title='Contrato A',
                client_id=1,
                value=5000.00,
                start_date=date(2024, 1, 1),
                end_date=date(2024, 12, 31),
                status='ativo',
                created_by=1
            ),
            Contract(
                title='Contrato B',
                client_id=2,
                value=7500.00,
                start_date=date(2024, 2, 1),
                end_date=date(2024, 11, 30),
                status='ativo',
                created_by=1
            ),
            Contract(
                title='Contrato C',
                client_id=3,
                value=3000.00,
                start_date=date(2024, 3, 1),
                end_date=date(2024, 10, 31),
                status='concluído',
                created_by=1
            )
        ]
        
        for contract in contracts:
            db.session.add(contract)
        
        db.session.commit()
        
        # Criar notificações
        notifications = [
            Notification(
                title='Bem-vindo!',
                message='Bem-vindo ao sistema',
                notification_type='info',
                user_id=1
            ),
            Notification(
                title='Contrato expirando',
                message='Um contrato está expirando em breve',
                notification_type='warning',
                user_id=1
            )
        ]
        
        for notification in notifications:
            db.session.add(notification)
        
        db.session.commit()
        
        yield db

@pytest.fixture
def mock_openai(mocker):
    """Mock da API OpenAI"""
    mock_response = {
        'choices': [{
            'message': {
                'content': 'Resposta simulada da OpenAI'
            }
        }]
    }
    
    mocker.patch('openai.ChatCompletion.create', return_value=mock_response)
    return mock_response

# Helpers para testes
def login_user(client, username='testuser', password='testpass'):
    """Faz login de usuário de teste"""
    response = client.post('/login', data={
        'username': username,
        'password': password
    })
    return response

def logout_user(client):
    """Faz logout de usuário de teste"""
    return client.get('/logout')

def create_test_user(db, username='testuser', email='test@example.com'):
    """Cria usuário de teste no banco"""
    user = User(username=username, email=email)
    user.set_password('testpass')
    db.session.add(user)
    db.session.commit()
    return user

def create_test_client(db, name='Test Client', user_id=1):
    """Cria cliente de teste no banco"""
    client = Client(
        name=name,
        email=f'{name.lower().replace(" ", "")}@test.com',
        created_by=user_id
    )
    db.session.add(client)
    db.session.commit()
    return client

def create_test_contract(db, title='Test Contract', client_id=1, user_id=1):
    """Cria contrato de teste no banco"""
    contract = Contract(
        title=title,
        client_id=client_id,
        value=1000.00,
        start_date=date.today(),
        end_date=date(2024, 12, 31),
        status='ativo',
        created_by=user_id
    )
    db.session.add(contract)
    db.session.commit()
    return contract

# Asserts customizados
def assert_valid_client(client_data):
    """Verifica se dados do cliente são válidos"""
    assert 'name' in client_data
    assert 'email' in client_data
    assert isinstance(client_data['name'], str)
    assert len(client_data['name']) > 0

def assert_valid_contract(contract_data):
    """Verifica se dados do contrato são válidos"""
    required_fields = ['title', 'client_id', 'value', 'start_date', 'end_date', 'status']
    for field in required_fields:
        assert field in contract_data
    
    assert isinstance(contract_data['value'], (int, float))
    assert contract_data['value'] > 0
    assert contract_data['status'] in ['rascunho', 'ativo', 'suspenso', 'concluído', 'cancelado']

def assert_valid_notification(notification_data):
    """Verifica se dados da notificação são válidos"""
    required_fields = ['title', 'message', 'notification_type', 'user_id']
    for field in required_fields:
        assert field in notification_data
    
    assert notification_data['notification_type'] in ['info', 'warning', 'error', 'success']
    assert isinstance(notification_data['user_id'], int)
    assert notification_data['user_id'] > 0
