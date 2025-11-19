"""
Módulo de Análise Inteligente com IA
Fornece insights, alertas e análises preditivas baseadas em dados
"""
import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AIAnalytics:
    """Classe para análise inteligente de dados usando IA"""
    
    def __init__(self):
        """Inicializa o analisador de IA"""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    def analisar_metricas(self, metricas: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa métricas e gera insights
        
        Args:
            metricas: Dicionário com métricas do dashboard
            
        Returns:
            Dicionário com análise e insights
        """
        prompt = f"""
        Analise as seguintes métricas de contratos e forneça insights acionáveis:
        
        - Total de Contratos: {metricas.get('total_contratos', 0)}
        - Valor Total: R$ {metricas.get('valor_total', 0):,.2f}
        - Taxa de Renovação: {metricas.get('taxa_renovacao', 0)}%
        - Inadimplência: {metricas.get('inadimplencia', 0)}%
        - Crescimento Mensal: {metricas.get('crescimento_mensal', 0)}%
        
        Forneça:
        1. Análise geral da saúde do portfólio
        2. Pontos de atenção (se houver)
        3. Recomendações específicas
        4. Nível de risco (Baixo/Médio/Alto)
        
        Responda em formato JSON com as chaves: analise, pontos_atencao, recomendacoes, nivel_risco
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um analista financeiro especializado em gestão de contratos. Responda sempre em JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            resultado = response.choices[0].message.content
            
            # Tenta parsear JSON
            try:
                return json.loads(resultado)
            except json.JSONDecodeError:
                # Se não for JSON válido, retorna estrutura padrão
                return {
                    "analise": resultado,
                    "pontos_atencao": [],
                    "recomendacoes": [],
                    "nivel_risco": "Médio"
                }
                
        except Exception as e:
            return {
                "analise": f"Erro na análise: {str(e)}",
                "pontos_atencao": [],
                "recomendacoes": [],
                "nivel_risco": "Desconhecido"
            }
    
    def detectar_anomalias(self, dados_historicos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detecta anomalias nos dados históricos
        
        Args:
            dados_historicos: Lista de dados históricos
            
        Returns:
            Lista de anomalias detectadas
        """
        anomalias = []
        
        # Análise simples de desvios
        if len(dados_historicos) >= 3:
            valores = [d.get('valor', 0) for d in dados_historicos]
            media = sum(valores) / len(valores)
            
            for i, dado in enumerate(dados_historicos):
                valor = dado.get('valor', 0)
                desvio = abs(valor - media) / media * 100 if media > 0 else 0
                
                if desvio > 30:  # Desvio maior que 30%
                    anomalias.append({
                        'tipo': 'desvio_valor',
                        'periodo': dado.get('mes', f'Período {i+1}'),
                        'valor': valor,
                        'media': media,
                        'desvio_percentual': round(desvio, 2),
                        'severidade': 'Alta' if desvio > 50 else 'Média',
                        'descricao': f'Valor {desvio:.1f}% {"acima" if valor > media else "abaixo"} da média'
                    })
        
        return anomalias
    
    def gerar_alertas(self, dados_completos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Gera alertas inteligentes baseados nos dados
        
        Args:
            dados_completos: Todos os dados do dashboard
            
        Returns:
            Lista de alertas
        """
        alertas = []
        metricas = dados_completos.get('metricas', {})
        
        # Alerta de inadimplência alta
        inadimplencia = metricas.get('inadimplencia', 0)
        if inadimplencia > 5:
            alertas.append({
                'tipo': 'inadimplencia',
                'severidade': 'Alta' if inadimplencia > 8 else 'Média',
                'titulo': 'Inadimplência Acima do Ideal',
                'mensagem': f'Taxa de inadimplência em {inadimplencia}%. Recomenda-se ação imediata.',
                'acao_sugerida': 'Revisar processos de cobrança e análise de crédito',
                'icone': '⚠️'
            })
        
        # Alerta de taxa de renovação baixa
        taxa_renovacao = metricas.get('taxa_renovacao', 0)
        if taxa_renovacao < 75:
            alertas.append({
                'tipo': 'renovacao',
                'severidade': 'Média',
                'titulo': 'Taxa de Renovação Baixa',
                'mensagem': f'Apenas {taxa_renovacao}% dos contratos estão sendo renovados.',
                'acao_sugerida': 'Implementar programa de retenção de clientes',
                'icone': '📉'
            })
        
        # Alerta de crescimento negativo
        crescimento = metricas.get('crescimento_mensal', 0)
        if crescimento < 0:
            alertas.append({
                'tipo': 'crescimento',
                'severidade': 'Alta',
                'titulo': 'Crescimento Negativo',
                'mensagem': f'Queda de {abs(crescimento)}% no último mês.',
                'acao_sugerida': 'Analisar causas e implementar estratégias de recuperação',
                'icone': '📊'
            })
        
        # Alerta de concentração de vencimentos
        timeline = dados_completos.get('timeline_vencimentos', [])
        if timeline:
            proximo_mes = timeline[0]
            if proximo_mes.get('quantidade', 0) > 15:
                alertas.append({
                    'tipo': 'vencimentos',
                    'severidade': 'Média',
                    'titulo': 'Concentração de Vencimentos',
                    'mensagem': f'{proximo_mes["quantidade"]} contratos vencem no próximo mês.',
                    'acao_sugerida': 'Preparar equipe para renovações em massa',
                    'icone': '📅'
                })
        
        return alertas
    
    def calcular_score_risco(self, dados_completos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula score de risco para o portfólio
        
        Args:
            dados_completos: Todos os dados do dashboard
            
        Returns:
            Dicionário com score e detalhes
        """
        metricas = dados_completos.get('metricas', {})
        
        # Fatores de risco (0-100, quanto maior pior)
        risco_inadimplencia = min(metricas.get('inadimplencia', 0) * 10, 100)
        risco_renovacao = max(0, (100 - metricas.get('taxa_renovacao', 100)))
        risco_crescimento = max(0, -metricas.get('crescimento_mensal', 0) * 5)
        
        # Score final (média ponderada)
        score_total = (
            risco_inadimplencia * 0.4 +
            risco_renovacao * 0.35 +
            risco_crescimento * 0.25
        )
        
        # Classificação
        if score_total < 30:
            classificacao = 'Baixo'
            cor = 'success'
        elif score_total < 60:
            classificacao = 'Médio'
            cor = 'warning'
        else:
            classificacao = 'Alto'
            cor = 'danger'
        
        return {
            'score': round(score_total, 1),
            'classificacao': classificacao,
            'cor': cor,
            'fatores': {
                'inadimplencia': round(risco_inadimplencia, 1),
                'renovacao': round(risco_renovacao, 1),
                'crescimento': round(risco_crescimento, 1)
            },
            'recomendacao': self._gerar_recomendacao_risco(classificacao)
        }
    
    def _gerar_recomendacao_risco(self, classificacao: str) -> str:
        """Gera recomendação baseada no nível de risco"""
        recomendacoes = {
            'Baixo': 'Portfólio saudável. Manter estratégias atuais e buscar oportunidades de expansão.',
            'Médio': 'Atenção necessária. Revisar processos e implementar melhorias incrementais.',
            'Alto': 'Ação imediata requerida. Revisar estratégia completa e implementar plano de recuperação.'
        }
        return recomendacoes.get(classificacao, 'Análise detalhada necessária.')
    
    def prever_tendencias(self, timeline: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Prevê tendências futuras baseadas em dados históricos
        
        Args:
            timeline: Dados históricos de vencimentos
            
        Returns:
            Previsões e tendências
        """
        if len(timeline) < 3:
            return {
                'tendencia': 'Dados insuficientes',
                'previsao_proximo_mes': None,
                'confianca': 'Baixa'
            }
        
        # Análise simples de tendência
        valores = [t.get('valor', 0) for t in timeline[:6]]  # Últimos 6 meses
        quantidades = [t.get('quantidade', 0) for t in timeline[:6]]
        
        # Tendência de valor
        if len(valores) >= 3:
            tendencia_valor = 'crescente' if valores[-1] > valores[0] else 'decrescente'
            variacao_media = (valores[-1] - valores[0]) / len(valores)
            previsao_valor = valores[-1] + variacao_media
        else:
            tendencia_valor = 'estável'
            previsao_valor = valores[-1] if valores else 0
        
        # Tendência de quantidade
        if len(quantidades) >= 3:
            tendencia_qtd = 'crescente' if quantidades[-1] > quantidades[0] else 'decrescente'
            previsao_qtd = round((quantidades[-1] + quantidades[-2]) / 2)
        else:
            tendencia_qtd = 'estável'
            previsao_qtd = quantidades[-1] if quantidades else 0
        
        return {
            'tendencia_valor': tendencia_valor,
            'tendencia_quantidade': tendencia_qtd,
            'previsao_proximo_mes': {
                'valor': round(previsao_valor, 2),
                'quantidade': previsao_qtd
            },
            'confianca': 'Média',
            'observacao': f'Baseado nos últimos {len(valores)} períodos'
        }
    
    def analisar_grafico(self, tipo_grafico: str, dados: List[Dict[str, Any]]) -> str:
        """
        Analisa um gráfico específico e gera insights
        
        Args:
            tipo_grafico: Tipo do gráfico (status, clientes, setor, etc)
            dados: Dados do gráfico
            
        Returns:
            Análise textual do gráfico
        """
        if not dados:
            return "Sem dados disponíveis para análise."
        
        prompt = f"""
        Analise os seguintes dados do gráfico de {tipo_grafico} e forneça insights em português:
        
        Dados: {json.dumps(dados, ensure_ascii=False)}
        
        Forneça uma análise concisa (2-3 frases) destacando:
        1. Principal insight
        2. Padrão ou tendência observada
        3. Recomendação prática
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um analista de dados especializado. Seja conciso e prático."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Erro na análise: {str(e)}"
    
    def responder_pergunta_dados(self, pergunta: str, contexto_dados: Dict[str, Any]) -> str:
        """
        Responde perguntas sobre os dados usando IA
        
        Args:
            pergunta: Pergunta do usuário
            contexto_dados: Dados disponíveis para contexto
            
        Returns:
            Resposta da IA
        """
        prompt = f"""
        Com base nos seguintes dados do dashboard de contratos:
        
        {json.dumps(contexto_dados, ensure_ascii=False, indent=2)}
        
        Responda a seguinte pergunta de forma clara e objetiva:
        {pergunta}
        
        Se a pergunta não puder ser respondida com os dados disponíveis, informe educadamente.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em análise de contratos. Seja preciso e use os dados fornecidos."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Desculpe, ocorreu um erro ao processar sua pergunta: {str(e)}"