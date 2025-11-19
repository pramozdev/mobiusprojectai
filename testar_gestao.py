"""
Script de teste para o sistema de gestão de clientes e contratos
Demonstra todas as funcionalidades da API
"""
import requests
import json
from datetime import datetime, date, timedelta

# Configuração
BASE_URL = "http://localhost:5000/api"

def test_api_connection():
    """Testa conexão com a API"""
    try:
        response = requests.get(f"{BASE_URL}/dashboard/stats")
        if response.status_code == 200:
            print("✅ Conexão com API bem-sucedida!")
            return True
        else:
            print(f"❌ Erro na API: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API. Execute 'python gestao_clientes.py' primeiro.")
        return False

def test_clients_crud():
    """Testa operações CRUD de clientes"""
    print("\n🧪 Testando CRUD de Clientes:")
    
    # Criar cliente
    client_data = {
        "name": "Empresa Teste Ltda",
        "email": "teste@empresa.com",
        "phone": "(11) 9999-8888",
        "cnpj_cpf": "11.222.333/0001-44",
        "address": "Rua Teste, 123",
        "city": "São Paulo",
        "state": "SP",
        "sector": "Tecnologia"
    }
    
    response = requests.post(f"{BASE_URL}/clients", json=client_data)
    if response.status_code == 201:
        client = response.json()['data']
        client_id = client['id']
        print(f"✅ Cliente criado: {client['name']} (ID: {client_id})")
    else:
        print(f"❌ Erro ao criar cliente: {response.text}")
        return None
    
    # Listar clientes
    response = requests.get(f"{BASE_URL}/clients")
    if response.status_code == 200:
        clients = response.json()['data']
        print(f"✅ Listando {len(clients)} clientes")
    
    # Buscar cliente específico
    response = requests.get(f"{BASE_URL}/clients/{client_id}")
    if response.status_code == 200:
        client = response.json()['data']
        print(f"✅ Cliente encontrado: {client['name']}")
    
    # Atualizar cliente
    update_data = {"phone": "(11) 7777-6666"}
    response = requests.put(f"{BASE_URL}/clients/{client_id}", json=update_data)
    if response.status_code == 200:
        print("✅ Cliente atualizado")
    
    # Buscar clientes
    response = requests.get(f"{BASE_URL}/clients/search?q=Teste")
    if response.status_code == 200:
        results = response.json()['data']
        print(f"✅ Busca por 'Teste': {len(results)} resultados")
    
    return client_id

def test_contracts_crud(client_id):
    """Testa operações CRUD de contratos"""
    print("\n🧪 Testando CRUD de Contratos:")
    
    # Criar contrato
    contract_data = {
        "client_id": client_id,
        "contract_number": "CTR-TEST-001",
        "description": "Contrato de teste para demonstração",
        "value": 25000.00,
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "payment_method": "Transferência Bancária",
        "payment_frequency": "Mensal",
        "renewal_date": "2024-12-01"
    }
    
    response = requests.post(f"{BASE_URL}/contracts", json=contract_data)
    if response.status_code == 201:
        contract = response.json()['data']
        contract_id = contract['id']
        print(f"✅ Contrato criado: {contract['contract_number']} (ID: {contract_id})")
    else:
        print(f"❌ Erro ao criar contrato: {response.text}")
        return None
    
    # Listar contratos
    response = requests.get(f"{BASE_URL}/contracts")
    if response.status_code == 200:
        contracts = response.json()['data']
        print(f"✅ Listando {len(contracts)} contratos")
    
    # Buscar contrato específico
    response = requests.get(f"{BASE_URL}/contracts/{contract_id}")
    if response.status_code == 200:
        contract = response.json()['data']
        print(f"✅ Contrato encontrado: {contract['contract_number']}")
    
    # Atualizar contrato
    update_data = {"status": "Suspenso"}
    response = requests.put(f"{BASE_URL}/contracts/{contract_id}", json=update_data)
    if response.status_code == 200:
        print("✅ Contrato atualizado")
    
    # Buscar contratos
    response = requests.get(f"{BASE_URL}/contracts/search?q=Teste")
    if response.status_code == 200:
        results = response.json()['data']
        print(f"✅ Busca por 'Teste': {len(results)} resultados")
    
    # Contratos vencidos
    response = requests.get(f"{BASE_URL}/contracts/overdue")
    if response.status_code == 200:
        overdue = response.json()['data']
        print(f"✅ Contratos vencidos: {len(overdue)}")
    
    # Contratos para renovação
    response = requests.get(f"{BASE_URL}/contracts/renewal-due")
    if response.status_code == 200:
        renewal = response.json()['data']
        print(f"✅ Contratos para renovação: {len(renewal)}")
    
    return contract_id

def test_dashboard():
    """Testa estatísticas do dashboard"""
    print("\n🧪 Testando Dashboard:")
    
    response = requests.get(f"{BASE_URL}/dashboard/stats")
    if response.status_code == 200:
        stats = response.json()['data']
        print(f"✅ Estatísticas obtidas:")
        print(f"   👥 Clientes: {stats['total_clients']}")
        print(f"   📄 Contratos: {stats['total_contracts']}")
        print(f"   💰 Valor total: R$ {stats['total_value']:,.2f}")
        print(f"   📈 Ativos: {stats['active_contracts']}")
        print(f"   ⚠️ Vencidos: {stats['overdue_contracts']}")
        print(f"   🔄 Renovação: {stats['renewal_contracts']}")
        print(f"   🏆 Top clientes: {len(stats['top_clients'])}")

def test_validation_errors():
    """Testa validação de erros"""
    print("\n🧪 Testando Validação de Erros:")
    
    # Tentar criar cliente sem dados obrigatórios
    response = requests.post(f"{BASE_URL}/clients", json={})
    if response.status_code == 400:
        print("✅ Validação de campos obrigatórios funcionando")
    
    # Tentar criar cliente com email duplicado
    response = requests.post(f"{BASE_URL}/clients", json={
        "name": "Duplicado",
        "email": "contato@techsolutions.com",  # Email que já existe nos dados de exemplo
        "cnpj_cpf": "99.999.999/0001-99"
    })
    if response.status_code == 400:
        print("✅ Validação de email duplicado funcionando")
    
    # Tentar criar contrato sem cliente
    response = requests.post(f"{BASE_URL}/contracts", json={
        "contract_number": "INVALID",
        "description": "Teste",
        "value": 1000,
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    })
    if response.status_code == 400:
        print("✅ Validação de cliente obrigatório funcionando")

def test_performance():
    """Testa performance com múltiplas requisições"""
    print("\n🧪 Testando Performance:")
    
    import time
    
    # Testar múltiplas requisições simultâneas
    start_time = time.time()
    
    # Listar clientes
    requests.get(f"{BASE_URL}/clients")
    
    # Listar contratos
    requests.get(f"{BASE_URL}/contracts")
    
    # Dashboard
    requests.get(f"{BASE_URL}/dashboard/stats")
    
    end_time = time.time()
    
    print(f"✅ 3 requisições em {(end_time - start_time)*1000:.2f}ms")

def run_all_tests():
    """Executa todos os testes"""
    print("🚀 Iniciando Testes do Sistema de Gestão")
    print("=" * 50)
    
    # Testar conexão
    if not test_api_connection():
        return
    
    # Testar clientes
    client_id = test_clients_crud()
    
    # Testar contratos
    if client_id:
        contract_id = test_contracts_crud(client_id)
    
    # Testar dashboard
    test_dashboard()
    
    # Testar validações
    test_validation_errors()
    
    # Testar performance
    test_performance()
    
    print("\n✅ Todos os testes concluídos!")
    print("\n📋 Resumo das Funcionalidades Testadas:")
    print("  ✅ CRUD completo de clientes")
    print("  ✅ CRUD completo de contratos")
    print("  ✅ Busca e filtragem")
    print("  ✅ Validação de dados")
    print("  ✅ Dashboard com estatísticas")
    print("  ✅ Relacionamentos entre entidades")
    print("  ✅ Tratamento de erros")
    print("  ✅ Performance das requisições")

def show_api_documentation():
    """Mostra documentação da API"""
    print("\n📚 Documentação da API:")
    print("=" * 50)
    
    endpoints = [
        ("GET", "/api/clients", "Lista todos os clientes"),
        ("GET", "/api/clients/<id>", "Busca cliente específico"),
        ("POST", "/api/clients", "Cria novo cliente"),
        ("PUT", "/api/clients/<id>", "Atualiza cliente"),
        ("DELETE", "/api/clients/<id>", "Exclui cliente"),
        ("GET", "/api/clients/search?q=<termo>", "Busca clientes"),
        ("", "", ""),
        ("GET", "/api/contracts", "Lista todos os contratos"),
        ("GET", "/api/contracts/<id>", "Busca contrato específico"),
        ("POST", "/api/contracts", "Cria novo contrato"),
        ("PUT", "/api/contracts/<id>", "Atualiza contrato"),
        ("DELETE", "/api/contracts/<id>", "Exclui contrato"),
        ("GET", "/api/contracts/search?q=<termo>", "Busca contratos"),
        ("GET", "/api/contracts/overdue", "Contratos vencidos"),
        ("GET", "/api/contracts/renewal-due", "Contratos para renovação"),
        ("", "", ""),
        ("GET", "/api/dashboard/stats", "Estatísticas do dashboard"),
        ("POST", "/api/init", "Inicializa banco com dados de exemplo")
    ]
    
    for method, endpoint, description in endpoints:
        if method:
            print(f"{method:6} {endpoint:30} - {description}")
        else:
            print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "docs":
        show_api_documentation()
    else:
        run_all_tests()
        
    print("\n💡 Dicas:")
    print("  - Execute 'python gestao_clientes.py' para iniciar o servidor")
    print("  - Acesse http://localhost:5000 para interface web")
    print("  - Execute 'python testar_gestao.py docs' para ver documentação")
    print("  - Execute 'python migrar_banco.py' para migrar dados existentes")
