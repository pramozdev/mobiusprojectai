"""
Script para verificar o status do banco de dados
"""
import sqlite3
import os
from datetime import datetime

def verificar_banco_dados():
    """Verifica o status completo do banco de dados"""
    db_path = "instance/contratos.db"
    
    print("🔍 Verificando status do banco de dados")
    print("=" * 50)
    
    # 1. Verifica se o arquivo existe
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado em: {db_path}")
        return
    
    print(f"✅ Banco de dados encontrado: {db_path}")
    
    # 2. Verifica tamanho do arquivo
    size = os.path.getsize(db_path)
    print(f"📏 Tamanho: {size} bytes ({size/1024:.2f} KB)")
    
    try:
        # 3. Conecta ao banco
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 4. Lista todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📋 Tabelas encontradas ({len(tables)}):")
        for table in tables:
            table_name = table[0]
            print(f"\n  📁 {table_name}")
            
            # Conta registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"     Registros: {count}")
            
            # Mostra estrutura da tabela
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"     Colunas: {len(columns)}")
            
            # Mostra alguns dados se houver registros
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                rows = cursor.fetchall()
                print(f"     Amostra de dados:")
                for i, row in enumerate(rows, 1):
                    print(f"       {i}: {row}")
        
        # 5. Verifica integridade
        cursor.execute("PRAGMA integrity_check")
        integrity = cursor.fetchone()[0]
        print(f"\n🔒 Integridade: {integrity}")
        
        # 6. Estatísticas detalhadas
        print(f"\n📊 Estatísticas detalhadas:")
        
        # Users
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        print(f"  👥 Usuários: {users_count}")
        
        # Contracts
        cursor.execute("SELECT COUNT(*) FROM contracts")
        contracts_count = cursor.fetchone()[0]
        print(f"  📄 Contratos: {contracts_count}")
        
        if contracts_count > 0:
            cursor.execute("SELECT SUM(value) FROM contracts")
            total_value = cursor.fetchone()[0] or 0
            print(f"  💰 Valor total: R$ {total_value:,.2f}")
            
            cursor.execute("SELECT status, COUNT(*) FROM contracts GROUP BY status")
            status_counts = cursor.fetchall()
            print(f"  📈 Status dos contratos:")
            for status, count in status_counts:
                print(f"     {status}: {count}")
        
        # Notifications
        cursor.execute("SELECT COUNT(*) FROM notifications")
        notifications_count = cursor.fetchone()[0]
        print(f"  🔔 Notificações: {notifications_count}")
        
        # Chat Messages
        cursor.execute("SELECT COUNT(*) FROM chat_messages")
        chat_count = cursor.fetchone()[0]
        print(f"  💬 Mensagens de chat: {chat_count}")
        
        # 7. Verifica dados recentes
        print(f"\n🕐 Atividades recentes:")
        
        # Contratos recentes
        cursor.execute("""
            SELECT client_name, created_at 
            FROM contracts 
            ORDER BY created_at DESC 
            LIMIT 3
        """)
        recent_contracts = cursor.fetchall()
        if recent_contracts:
            print(f"  📄 Contratos recentes:")
            for name, date in recent_contracts:
                print(f"     {name} - {date}")
        
        # Mensagens recentes
        cursor.execute("""
            SELECT message, created_at 
            FROM chat_messages 
            ORDER BY created_at DESC 
            LIMIT 3
        """)
        recent_messages = cursor.fetchall()
        if recent_messages:
            print(f"  💬 Mensagens recentes:")
            for msg, date in recent_messages:
                msg_preview = msg[:30] + "..." if len(msg) > 30 else msg
                print(f"     {msg_preview} - {date}")
        
        conn.close()
        
        print(f"\n✅ Verificação concluída com sucesso!")
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao acessar banco de dados: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def criar_backup():
    """Cria um backup do banco de dados"""
    import shutil
    from datetime import datetime
    
    db_path = "instance/contratos.db"
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"instance/contratos_backup_{timestamp}.db"
        shutil.copy2(db_path, backup_path)
        print(f"🗄️ Backup criado: {backup_path}")
        return backup_path
    else:
        print("❌ Banco de dados não encontrado para backup")
        return None

def otimizar_banco():
    """Otimiza o banco de dados"""
    try:
        conn = sqlite3.connect("instance/contratos.db")
        cursor = conn.cursor()
        
        # Analisa o banco
        cursor.execute("ANALYZE")
        print("📊 Análise do banco concluída")
        
        # Vacuum para otimizar espaço
        cursor.execute("VACUUM")
        print("🧹 Otimização (VACUUM) concluída")
        
        conn.close()
        print("✅ Banco otimizado com sucesso!")
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao otimizar banco: {e}")

if __name__ == "__main__":
    verificar_banco_dados()
    
    print("\n" + "=" * 50)
    print("🔧 Opções adicionais:")
    print("1. Criar backup")
    print("2. Otimizar banco")
    print("3. Sair")
    
    while True:
        try:
            choice = input("\nEscolha uma opção (1-3): ").strip()
            
            if choice == "1":
                criar_backup()
            elif choice == "2":
                otimizar_banco()
            elif choice == "3":
                break
            else:
                print("❌ Opção inválida")
        except KeyboardInterrupt:
            print("\n👋 Encerrando...")
            break
