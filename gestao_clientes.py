"""
Sistema completo de gestão de clientes e contratos
API endpoints para CRUD completo
"""
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, date, timedelta
import os
from models_atualizado import db, Client, Contract, Notification, init_db, create_sample_data

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "contratos.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ==================== CLIENTES ====================

@app.route('/api/clients', methods=['GET'])
def get_clients():
    """Lista todos os clientes"""
    try:
        clients = Client.query.all()
        return jsonify({
            'success': True,
            'data': [client.to_dict() for client in clients],
            'total': len(clients)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    """Busca cliente específico"""
    try:
        client = Client.query.get_or_404(client_id)
        return jsonify({
            'success': True,
            'data': client.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clients', methods=['POST'])
def create_client():
    """Cria novo cliente"""
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('name') or not data.get('email') or not data.get('cnpj_cpf'):
            return jsonify({
                'success': False,
                'error': 'Campos obrigatórios: name, email, cnpj_cpf'
            }), 400
        
        # Verifica se email já existe
        if Client.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'error': 'Email já cadastrado'
            }), 400
        
        # Verifica se CNPJ/CPF já existe
        if Client.query.filter_by(cnpj_cpf=data['cnpj_cpf']).first():
            return jsonify({
                'success': False,
                'error': 'CNPJ/CPF já cadastrado'
            }), 400
        
        client = Client(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            cnpj_cpf=data['cnpj_cpf'],
            address=data.get('address', ''),
            city=data.get('city', ''),
            state=data.get('state', ''),
            sector=data.get('sector', '')
        )
        
        db.session.add(client)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente criado com sucesso',
            'data': client.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    """Atualiza cliente existente"""
    try:
        client = Client.query.get_or_404(client_id)
        data = request.get_json()
        
        # Validações
        if 'email' in data and data['email'] != client.email:
            if Client.query.filter_by(email=data['email']).first():
                return jsonify({
                    'success': False,
                    'error': 'Email já cadastrado'
                }), 400
        
        if 'cnpj_cpf' in data and data['cnpj_cpf'] != client.cnpj_cpf:
            if Client.query.filter_by(cnpj_cpf=data['cnpj_cpf']).first():
                return jsonify({
                    'success': False,
                    'error': 'CNPJ/CPF já cadastrado'
                }), 400
        
        # Atualiza campos
        for field in ['name', 'email', 'phone', 'cnpj_cpf', 'address', 'city', 'state', 'sector']:
            if field in data:
                setattr(client, field, data[field])
        
        client.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente atualizado com sucesso',
            'data': client.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    """Exclui cliente (e seus contratos)"""
    try:
        client = Client.query.get_or_404(client_id)
        
        # Verifica se há contratos ativos
        active_contracts = [c for c in client.contracts if c.status == 'Ativo']
        if active_contracts:
            return jsonify({
                'success': False,
                'error': f'Cliente possui {len(active_contracts)} contrato(s) ativo(s). Não é possível excluir.'
            }), 400
        
        db.session.delete(client)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente excluído com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clients/search', methods=['GET'])
def search_clients():
    """Busca clientes por nome, email ou CNPJ/CPF"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'success': False, 'error': 'Informe um termo de busca'}), 400
        
        clients = Client.query.filter(
            db.or_(
                Client.name.contains(query),
                Client.email.contains(query),
                Client.cnpj_cpf.contains(query)
            )
        ).all()
        
        return jsonify({
            'success': True,
            'data': [client.to_dict() for client in clients],
            'total': len(clients),
            'query': query
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== CONTRATOS ====================

@app.route('/api/contracts', methods=['GET'])
def get_contracts():
    """Lista todos os contratos"""
    try:
        contracts = Contract.query.all()
        return jsonify({
            'success': True,
            'data': [contract.to_dict() for contract in contracts],
            'total': len(contracts)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/contracts/<int:contract_id>', methods=['GET'])
def get_contract(contract_id):
    """Busca contrato específico"""
    try:
        contract = Contract.query.get_or_404(contract_id)
        return jsonify({
            'success': True,
            'data': contract.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/contracts', methods=['POST'])
def create_contract():
    """Cria novo contrato"""
    try:
        data = request.get_json()
        
        # Validações
        required_fields = ['client_id', 'contract_number', 'description', 'value', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Campo obrigatório: {field}'
                }), 400
        
        # Verifica se cliente existe
        client = Client.query.get(data['client_id'])
        if not client:
            return jsonify({
                'success': False,
                'error': 'Cliente não encontrado'
            }), 400
        
        # Verifica se número do contrato já existe
        if Contract.query.filter_by(contract_number=data['contract_number']).first():
            return jsonify({
                'success': False,
                'error': 'Número de contrato já existe'
            }), 400
        
        # Converte datas
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        if start_date >= end_date:
            return jsonify({
                'success': False,
                'error': 'Data de início deve ser anterior à data de término'
            }), 400
        
        renewal_date = None
        if data.get('renewal_date'):
            renewal_date = datetime.strptime(data['renewal_date'], '%Y-%m-%d').date()
        
        contract = Contract(
            client_id=data['client_id'],
            contract_number=data['contract_number'],
            description=data['description'],
            value=float(data['value']),
            start_date=start_date,
            end_date=end_date,
            payment_method=data.get('payment_method', ''),
            payment_frequency=data.get('payment_frequency', ''),
            renewal_date=renewal_date,
            status=data.get('status', 'Ativo')
        )
        
        db.session.add(contract)
        db.session.commit()
        
        # Cria notificação para novo contrato
        notification = Notification(
            user_id=1,  # Assumindo usuário admin
            contract_id=contract.id,
            title='Novo contrato criado',
            message=f'Contrato {contract.contract_number} criado para {client.name}',
            type='success'
        )
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Contrato criado com sucesso',
            'data': contract.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'success': False, 'error': f'Erro de formato: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/contracts/<int:contract_id>', methods=['PUT'])
def update_contract(contract_id):
    """Atualiza contrato existente"""
    try:
        contract = Contract.query.get_or_404(contract_id)
        data = request.get_json()
        
        # Validações
        if 'contract_number' in data and data['contract_number'] != contract.contract_number:
            if Contract.query.filter_by(contract_number=data['contract_number']).first():
                return jsonify({
                    'success': False,
                    'error': 'Número de contrato já existe'
                }), 400
        
        if 'client_id' in data:
            client = Client.query.get(data['client_id'])
            if not client:
                return jsonify({
                    'success': False,
                    'error': 'Cliente não encontrado'
                }), 400
        
        # Atualiza datas se fornecidas
        if 'start_date' in data:
            contract.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        
        if 'end_date' in data:
            contract.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        if 'renewal_date' in data and data['renewal_date']:
            contract.renewal_date = datetime.strptime(data['renewal_date'], '%Y-%m-%d').date()
        elif 'renewal_date' in data and not data['renewal_date']:
            contract.renewal_date = None
        
        # Atualiza outros campos
        for field in ['client_id', 'contract_number', 'description', 'value', 'payment_method', 'payment_frequency', 'status']:
            if field in data:
                if field == 'value':
                    setattr(contract, field, float(data[field]))
                else:
                    setattr(contract, field, data[field])
        
        contract.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Contrato atualizado com sucesso',
            'data': contract.to_dict()
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'error': f'Erro de formato: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/contracts/<int:contract_id>', methods=['DELETE'])
def delete_contract(contract_id):
    """Exclui contrato"""
    try:
        contract = Contract.query.get_or_404(contract_id)
        
        db.session.delete(contract)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Contrato excluído com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/contracts/search', methods=['GET'])
def search_contracts():
    """Busca contratos por número, cliente ou descrição"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'success': False, 'error': 'Informe um termo de busca'}), 400
        
        contracts = Contract.query.join(Client).filter(
            db.or_(
                Contract.contract_number.contains(query),
                Contract.description.contains(query),
                Client.name.contains(query)
            )
        ).all()
        
        return jsonify({
            'success': True,
            'data': [contract.to_dict() for contract in contracts],
            'total': len(contracts),
            'query': query
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/contracts/overdue', methods=['GET'])
def get_overdue_contracts():
    """Lista contratos vencidos"""
    try:
        today = date.today()
        contracts = Contract.query.filter(
            Contract.end_date < today,
            Contract.status == 'Ativo'
        ).all()
        
        return jsonify({
            'success': True,
            'data': [contract.to_dict() for contract in contracts],
            'total': len(contracts)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/contracts/renewal-due', methods=['GET'])
def get_renewal_due_contracts():
    """Lista contratos próximos da renovação"""
    try:
        today = date.today()
        future_date = today + timedelta(days=30)
        
        contracts = Contract.query.filter(
            Contract.renewal_date.isnot(None),
            Contract.renewal_date >= today,
            Contract.renewal_date <= future_date,
            Contract.status == 'Ativo'
        ).all()
        
        return jsonify({
            'success': True,
            'data': [contract.to_dict() for contract in contracts],
            'total': len(contracts)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== DASHBOARD ====================

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Estatísticas do dashboard"""
    try:
        # Estatísticas básicas
        total_clients = Client.query.count()
        total_contracts = Contract.query.count()
        active_contracts = Contract.query.filter_by(status='Ativo').count()
        
        # Valor total dos contratos ativos
        total_value = db.session.query(db.func.sum(Contract.value)).filter_by(status='Ativo').scalar() or 0
        
        # Contratos vencidos
        overdue_contracts = Contract.query.filter(
            Contract.end_date < date.today(),
            Contract.status == 'Ativo'
        ).count()
        
        # Contratos para renovação
        renewal_contracts = Contract.query.filter(
            Contract.renewal_date.isnot(None),
            Contract.renewal_date >= date.today(),
            Contract.renewal_date <= date.today() + timedelta(days=30),
            Contract.status == 'Ativo'
        ).count()
        
        # Top 5 clientes por valor de contrato
        top_clients = db.session.query(
            Client.name,
            db.func.sum(Contract.value).label('total_value')
        ).join(Contract).filter(
            Contract.status == 'Ativo'
        ).group_by(Client.id).order_by(
            db.func.sum(Contract.value).desc()
        ).limit(5).all()
        
        return jsonify({
            'success': True,
            'data': {
                'total_clients': total_clients,
                'total_contracts': total_contracts,
                'active_contracts': active_contracts,
                'total_value': total_value,
                'overdue_contracts': overdue_contracts,
                'renewal_contracts': renewal_contracts,
                'top_clients': [
                    {'name': name, 'total_value': value}
                    for name, value in top_clients
                ]
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== INICIALIZAÇÃO ====================

@app.route('/api/init', methods=['POST'])
def initialize_database():
    """Inicializa o banco de dados com dados de exemplo"""
    try:
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create sample data
        create_sample_data()
        
        return jsonify({
            'success': True,
            'message': 'Banco de dados inicializado com sucesso!'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== PÁGINA WEB ====================

@app.route('/')
def index():
    """Página principal com interface de gestão"""
    return render_template('gestao.html')

if __name__ == '__main__':
    with app.app_context():
        # Verifica se o banco existe
        if not os.path.exists('instance/contratos.db'):
            print("🔧 Criando banco de dados...")
            init_db()
            create_sample_data()
    
    print("🚀 Servidor de gestão de clientes iniciado!")
    print("📡 API disponível em: http://localhost:5000/api")
    print("🌐 Interface web: http://localhost:5000")
    
    app.run(debug=True, port=5000)
