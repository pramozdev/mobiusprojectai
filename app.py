from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from agente_ia import AgenteIA
from models import db
from utils import (
    gerar_dados_contratos, 
    obter_resumo_contratos,
    gerar_metricas_dashboard,
    gerar_distribuicao_status,
    gerar_top_clientes,
    gerar_valor_por_setor,
    gerar_valor_por_regiao,
    gerar_timeline_vencimentos,
    gerar_mapa_calor_pagamentos,
    gerar_indicadores_mercado,
    gerar_comparacao_setores
)
from ai_analytics import AIAnalytics
from config import config
import os

# Cria a aplicação Flask
app = Flask(__name__)

# Carrega configurações
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Inicializa extensões
CORS(app, supports_credentials=True)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Inicializa o agente e analytics
agente = AgenteIA(nome="Dominó")
ai_analytics = AIAnalytics()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

@app.route('/')
def home():
    contratos = gerar_dados_contratos()
    resumo = obter_resumo_contratos(contratos)
    return render_template('index.html', resumo=resumo)


@app.route('/dashboard')
def dashboard():
    """Página do dashboard avançado"""
    return render_template('dashboard.html')

@app.route('/api/contratos')
def get_contratos():
    contratos = gerar_dados_contratos()
    resumo = obter_resumo_contratos(contratos)
    return jsonify({
        'resumo': resumo,
        'contratos': contratos
    })


@app.route('/api/dashboard')
def get_dashboard_data():
    """Retorna todos os dados do dashboard avançado com análises de IA"""
    # Gera dados
    metricas = gerar_metricas_dashboard()
    timeline = gerar_timeline_vencimentos()
    
    dados_completos = {
        'metricas': metricas,
        'distribuicao_status': gerar_distribuicao_status(),
        'top_clientes': gerar_top_clientes(),
        'valor_por_setor': gerar_valor_por_setor(),
        'valor_por_regiao': gerar_valor_por_regiao(),
        'timeline_vencimentos': timeline,
        'mapa_calor': gerar_mapa_calor_pagamentos(),
        'indicadores_mercado': gerar_indicadores_mercado(),
        'comparacao_setores': gerar_comparacao_setores()
    }
    
    # Adiciona análises de IA
    try:
        dados_completos['ai_insights'] = {
            'analise_metricas': ai_analytics.analisar_metricas(metricas),
            'alertas': ai_analytics.gerar_alertas(dados_completos),
            'score_risco': ai_analytics.calcular_score_risco(dados_completos),
            'tendencias': ai_analytics.prever_tendencias(timeline),
            'anomalias': ai_analytics.detectar_anomalias(timeline)
        }
    except Exception as e:
        print(f"Erro ao gerar insights de IA: {e}")
        dados_completos['ai_insights'] = None
    
    return jsonify(dados_completos)


@app.route('/api/analisar-grafico', methods=['POST'])
def analisar_grafico():
    """Analisa um gráfico específico com IA"""
    try:
        data = request.json
        tipo_grafico = data.get('tipo')
        dados = data.get('dados')
        
        if not tipo_grafico or not dados:
            return jsonify({'erro': 'Tipo de gráfico e dados são obrigatórios'}), 400
        
        analise = ai_analytics.analisar_grafico(tipo_grafico, dados)
        return jsonify({'analise': analise})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/perguntar-dados', methods=['POST'])
def perguntar_dados():
    """Responde perguntas sobre os dados usando IA"""
    try:
        data = request.json
        pergunta = data.get('pergunta', '').strip()
        
        if not pergunta:
            return jsonify({'erro': 'Pergunta vazia'}), 400
        
        # Obtém contexto dos dados
        metricas = gerar_metricas_dashboard()
        timeline = gerar_timeline_vencimentos()
        
        contexto = {
            'metricas': metricas,
            'timeline': timeline[:3],  # Últimos 3 meses
            'setores': gerar_valor_por_setor(),
            'regioes': gerar_valor_por_regiao()
        }
        
        resposta = ai_analytics.responder_pergunta_dados(pergunta, contexto)
        return jsonify({'resposta': resposta})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        mensagem = data.get('mensagem', '').strip()
        
        if not mensagem:
            return jsonify({'erro': 'Mensagem vazia'}), 400
            
        resposta = agente.processar_mensagem(mensagem)
        return jsonify({'resposta': resposta})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    # Cria a pasta de templates se não existir
    os.makedirs('templates', exist_ok=True)
    
    # Inicializa o banco de dados
    with app.app_context():
        db.create_all()
        print("✅ Banco de dados inicializado!")
    
    # Inicia o servidor
    app.run(
        debug=app.config['DEBUG'],
        port=app.config['PORT'],
        host='0.0.0.0'
    )
