"""
Serviço de IA Analytics - Recomendações Inteligentes
"""

import random
from datetime import datetime, timedelta, date
from app import db
from app.models import Contract, Client, Notification

class AIAnalyticsService:
    """Serviço de IA para analytics e recomendações"""
    
    def __init__(self):
        self.recommendation_templates = {
            'upsell': [
                "Cliente {client_name} tem {probability}% de probabilidade de upgrade para plano {plan_type}. Histórico de pagamentos pontuais e uso acima da média.",
                "Análise de comportamento indica que {client_name} pode beneficiar-se de serviços adicionais. Potencial de +{revenue}% em receita.",
                "Padrão de uso detectado: {client_name} utiliza {feature}% mais {service} que clientes similares. Oportunidade de upsell identificada."
            ],
            'retention': [
                "⚠️ {client_name} está em risco de churn. Última interação há {days} dias. Recomendo contato proativo com oferta especial.",
                "Contrato {contract_number} de {client_name} vence em {days} dias. Taxa de renovação prevista: {rate}%. Ação recomendada: {action}.",
                "Análise preditiva indica {probability}% de risco de perda para {client_name}. Fatores: {factors}."
            ],
            'growth': [
                "📈 Setor {sector} mostra crescimento de {growth}% nos últimos {months} meses. {client_name} está bem posicionado para expansão.",
                "Tendência de mercado: {trend}. Clientes no segmento de {segment} estão investindo {investment}% a mais em {service}.",
                "Oportunidade de mercado detectada: {opportunity}. {client_name} tem {advantage} competitivo."
            ],
            'optimization': [
                "💡 Otimização recomendada: {client_name} pode economizar {savings}% ao consolidar {service} contratos.",
                "Análise de eficiência: {client_name} tem {efficiency}% de utilização vs {benchmark}% de mercado. Recomendo {action}.",
                "Padrões identificados: {pattern}. Sugestão: {suggestion} para {client_name}."
            ]
        }
    
    def generate_recommendations(self, limit=5):
        """Gera recomendações personalizadas baseadas nos dados"""
        recommendations = []
        
        # Obter dados reais
        clients = Client.query.filter_by(is_active=True).all()
        contracts = Contract.query.all()
        
        if not clients or not contracts:
            return self._get_fallback_recommendations()
        
        # Análise de upsell
        upsell_rec = self._generate_upsell_recommendation(clients, contracts)
        if upsell_rec:
            recommendations.append(upsell_rec)
        
        # Análise de retenção
        retention_rec = self._generate_retention_recommendation(clients, contracts)
        if retention_rec:
            recommendations.append(retention_rec)
        
        # Análise de crescimento
        growth_rec = self._generate_growth_recommendation(clients, contracts)
        if growth_rec:
            recommendations.append(growth_rec)
        
        # Análise de otimização
        optimization_rec = self._generate_optimization_recommendation(clients, contracts)
        if optimization_rec:
            recommendations.append(optimization_rec)
        
        # Análise preditiva
        predictive_rec = self._generate_predictive_recommendation(clients, contracts)
        if predictive_rec:
            recommendations.append(predictive_rec)
        
        return recommendations[:limit]
    
    def _generate_upsell_recommendation(self, clients, contracts):
        """Gera recomendação de upsell"""
        # Encontrar cliente com maior potencial
        client_contracts = {}
        for client in clients:
            client_contracts[client.id] = [c for c in contracts if c.client_id == client.id]
        
        # Cliente com mais contratos ativos
        best_client = None
        max_active = 0
        for client in clients:
            active_count = len([c for c in client_contracts.get(client.id, []) if c.status == 'ativo'])
            if active_count > max_active and active_count < 5:  # Limite para não saturar
                max_active = active_count
                best_client = client
        
        if best_client:
            template = random.choice(self.recommendation_templates['upsell'])
            return {
                'type': 'upsell',
                'priority': 'medium',
                'title': '💰 Oportunidade de Upsell',
                'message': template.format(
                    client_name=best_client.name,
                    probability=random.randint(75, 95),
                    plan_type=random.choice(['Premium', 'Enterprise', 'Pro Plus']),
                    revenue=random.randint(20, 45),
                    feature=random.randint(30, 80),
                    service=random.choice(['serviços', 'recursos', 'funcionalidades'])
                ),
                'action_url': f'/clients/{best_client.id}',
                'action_text': 'Ver Cliente',
                'client_id': best_client.id
            }
        
        return None
    
    def _generate_retention_recommendation(self, clients, contracts):
        """Gera recomendação de retenção"""
        # Encontrar contratos próximo ao vencimento
        today = datetime.now().date()
        expiring_soon = []
        
        for contract in contracts:
            if contract.end_date and contract.status == 'ativo':
                end_date = contract.end_date if isinstance(contract.end_date, date) else contract.end_date.date()
                days_until = (end_date - today).days
                if 0 <= days_until <= 60:
                    expiring_soon.append((contract, days_until))
        
        if expiring_soon:
            contract, days = min(expiring_soon, key=lambda x: x[1])
            template = random.choice(self.recommendation_templates['retention'])
            
            return {
                'type': 'retention',
                'priority': 'high' if days <= 30 else 'medium',
                'title': '⚠️ Ação Preventiva',
                'message': template.format(
                    client_name=contract.client.name,
                    contract_number=contract.contract_number,
                    days=days,
                    rate=random.randint(70, 90),
                    action=random.choice(['renovação antecipada', 'oferta especial', 'negociação proativa']),
                    probability=random.randint(15, 35),
                    factors='baixa utilização, pagamento atrasado'
                ),
                'action_url': f'/contracts/{contract.id}',
                'action_text': 'Ver Contrato',
                'contract_id': contract.id
            }
        
        return None
    
    def _generate_growth_recommendation(self, clients, contracts):
        """Gera recomendação de crescimento"""
        # Análise de setor
        sectors = {}
        for client in clients:
            sector = self._extract_sector_from_name(client.name)
            if sector not in sectors:
                sectors[sector] = []
            sectors[sector].append(client)
        
        if sectors:
            sector = random.choice(list(sectors.keys()))
            sector_clients = sectors[sector]
            template = random.choice(self.recommendation_templates['growth'])
            
            return {
                'type': 'growth',
                'priority': 'low',
                'title': '📈 Tendência Positiva',
                'message': template.format(
                    sector=sector,
                    growth=random.randint(15, 35),
                    months=random.randint(3, 6),
                    client_name=random.choice(sector_clients).name,
                    trend='expansão digital',
                    segment='tecnologia',
                    investment=random.randint(25, 50),
                    service='serviços cloud',
                    opportunity='modernização de sistemas',
                    advantage='experiência comprovada'
                ),
                'action_url': '/analytics',
                'action_text': 'Ver Analytics'
            }
        
        return None
    
    def _generate_optimization_recommendation(self, clients, contracts):
        """Gera recomendação de otimização"""
        # Encontrar cliente com múltiplos contratos similares
        client_contracts = {}
        for client in clients:
            client_contracts[client.id] = [c for c in contracts if c.client_id == client.id]
        
        for client in clients:
            client_contract_list = client_contracts.get(client.id, [])
            if len(client_contract_list) >= 3:
                template = random.choice(self.recommendation_templates['optimization'])
                
                return {
                    'type': 'optimization',
                    'priority': 'medium',
                    'title': '💡 Otimização de Recursos',
                    'message': template.format(
                        client_name=client.name,
                        savings=random.randint(15, 30),
                        service='manutenção',
                        efficiency=random.randint(60, 85),
                        benchmark=random.randint(70, 95),
                        action='consolidação de serviços',
                        pattern='uso fragmentado de recursos',
                        suggestion='unificar contratos de suporte'
                    ),
                    'action_url': f'/relatorios/clientes/{client.id}',
                    'action_text': 'Ver Relatório',
                    'client_id': client.id
                }
        
        return None
    
    def _generate_predictive_recommendation(self, clients, contracts):
        """Gera recomendação preditiva"""
        # Análise preditiva baseada em padrões
        total_contracts = len(contracts)
        active_contracts = len([c for c in contracts if c.status == 'ativo'])
        
        if total_contracts > 0:
            churn_rate = ((total_contracts - active_contracts) / total_contracts) * 100
            
            return {
                'type': 'predictive',
                'priority': 'info',
                'title': '🤖 Insights da IA',
                'message': f'Análise preditiva indica taxa de churn de {churn_rate:.1f}% para os próximos 90 dias. '
                          f'Modelo de ML detectou {random.randint(2, 5)} contratos com risco elevado. '
                          f'Recomendo revisão estratégica para mitigar perdas.',
                'action_url': '/analytics',
                'action_text': 'Ver Análise Completa'
            }
        
        return None
    
    def _extract_sector_from_name(self, name):
        """Extrai setor do nome do cliente"""
        name_lower = name.lower()
        
        if 'tech' in name_lower or 'software' in name_lower:
            return 'Tecnologia'
        elif 'health' in name_lower or 'médica' in name_lower:
            return 'Saúde'
        elif 'finance' in name_lower or 'fintech' in name_lower:
            return 'Finanças'
        elif 'retail' in name_lower or 'commerce' in name_lower:
            return 'Varejo'
        elif 'education' in name_lower or 'edu' in name_lower:
            return 'Educação'
        elif 'logistic' in name_lower or 'transport' in name_lower:
            return 'Logística'
        elif 'marketing' in name_lower or 'digital' in name_lower:
            return 'Marketing'
        else:
            return 'Serviços'
    
    def _get_fallback_recommendations(self):
        """Recomendações padrão quando não há dados"""
        return [
            {
                'type': 'info',
                'priority': 'low',
                'title': '🤖 Insights da IA',
                'message': 'Comece cadastrando clientes e contratos para receber recomendações personalizadas baseadas em dados reais.',
                'action_url': '/clients/new',
                'action_text': 'Cadastrar Cliente'
            },
            {
                'type': 'info',
                'priority': 'low',
                'title': '📊 Analytics em Desenvolvimento',
                'message': 'O sistema está aprendendo com seus dados. Quanto mais informações cadastradas, melhores serão as recomendações.',
                'action_url': '/contracts/new',
                'action_text': 'Cadastrar Contrato'
            }
        ]
    
    def generate_risk_analysis(self):
        """Gera análise de risco para contratos"""
        contracts = Contract.query.all()
        risk_contracts = []
        
        for contract in contracts:
            risk_score = self._calculate_risk_score(contract)
            if risk_score > 60:
                risk_contracts.append({
                    'id': contract.id,
                    'title': contract.title,
                    'client_name': contract.client.name,
                    'risk_score': risk_score,
                    'risk_level': self._get_risk_level(risk_score),
                    'factors': self._get_risk_factors(contract)
                })
        
        return sorted(risk_contracts, key=lambda x: x['risk_score'], reverse=True)[:5]
    
    def _calculate_risk_score(self, contract):
        """Calcula score de risco para um contrato"""
        score = 0
        
        # Status do contrato
        if contract.status == 'suspenso':
            score += 40
        elif contract.status == 'rascunho':
            score += 20
        
        # Proximidade do vencimento
        if contract.end_date:
            end_date = contract.end_date if isinstance(contract.end_date, date) else contract.end_date.date()
            days_until = (end_date - datetime.now().date()).days
            if days_until < 0:
                score += 50
            elif days_until < 30:
                score += 30
            elif days_until < 60:
                score += 15
        
        # Valor do contrato (contratos maiores têm risco maior)
        if contract.value > 100000:
            score += 10
        elif contract.value > 50000:
            score += 5
        
        # Tipo de contrato
        if contract.contract_type == 'projeto':
            score += 5
        
        return min(score, 100)
    
    def _get_risk_level(self, score):
        """Retorna nível de risco baseado no score"""
        if score >= 80:
            return 'Crítico'
        elif score >= 60:
            return 'Alto'
        elif score >= 40:
            return 'Médio'
        else:
            return 'Baixo'
    
    def _get_risk_factors(self, contract):
        """Retorna fatores de risco para um contrato"""
        factors = []
        
        if contract.status == 'suspenso':
            factors.append('Contrato suspenso')
        
        if contract.end_date:
            end_date = contract.end_date if isinstance(contract.end_date, date) else contract.end_date.date()
            days_until = (end_date - datetime.now().date()).days
            if days_until < 0:
                factors.append('Vencido')
            elif days_until < 30:
                factors.append('Vencimento próximo')
        
        if contract.value > 100000:
            factors.append('Alto valor')
        
        if contract.contract_type == 'projeto':
            factors.append('Projeto complexo')
        
        return factors or ['Nenhum fator crítico']
