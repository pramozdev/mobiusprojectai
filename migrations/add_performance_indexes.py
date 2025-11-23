"""
Add database indexes for frequently queried fields to improve performance
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import Client, Contract, Notification

def add_performance_indexes():
    """Add indexes to improve query performance"""
    
    app = create_app()
    
    with app.app_context():
        # Indexes for Client table
        client_indexes = [
            "CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email)",
            "CREATE INDEX IF NOT EXISTS idx_clients_is_active ON clients(is_active)",
            "CREATE INDEX IF NOT EXISTS idx_clients_created_at ON clients(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_clients_name ON clients(name)",
        ]
        
        # Indexes for Contract table
        contract_indexes = [
            "CREATE INDEX IF NOT EXISTS idx_contracts_status ON contracts(status)",
            "CREATE INDEX IF NOT EXISTS idx_contracts_client_id ON contracts(client_id)",
            "CREATE INDEX IF NOT EXISTS idx_contracts_end_date ON contracts(end_date)",
            "CREATE INDEX IF NOT EXISTS idx_contracts_start_date ON contracts(start_date)",
            "CREATE INDEX IF NOT EXISTS idx_contracts_created_at ON contracts(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_contracts_auto_renew ON contracts(auto_renew)",
            "CREATE INDEX IF NOT EXISTS idx_contracts_value ON contracts(value)",
            # Composite indexes for common query patterns
            "CREATE INDEX IF NOT EXISTS idx_contracts_status_end_date ON contracts(status, end_date)",
            "CREATE INDEX IF NOT EXISTS idx_contracts_client_status ON contracts(client_id, status)",
        ]
        
        # Indexes for Notification table
        notification_indexes = [
            "CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read)",
            "CREATE INDEX IF NOT EXISTS idx_notifications_user_read ON notifications(user_id, is_read)",
            "CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at)",
        ]
        
        all_indexes = client_indexes + contract_indexes + notification_indexes
        
        print("Adicionando índices de performance...")
        for index_sql in all_indexes:
            try:
                from app import db
                db.session.execute(index_sql)
                print(f"✓ Criado: {index_sql}")
            except Exception as e:
                print(f"✗ Erro ao criar índice: {e}")
        
        try:
            from app import db
            db.session.commit()
            print("Todos os índices criados com sucesso!")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao commitar índices: {e}")

if __name__ == "__main__":
    add_performance_indexes()
