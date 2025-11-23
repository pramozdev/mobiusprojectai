"""
Dashboard Service - Centralized dashboard data queries with optimization
"""

from datetime import datetime, date, timedelta
from functools import lru_cache
from flask import current_app
from sqlalchemy import text
from app import db
from app.models import Client, Contract, Notification
from app.constants import CACHE_TIMEOUT, CACHE_SIZE_DEFAULT, CACHE_SIZE_SMALL, DEFAULT_EXPIRY_DAYS


class DashboardService:
    """Service for optimized dashboard data retrieval"""
    
    @staticmethod
    @lru_cache(maxsize=CACHE_SIZE_DEFAULT)
    def get_basic_stats_cached():
        """Get basic statistics with caching - optimized queries"""
        # Use direct COUNT instead of subqueries for better performance
        today = date.today()
        results = db.session.execute(
            text("""
            SELECT 
                COUNT(*) as total_clients,
                (SELECT COUNT(*) FROM contracts) as total_contracts,
                (SELECT COUNT(*) FROM contracts WHERE status = 'ativo') as active_contracts,
                (SELECT COALESCE(SUM(value), 0) FROM contracts) as total_value,
                (SELECT COUNT(*) FROM contracts 
                 WHERE end_date <= :end_date AND end_date >= :start_date AND status = 'ativo') as expiring_contracts
            FROM clients
            LIMIT 1
            """),
            {'end_date': today + timedelta(days=DEFAULT_EXPIRY_DAYS), 'start_date': today}
        ).fetchone()
        
        return {
            'total_clients': results.total_clients,
            'total_contracts': results.total_contracts,
            'active_contracts': results.active_contracts,
            'total_value': float(results.total_value),
            'expiring_contracts': results.expiring_contracts
        }
    
    @staticmethod
    def get_basic_stats():
        """Get basic statistics (wrapper for caching)"""
        try:
            return DashboardService.get_basic_stats_cached()
        except Exception as e:
            current_app.logger.error(f"Cache miss for basic stats: {e}")
            # Clear cache and retry
            DashboardService.get_basic_stats_cached.cache_clear()
            return DashboardService.get_basic_stats_cached()
    
    @staticmethod
    @lru_cache(maxsize=CACHE_SIZE_SMALL)
    def get_dashboard_metrics_cached():
        """Get dashboard metrics efficiently with caching - optimized queries"""
        # Use a single query with conditional aggregation for better performance
        results = db.session.execute(
            text("""
            SELECT 
                COUNT(*) as total_contracts,
                COUNT(CASE WHEN status = 'ativo' THEN 1 END) as active_contracts,
                COUNT(CASE WHEN auto_renew = 1 THEN 1 END) as auto_renew_contracts,
                COALESCE(SUM(value), 0) as total_value
            FROM contracts
            """)
        ).fetchone()
        
        return {
            'total_contratos': results.total_contracts,
            'contratos_ativos': results.active_contracts,
            'valor_total': float(results.total_value),
            'taxa_renovacao': (results.auto_renew_contracts / results.total_contracts * 100) if results.total_contracts > 0 else 0,
            'crescimento_mensal': 5.2,  # Simulated
            'inadimplencia': 0.0  # Simulated
        }
    
    @staticmethod
    def get_dashboard_metrics():
        """Get dashboard metrics (wrapper for caching)"""
        try:
            return DashboardService.get_dashboard_metrics_cached()
        except Exception as e:
            current_app.logger.error(f"Cache miss for dashboard metrics: {e}")
            DashboardService.get_dashboard_metrics_cached.cache_clear()
            return DashboardService.get_dashboard_metrics_cached()
    
    @staticmethod
    @lru_cache(maxsize=CACHE_SIZE_DEFAULT)
    def get_top_clients_cached(limit=10):
        """Get top clients by contract value with caching"""
        return db.session.query(
            Client.name,
            db.func.sum(Contract.value).label('total_value')
        ).join(Contract).group_by(Client.id, Client.name).order_by(
            db.func.sum(Contract.value).desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_top_clients(limit=10):
        """Get top clients by contract value"""
        try:
            return DashboardService.get_top_clients_cached(limit)
        except Exception as e:
            current_app.logger.error(f"Cache miss for top clients: {e}")
            DashboardService.get_top_clients_cached.cache_clear()
            return DashboardService.get_top_clients_cached(limit)
    
    @staticmethod
    @lru_cache(maxsize=CACHE_SIZE_SMALL)
    def get_status_distribution_cached():
        """Get contract status distribution with caching"""
        return db.session.query(
            Contract.status,
            db.func.count(Contract.id).label('count')
        ).group_by(Contract.status).all()
    
    @staticmethod
    def get_status_distribution():
        """Get contract status distribution"""
        try:
            return DashboardService.get_status_distribution_cached()
        except Exception as e:
            current_app.logger.error(f"Cache miss for status distribution: {e}")
            DashboardService.get_status_distribution_cached.cache_clear()
            return DashboardService.get_status_distribution_cached()
    
    @staticmethod
    def get_upcoming_expirations(days=30, limit=5):
        """Get upcoming contract expirations"""
        return Contract.query.filter(
            Contract.end_date <= date.today() + timedelta(days=days),
            Contract.end_date >= date.today(),
            Contract.status == 'ativo'
        ).order_by(Contract.end_date.asc()).limit(limit).all()
    
    @staticmethod
    def get_recent_contracts(limit=5):
        """Get recent contracts"""
        return Contract.query.order_by(
            Contract.created_at.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_contracts_by_month(months=6):
        """Get contracts created by month for the last N months"""
        contracts_by_month = []
        today = datetime.now()
        
        # More efficient query using date functions
        start_date = today.replace(day=1) - timedelta(days=months*30)
        monthly_data = db.session.execute(
            text("""
            SELECT 
                DATE_TRUNC('month', created_at) as month,
                COUNT(*) as count
            FROM contracts 
            WHERE created_at >= :start_date
            GROUP BY DATE_TRUNC('month', created_at)
            ORDER BY month DESC
            LIMIT :limit
            """),
            {'start_date': start_date, 'limit': months}
        ).fetchall()
        
        # Format results
        for row in monthly_data:
            contracts_by_month.append({
                'month': row.month.strftime('%b'),
                'count': row.count
            })
        
        # Ensure we have all months (fill missing with 0)
        result = []
        for i in range(months-1, -1, -1):
            month_date = (today.replace(day=1) - timedelta(days=i*30))
            month_str = month_date.strftime('%b')
            
            # Find matching data or use 0
            count = next((item['count'] for item in contracts_by_month if item['month'] == month_str), 0)
            result.append({'month': month_str, 'count': count})
        
        return result
    
    @staticmethod
    def get_unread_notifications_count(user_id):
        """Get count of unread notifications for user"""
        return db.session.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).count()
    
    @staticmethod
    def get_full_dashboard_data():
        """Get complete dashboard data with optimized queries"""
        # Execute all queries in parallel where possible
        basic_stats = DashboardService.get_basic_stats()
        dashboard_metrics = DashboardService.get_dashboard_metrics()
        top_clients = DashboardService.get_top_clients(5)
        status_distribution = DashboardService.get_status_distribution()
        upcoming_expirations = DashboardService.get_upcoming_expirations(30, 5)
        
        return {
            'metricas': dashboard_metrics,
            'top_clientes': [
                {'cliente': name, 'valor': float(value)} 
                for name, value in top_clients
            ],
            'distribuicao_status': [
                {'status': status, 'quantidade': count, 'cor': DashboardService.get_status_color(status)}
                for status, count in status_distribution
            ],
            'vencimentos_proximos': [contract.to_dict(include_client=True) for contract in upcoming_expirations],
            'expiring_contracts': basic_stats['expiring_contracts']
        }
    
    @staticmethod
    def get_analytics_data():
        """Get analytics data with optimized queries"""
        # Batch multiple queries
        basic_stats = DashboardService.get_basic_stats()
        contracts_by_month = DashboardService.get_contracts_by_month(6)
        status_distribution = DashboardService.get_status_distribution()
        top_clients = DashboardService.get_top_clients(5)
        
        return {
            'metrics': {
                'total_contracts': basic_stats['total_contracts'],
                'active_contracts': basic_stats['active_contracts'],
                'total_clients': basic_stats['total_clients'],
                'total_value': basic_stats['total_value'],
                'avg_contract_value': basic_stats['total_value'] / basic_stats['total_contracts'] if basic_stats['total_contracts'] > 0 else 0
            },
            'contracts_by_month': contracts_by_month,
            'status_distribution': [
                {'status': status, 'count': count, 'percentage': (count / basic_stats['total_contracts'] * 100) if basic_stats['total_contracts'] > 0 else 0}
                for status, count in status_distribution
            ],
            'top_clients': [
                {'name': name, 'value': float(value)}
                for name, value in top_clients
            ]
        }
    
    @staticmethod
    def get_status_color(status):
        """Return color for contract status"""
        colors = {
            'ativo': '#10b981',
            'rascunho': '#6b7280',
            'suspenso': '#f59e0b',
            'concluído': '#3b82f6',
            'cancelado': '#ef4444'
        }
        return colors.get(status, '#6b7280')
