#!/usr/bin/env python3
"""
Script para popular o banco com dados fictícios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Client, Contract, Notification
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Cria dados fictícios para demonstração"""
    app = create_app()
    
    with app.app_context():
        print("🌱 Criando dados fictícios...")
        
        # Limpar dados existentes (opcional)
        # Contract.query.delete()
        # Client.query.delete()
        # Notification.query.delete()
        # db.session.commit()
        
        # Clientes fictícios
        clients_data = [
            {
                "name": "Tech Solutions Ltda",
                "email": "contato@techsolutions.com.br",
                "phone": "(11) 3456-7890",
                "document": "12.345.678/0001-90",
                "address": "Av. Paulista, 1000",
                "city": "São Paulo",
                "state": "SP",
                "postal_code": "01310-100",
                "is_active": True
            },
            {
                "name": "Digital Marketing Agency",
                "email": "hello@digitalagency.com",
                "phone": "(21) 2345-6789",
                "document": "45.678.901/0002-34",
                "address": "Rua das Flores, 500",
                "city": "Rio de Janeiro",
                "state": "RJ",
                "postal_code": "20040-020",
                "is_active": True
            },
            {
                "name": "E-commerce Brasil",
                "email": "suporte@ecommercebrasil.com",
                "phone": "(31) 98765-4321",
                "document": "78.901.234/0003-56",
                "address": "Rua Afonso Pena, 2000",
                "city": "Belo Horizonte",
                "state": "MG",
                "postal_code": "30130-007",
                "is_active": True
            },
            {
                "name": "FinTech Innovations",
                "email": "business@fintech.io",
                "phone": "(41) 3456-7890",
                "document": "23.456.789/0004-78",
                "address": "Rua XV de Novembro, 1500",
                "city": "Curitiba",
                "state": "PR",
                "postal_code": "80010-000",
                "is_active": True
            },
            {
                "name": "HealthCare Plus",
                "email": "contato@healthcareplus.com.br",
                "phone": "(51) 2345-6789",
                "document": "56.789.012/0005-90",
                "address": "Av. Osvaldo Aranha, 800",
                "city": "Porto Alegre",
                "state": "RS",
                "postal_code": "90035-190",
                "is_active": True
            },
            {
                "name": "EduTech Solutions",
                "email": "info@edutech.com",
                "phone": "(62) 3456-7890",
                "document": "89.012.345/0006-12",
                "address": "Rua 26, 1500",
                "city": "Goiânia",
                "state": "GO",
                "postal_code": "74010-150",
                "is_active": True
            },
            {
                "name": "Logistics Express",
                "email": "ops@logisticsexpress.com.br",
                "phone": "(81) 2345-6789",
                "document": "34.567.890/0007-34",
                "address": "Av. Agamenon Magalhães, 2000",
                "city": "Recife",
                "state": "PE",
                "postal_code": "50070-000",
                "is_active": True
            },
            {
                "name": "Green Energy Corp",
                "email": "contact@greenenergy.com",
                "phone": "(48) 3456-7890",
                "document": "67.890.123/0008-56",
                "address": "Rua Tenente Silveira, 300",
                "city": "Florianópolis",
                "state": "SC",
                "postal_code": "88010-300",
                "is_active": True
            },
            {
                "name": "Retail Max",
                "email": "comercial@retailmax.com.br",
                "phone": "(85) 2345-6789",
                "document": "90.123.456/0009-78",
                "address": "Av. Santos Dumont, 3000",
                "city": "Fortaleza",
                "state": "CE",
                "postal_code": "60020-061",
                "is_active": True
            },
            {
                "name": "Cloud Services Inc",
                "email": "sales@cloudservices.io",
                "phone": "(92) 3456-7890",
                "document": "12.345.678/0010-90",
                "address": "Rua Eduardo Ribeiro, 500",
                "city": "Manaus",
                "state": "AM",
                "postal_code": "69010-150",
                "is_active": True
            }
        ]
        
        # Criar clientes
        created_clients = []
        for client_data in clients_data:
            # Verificar se cliente já existe
            existing = Client.query.filter_by(email=client_data["email"]).first()
            if not existing:
                client = Client(
                    created_by=1,
                    **client_data
                )
                db.session.add(client)
                created_clients.append(client)
                print(f"  ✅ Cliente criado: {client_data['name']}")
            else:
                created_clients.append(existing)
                print(f"  ⏭️  Cliente já existe: {client_data['name']}")
        
        db.session.commit()
        
        # Contratos fictícios
        contracts_data = [
            # Tech Solutions Ltda - 4 contratos
            {
                "client_index": 0,
                "title": "Desenvolvimento de Software Customizado",
                "description": "Sistema ERP completo para gestão empresarial",
                "value": 150000.00,
                "status": "ativo",
                "contract_type": "serviço",
                "start_date": datetime.now() - timedelta(days=365),
                "end_date": datetime.now() + timedelta(days=30),
                "contract_number": "TS-2024-001"
            },
            {
                "client_index": 0,
                "title": "Manutenção e Suporte Técnico",
                "description": "Suporte 24/7 para sistemas críticos",
                "value": 25000.00,
                "status": "ativo",
                "contract_type": "serviço",
                "start_date": datetime.now() - timedelta(days=180),
                "end_date": datetime.now() + timedelta(days=185),
                "contract_number": "TS-2024-002"
            },
            {
                "client_index": 0,
                "title": "Consultoria em Cloud Computing",
                "description": "Migração para AWS e otimização",
                "value": 45000.00,
                "status": "ativo",
                "contract_type": "consultoria",
                "start_date": datetime.now() - timedelta(days=90),
                "end_date": datetime.now() + timedelta(days=275),
                "contract_number": "TS-2024-003"
            },
            {
                "client_index": 0,
                "title": "Treinamento Técnico Avançado",
                "description": "Capacitação equipe de desenvolvimento",
                "value": 15000.00,
                "status": "concluído",
                "contract_type": "serviço",
                "start_date": datetime.now() - timedelta(days=200),
                "end_date": datetime.now() - timedelta(days=50),
                "contract_number": "TS-2024-004"
            },
            # Digital Marketing Agency - 3 contratos
            {
                "client_index": 1,
                "title": "Gestão de Tráfego Pago",
                "description": "Campanhas Google Ads e Facebook Ads",
                "value": 35000.00,
                "status": "ativo",
                "contract_type": "serviço",
                "start_date": datetime.now() - timedelta(days=120),
                "end_date": datetime.now() + timedelta(days=245),
                "contract_number": "DMA-2024-001"
            },
            {
                "client_index": 1,
                "title": "SEO e Conteúdo",
                "description": "Otimização para buscadores e produção de conteúdo",
                "value": 20000.00,
                "status": "ativo",
                "contract_type": "serviço",
                "start_date": datetime.now() - timedelta(days=60),
                "end_date": datetime.now() + timedelta(days=305),
                "contract_number": "DMA-2024-002"
            },
            {
                "client_index": 1,
                "title": "E-mail Marketing",
                "description": "Automação de campanhas de e-mail",
                "value": 12000.00,
                "status": "rascunho",
                "contract_type": "serviço",
                "start_date": datetime.now() + timedelta(days=30),
                "end_date": datetime.now() + timedelta(days=395),
                "contract_number": "DMA-2024-003"
            },
            # E-commerce Brasil - 3 contratos
            {
                "client_index": 2,
                "title": "Plataforma E-commerce",
                "description": "Desenvolvimento de loja virtual completa",
                "value": 80000.00,
                "status": "ativo",
                "contract_type": "projeto",
                "start_date": datetime.now() - timedelta(days=300),
                "end_date": datetime.now() + timedelta(days=65),
                "contract_number": "ECB-2024-001"
            },
            {
                "client_index": 2,
                "title": "Integração com Marketplaces",
                "description": "Conexão com Mercado Livre, Amazon, etc",
                "value": 25000.00,
                "status": "ativo",
                "contract_type": "projeto",
                "start_date": datetime.now() - timedelta(days=150),
                "end_date": datetime.now() + timedelta(days=215),
                "contract_number": "ECB-2024-002"
            },
            {
                "client_index": 2,
                "title": "Análise de Dados e BI",
                "description": "Dashboard e relatórios personalizados",
                "value": 30000.00,
                "status": "suspenso",
                "contract_type": "consultoria",
                "start_date": datetime.now() - timedelta(days=90),
                "end_date": datetime.now() + timedelta(days=90),
                "contract_number": "ECB-2024-003"
            },
            # FinTech Innovations - 2 contratos
            {
                "client_index": 3,
                "title": "Aplicativo Mobile Banking",
                "description": "Desenvolvimento app iOS e Android",
                "value": 200000.00,
                "status": "ativo",
                "contract_type": "projeto",
                "start_date": datetime.now() - timedelta(days=240),
                "end_date": datetime.now() + timedelta(days=125),
                "contract_number": "FTI-2024-001"
            },
            {
                "client_index": 3,
                "title": "Segurança da Informação",
                "description": "Auditoria e implementação de segurança",
                "value": 40000.00,
                "status": "ativo",
                "contract_type": "consultoria",
                "start_date": datetime.now() - timedelta(days=45),
                "end_date": datetime.now() + timedelta(days=320),
                "contract_number": "FTI-2024-002"
            },
            # HealthCare Plus - 3 contratos
            {
                "client_index": 4,
                "title": "Sistema de Prontuário Eletrônico",
                "description": "Software para gestão de clínicas médicas",
                "value": 120000.00,
                "status": "ativo",
                "contract_type": "projeto",
                "start_date": datetime.now() - timedelta(days=180),
                "end_date": datetime.now() + timedelta(days=185),
                "contract_number": "HCP-2024-001"
            },
            {
                "client_index": 4,
                "title": "Telemedicina Platform",
                "description": "Plataforma de consultas online",
                "value": 60000.00,
                "status": "rascunho",
                "contract_type": "projeto",
                "start_date": datetime.now() + timedelta(days=60),
                "end_date": datetime.now() + timedelta(days=425),
                "contract_number": "HCP-2024-002"
            },
            {
                "client_index": 4,
                "title": "Integração com Planos de Saúde",
                "description": "Conexão com operadoras de saúde",
                "value": 35000.00,
                "status": "ativo",
                "contract_type": "serviço",
                "start_date": datetime.now() - timedelta(days=30),
                "end_date": datetime.now() + timedelta(days=335),
                "contract_number": "HCP-2024-003"
            },
            # EduTech Solutions - 2 contratos
            {
                "client_index": 5,
                "title": "Plataforma EAD",
                "description": "Sistema de ensino a distância completo",
                "value": 90000.00,
                "status": "ativo",
                "contract_type": "projeto",
                "start_date": datetime.now() - timedelta(days=270),
                "end_date": datetime.now() + timedelta(days=95),
                "contract_number": "EDT-2024-001"
            },
            {
                "client_index": 5,
                "title": "Gamificação e Engajamento",
                "description": "Sistema de pontos e recompensas",
                "value": 25000.00,
                "status": "ativo",
                "contract_type": "serviço",
                "start_date": datetime.now() - timedelta(days=90),
                "end_date": datetime.now() + timedelta(days=275),
                "contract_number": "EDT-2024-002"
            }
        ]
        
        # Criar contratos
        created_contracts = []
        for contract_data in contracts_data:
            client = created_clients[contract_data["client_index"]]
            
            # Verificar se contrato já existe
            existing = Contract.query.filter_by(contract_number=contract_data["contract_number"]).first()
            if not existing:
                contract = Contract(
                    client_id=client.id,
                    created_by=1,
                    **{k: v for k, v in contract_data.items() if k != "client_index"}
                )
                db.session.add(contract)
                created_contracts.append(contract)
                print(f"  ✅ Contrato criado: {contract_data['contract_number']} - {contract_data['title']}")
            else:
                created_contracts.append(existing)
                print(f"  ⏭️  Contrato já existe: {contract_data['contract_number']}")
        
        db.session.commit()
        
        # Notificações fictícias
        notifications_data = [
            {
                "title": "Novo contrato assinado",
                "message": "Tech Solutions Ltda assinou novo contrato de Desenvolvimento de Software",
                "notification_type": "success",
                "category": "contract",
                "action_url": f"/contracts/{created_contracts[0].id}" if created_contracts else None,
                "action_text": "Ver Contrato"
            },
            {
                "title": "Contrato próximo ao vencimento",
                "message": "Contrato TS-2024-001 vence em 30 dias",
                "notification_type": "warning",
                "category": "contract",
                "action_url": f"/contracts/{created_contracts[0].id}" if created_contracts else None,
                "action_text": "Ver Detalhes"
            },
            {
                "title": "Oportunidade de upsell",
                "message": "Digital Marketing Agency tem potencial para upgrade de plano",
                "notification_type": "info",
                "category": "client",
                "action_url": f"/clients/{created_clients[1].id}" if created_clients else None,
                "action_text": "Ver Cliente"
            },
            {
                "title": "Relatório mensal disponível",
                "message": "Relatório de performance de contratos já está disponível",
                "notification_type": "info",
                "category": "system",
                "action_url": "/analytics",
                "action_text": "Ver Analytics"
            },
            {
                "title": "Contrato em risco",
                "message": "E-commerce Brasil - Contrato ECB-2024-003 está suspenso",
                "notification_type": "error",
                "category": "contract",
                "action_url": f"/contracts/{created_contracts[9].id}" if len(created_contracts) > 9 else None,
                "action_text": "Ver Contrato"
            }
        ]
        
        # Criar notificações
        for notif_data in notifications_data:
            # Verificar se notificação já existe
            existing = Notification.query.filter_by(title=notif_data["title"]).first()
            if not existing:
                notification = Notification(
                    user_id=1,
                    **notif_data
                )
                db.session.add(notification)
                print(f"  ✅ Notificação criada: {notif_data['title']}")
            else:
                print(f"  ⏭️  Notificação já existe: {notif_data['title']}")
        
        db.session.commit()
        
        print("\n🎉 Dados fictícios criados com sucesso!")
        print(f"📊 Total: {len(created_clients)} clientes, {len(created_contracts)} contratos, {len(notifications_data)} notificações")

if __name__ == "__main__":
    create_sample_data()
