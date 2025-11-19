"""
Utilitários para geração de dados e formatação
"""
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any


def formatar_moeda_brasileira(valor: float) -> str:
    """
    Formata um valor numérico para o formato de moeda brasileira.
    
    Args:
        valor: Valor numérico a ser formatado
        
    Returns:
        String formatada como moeda brasileira (ex: R$ 1.234,56)
    """
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def formatar_percentual(valor: float) -> str:
    """Formata um valor como percentual"""
    return f'{valor:.2f}%'


def gerar_dados_contratos() -> list[dict]:
    """
    Gera dados de exemplo para contratos.
    
    Returns:
        Lista de dicionários com dados de contratos
    """
    clientes = ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E']
    contratos = []
    hoje = datetime.now()
    
    for i in range(15):
        data_vencimento = hoje + timedelta(days=random.randint(1, 90))
        cliente = random.choice(clientes)
        valor = round(random.uniform(1000, 10000), 2)
        dias_para_vencer = (data_vencimento - hoje).days
        
        contratos.append({
            'id': i + 1,
            'cliente': cliente,
            'valor': formatar_moeda_brasileira(valor),
            'data_vencimento': data_vencimento.strftime('%d/%m/%Y'),
            'dias_para_vencer': dias_para_vencer,
            'status': 'A vencer' if dias_para_vencer > 7 else 'Próximo do vencimento'
        })
    
    return sorted(contratos, key=lambda x: x['dias_para_vencer'])


def obter_resumo_contratos(contratos: list[dict]) -> dict:
    """
    Calcula resumo estatístico dos contratos.
    
    Args:
        contratos: Lista de contratos
        
    Returns:
        Dicionário com estatísticas dos contratos
    """
    hoje = datetime.now()
    mes_atual = hoje.month
    mes_proximo = (hoje.month % 12) + 1
    
    vencendo_este_mes = [
        c for c in contratos 
        if datetime.strptime(c['data_vencimento'], '%d/%m/%Y').month == mes_atual
    ]
    vencendo_proximo_mes = [
        c for c in contratos 
        if datetime.strptime(c['data_vencimento'], '%d/%m/%Y').month == mes_proximo
    ]
    
    return {
        'total_contratos': len(contratos),
        'vencendo_este_mes': len(vencendo_este_mes),
        'vencendo_proximo_mes': len(vencendo_proximo_mes),
        'proximos_vencimentos': contratos[:5]  # 5 próximos vencimentos
    }


def gerar_metricas_dashboard() -> Dict[str, Any]:
    """Gera métricas principais do dashboard"""
    return {
        'total_contratos': random.randint(80, 150),
        'valor_total': round(random.uniform(500000, 2000000), 2),
        'taxa_renovacao': round(random.uniform(75, 95), 2),
        'inadimplencia': round(random.uniform(2, 8), 2),
        'contratos_ativos': random.randint(60, 120),
        'contratos_pendentes': random.randint(5, 15),
        'crescimento_mensal': round(random.uniform(-5, 15), 2)
    }


def gerar_distribuicao_status() -> List[Dict[str, Any]]:
    """Gera dados de distribuição por status"""
    return [
        {'status': 'Ativo', 'quantidade': random.randint(50, 80), 'cor': '#10b981'},
        {'status': 'Pendente', 'quantidade': random.randint(10, 20), 'cor': '#f59e0b'},
        {'status': 'Vencido', 'quantidade': random.randint(5, 15), 'cor': '#ef4444'},
        {'status': 'Renovado', 'quantidade': random.randint(15, 30), 'cor': '#3b82f6'},
        {'status': 'Cancelado', 'quantidade': random.randint(3, 10), 'cor': '#6b7280'}
    ]


def gerar_top_clientes() -> List[Dict[str, Any]]:
    """Gera dados dos top 5 clientes por valor"""
    clientes = ['TechCorp Ltda', 'Indústria XYZ', 'Comércio ABC', 'Serviços Delta', 'Empresa Omega']
    return [
        {
            'cliente': cliente,
            'valor': round(random.uniform(50000, 200000), 2)
        }
        for cliente in clientes
    ]


def gerar_valor_por_setor() -> List[Dict[str, Any]]:
    """Gera dados de valor por setor"""
    setores = ['Tecnologia', 'Indústria', 'Comércio', 'Serviços', 'Saúde', 'Educação']
    return [
        {
            'setor': setor,
            'valor': round(random.uniform(30000, 150000), 2),
            'contratos': random.randint(5, 25)
        }
        for setor in setores
    ]


def gerar_valor_por_regiao() -> List[Dict[str, Any]]:
    """Gera dados de valor por região"""
    regioes = ['Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste', 'Norte']
    return [
        {
            'regiao': regiao,
            'valor': round(random.uniform(40000, 180000), 2),
            'percentual': round(random.uniform(10, 35), 2)
        }
        for regiao in regioes
    ]


def gerar_timeline_vencimentos() -> List[Dict[str, Any]]:
    """Gera timeline de vencimentos para os próximos 12 meses"""
    hoje = datetime.now()
    timeline = []
    
    for i in range(12):
        mes = hoje + timedelta(days=30 * i)
        timeline.append({
            'mes': mes.strftime('%b/%y'),
            'quantidade': random.randint(5, 25),
            'valor': round(random.uniform(20000, 100000), 2)
        })
    
    return timeline


def gerar_mapa_calor_pagamentos() -> List[Dict[str, Any]]:
    """Gera mapa de calor de pagamentos (últimos 12 meses)"""
    hoje = datetime.now()
    mapa = []
    
    for i in range(12):
        mes = hoje - timedelta(days=30 * (11 - i))
        mapa.append({
            'mes': mes.strftime('%b'),
            'semana1': round(random.uniform(5000, 25000), 2),
            'semana2': round(random.uniform(5000, 25000), 2),
            'semana3': round(random.uniform(5000, 25000), 2),
            'semana4': round(random.uniform(5000, 25000), 2)
        })
    
    return mapa


def gerar_indicadores_mercado() -> Dict[str, Any]:
    """Gera indicadores de mercado financeiro"""
    return {
        'taxa_juros': {
            'valor': round(random.uniform(10, 14), 2),
            'variacao': round(random.uniform(-0.5, 0.5), 2),
            'tendencia': 'alta' if random.random() > 0.5 else 'baixa'
        },
        'ipca': {
            'valor': round(random.uniform(3, 6), 2),
            'variacao': round(random.uniform(-0.3, 0.3), 2),
            'tendencia': 'alta' if random.random() > 0.5 else 'baixa'
        },
        'igpm': {
            'valor': round(random.uniform(2, 5), 2),
            'variacao': round(random.uniform(-0.4, 0.4), 2),
            'tendencia': 'alta' if random.random() > 0.5 else 'baixa'
        },
        'cdi': {
            'valor': round(random.uniform(11, 13), 2),
            'variacao': round(random.uniform(-0.2, 0.2), 2),
            'tendencia': 'alta' if random.random() > 0.5 else 'baixa'
        },
        'dolar': {
            'valor': round(random.uniform(4.8, 5.5), 2),
            'variacao': round(random.uniform(-2, 2), 2),
            'tendencia': 'alta' if random.random() > 0.5 else 'baixa'
        },
        'ibovespa': {
            'valor': random.randint(115000, 135000),
            'variacao': round(random.uniform(-1.5, 1.5), 2),
            'tendencia': 'alta' if random.random() > 0.5 else 'baixa'
        }
    }


def gerar_comparacao_setores() -> List[Dict[str, Any]]:
    """Gera comparação de performance por setor"""
    setores = ['Tecnologia', 'Indústria', 'Comércio', 'Serviços', 'Saúde']
    return [
        {
            'setor': setor,
            'crescimento': round(random.uniform(-10, 25), 2),
            'inadimplencia': round(random.uniform(1, 8), 2),
            'renovacao': round(random.uniform(70, 95), 2)
        }
        for setor in setores
    ]