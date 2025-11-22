"""
Testes do Dashboard - Testes unitários para funcionalidades do dashboard
"""
import pytest
import json
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from services.dashboard_service import DashboardService
from repositories.contract_repository import ContractRepository
from repositories.client_repository import ClientRepository
from utils.formatters import format_currency, format_percentage
from utils.validators import validate_date_range, ValidationError

class TestDashboardService:
    """Testes para DashboardService"""
    
    @pytest.fixture
    def dashboard_service(self):
        """Fixture para DashboardService"""
        # Mock repositories
        mock_contract_repo = Mock(spec=ContractRepository)
        mock_client_repo = Mock(spec=ClientRepository)
        
        service = DashboardService()
        service.contract_repository = mock_contract_repo
        service.client_repository = mock_client_repo
        
        return service
    
    @pytest.fixture
    def sample_contracts(self):
        """Fixture com dados de contratos de exemplo"""
        return [
            {
                'id': 1,
                'value': 100000.0,
                'status': 'Ativo',
                'end_date': '2024-12-31',
                'client_id': 1
            },
            {
                'id': 2,
                'value': 50000.0,
                'status': 'Pendente',
                'end_date': '2024-11-15',
                'client_id': 2
            },
            {
                'id': 3,
                'value': 75000.0,
                'status': 'Ativo',
                'end_date': '2025-01-15',
                'client_id': 1
            }
        ]
    
    @pytest.fixture
    def sample_clients(self):
        """Fixture com dados de clientes de exemplo"""
        return [
            {'id': 1, 'name': 'Cliente A', 'email': 'cliente_a@email.com'},
            {'id': 2, 'name': 'Cliente B', 'email': 'cliente_b@email.com'}
        ]
    
    def test_get_complete_dashboard_data_success(self, dashboard_service, sample_contracts, sample_clients):
        """Testa obtenção completa de dados do dashboard"""
        # Setup mocks
        dashboard_service.contract_repository.get_contracts_with_filters.return_value = sample_contracts
        dashboard_service.client_repository.get_all_clients.return_value = sample_clients
        
        # Executar
        result = dashboard_service.get_complete_dashboard_data({})
        
        # Verificar
        assert 'metricas' in result
        assert 'distribuicao_status' in result
        assert 'top_clientes' in result
        assert 'ai_insights' in result
        
        # Verificar métricas
        metrics = result['metricas']
        assert metrics['total_contratos'] == 3
        assert metrics['valor_total'] == 225000.0
        assert metrics['contratos_ativos'] == 2
        assert metrics['inadimplencia'] == 0.0
    
    def test_get_complete_dashboard_data_with_filters(self, dashboard_service, sample_contracts, sample_clients):
        """Testa obtenção de dados com filtros"""
        # Setup
        filters = {'status': 'Ativo', 'start_date': '2024-01-01'}
        filtered_contracts = [c for c in sample_contracts if c['status'] == 'Ativo']
        
        dashboard_service.contract_repository.get_contracts_with_filters.return_value = filtered_contracts
        dashboard_service.client_repository.get_all_clients.return_value = sample_clients
        
        # Executar
        result = dashboard_service.get_complete_dashboard_data(filters)
        
        # Verificar
        assert result['metricas']['total_contratos'] == 2
        assert result['metricas']['contratos_ativos'] == 2
    
    def test_get_complete_dashboard_data_empty_contracts(self, dashboard_service):
        """Testa comportamento com lista vazia de contratos"""
        # Setup
        dashboard_service.contract_repository.get_contracts_with_filters.return_value = []
        dashboard_service.client_repository.get_all_clients.return_value = []
        
        # Executar
        result = dashboard_service.get_complete_dashboard_data({})
        
        # Verificar métricas padrão para lista vazia
        metrics = result['metricas']
        assert metrics['total_contratos'] == 0
        assert metrics['valor_total'] == 0
        assert metrics['contratos_ativos'] == 0
        assert metrics['inadimplencia'] == 0.0
    
    def test_get_key_metrics(self, dashboard_service, sample_contracts):
        """Testa obtenção de métricas chave"""
        # Setup
        dashboard_service.contract_repository.get_all_contracts.return_value = sample_contracts
        
        # Executar
        result = dashboard_service.get_key_metrics()
        
        # Verificar
        assert result['total_contratos'] == 3
        assert result['valor_total'] == 225000.0
    
    def test_get_chart_data_status(self, dashboard_service, sample_contracts):
        """Testa obtenção de dados do gráfico de status"""
        # Setup
        dashboard_service.contract_repository.get_all_contracts.return_value = sample_contracts
        
        # Executar
        result = dashboard_service.get_chart_data('status')
        
        # Verificar
        assert isinstance(result, list)
        assert len(result) == 2  # Ativo e Pendente
        
        # Verificar estrutura dos itens
        for item in result:
            assert 'status' in item
            assert 'quantidade' in item
            assert 'cor' in item
            assert 'percentual' in item
    
    def test_get_chart_data_invalid_type(self, dashboard_service):
        """Testa obtenção de dados com tipo de gráfico inválido"""
        # Executar e verificar exceção
        with pytest.raises(ValueError, match="Tipo de gráfico não suportado"):
            dashboard_service.get_chart_data('invalid_type')
    
    def test_cache_functionality(self, dashboard_service, sample_contracts, sample_clients):
        """Testa funcionalidade de cache"""
        # Setup
        dashboard_service.contract_repository.get_contracts_with_filters.return_value = sample_contracts
        dashboard_service.client_repository.get_all_clients.return_value = sample_clients
        
        # Primeira chamada (deve calcular)
        result1 = dashboard_service.get_complete_dashboard_data({})
        
        # Segunda chamada (deve usar cache)
        result2 = dashboard_service.get_complete_dashboard_data({})
        
        # Verificar que são iguais
        assert result1 == result2
        
        # Verificar que repository foi chamado apenas uma vez
        assert dashboard_service.contract_repository.get_contracts_with_filters.call_count == 1
    
    def test_invalidate_cache(self, dashboard_service):
        """Testa invalidação de cache"""
        # Inserir algo no cache
        dashboard_service._cache['test'] = {'data': 'test'}
        
        # Invalidar
        dashboard_service.invalidate_cache()
        
        # Verificar que cache foi limpo
        assert len(dashboard_service._cache) == 0
    
    def test_calculate_status_distribution(self, dashboard_service, sample_contracts):
        """Testa cálculo de distribuição por status"""
        # Executar
        result = dashboard_service._calculate_status_distribution(sample_contracts)
        
        # Verificar
        assert len(result) == 2
        
        # Encontrar status 'Ativo'
        ativo_status = next((item for item in result if item['status'] == 'Ativo'), None)
        assert ativo_status is not None
        assert ativo_status['quantidade'] == 2
        assert ativo_status['percentual'] == 66.67  # 2/3 * 100
    
    def test_calculate_top_clients(self, dashboard_service, sample_contracts, sample_clients):
        """Testa cálculo de top clientes"""
        # Executar
        result = dashboard_service._calculate_top_clients(sample_contracts, sample_clients)
        
        # Verificar
        assert len(result) <= 5  # Máximo 5 clientes
        
        # Cliente A deve estar no topo (2 contratos)
        if result:
            top_client = result[0]
            assert top_client['cliente'] == 'Cliente A'
            assert top_client['valor'] == 175000.0  # 100000 + 75000
    
    def test_generate_insights(self, dashboard_service):
        """Testa geração de insights"""
        # Setup
        metrics = {
            'total_contratos': 10,
            'inadimplencia': 8.0,
            'vencimentos_proximos': 3
        }
        contracts = [{'id': i} for i in range(10)]
        
        # Executar
        result = dashboard_service._generate_insights(metrics, contracts)
        
        # Verificar estrutura
        assert 'alertas' in result
        assert 'score_risco' in result
        assert 'analise_metricas' in result
        assert 'tendencias' in result
        assert 'recomendacoes' in result
        
        # Verificar alertas
        alertas = result['alertas']
        assert len(alertas) >= 2  # Deve ter alerta de inadimplência e vencimentos
        
        # Verificar score de risco
        score_risco = result['score_risco']
        assert 'pontuacao' in score_risco
        assert 'nivel' in score_risco
        assert score_risco['nivel'] == 'Alto'  # Inadimplência de 8%

class TestDashboardAPI:
    """Testes para API do Dashboard"""
    
    def test_dashboard_data_endpoint_success(self, client):
        """Testa endpoint /api/dashboard/data com sucesso"""
        # Mock do serviço
        mock_data = {
            'metricas': {
                'total_contratos': 5,
                'valor_total': 250000.0,
                'contratos_ativos': 3
            },
            'distribuicao_status': [],
            'top_clientes': []
        }
        
        with patch('services.dashboard_service.DashboardService.get_complete_dashboard_data', return_value=mock_data):
            response = client.get('/api/dashboard/data')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['metricas']['total_contratos'] == 5
    
    def test_dashboard_data_endpoint_with_filters(self, client):
        """Testa endpoint com filtros"""
        mock_data = {'metricas': {'total_contratos': 2}}
        
        with patch('services.dashboard_service.DashboardService.get_complete_dashboard_data', return_value=mock_data):
            response = client.get('/api/dashboard/data?status=Ativo&start_date=2024-01-01')
            
            assert response.status_code == 200
    
    def test_dashboard_data_endpoint_validation_error(self, client):
        """Testa endpoint com erro de validação"""
        with patch('services.dashboard_service.DashboardService.get_complete_dashboard_data', side_effect=ValidationError("Data inválida")):
            response = client.get('/api/dashboard/data?start_date=invalid')
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert data['error'] == 'validation_error'
    
    def test_dashboard_metrics_endpoint(self, client):
        """Testa endpoint /api/dashboard/metrics"""
        mock_metrics = {
            'total_contratos': 10,
            'valor_total': 500000.0
        }
        
        with patch('services.dashboard_service.DashboardService.get_key_metrics', return_value=mock_metrics):
            response = client.get('/api/dashboard/metrics')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['metricas']['total_contratos'] == 10
    
    def test_dashboard_charts_endpoint(self, client):
        """Testa endpoint /api/dashboard/charts/<type>"""
        mock_chart_data = [
            {'status': 'Ativo', 'quantidade': 5, 'cor': '#10b981'}
        ]
        
        with patch('services.dashboard_service.DashboardService.get_chart_data', return_value=mock_chart_data):
            response = client.get('/api/dashboard/charts/status')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['chart_type'] == 'status'
            assert len(data['data']) == 1
    
    def test_dashboard_charts_invalid_type(self, client):
        """Testa endpoint com tipo de gráfico inválido"""
        with patch('services.dashboard_service.DashboardService.get_chart_data', side_effect=ValueError("Tipo inválido")):
            response = client.get('/api/dashboard/charts/invalid')
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert data['error'] == 'validation_error'

class TestDashboardIntegration:
    """Testes de integração do Dashboard"""
    
    @pytest.mark.integration
    def test_full_dashboard_flow(self, client):
        """Testa fluxo completo do dashboard"""
        # Este teste requer banco de dados real
        # Deve ser executado em ambiente de integração
        
        # 1. Obter dados do dashboard
        response = client.get('/api/dashboard/data')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        
        # 2. Verificar estrutura básica
        required_keys = ['metricas', 'distribuicao_status', 'top_clientes']
        for key in required_keys:
            assert key in data
        
        # 3. Verificar métricas
        metrics = data['metricas']
        assert isinstance(metrics['total_contratos'], int)
        assert isinstance(metrics['valor_total'], (int, float))
        assert isinstance(metrics['contratos_ativos'], int)
    
    @pytest.mark.integration
    def test_dashboard_performance(self, client):
        """Testa performance do dashboard"""
        import time
        
        # Medir tempo de resposta
        start_time = time.time()
        response = client.get('/api/dashboard/data')
        end_time = time.time()
        
        # Verificar que resposta é rápida (< 2 segundos)
        assert response.status_code == 200
        assert (end_time - start_time) < 2.0
    
    @pytest.mark.integration
    def test_dashboard_concurrent_requests(self, client):
        """Testa múltiplas requisições concorrentes"""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = client.get('/api/dashboard/data')
            results.append(response.status_code)
        
        # Criar múltiplas threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Esperar todas as threads
        for thread in threads:
            thread.join()
        
        # Verificar que todas as requisições foram bem-sucedidas
        assert all(status == 200 for status in results)

class TestDashboardErrorHandling:
    """Testes de tratamento de erros do Dashboard"""
    
    def test_database_error_handling(self, dashboard_service):
        """Testa tratamento de erros de banco de dados"""
        # Simular erro no repositório
        dashboard_service.contract_repository.get_contracts_with_filters.side_effect = Exception("Database error")
        
        # Executar e verificar exceção
        with pytest.raises(Exception, match="Database error"):
            dashboard_service.get_complete_dashboard_data({})
    
    def test_invalid_date_filter(self, dashboard_service):
        """Testa filtros com datas inválidas"""
        invalid_filters = {'start_date': '2024-13-01'}  # Mês inválido
        
        with patch('utils.validators.validate_date_range', side_effect=ValidationError("Data inválida")):
            with pytest.raises(ValidationError):
                dashboard_service.get_complete_dashboard_data(invalid_filters)
    
    def test_empty_database_handling(self, dashboard_service):
        """Testa comportamento com banco de dados vazio"""
        # Setup
        dashboard_service.contract_repository.get_contracts_with_filters.return_value = []
        dashboard_service.client_repository.get_all_clients.return_value = []
        
        # Executar
        result = dashboard_service.get_complete_dashboard_data({})
        
        # Verificar que não há erros e dados vazios são tratados corretamente
        assert result['metricas']['total_contratos'] == 0
        assert len(result['distribuicao_status']) == 0
        assert len(result['top_clientes']) == 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
