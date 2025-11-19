"""
Script de migração do banco de dados
Atualiza o schema existente para incluir clientes e relacionamentos
"""
import sqlite3
import os
from datetime import datetime, date, timedelta

def backup_database():
    """Cria backup do banco atual"""
    import shutil
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"instance/contratos_backup_{timestamp}.db"
    shutil.copy2("instance/contratos.db", backup_path)
    print(f"✅ Backup criado: {backup_path}")
    return backup_path

def migrate_database():
    """Realiza a migração do banco de dados"""
    print("🔧 Iniciando migração do banco de dados...")
    
    # Criar backup
    backup_path = backup_database()
    
    try:
        conn = sqlite3.connect("instance/contratos.db")
        cursor = conn.cursor()
        
        # 1. Criar tabela de clientes
        print("📋 Criando tabela de clientes...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(120) NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                phone VARCHAR(20),
                cnpj_cpf VARCHAR(20) UNIQUE NOT NULL,
                address TEXT,
                city VARCHAR(100),
                state VARCHAR(2),
                sector VARCHAR(50),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 2. Migrar dados da tabela contracts para o novo formato
        print("📄 Migrando tabela de contratos...")
        
        # Criar tabela temporária com novo schema
        cursor.execute("""
            CREATE TABLE contracts_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                contract_number VARCHAR(50) UNIQUE NOT NULL,
                description TEXT NOT NULL,
                value REAL NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                payment_method VARCHAR(50),
                payment_frequency VARCHAR(20),
                status VARCHAR(20) DEFAULT 'Ativo',
                renewal_date DATE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (id)
            )
        """)
        
        # Migrar dados existentes
        cursor.execute("SELECT * FROM contracts")
        old_contracts = cursor.fetchall()
        
        # Obter colunas da tabela antiga
        cursor.execute("PRAGMA table_info(contracts)")
        old_columns = [col[1] for col in cursor.fetchall()]
        
        # Criar clientes a partir dos contratos existentes
        client_map = {}
        client_id = 1
        
        for contract in old_contracts:
            contract_dict = dict(zip(old_columns, contract))
            client_name = contract_dict.get('client_name', f'Cliente {client_id}')
            
            if client_name not in client_map:
                # Criar cliente
                cursor.execute("""
                    INSERT INTO clients (name, email, cnpj_cpf, sector)
                    VALUES (?, ?, ?, ?)
                """, (
                    client_name,
                    f"cliente{client_id}@email.com",
                    f"{client_id:014}",  # CNPJ fictício
                    "Geral"
                ))
                client_map[client_name] = client_id
                client_id += 1
        
        # Migrar contratos para nova tabela
        for contract in old_contracts:
            contract_dict = dict(zip(old_columns, contract))
            client_name = contract_dict.get('client_name', f'Cliente {client_id}')
            
            # Gerar número do contrato se não existir
            contract_number = f"CTR-{datetime.now().year}-{contract_dict['id']:03d}"
            
            cursor.execute("""
                INSERT INTO contracts_new (
                    id, client_id, contract_number, description, value,
                    start_date, end_date, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contract_dict['id'],
                client_map[client_name],
                contract_number,
                f"Contrato migrado: {client_name}",
                contract_dict['value'],
                contract_dict['start_date'],
                contract_dict['end_date'],
                contract_dict['status'],
                contract_dict['created_at'],
                contract_dict['updated_at'] if contract_dict.get('updated_at') else contract_dict['created_at']
            ))
        
        # Substituir tabela antiga
        cursor.execute("DROP TABLE contracts")
        cursor.execute("ALTER TABLE contracts_new RENAME TO contracts")
        
        # 3. Atualizar tabela de notificações
        print("🔔 Atualizando tabela de notificações...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                contract_id INTEGER,
                title VARCHAR(200) NOT NULL,
                message VARCHAR(500) NOT NULL,
                type VARCHAR(20) DEFAULT 'info',
                is_read BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contract_id) REFERENCES contracts (id)
            )
        """)
        
        # Migrar notificações existentes
        cursor.execute("SELECT * FROM notifications")
        old_notifications = cursor.fetchall()
        
        if old_notifications:
            cursor.execute("PRAGMA table_info(notifications)")
            old_notif_columns = [col[1] for col in cursor.fetchall()]
            
            for notif in old_notifications:
                notif_dict = dict(zip(old_notif_columns, notif))
                
                cursor.execute("""
                    INSERT INTO notifications_new (
                        id, user_id, contract_id, title, message, type, is_read, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    notif_dict['id'],
                    notif_dict['user_id'],
                    notif_dict.get('contract_id'),
                    "Notificação migrada",
                    notif_dict['message'],
                    'info',
                    notif_dict['is_read'],
                    notif_dict['created_at']
                ))
        
        cursor.execute("DROP TABLE notifications")
        cursor.execute("ALTER TABLE notifications_new RENAME TO notifications")
        
        # 4. Criar dados de exemplo se o banco estiver vazio
        cursor.execute("SELECT COUNT(*) FROM clients")
        client_count = cursor.fetchone()[0]
        
        if client_count == 0:
            print("📝 Criando dados de exemplo...")
            create_sample_data(cursor)
        
        conn.commit()
        conn.close()
        
        print("✅ Migração concluída com sucesso!")
        print(f"📊 Resumo:")
        print(f"   - {len(client_map)} clientes criados")
        print(f"   - {len(old_contracts)} contratos migrados")
        print(f"   - {len(old_notifications)} notificações migradas")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante migração: {e}")
        print(f"🔄 Restaurando backup: {backup_path}")
        
        # Restaurar backup em caso de erro
        import shutil
        shutil.copy2(backup_path, "instance/contratos.db")
        return False

def create_sample_data(cursor):
    """Cria dados de exemplo para teste"""
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
    
    client_ids = []
    for client_data in clients_data:
        cursor.execute("""
            INSERT INTO clients (name, email, phone, cnpj_cpf, address, city, state, sector)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            client_data['name'], client_data['email'], client_data['phone'],
            client_data['cnpj_cpf'], client_data['address'], client_data['city'],
            client_data['state'], client_data['sector']
        ))
        client_ids.append(cursor.lastrowid)
    
    # Criar contratos de exemplo
    contracts_data = [
        {
            'client_id': client_ids[0],
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
            'client_id': client_ids[0],
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
            'client_id': client_ids[1],
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
            'client_id': client_ids[2],
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
    
    contract_ids = []
    for contract_data in contracts_data:
        cursor.execute("""
            INSERT INTO contracts (
                client_id, contract_number, description, value, start_date, end_date,
                payment_method, payment_frequency, status, renewal_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            contract_data['client_id'], contract_data['contract_number'],
            contract_data['description'], contract_data['value'],
            contract_data['start_date'], contract_data['end_date'],
            contract_data['payment_method'], contract_data['payment_frequency'],
            contract_data.get('status', 'Ativo'), contract_data['renewal_date']
        ))
        contract_ids.append(cursor.lastrowid)
    
    # Criar notificações de exemplo
    notifications_data = [
        {
            'user_id': 1,
            'contract_id': contract_ids[0],
            'title': 'Contrato próximo ao vencimento',
            'message': 'O contrato CTR-2024-001 vence em 30 dias',
            'type': 'warning'
        },
        {
            'user_id': 1,
            'contract_id': contract_ids[1],
            'title': 'Nova renovação disponível',
            'message': 'O contrato CTR-2024-002 pode ser renovado',
            'type': 'info'
        }
    ]
    
    for notif_data in notifications_data:
        cursor.execute("""
            INSERT INTO notifications (user_id, contract_id, title, message, type)
            VALUES (?, ?, ?, ?, ?)
        """, (
            notif_data['user_id'], notif_data['contract_id'],
            notif_data['title'], notif_data['message'], notif_data['type']
        ))

def verify_migration():
    """Verifica se a migração foi bem-sucedida"""
    try:
        conn = sqlite3.connect("instance/contratos.db")
        cursor = conn.cursor()
        
        # Verificar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['clients', 'contracts', 'notifications', 'users', 'chat_messages']
        
        print("\n🔍 Verificação da migração:")
        print(f"✅ Tabelas encontradas: {len(tables)}")
        
        for table in expected_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  📁 {table}: {count} registros")
            else:
                print(f"  ❌ {table}: não encontrada")
        
        # Verificar relacionamentos
        cursor.execute("""
            SELECT c.name, COUNT(co.id) as contract_count
            FROM clients c
            LEFT JOIN contracts co ON c.id = co.client_id
            GROUP BY c.id
            LIMIT 5
        """)
        
        client_contracts = cursor.fetchall()
        if client_contracts:
            print("\n📊 Relacionamentos cliente-contrato:")
            for client_name, count in client_contracts:
                print(f"  🤝 {client_name}: {count} contrato(s)")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Sistema de Migração de Banco de Dados")
    print("=" * 50)
    
    if not os.path.exists("instance/contratos.db"):
        print("❌ Banco de dados não encontrado!")
        print("Execute primeiro o aplicativo para criar o banco.")
    else:
        success = migrate_database()
        if success:
            verify_migration()
            print("\n✅ Migração concluída! Execute 'python gestao_clientes.py' para iniciar o sistema.")
        else:
            print("\n❌ Migração falhou! Verifique o erro acima.")
