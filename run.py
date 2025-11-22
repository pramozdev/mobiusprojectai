"""
Entry point da aplicação Flask
Modo de execução profissional com configuração de ambiente
"""

import os
from datetime import datetime, date
from app import create_app, db
from app.models import User, Client, Contract, Notification

def deploy():
    """Deployment da aplicação"""
    app = create_app(os.getenv('FLASK_ENV') or 'default')
    
    with app.app_context():
        # Criar banco de dados
        db.create_all()
        
        # Criar usuário administrador se não existir
        if User.query.filter_by(username='admin').first() is None:
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('✅ Usuário administrador criado')
        
        # Criar dados de exemplo se não existirem
        if Client.query.count() == 0:
            create_sample_data()
            print('✅ Dados de exemplo criados')
        
        print('🚀 Deploy concluído com sucesso!')

def create_sample_data():
    """Cria dados de exemplo para demonstração"""
    # Criar clientes
    clients = [
        Client(
            name='Tech Solutions Ltda',
            email='contato@techsolutions.com',
            phone='1134567890',
            document='12345678000195',
            address='Av. Paulista, 1000',
            city='São Paulo',
            state='SP',
            postal_code='01310200',
            created_by=1
        ),
        Client(
            name='Consultoria Empresarial S/A',
            email='info@consultoria.com',
            phone='2123456789',
            document='98765432000167',
            address='Rua Rio de Janeiro, 500',
            city='Rio de Janeiro',
            state='RJ',
            postal_code='20040030',
            created_by=1
        ),
        Client(
            name='Comércio Varejista ME',
            email='varejo@email.com',
            phone='3112345678',
            document='45678912000134',
            address='Rua Afonso Pena, 200',
            city='Belo Horizonte',
            state='MG',
            postal_code='30130000',
            created_by=1
        )
    ]
    
    for client in clients:
        db.session.add(client)
    
    db.session.commit()
    
    # Criar contratos
    contracts = [
        Contract(
            title='Desenvolvimento de Sistema ERP',
            description='Sistema completo de gestão empresarial',
            client_id=1,
            value=186000.00,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            status='ativo',
            contract_type='serviço',
            auto_renew=True,
            renewal_days=30,
            payment_method='transferência',
            payment_frequency='mensal',
            created_by=1
        ),
        Contract(
            title='Consultoria em Processos',
            description='Análise e otimização de processos de negócio',
            client_id=2,
            value=85000.00,
            start_date=date(2024, 2, 1),
            end_date=date(2024, 11, 30),
            status='ativo',
            contract_type='consultoria',
            auto_renew=False,
            renewal_days=60,
            payment_method='boleto',
            payment_frequency='trimestral',
            created_by=1
        ),
        Contract(
            title='Manutenção de Infraestrutura',
            description='Suporte técnico e manutenção de servidores',
            client_id=3,
            value=45000.00,
            start_date=date(2024, 3, 1),
            end_date=date(2024, 10, 31),
            status='concluído',
            contract_type='serviço',
            auto_renew=False,
            payment_method='transferência',
            payment_frequency='mensal',
            created_by=1
        ),
        Contract(
            title='Marketing Digital',
            description='Gestão de campanhas de marketing digital',
            client_id=1,
            value=25000.00,
            start_date=date(2024, 4, 1),
            end_date=date(2024, 9, 30),
            status='suspenso',
            contract_type='serviço',
            auto_renew=False,
            payment_method='cartão',
            payment_frequency='mensal',
            created_by=1
        )
    ]
    
    for contract in contracts:
        db.session.add(contract)
    
    db.session.commit()
    
    # Criar notificações
    notifications = [
        Notification(
            title='🎉 Bem-vindo ao Sistema!',
            message='Seja bem-vindo ao Sistema de Gestão de Contratos. Explore todas as funcionalidades disponíveis.',
            notification_type='success',
            category='system',
            user_id=1,
            action_url='/dashboard',
            action_text='Ver Dashboard'
        ),
        Notification(
            title='📊 Novos Contratos Ativos',
            message=f'Você possui {Contract.query.filter_by(status="ativo").count()} contratos ativos no sistema.',
            notification_type='info',
            category='contract',
            user_id=1,
            action_url='/contracts?status=ativo',
            action_text='Ver Contratos'
        ),
        Notification(
            title='⚠️ Contrato Expirando',
            message='O contrato "Desenvolvimento de Sistema ERP" está expirando em breve. Verifique as opções de renovação.',
            notification_type='warning',
            category='contract',
            user_id=1,
            action_url='/contracts/1',
            action_text='Ver Contrato'
        )
    ]
    
    for notification in notifications:
        db.session.add(notification)
    
    db.session.commit()

if __name__ == '__main__':
    # Determinar ambiente
    env = os.getenv('FLASK_ENV', 'development')
    
    # Criar aplicação
    app = create_app(env)
    
    # Validar configuração
    from config import validate_config
    issues = validate_config()
    
    if issues:
        print('⚠️ Problemas de configuração encontrados:')
        for issue in issues:
            print(f'  - {issue}')
        print()
    
    # Informações de inicialização
    print(f'🚀 Iniciando aplicação em modo {env.upper()}')
    print(f'📁 Database: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    print(f'🔐 Secret Key: {"✅ Configurada" if app.config["SECRET_KEY"] else "❌ Não configurada"}')
    print(f'🌐 CORS Origins: {app.config["CORS_ORIGINS"]}')
    print()
    
    # Deploy automático em desenvolvimento
    if env == 'development':
        with app.app_context():
            deploy()
    
    # Iniciar servidor
    try:
        app.run(
            host='0.0.0.0',
            port=int(os.getenv('PORT', 5000)),
            debug=app.config.get('DEBUG', False)
        )
    except KeyboardInterrupt:
        print('\n👋 Aplicação encerrada pelo usuário')
    except Exception as e:
        print(f'❌ Erro ao iniciar aplicação: {e}')
        exit(1)
