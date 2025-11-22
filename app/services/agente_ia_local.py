"""
Agente IA Local - Alternativa quando OpenAI não está disponível
Usa regras e templates pré-definidos
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class AgenteIALocal:
    """Agente IA local para análise de contratos sem OpenAI"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Agente IA Local inicializado")
    
    def analisar_contrato(self, contrato_data: Dict) -> Dict:
        """Analisa contrato usando regras pré-definidas"""
        
        try:
            valor = contrato_data.get('value', 0)
            status = contrato_data.get('status', '').lower()
            dias_restantes = self._calcular_dias_restantes(contrato_data)
            
            # Análise baseada em regras
            analise = {
                'risco': self._avaliar_risco(valor, status, dias_restantes),
                'oportunidades': self._identificar_oportunidades(valor, status),
                'alertas': self._gerar_alertas(status, dias_restantes),
                'recomendacoes': self._gerar_recomendacoes(valor, status, dias_restantes),
                'score': self._calcular_score(valor, status, dias_restantes)
            }
            
            self.logger.info(f"Análise local concluída para contrato {contrato_data.get('id')}")
            return analise
            
        except Exception as e:
            self.logger.error(f"Erro na análise local: {str(e)}")
            return {'error': str(e)}
    
    def _calcular_dias_restantes(self, contrato_data: Dict) -> int:
        """Calcula dias restantes até o vencimento"""
        try:
            end_date = contrato_data.get('end_date')
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            hoje = datetime.now().date()
            delta = end_date - hoje
            return max(0, delta.days)
        except:
            return 0
    
    def _avaliar_risco(self, valor: float, status: str, dias: int) -> str:
        """Avalia nível de risco do contrato"""
        if status == 'cancelado':
            return 'Baixo (Contrato cancelado)'
        elif status == 'suspenso':
            return 'Alto (Contrato suspenso)'
        elif dias < 30:
            return 'Alto (Vencimento próximo)'
        elif valor > 100000:
            return 'Médio (Alto valor)'
        else:
            return 'Baixo (Contrato estável)'
    
    def _identificar_oportunidades(self, valor: float, status: str) -> List[str]:
        """Identifica oportunidades de negócio"""
        oportunidades = []
        
        if status == 'ativo' and valor > 50000:
            oportunidades.append('Expandir serviços para este cliente')
        
        if status == 'concluído':
            oportunidades.append('Renovação de contrato')
            oportunidades.append('Novos projetos similares')
        
        if valor < 30000:
            oportunidades.append('Upsell de serviços adicionais')
        
        return oportunidades
    
    def _gerar_alertas(self, status: str, dias: int) -> List[str]:
        """Gera alertas importantes"""
        alertas = []
        
        if dias < 30 and dias > 0:
            alertas.append(f'⚠️ Contrato vence em {dias} dias')
        elif dias == 0:
            alertas.append('🚨 Contrato vence hoje!')
        
        if status == 'suspenso':
            alertas.append('🔴 Contrato suspenso - atenção necessária')
        
        if status == 'ativo' and dias < 60:
            alertas.append('📅 Iniciar renovação em breve')
        
        return alertas
    
    def _gerar_recomendacoes(self, valor: float, status: str, dias: int) -> List[str]:
        """Gera recomendações de ação"""
        recomendacoes = []
        
        if dias < 30 and status == 'ativo':
            recomendacoes.append('Contatar cliente sobre renovação')
            recomendacoes.append('Preparar proposta de renovação')
        
        if valor > 100000:
            recomendacoes.append('Revisar clauses de risco')
            recomendacoes.append('Monitorar entregas com atenção')
        
        if status == 'suspenso':
            recomendacoes.append('Investigar motivo da suspensão')
            recomendacoes.append('Agendar reunião com cliente')
        
        if status == 'concluído':
            recomendacoes.append('Coletar feedback do cliente')
            recomendacoes.append('Enviar proposta de novos serviços')
        
        return recomendacoes
    
    def _calcular_score(self, valor: float, status: str, dias: int) -> int:
        """Calcula score de saúde do contrato (0-100)"""
        score = 50  # Base
        
        # Status
        if status == 'ativo':
            score += 30
        elif status == 'concluído':
            score += 20
        elif status == 'suspenso':
            score -= 20
        elif status == 'cancelado':
            score -= 30
        
        # Dias restantes
        if dias > 90:
            score += 20
        elif dias > 30:
            score += 10
        elif dias < 30:
            score -= 10
        
        # Valor
        if valor > 50000:
            score += 5
        elif valor > 100000:
            score += 10
        
        return max(0, min(100, score))
    
    def gerar_resumo_contratos(self, contratos: List[Dict]) -> Dict:
        """Gera resumo analítico de múltiplos contratos"""
        
        total = len(contratos)
        if total == 0:
            return {'error': 'Nenhum contrato encontrado'}
        
        ativos = sum(1 for c in contratos if c.get('status') == 'ativo')
        valor_total = sum(c.get('value', 0) for c in contratos)
        
        # Análises por status
        por_status = {}
        for contrato in contratos:
            status = contrato.get('status', 'desconhecido')
            if status not in por_status:
                por_status[status] = {'count': 0, 'value': 0}
            por_status[status]['count'] += 1
            por_status[status]['value'] += contrato.get('value', 0)
        
        # Contratos vencendo em breve
        vencendo_breve = []
        for contrato in contratos:
            dias = self._calcular_dias_restantes(contrato)
            if 0 < dias <= 30:
                vencendo_breve.append({
                    'id': contrato.get('id'),
                    'title': contrato.get('title'),
                    'dias': dias
                })
        
        return {
            'total_contratos': total,
            'contratos_ativos': ativos,
            'valor_total': valor_total,
            'valor_medio': valor_total / total if total > 0 else 0,
            'distribuicao_status': por_status,
            'vencendo_breve': vencendo_breve,
            'taxa_ativacao': (ativos / total * 100) if total > 0 else 0
        }
    
    def chat_assistente(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """Chat assistente baseado em regras"""
        
        mensagem_lower = mensagem.lower()
        
        # Respostas baseadas em padrões
        if 'oi' in mensagem_lower or 'olá' in mensagem_lower:
            return "Olá! Sou o assistente virtual do sistema de contratos. Como posso ajudar você hoje?"
        
        elif 'contrato' in mensagem_lower and 'ativo' in mensagem_lower:
            return f"Você tem {contexto.get('contratos_ativos', 0)} contratos ativos no sistema."
        
        elif 'vencendo' in mensagem_lower or 'vencer' in mensagem_lower:
            vencendo = len(contexto.get('vencendo_breve', []))
            return f"Você tem {vencendo} contrato(s) vencendo nos próximos 30 dias."
        
        elif 'valor' in mensagem_lower or 'total' in mensagem_lower:
            valor_total = contexto.get('valor_total', 0)
            return f"O valor total dos contratos é R$ {valor_total:,.2f}"
        
        elif 'ajuda' in mensagem_lower or 'help' in mensagem_lower:
            return """Posso ajudar com:
            • Status dos contratos
            • Valores totais  
            • Contratos vencendo
            • Análise de riscos
            • Recomendações
            
            O que você precisa saber?"""
        
        else:
            return "Entendi sua pergunta. Para melhor assistência, tente perguntar sobre: contratos ativos, valores, vencimentos ou diga 'ajuda'."

# Instância global
agente_ia_local = AgenteIALocal()
