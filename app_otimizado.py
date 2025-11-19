"""
Versão otimizada do app.py com tratamento robusto de erros
e uso eficiente da API OpenAI
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from agente_ia_otimizado import AgenteIAOtimizado
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
from error_handler import (
    handle_openai_errors, 
    retry_with_backoff,
    flask_error_handler,
    APIError,
    QuotaExceededError,
    RateLimitExceededError,
    monitor_api_usage,
    api_monitor
)
from config_otimizada import get_config, validate_config
import os
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria a aplicação Flask
app = Flask(__name__)

# Carrega configurações otimizadas
current_config = get_config()
app.config.from_object(current_config)

# Valida configurações
validation_result = validate_config()
if not validation_result['valid']:
    logger.error("Configuração inválida! Verifique os problemas:")
    for issue in validation_result['issues']:
        logger.error(f"  - {issue}")

# Inicializa extensões
CORS(app, supports_credentials=True)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Registra handlers de erro globais
flask_error_handler(app)

# Inicializa o agente otimizado
try:
    agente = AgenteIAOtimizado(
        nome="Dominó Otimizado",
        config={
            'model': current_config.OPENAI_CONFIG['model'],
            'max_tokens': current_config.OPENAI_CONFIG['max_tokens'],
            'temperature': current_config.OPENAI_CONFIG['temperature'],
            'max_retries': current_config.OPENAI_CONFIG['max_retries'],
            'retry_delay': current_config.OPENAI_CONFIG['retry_delay'],
            'cache_enabled': current_config.CACHE_CONFIG['enabled'],
            'cache_size': current_config.CACHE_CONFIG['size'],
            'max_historico': 10  # Reduzido para economizar tokens
        }
    )
    logger.info("Agente IA inicializado com sucesso")
except Exception as e:
    logger.error(f"Falha ao inicializar agente IA: {e}")
    agente = None

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

@app.route('/')
def home():
    """Página inicial com tratamento de erros"""
    try:
        contratos = gerar_dados_contratos()
        resumo = obter_resumo_contratos(contratos)
        return render_template('index.html', resumo=resumo)
    except Exception as e:
        logger.error(f"Erro na página inicial: {e}")
        return render_template('error.html', error=str(e)), 500

@app.route('/dashboard')
def dashboard():
    """Página do dashboard avançado"""
    try:
        return render_template('dashboard.html')
    except Exception as e:
        logger.error(f"Erro no dashboard: {e}")
        return jsonify({"error": "Erro ao carregar dashboard"}), 500

@app.route('/api/contratos')
def get_contratos():
    """API para obter contratos com cache"""
    try:
        contratos = gerar_dados_contratos()
        return jsonify(contratos)
    except Exception as e:
        logger.error(f"Erro ao obter contratos: {e}")
        return jsonify({"error": "Erro ao carregar contratos"}), 500

@app.route('/api/dashboard/data')
@monitor_api_usage
def get_dashboard_data():
    """
    Retorna dados do dashboard com tratamento robusto de erros
    e otimização de uso da API
    """
    try:
        # Dados básicos (sem IA)
        contratos = gerar_dados_contratos()
        resumo = obter_resumo_contratos(contratos)
        
        # Métricas básicas
        metricas = gerar_metricas_dashboard(contratos)
        distribuicao = gerar_distribuicao_status(contratos)
        top_clientes = gerar_top_clientes(contratos)
        valor_setor = gerar_valor_por_setor(contratos)
        valor_regiao = gerar_valor_por_regiao(contratos)
        timeline = gerar_timeline_vencimentos(contratos)
        mapa_calor = gerar_mapa_calor_pagamentos(contratos)
        
        # Análises de IA (com tratamento de erro)
        indicadores_mercado = None
        comparacao_setores = None
        
        if agente:
            try:
                indicadores_mercado = gerar_indicadores_mercado(contratos)
            except Exception as e:
                logger.warning(f"Erro ao gerar indicadores de mercado: {e}")
            
            try:
                comparacao_setores = gerar_comparacao_setores(contratos)
            except Exception as e:
                logger.warning(f"Erro ao gerar comparação de setores: {e}")
        
        return jsonify({
            'resumo': resumo,
            'metricas': metricas,
            'distribuicao': distribuicao,
            'top_clientes': top_clientes,
            'valor_setor': valor_setor,
            'valor_regiao': valor_regiao,
            'timeline': timeline,
            'mapa_calor': mapa_calor,
            'indicadores_mercado': indicadores_mercado,
            'comparacao_setores': comparacao_setores,
            'api_stats': api_monitor.get_stats()
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter dados do dashboard: {e}")
        raise APIError("Erro ao carregar dados do dashboard")

@app.route('/api/analise/grafico', methods=['POST'])
@monitor_api_usage
@handle_openai_errors
@retry_with_backoff(max_retries=2)
def analisar_grafico():
    """
    Analisa um gráfico específico com IA e tratamento robusto de erros
    """
    if not agente:
        raise APIError("Serviço de IA não disponível no momento")
    
    try:
        data = request.get_json()
        grafico_tipo = data.get('tipo', '')
        dados = data.get('dados', {})
        
        if not grafico_tipo:
            raise APIError("Tipo de gráfico não especificado")
        
        # Constrói prompt otimizado
        prompt = f"""
        Analise este {grafico_tipo} com os seguintes dados:
        {dados}
        
        Forneça uma análise concisa (máximo 3 frases) destacando:
        1. Principal tendência
        2. Ponto de atenção
        3. Recomendação rápida
        """
        
        resposta = agente.processar_mensagem(prompt)
        
        return jsonify({
            'analise': resposta,
            'grafico_tipo': grafico_tipo,
            'timestamp': time.time()
        })
        
    except Exception as e:
        logger.error(f"Erro na análise do gráfico: {e}")
        raise

@app.route('/api/perguntar', methods=['POST'])
@monitor_api_usage
@handle_openai_errors
@retry_with_backoff(max_retries=2)
def perguntar_dados():
    """
    Responde perguntas sobre os dados usando IA com otimização
    """
    if not agente:
        raise APIError("Serviço de IA não disponível no momento")
    
    try:
        data = request.get_json()
        pergunta = data.get('pergunta', '')
        contexto = data.get('contexto', {})
        
        if not pergunta:
            raise APIError("Pergunta não fornecida")
        
        # Otimiza o contexto para economizar tokens
        contexto_resumido = {}
        if contexto:
            # Inclui apenas dados relevantes
            for key, value in contexto.items():
                if isinstance(value, list) and len(value) > 5:
                    contexto_resumido[key] = value[:5]  # Limita listas
                else:
                    contexto_resumido[key] = value
        
        # Constrói prompt otimizado
        prompt = f"""
        Pergunta: {pergunta}
        
        Contexto dos dados:
        {contexto_resumido}
        
        Responda de forma concisa e direta (máximo 2-3 frases).
        """
        
        resposta = agente.processar_mensagem(prompt)
        
        return jsonify({
            'resposta': resposta,
            'pergunta': pergunta,
            'timestamp': time.time()
        })
        
    except Exception as e:
        logger.error(f"Erro ao responder pergunta: {e}")
        raise

@app.route('/api/chat', methods=['POST'])
@monitor_api_usage
@handle_openai_errors
def chat():
    """
    Endpoint de chat otimizado
    """
    if not agente:
        raise APIError("Serviço de IA não disponível no momento")
    
    try:
        data = request.get_json()
        mensagem = data.get('mensagem', '')
        
        if not mensagem:
            raise APIError("Mensagem não fornecida")
        
        # Limita tamanho da mensagem
        if len(mensagem) > 500:
            mensagem = mensagem[:500] + "..."
        
        resposta = agente.processar_mensagem(mensagem)
        
        return jsonify({
            'resposta': resposta,
            'timestamp': time.time(),
            'agent_stats': agente.get_estatisticas()
        })
        
    except Exception as e:
        logger.error(f"Erro no chat: {e}")
        raise

@app.route('/api/stats')
def get_api_stats():
    """Retorna estatísticas de uso da API"""
    try:
        stats = {
            'api_monitor': api_monitor.get_stats(),
            'config_summary': validate_config()['config_summary']
        }
        
        if agente:
            stats['agent_stats'] = agente.get_estatisticas()
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        return jsonify({"error": "Erro ao obter estatísticas"}), 500

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Limpa o cache do agente"""
    try:
        if agente:
            agente.limpar_cache()
            return jsonify({"message": "Cache limpo com sucesso"})
        else:
            return jsonify({"error": "Agente não disponível"}), 503
            
    except Exception as e:
        logger.error(f"Erro ao limpar cache: {e}")
        return jsonify({"error": "Erro ao limpar cache"}), 500

# Handlers de erro personalizados
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Recurso não encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Erro interno do servidor"}), 500

if __name__ == '__main__':
    # Imprime resumo das configurações
    print("🚀 Iniciando aplicação otimizada")
    print("=" * 50)
    
    validation = validate_config()
    
    if validation['valid']:
        print("✅ Configuração validada com sucesso")
        
        if validation['warnings']:
            print("⚠️ Avisos:")
            for warning in validation['warnings']:
                print(f"  - {warning}")
        
        # Cria pastas necessárias
        os.makedirs('templates', exist_ok=True)
        os.makedirs('static', exist_ok=True)
        
        # Inicia o servidor
        port = current_config.PORT
        debug = current_config.DEBUG
        
        print(f"🌐 Servidor iniciando em http://localhost:{port}")
        print(f"🔧 Modo: {'Desenvolvimento' if debug else 'Produção'}")
        print(f"🤖 Modelo OpenAI: {current_config.OPENAI_CONFIG['model']}")
        print(f"💾 Cache: {'Ativado' if current_config.CACHE_CONFIG['enabled'] else 'Desativado'}")
        print(f"⏱️ Rate Limiting: {'Ativado' if current_config.RATE_LIMIT_CONFIG['enabled'] else 'Desativado'}")
        
        app.run(host='0.0.0.0', port=port, debug=debug)
    else:
        print("❌ Configuração inválida! Corrija os problemas antes de iniciar:")
        for issue in validation['issues']:
            print(f"  - {issue}")
        exit(1)
