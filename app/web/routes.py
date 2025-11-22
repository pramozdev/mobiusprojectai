"""
Web Routes - Páginas web da aplicação
"""

from app.utils.imports import (
    render_template, request, redirect, url_for, flash, abort, current_app,
    datetime, date, timedelta
)
from app import db
from app.models import Client, Contract, User, Notification
from app.web import bp

@bp.route('/')
def index():
    """Página principal"""
    try:
        # Estatísticas básicas
        total_clients = Client.query.count()
        total_contracts = Contract.query.count()
        active_contracts = Contract.query.filter_by(status='ativo').count()
        total_value = db.session.query(db.func.sum(Contract.value)).scalar() or 0
        
        # Contratos vencendo em breve
        expiring_contracts = Contract.query.filter(
            Contract.end_date <= date.today() + timedelta(days=30),
            Contract.end_date >= date.today(),
            Contract.status == 'ativo'
        ).count()
        
        stats = {
            'total_clients': total_clients,
            'total_contracts': total_contracts,
            'active_contracts': active_contracts,
            'total_value': float(total_value),
            'expiring_contracts': expiring_contracts
        }
        
        return render_template('index.html', stats=stats)
        
    except Exception as e:
        current_app.logger.error(f"Erro na página inicial: {str(e)}")
        flash('Erro ao carregar a página inicial', 'error')
        return render_template('index.html', stats={})

@bp.route('/dashboard')
def dashboard():
    """Dashboard principal"""
    try:
        # Métricas
        total_contracts = Contract.query.count()
        active_contracts = Contract.query.filter_by(status='ativo').count()
        total_value = db.session.query(db.func.sum(Contract.value)).scalar() or 0
        
        # Top clientes
        top_clients = db.session.query(
            Client.name,
            db.func.sum(Contract.value).label('total_value')
        ).join(Contract).group_by(Client.id, Client.name).order_by(
            db.func.sum(Contract.value).desc()
        ).limit(10).all()
        
        # Contratos recentes
        recent_contracts = Contract.query.order_by(
            Contract.created_at.desc()
        ).limit(5).all()
        
        # Vencimentos próximos
        upcoming_expirations = Contract.query.filter(
            Contract.end_date <= date.today() + timedelta(days=30),
            Contract.end_date >= date.today(),
            Contract.status == 'ativo'
        ).order_by(Contract.end_date.asc()).limit(5).all()
        
        # Distribuição por status
        status_data = db.session.query(
            Contract.status,
            db.func.count(Contract.id).label('count')
        ).group_by(Contract.status).all()
        
        dashboard_data = {
            'metricas': {
                'total_contratos': total_contracts,
                'contratos_ativos': active_contracts,
                'valor_total': float(total_value),
                'taxa_renovacao': 85.0,  # Simulado
                'crescimento_mensal': 5.2,  # Simulado
                'inadimplencia': 0.0  # Simulado
            },
            'top_clientes': [
                {'cliente': name, 'valor': float(value)} 
                for name, value in top_clients
            ],
            'distribuicao_status': [
                {'status': status, 'quantidade': count, 'cor': get_status_color(status)}
                for status, count in status_data
            ],
            'contratos_recentes': [contract.to_dict(include_client=True) for contract in recent_contracts],
            'vencimentos_proximos': [contract.to_dict(include_client=True) for contract in upcoming_expirations]
        }
        
        return render_template('dashboard.html', data=dashboard_data)
        
    except Exception as e:
        current_app.logger.error(f"Erro no dashboard: {str(e)}")
        flash('Erro ao carregar o dashboard', 'error')
        return render_template('dashboard.html', data={})

@bp.route('/clients')
def clients():
    """Lista de clientes"""
    try:
        # Obter todos os clientes (sem paginação por enquanto)
        clients = Client.query.all()
        
        # Obter contratos por cliente para estatísticas
        contracts_by_client = {}
        for client in clients:
            contracts_by_client[client.id] = Contract.query.filter_by(client_id=client.id).all()
        
        # Total de contratos para estatísticas
        contracts_count = Contract.query.count()
        
        return render_template('clients/list.html', 
                             clients=clients, 
                             contracts_by_client=contracts_by_client,
                             contracts_count=contracts_count)
        
    except Exception as e:
        current_app.logger.error(f"Erro ao listar clientes: {str(e)}")
        flash('Erro ao carregar lista de clientes', 'error')
        return render_template('clients/list.html', clients=[], contracts_by_client={}, contracts_count=0)

@bp.route('/clientes')
def clientes_pt():
    """Lista de clientes (rota em português)"""
    return clients()  # Reutiliza a mesma função

@bp.route('/clients/<int:client_id>')
def client_detail(client_id):
    """Detalhes do cliente"""
    try:
        client = Client.query.get_or_404(client_id)
        client_contracts = Contract.query.filter_by(client_id=client.id).all()
        total_contract_value = sum(c.value for c in client_contracts)
        
        return render_template('clients/detail.html', 
                             client=client, 
                             client_contracts=client_contracts,
                             total_contract_value=total_contract_value)
        
    except Exception as e:
        current_app.logger.error(f"Erro ao detalhar cliente {client_id}: {str(e)}")
        flash('Erro ao carregar detalhes do cliente', 'error')
        return redirect(url_for('web.clients'))

@bp.route('/clients/new', methods=['GET', 'POST'])
def new_client():
    """Novo cliente"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            document = request.form.get('document', '').strip()
            address = request.form.get('address', '').strip()
            city = request.form.get('city', '').strip()
            state = request.form.get('state', '').strip()
            postal_code = request.form.get('postal_code', '').strip()
            
            # Validações básicas
            if not name:
                flash('Nome é obrigatório', 'error')
                return render_template('clients/form.html')
            
            # Verificar email único
            if email and Client.query.filter_by(email=email).first():
                flash('Email já cadastrado', 'error')
                return render_template('clients/form.html')
            
            # TODO: Obter user_id da sessão quando implementar auth
            user_id = 1  # Temporário
            
            client = Client(
                name=name,
                email=email if email else None,
                phone=phone if phone else None,
                document=document if document else None,
                address=address if address else None,
                city=city if city else None,
                state=state if state else None,
                postal_code=postal_code if postal_code else None,
                created_by=user_id
            )
            
            db.session.add(client)
            db.session.commit()
            
            flash('Cliente criado com sucesso!', 'success')
            return redirect(url_for('web.client_detail', client_id=client.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro ao criar cliente: {str(e)}")
            flash('Erro ao criar cliente', 'error')
    
    return render_template('clients/form.html')

@bp.route('/clients/<int:client_id>/edit', methods=['GET', 'POST'])
def edit_client(client_id):
    """Editar cliente"""
    client = Client.query.get_or_404(client_id)
    
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            document = request.form.get('document', '').strip()
            address = request.form.get('address', '').strip()
            city = request.form.get('city', '').strip()
            state = request.form.get('state', '').strip()
            postal_code = request.form.get('postal_code', '').strip()
            is_active = request.form.get('is_active') == 'on'
            
            # Validações básicas
            if not name:
                flash('Nome é obrigatório', 'error')
                return render_template('clients/form.html', client=client)
            
            # Verificar email único se alterado
            if email and email != client.email:
                if Client.query.filter_by(email=email).first():
                    flash('Email já cadastrado', 'error')
                    return render_template('clients/form.html', client=client)
            
            client.name = name
            client.email = email if email else None
            client.phone = phone if phone else None
            client.document = document if document else None
            client.address = address if address else None
            client.city = city if city else None
            client.state = state if state else None
            client.postal_code = postal_code if postal_code else None
            client.is_active = is_active
            
            db.session.commit()
            
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('web.client_detail', client_id=client.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro ao atualizar cliente {client_id}: {str(e)}")
            flash('Erro ao atualizar cliente', 'error')
    
    return render_template('clients/form.html', client=client)

@bp.route('/contracts')
def contracts():
    """Lista de contratos"""
    try:
        page = request.args.get('page', 1, type=int)
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
            per_page=20, 
            error_out=False
        )
        
        return render_template('contracts/list.html', contracts=contracts, search=search, status=status)
        
    except Exception as e:
        current_app.logger.error(f"Erro ao listar contratos: {str(e)}")
        flash('Erro ao carregar contratos', 'error')
        return render_template('contracts/list.html', contracts=None)

@bp.route('/contratos')
def contratos_pt():
    """Lista de contratos (rota em português)"""
    return contracts()  # Reutiliza a mesma função

@bp.route('/contracts/<int:contract_id>')
def contract_detail(contract_id):
    """Detalhes do contrato"""
    try:
        contract = Contract.query.get_or_404(contract_id)
        return render_template('contracts/detail.html', contract=contract)
        
    except Exception as e:
        current_app.logger.error(f"Erro ao detalhar contrato {contract_id}: {str(e)}")
        flash('Erro ao carregar detalhes do contrato', 'error')
        return redirect(url_for('web.contracts'))

@bp.route('/contracts/<int:contract_id>/edit', methods=['GET', 'POST'])
def edit_contract(contract_id):
    """Editar contrato"""
    contract = Contract.query.get_or_404(contract_id)
    
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            client_id = request.form.get('client_id', type=int)
            value = request.form.get('value', type=float)
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            status = request.form.get('status', 'rascunho')
            contract_type = request.form.get('contract_type', 'serviço')
            auto_renew = request.form.get('auto_renew') == 'on'
            renewal_days = request.form.get('renewal_days', 30, type=int)
            
            # Validações básicas
            if not all([title, client_id, value, start_date, end_date]):
                flash('Campos obrigatórios não preenchidos', 'error')
                return render_template('contracts/form.html', contract=contract)
            
            # Validar datas
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if end_date_obj < start_date_obj:
                flash('Data de término deve ser posterior à data de início', 'error')
                return render_template('contracts/form.html', contract=contract)
            
            # Validar cliente
            client = Client.query.get(client_id)
            if not client:
                flash('Cliente não encontrado', 'error')
                return render_template('contracts/form.html', contract=contract)
            
            # Atualizar contrato
            contract.title = title
            contract.description = description if description else None
            contract.client_id = client_id
            contract.value = value
            contract.start_date = start_date_obj
            contract.end_date = end_date_obj
            contract.status = status
            contract.contract_type = contract_type
            contract.auto_renew = auto_renew
            contract.renewal_days = renewal_days
            contract.updated_at = datetime.now()
            
            # Campos opcionais
            contract.contract_number = request.form.get('contract_number') if request.form.get('contract_number') else None
            contract.currency = request.form.get('currency', 'BRL')
            contract.signature_date = datetime.strptime(request.form.get('signature_date'), '%Y-%m-%d').date() if request.form.get('signature_date') else None
            contract.payment_method = request.form.get('payment_method') if request.form.get('payment_method') else None
            contract.payment_frequency = request.form.get('payment_frequency') if request.form.get('payment_frequency') else None
            contract.notes = request.form.get('notes') if request.form.get('notes') else None
            
            db.session.commit()
            
            flash('Contrato atualizado com sucesso!', 'success')
            return redirect(url_for('web.contract_detail', contract_id=contract.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro ao atualizar contrato {contract_id}: {str(e)}")
            flash('Erro ao atualizar contrato', 'error')
    
    # Carregar clientes para o select
    clients = Client.query.filter_by(is_active=True).all()
    return render_template('contracts/form.html', contract=contract, clients=clients)

@bp.route('/contracts/new', methods=['GET', 'POST'])
def new_contract():
    """Novo contrato"""
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            client_id = request.form.get('client_id', type=int)
            value = request.form.get('value', type=float)
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            status = request.form.get('status', 'rascunho')
            contract_type = request.form.get('contract_type', 'serviço')
            auto_renew = request.form.get('auto_renew') == 'on'
            renewal_days = request.form.get('renewal_days', 30, type=int)
            
            # Validações básicas
            if not all([title, client_id, value, start_date, end_date]):
                flash('Campos obrigatórios não preenchidos', 'error')
                return render_template('contracts/form.html')
            
            # Validar datas
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if end_date_obj < start_date_obj:
                flash('Data de término deve ser posterior à data de início', 'error')
                return render_template('contracts/form.html')
            
            # Validar cliente
            client = Client.query.get(client_id)
            if not client:
                flash('Cliente não encontrado', 'error')
                return render_template('contracts/form.html')
            
            # TODO: Obter user_id da sessão quando implementar auth
            user_id = 1  # Temporário
            
            contract = Contract(
                title=title,
                description=description if description else None,
                client_id=client_id,
                value=value,
                start_date=start_date_obj,
                end_date=end_date_obj,
                status=status,
                contract_type=contract_type,
                auto_renew=auto_renew,
                renewal_days=renewal_days,
                created_by=user_id
            )
            
            db.session.add(contract)
            db.session.commit()
            
            flash('Contrato criado com sucesso!', 'success')
            return redirect(url_for('web.contract_detail', contract_id=contract.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro ao criar contrato: {str(e)}")
            flash('Erro ao criar contrato', 'error')
    
    clients = Client.query.filter_by(is_active=True).all()
    return render_template('contracts/form.html', clients=clients)

@bp.route('/reports')
def reports():
    """Página de relatórios"""
    return render_template('reports/index.html')

@bp.route('/relatorios')
def relatorios_pt():
    """Página de relatórios (rota em português)"""
    return reports()  # Reutiliza a mesma função

@bp.route('/reports/clients/<int:client_id>')
def client_report(client_id):
    """Relatório detalhado do cliente"""
    try:
        client = Client.query.get_or_404(client_id)
        contracts = Contract.query.filter_by(client_id=client.id).all()
        
        # Estatísticas
        total_contracts = len(contracts)
        active_contracts = len([c for c in contracts if c.status == 'ativo'])
        total_value = sum(c.value for c in contracts)
        
        report_data = {
            'client': client,
            'contracts': contracts,
            'stats': {
                'total_contracts': total_contracts,
                'active_contracts': active_contracts,
                'total_value': total_value,
                'avg_contract_value': total_value / total_contracts if total_contracts > 0 else 0
            }
        }
        
        return render_template('reports/client_detail.html', report=report_data)
        
    except Exception as e:
        current_app.logger.error(f"Erro ao gerar relatório do cliente {client_id}: {str(e)}")
        flash('Erro ao gerar relatório', 'error')
        return redirect(url_for('web.clients'))

@bp.route('/relatorios/clientes/<int:client_id>')
def client_report_pt(client_id):
    """Relatório detalhado do cliente (rota em português)"""
    return client_report(client_id)  # Reutiliza a mesma função

@bp.route('/analytics')
def analytics():
    """Página de analytics com IA"""
    try:
        # Importar serviço de IA
        from app.services.ai_analytics import AIAnalyticsService
        
        # Dados para analytics
        total_contracts = Contract.query.count()
        active_contracts = Contract.query.filter_by(status='ativo').count()
        total_clients = Client.query.count()
        
        # Valor total dos contratos
        total_value = db.session.query(db.func.sum(Contract.value)).scalar() or 0
        
        # Contratos por mês (últimos 6 meses)
        contracts_by_month = []
        for i in range(6):
            month_start = datetime.now().replace(day=1) - timedelta(days=i*30)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            count = Contract.query.filter(
                Contract.created_at >= month_start,
                Contract.created_at <= month_end
            ).count()
            
            contracts_by_month.append({
                'month': month_start.strftime('%b'),
                'count': count
            })
        
        contracts_by_month.reverse()
        
        # Distribuição por status
        status_data = db.session.query(
            Contract.status,
            db.func.count(Contract.id).label('count')
        ).group_by(Contract.status).all()
        
        # Top clientes por valor
        top_clients = db.session.query(
            Client.name,
            db.func.sum(Contract.value).label('total_value')
        ).join(Contract).group_by(Client.id, Client.name).order_by(
            db.func.sum(Contract.value).desc()
        ).limit(5).all()
        
        # IA Service - Gerar recomendações e análises
        ai_service = AIAnalyticsService()
        ai_recommendations = ai_service.generate_recommendations(limit=5)
        risk_contracts = ai_service.generate_risk_analysis()
        
        # Previsões simuladas da IA (mantidas para compatibilidade)
        ai_predictions = {
            'renewal_rate': 85.5,
            'churn_risk': 12.3,
            'upsell_opportunities': len([r for r in ai_recommendations if r['type'] == 'upsell']),
            'revenue_growth': 18.7,
            'risk_contracts': risk_contracts
        }
        
        analytics_data = {
            'metrics': {
                'total_contracts': total_contracts,
                'active_contracts': active_contracts,
                'total_clients': total_clients,
                'total_value': float(total_value),
                'avg_contract_value': float(total_value / total_contracts) if total_contracts > 0 else 0
            },
            'contracts_by_month': contracts_by_month,
            'status_distribution': [
                {'status': status, 'count': count, 'percentage': (count / total_contracts * 100) if total_contracts > 0 else 0}
                for status, count in status_data
            ],
            'top_clients': [
                {'name': name, 'value': float(value)}
                for name, value in top_clients
            ],
            'ai_predictions': ai_predictions,
            'ai_recommendations': ai_recommendations
        }
        
        return render_template('analytics/index.html', data=analytics_data)
        
    except Exception as e:
        current_app.logger.error(f"Erro ao carregar analytics: {str(e)}")
        flash('Erro ao carregar analytics', 'error')
        return render_template('analytics/index.html', data={})

@bp.route('/analiticos')
def analytics_pt():
    """Página de analytics com IA (rota em português)"""
    return analytics()  # Reutiliza a mesma função

@bp.route('/settings')
def settings():
    """Página de configurações"""
    return render_template('settings.html')

@bp.route('/configuracoes')
def configuracoes_pt():
    """Página de configurações (rota em português)"""
    return settings()  # Reutiliza a mesma função

@bp.route('/notifications')
def notifications():
    """Notificações do usuário"""
    try:
        # TODO: Obter user_id da sessão quando implementar auth
        user_id = 1  # Temporário
        notifications = Notification.query.filter_by(
            user_id=user_id,
            is_active=True
        ).order_by(Notification.created_at.desc()).limit(50).all()
        
        return render_template('notifications.html', notifications=notifications)
        
    except Exception as e:
        current_app.logger.error(f"Erro ao carregar notificações: {str(e)}")
        flash('Erro ao carregar notificações', 'error')
        return render_template('notifications.html', notifications=[])

@bp.route('/notificacoes')
def notificacoes_pt():
    """Notificações do usuário (rota em português)"""
    return notifications()  # Reutiliza a mesma função

@bp.route('/notifications/<int:notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    """Marca notificação como lida"""
    try:
        # TODO: Obter user_id da sessão quando implementar auth
        user_id = 1  # Temporário
        
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first_or_404()
        
        notification.mark_as_read()
        return jsonify({'success': True})
        
    except Exception as e:
        current_app.logger.error(f"Erro ao marcar notificação {notification_id}: {str(e)}")
        return jsonify({'success': False}), 500

# Funções auxiliares
def get_status_color(status):
    """Retorna cor para status do contrato"""
    colors = {
        'ativo': '#10b981',
        'rascunho': '#6b7280',
        'suspenso': '#f59e0b',
        'concluído': '#3b82f6',
        'cancelado': '#ef4444'
    }
    return colors.get(status, '#6b7280')
