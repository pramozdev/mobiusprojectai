"""
API Routes - Endpoints REST para a aplicação
"""

from app.utils.imports import (
    datetime, date, timedelta, jsonify, request, current_app
)
from app import db
from app.models import Client, Contract, User, Notification
from app.api import bp
from app.services.dashboard_service import DashboardService
from app.utils.decorators import handle_route_errors, validate_json

# Error handlers
@bp.errorhandler(404)
def not_found(error):
    """Trata recursos não encontrados"""
    return jsonify({
        'error': 'Not Found',
        'message': 'Recurso não encontrado'
    }), 404

@bp.errorhandler(500)
def internal_error(error):
    """Trata erros internos"""
    db.session.rollback()
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'Erro interno do servidor'
    }), 500

# Dashboard endpoints
@bp.route('/dashboard/data', methods=['GET'])
@handle_route_errors(json_response=True)
def get_dashboard_data():
    """Retorna dados completos do dashboard"""
    # Use optimized dashboard service
    data = DashboardService.get_full_dashboard_data()
    
    # Add additional API-specific data
    data.update({
        # Timeline de vencimentos
        'timeline_vencimentos': get_upcoming_expirations(),
        # Valor por setor (simulado - poderia vir de campo no modelo)
        'valor_por_setor': [
            {'setor': 'Tecnologia', 'valor': 800000, 'contratos': 45, 'crescimento': 12.5},
            {'setor': 'Consultoria', 'valor': 450000, 'contratos': 30, 'crescimento': 8.3},
            {'setor': 'Varejo', 'valor': 250000, 'contratos': 25, 'crescimento': -2.1}
        ],
        # Insights de IA (simulados)
        'ai_insights': {
            'alertas': [
                {'mensagem': f"{data['metricas']['contratos_ativos']} contratos ativos no sistema", 'tipo': 'warning'},
                {'mensagem': f"Valor total em contratos: R$ {data['metricas']['valor_total']:,.2f}", 'tipo': 'info'}
            ],
            'analise_metricas': f"O sistema possui {data['metricas']['total_contratos']} contratos cadastrados.",
            'score_risco': {'nivel': 'Moderado', 'pontuacao': 75},
            'tendencias': 'Métricas baseadas em dados reais do banco de dados.'
        },
        # Indicadores de mercado (simulados)
        'indicadores_mercado': {
            'dolar': {'valor': 5.25, 'variacao': 0.5, 'tendencia': 'alta'},
            'ibovespa': {'valor': 120000, 'variacao': 2.1, 'tendencia': 'alta'},
            'selic': {'valor': 13.25, 'variacao': 0, 'tendencia': 'estavel'}
        },
        'comparacao_setores': [
            {'setor': 'Tecnologia', 'valor': 800000, 'contratos': 45, 'crescimento': 12.5},
            {'setor': 'Consultoria', 'valor': 450000, 'contratos': 30, 'crescimento': 8.3},
            {'setor': 'Varejo', 'valor': 250000, 'contratos': 25, 'crescimento': -2.1}
        ],
        'valor_por_regiao': [
            {'regiao': 'São Paulo', 'valor': 900000},
            {'regiao': 'Rio de Janeiro', 'valor': 400000},
            {'regiao': 'Minas Gerais', 'valor': 200000}
        ]
    })
    
    return jsonify(data)

# Client endpoints
@bp.route('/clients', methods=['GET'])
def get_clients():
    """Lista todos os clientes"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        search = request.args.get('search', '', type=str)
        
        query = Client.query
        
        if search:
            query = query.filter(
                Client.name.ilike(f'%{search}%') |
                Client.email.ilike(f'%{search}%')
            )
        
        clients = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'clients': [client.to_dict() for client in clients.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': clients.total,
                'pages': clients.pages,
                'has_next': clients.has_next,
                'has_prev': clients.has_prev
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Erro ao listar clientes: {str(e)}")
        return jsonify({
            'error': 'Internal Error',
            'message': 'Erro ao listar clientes'
        }), 500

@bp.route('/clients', methods=['POST'])
def create_client():
    """Cria um novo cliente"""
    try:
        data = request.get_json()
        
        # Validação básica
        if not data or not data.get('name'):
            return jsonify({
                'error': 'Validation Error',
                'message': 'Nome é obrigatório'
            }), 400
        
        # Verificar email único
        if data.get('email') and Client.query.filter_by(email=data['email']).first():
            return jsonify({
                'error': 'Conflict',
                'message': 'Email já cadastrado'
            }), 409
        
        # TODO: Obter user_id da sessão
        user_id = 1  # Temporário
        
        client = Client(
            name=data['name'],
            email=data.get('email'),
            phone=data.get('phone'),
            document=data.get('document'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            postal_code=data.get('postal_code'),
            country=data.get('country', 'Brasil'),
            created_by=user_id
        )
        
        db.session.add(client)
        db.session.commit()
        
        return jsonify(client.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar cliente: {str(e)}")
        return jsonify({
            'error': 'Internal Error',
            'message': 'Erro ao criar cliente'
        }), 500

@bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    """Retorna detalhes de um cliente"""
    try:
        client = Client.query.get_or_404(client_id)
        return jsonify(client.to_dict(include_contracts=True))
        
    except Exception as e:
        current_app.logger.error(f"Erro ao obter cliente {client_id}: {str(e)}")
        return jsonify({
            'error': 'Internal Error',
            'message': 'Erro ao obter cliente'
        }), 500

@bp.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    """Atualiza um cliente"""
    try:
        client = Client.query.get_or_404(client_id)
        data = request.get_json()
        
        # Verificar email único se alterado
        if data and 'email' in data and data['email'] != client.email:
            if Client.query.filter_by(email=data['email']).first():
                return jsonify({
                    'error': 'Conflict',
                    'message': 'Email já cadastrado'
                }), 409
        
        if data:
            client.update_from_dict(data)
        
        db.session.commit()
        
        return jsonify(client.to_dict())
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar cliente {client_id}: {str(e)}")
        return jsonify({
            'error': 'Internal Error',
            'message': 'Erro ao atualizar cliente'
        }), 500

@bp.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    """Exclui um cliente"""
    try:
        client = Client.query.get_or_404(client_id)
        
        # Verificar se possui contratos
        if client.contracts.count() > 0:
            return jsonify({
                'error': 'Conflict',
                'message': 'Cliente possui contratos vinculados'
            }), 409
        
        db.session.delete(client)
        db.session.commit()
        
        return jsonify({'message': 'Cliente excluído com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao excluir cliente {client_id}: {str(e)}")
        return jsonify({
            'error': 'Internal Error',
            'message': 'Erro ao excluir cliente'
        }), 500

# Contract endpoints
@bp.route('/contracts', methods=['GET'])
def get_contracts():
    """Lista todos os contratos"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        search = request.args.get('search', '', type=str)
        status = request.args.get('status', '', type=str)
        
        query = Contract.query
        
        if search:
            query = query.filter(
                Contract.title.ilike(f'%{search}%') |
                Contract.contract_number.ilike(f'%{search}%')
            )
        
        if status:
            query = query.filter_by(status=status)
        
        contracts = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'contracts': [contract.to_dict(include_client=True) for contract in contracts.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': contracts.total,
                'pages': contracts.pages,
                'has_next': contracts.has_next,
                'has_prev': contracts.has_prev
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Erro ao listar contratos: {str(e)}")
        return jsonify({
            'error': 'Internal Error',
            'message': 'Erro ao listar contratos'
        }), 500

# Funções auxiliares
def calculate_renewal_rate():
    """Calcula taxa de renovação (otimizado)"""
    # Use dashboard service for consistent data
    metrics = DashboardService.get_dashboard_metrics()
    return metrics['taxa_renovacao']

def get_upcoming_expirations():
    """Retorna vencimentos próximos (otimizado)"""
    today = date.today()
    dates = []
    
    # Use dashboard service for consistent data
    for i in range(3):
        future_date = today + timedelta(days=30 * (i + 1))
        expiring_contracts = DashboardService.get_upcoming_expirations(days=30*(i+1), limit=50)
        
        # Filter for specific date range
        filtered_contracts = [
            contract for contract in expiring_contracts
            if contract.end_date <= future_date and contract.end_date >= today
        ]
        
        total_value = sum(contract.value for contract in filtered_contracts)
        
        dates.append({
            'data': future_date.strftime('%Y-%m-%d'),
            'contratos': len(filtered_contracts),
            'valor': float(total_value)
        })
    
    return dates

