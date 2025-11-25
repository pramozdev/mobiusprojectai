import { Formatters } from './utils/formatters.js';
import { errorHandler } from './utils/errorHandler.js';
import apiService from './services/api.js';
import { config } from './config.js';
import { CONSTANTS } from './constants.js';

/**
 * Dashboard Avançado - JavaScript
 * Gerenciamento de gráficos e dados do dashboard
 */

// Estado global
const DashboardState = {
    charts: {},
    updateInterval: null,
    isLoading: false
};

// Atualizar estado de carregamento
function updateLoadingState(isLoading) {
    const loading = document.querySelector(CONSTANTS.SELECTORS.LOADING);
    const dashboard = document.querySelector(CONSTANTS.SELECTORS.DASHBOARD);
    
    if (loading) {
        loading.style.display = isLoading ? 'flex' : 'none';
    }
    if (dashboard) {
        dashboard.style.display = isLoading ? 'none' : 'block';
    }
}

// Atualizar timestamp
function atualizarTimestamp() {
    const agora = new Date();
    const elemento = document.getElementById('lastUpdate');
    if (elemento) {
        elemento.textContent = agora.toLocaleString('pt-BR');
    }
}

// Criar métricas principais
function criarMetricas(metricas) {
    const container = document.getElementById('metricas');
    if (!container) return;

    container.innerHTML = `
        <div class="metric-card">
            <div class="metric-label">Total de Contratos</div>
            <div class="metric-value">${Formatters.number(metricas.total_contratos)}</div>
            <div class="metric-change positive">
                <span>↗</span> ${metricas.contratos_ativos} ativos
            </div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Valor Total</div>
            <div class="metric-value">${Formatters.currency(metricas.valor_total)}</div>
            <div class="metric-change ${metricas.crescimento_mensal >= 0 ? 'positive' : 'negative'}">
                <span>${metricas.crescimento_mensal >= 0 ? '↗' : '↘'}</span> 
                ${Formatters.percent(Math.abs(metricas.crescimento_mensal))} este mês
            </div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Taxa de Renovação</div>
            <div class="metric-value">${Formatters.percent(metricas.taxa_renovacao)}</div>
            <div class="metric-change positive">
                <span>↗</span> Acima da média
            </div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Inadimplência</div>
            <div class="metric-value">${Formatters.percent(metricas.inadimplencia)}</div>
            <div class="metric-change ${metricas.inadimplencia < 5 ? 'positive' : 'negative'}">
                <span>${metricas.inadimplencia < 5 ? '↘' : '↗'}</span> 
                ${metricas.inadimplencia < 5 ? 'Baixa' : 'Atenção'}
            </div>
        </div>
    `;
}

// Criar indicadores de mercado
function criarIndicadores(indicadores) {
    const container = document.getElementById('indicadores');
    if (!container) return;

    const items = Object.entries(indicadores).map(([key, data]) => {
        const nome = key.toUpperCase().replace('_', ' ');
        const isPositive = data.variacao >= 0;
        const icon = data.tendencia === 'alta' ? '↗' : '↘';
        const colorClass = data.tendencia === 'alta' ? 'positive' : 'negative';
        
        let valorFormatado = data.valor;
        if (key === 'dolar') {
            valorFormatado = `R$ ${data.valor.toFixed(2)}`;
        } else if (key === 'ibovespa') {
            valorFormatado = Formatters.number(data.valor);
        } else {
            valorFormatado = `${Formatters.percent(data.valor)}`;
        }

        return `
            <div class="indicator-card">
                <div class="indicator-name">${nome}</div>
                <div class="indicator-value">${valorFormatado}</div>
                <div class="indicator-change ${colorClass}">
                    <span class="trend-icon">${icon}</span>
                    ${isPositive ? '+' : ''}${Formatters.percent(data.variacao)}
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = items;
}

// Configurações comuns dos gráficos
const ChartConfig = {
    commonOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            tooltip: {
                backgroundColor: '#1e293b',
                titleColor: '#f1f5f9',
                bodyColor: '#f1f5f9',
                borderColor: '#334155',
                borderWidth: 1
            }
        }
    },

    colors: {
        primary: '#3b82f6',
        success: '#10b981',
        warning: '#f59e0b',
        danger: '#ef4444',
        info: '#06b6d4',
        purple: '#8b5cf6',
        pink: '#ec4899'
    }
};

// Criar gráfico de distribuição por status
function criarGraficoStatus(dados) {
    const ctx = document.getElementById('chartStatus');
    if (!ctx) return;

    if (DashboardState.charts.status) {
        DashboardState.charts.status.destroy();
    }
    
    DashboardState.charts.status = new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: dados.map(d => d.status),
            datasets: [{
                data: dados.map(d => d.quantidade),
                backgroundColor: dados.map(d => d.cor),
                borderWidth: 0
            }]
        },
        options: {
            ...ChartConfig.commonOptions,
            plugins: {
                ...ChartConfig.commonOptions.plugins,
                legend: {
                    position: 'bottom',
                    labels: { color: '#94a3b8', padding: 15 }
                }
            }
        }
    });
}

// Criar gráfico de top clientes
function criarGraficoClientes(dados) {
    const ctx = document.getElementById('chartClientes');
    if (!ctx) return;

    if (DashboardState.charts.clientes) {
        DashboardState.charts.clientes.destroy();
    }
    
    DashboardState.charts.clientes = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: dados.map(d => d.cliente),
            datasets: [{
                label: 'Valor (R$)',
                data: dados.map(d => d.valor),
                backgroundColor: 'rgba(59, 130, 246, 0.8)',
                borderRadius: 8
            }]
        },
        options: {
            ...ChartConfig.commonOptions,
            indexAxis: 'y',
            plugins: {
                ...ChartConfig.commonOptions.plugins,
                legend: { display: false },
                tooltip: {
                    ...ChartConfig.commonOptions.plugins.tooltip,
                    callbacks: {
                        label: (context) => Formatters.currency(context.parsed.x)
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: '#334155' },
                    ticks: { 
                        color: '#94a3b8',
                        callback: (value) => Formatters.currency(value)
                    }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });
}

// Criar gráfico de valor por setor
function criarGraficoSetor(dados) {
    const ctx = document.getElementById('chartSetor');
    if (!ctx) return;

    if (DashboardState.charts.setor) {
        DashboardState.charts.setor.destroy();
    }
    
    const cores = [
        ChartConfig.colors.primary,
        ChartConfig.colors.purple,
        ChartConfig.colors.pink,
        ChartConfig.colors.warning,
        ChartConfig.colors.success,
        ChartConfig.colors.info
    ];
    
    DashboardState.charts.setor = new Chart(ctx.getContext('2d'), {
        type: 'pie',
        data: {
            labels: dados.map(d => d.setor),
            datasets: [{
                data: dados.map(d => d.valor),
                backgroundColor: cores,
                borderWidth: 0
            }]
        },
        options: {
            ...ChartConfig.commonOptions,
            plugins: {
                ...ChartConfig.commonOptions.plugins,
                legend: {
                    position: 'bottom',
                    labels: { color: '#94a3b8', padding: 15 }
                },
                tooltip: {
                    ...ChartConfig.commonOptions.plugins.tooltip,
                    callbacks: {
                        label: (context) => {
                            const label = context.label || '';
                            const value = Formatters.currency(context.parsed);
                            return `${label}: ${value}`;
                        }
                    }
                }
            }
        }
    });
}

// Criar gráfico de valor por região
function criarGraficoRegiao(dados) {
    const ctx = document.getElementById('chartRegiao');
    if (!ctx) return;

    if (DashboardState.charts.regiao) {
        DashboardState.charts.regiao.destroy();
    }
    
    DashboardState.charts.regiao = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: dados.map(d => d.regiao),
            datasets: [{
                label: 'Valor (R$)',
                data: dados.map(d => d.valor),
                backgroundColor: 'rgba(139, 92, 246, 0.8)',
                borderRadius: 8
            }]
        },
        options: {
            ...ChartConfig.commonOptions,
            plugins: {
                ...ChartConfig.commonOptions.plugins,
                legend: { display: false },
                tooltip: {
                    ...ChartConfig.commonOptions.plugins.tooltip,
                    callbacks: {
                        label: (context) => Formatters.currency(context.parsed.y)
                    }
                }
            },
            scales: {
                y: {
                    grid: { color: '#334155' },
                    ticks: { 
                        color: '#94a3b8',
                        callback: (value) => Formatters.currency(value)
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });
}

// Criar timeline de vencimentos
function criarTimeline(dados) {
    const ctx = document.getElementById('chartTimeline');
    if (!ctx) return;

    if (DashboardState.charts.timeline) {
        DashboardState.charts.timeline.destroy();
    }
    
    DashboardState.charts.timeline = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: dados.map(d => d.mes),
            datasets: [
                {
                    label: 'Quantidade',
                    data: dados.map(d => d.quantidade),
                    borderColor: ChartConfig.colors.primary,
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    yAxisID: 'y',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Valor (R$)',
                    data: dados.map(d => d.valor),
                    borderColor: ChartConfig.colors.success,
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    yAxisID: 'y1',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            ...ChartConfig.commonOptions,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                ...ChartConfig.commonOptions.plugins,
                legend: {
                    labels: { color: '#94a3b8', padding: 15 }
                },
                tooltip: {
                    ...ChartConfig.commonOptions.plugins.tooltip,
                    callbacks: {
                        label: (context) => {
                            let label = context.dataset.label || '';
                            if (label.includes('Valor')) {
                                label += ': ' + Formatters.currency(context.parsed.y);
                            } else {
                                label += ': ' + context.parsed.y;
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    grid: { color: '#334155' },
                    ticks: { color: '#94a3b8' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    grid: { drawOnChartArea: false },
                    ticks: { 
                        color: '#94a3b8',
                        callback: (value) => Formatters.currency(value)
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });
}

// Criar tabela de comparação por setor
function criarTabelaSetores(dados) {
    const tbody = document.querySelector('#tabelaSetores tbody');
    if (!tbody) return;

    tbody.innerHTML = dados.map(d => `
        <tr>
            <td><strong>${d.setor}</strong></td>
            <td>
                <span class="metric-change ${d.crescimento >= 0 ? 'positive' : 'negative'}">
                    ${d.crescimento >= 0 ? '↗' : '↘'} ${Formatters.percent(Math.abs(d.crescimento))}
                </span>
            </td>
            <td>
                <span class="metric-change ${d.inadimplencia < 5 ? 'positive' : 'negative'}">
                    ${Formatters.percent(d.inadimplencia)}
                </span>
            </td>
            <td>${Formatters.percent(d.renovacao)}</td>
            <td>
                <span class="badge ${
                    d.crescimento >= 10 ? 'badge-success' : 
                    d.crescimento >= 0 ? 'badge-warning' : 
                    'badge-danger'
                }">
                    ${d.crescimento >= 10 ? 'Excelente' : d.crescimento >= 0 ? 'Bom' : 'Atenção'}
                </span>
            </td>
        </tr>
    `).join('');
}

// Renderizar dashboard com os dados
function renderDashboard(data) {
    if (!data) return;

    // Criar todas as visualizações
    if (data.metricas) criarMetricas(data.metricas);
    if (data.indicadores_mercado) criarIndicadores(data.indicadores_mercado);
    if (data.distribuicao_status) criarGraficoStatus(data.distribuicao_status);
    if (data.top_clientes) criarGraficoClientes(data.top_clientes);
    if (data.valor_por_setor) criarGraficoSetor(data.valor_por_setor);
    if (data.valor_por_regiao) criarGraficoRegiao(data.valor_por_regiao);
    if (data.timeline_vencimentos) criarTimeline(data.timeline_vencimentos);
    if (data.comparacao_setores) criarTabelaSetores(data.comparacao_setores);
    
    // Criar seções de IA
    if (data.ai_insights) {
        if (data.ai_insights.alertas) criarSecaoAlertas(data.ai_insights.alertas);
        if (data.ai_insights.score_risco) criarScoreRisco(data.ai_insights.score_risco);
        if (data.ai_insights.analise_metricas) criarInsightsIA(data.ai_insights.analise_metricas);
        if (data.ai_insights.tendencias) criarPrevisoes(data.ai_insights.tendencias);
    }
}

// Carregar dados do dashboard
async function loadDashboardData() {
    console.log('🚀 Iniciando loadDashboardData...');
    
    if (DashboardState.isLoading) {
        console.log('⏳ Já está carregando, ignorando...');
        return;
    }
    
    console.log('📊 Atualizando estado para loading...');
    DashboardState.isLoading = true;
    updateLoadingState(true);

    try {
        console.log('🌐 Chamando apiService.getDashboardData()...');
        console.log('🔧 apiService disponível:', typeof apiService);
        console.log('🔧 getDashboardData disponível:', typeof apiService.getDashboardData);
        
        const data = await apiService.getDashboardData();
        console.log('📋 Resposta da API:', data);
        
        if (data && !data.error) {
            console.log('✅ Dados recebidos com sucesso');
            console.log('📊 Estrutura dos dados:', Object.keys(data));
            
            DashboardState.currentData = data;
            DashboardState.aiInsights = data.ai_insights;
            
            console.log('🎨 Renderizando dashboard...');
            renderDashboard(data);
            atualizarTimestamp();
            
            console.log('✅ Dashboard renderizado com sucesso!');
        } else {
            console.error('❌ Erro nos dados:', data);
            throw new Error(data?.error?.message || 'Dados inválidos recebidos');
        }
    } catch (error) {
        console.error('💥 Erro em loadDashboardData:', error);
        console.error('📍 Stack trace:', error.stack);
        
        // Tentar usar dados mock se a API falhar
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            console.log('🔄 API falhou, usando dados mock...');
            try {
                const mockData = getMockData();
                renderDashboard(mockData);
                atualizarTimestamp();
                console.log('✅ Dashboard renderizado com dados mock!');
            } catch (mockError) {
                console.error('💥 Erro ao usar dados mock:', mockError);
            }
        }
        
        errorHandler.handle(error, 'Erro ao carregar dados do dashboard');
    } finally {
        console.log('🏁 Finalizando carregamento...');
        DashboardState.isLoading = false;
        updateLoadingState(false);
    }
}

// Dados mock para fallback
function getMockData() {
    return {
        metricas: {
            total_contratos: 150,
            valor_total: 1500000,
            contratos_ativos: 120,
            crescimento_mensal: 5.2,
            taxa_renovacao: 85,
            inadimplencia: 3.1
        },
        indicadores_mercado: {
            dolar: { valor: 5.25, variacao: 0.5, tendencia: 'alta' },
            selic: { valor: 13.25, variacao: 0, tendencia: 'estavel' },
            ibovespa: { valor: 120000, variacao: 2.1, tendencia: 'alta' }
        },
        distribuicao_status: [
            { status: 'Ativo', quantidade: 120, cor: '#10b981' },
            { status: 'Pendente', quantidade: 20, cor: '#f59e0b' },
            { status: 'Cancelado', quantidade: 10, cor: '#ef4444' }
        ],
        top_clientes: [
            { cliente: 'Tech Solutions Ltda', valor: 500000 },
            { cliente: 'Consultoria Empresarial', valor: 350000 },
            { cliente: 'Comércio Variejista ME', valor: 200000 }
        ],
        valor_por_setor: [
            { setor: 'Tecnologia', valor: 800000 },
            { setor: 'Consultoria', valor: 450000 },
            { setor: 'Varejo', valor: 250000 }
        ],
        valor_por_regiao: [
            { regiao: 'São Paulo', valor: 900000 },
            { regiao: 'Rio de Janeiro', valor: 400000 },
            { regiao: 'Minas Gerais', valor: 200000 }
        ],
        timeline_vencimentos: [
            { data: '2024-12-01', valor: 150000, contratos: 3 },
            { data: '2024-12-15', valor: 200000, contratos: 4 },
            { data: '2025-01-01', valor: 300000, contratos: 5 }
        ],
        comparacao_setores: [
            { setor: 'Tecnologia', contratos: 45, valor: 800000, ticket_medio: 17778, crescimento: 12.5 },
            { setor: 'Consultoria', contratos: 30, valor: 450000, ticket_medio: 15000, crescimento: 8.3 },
            { setor: 'Varejo', contratos: 25, valor: 250000, ticket_medio: 10000, crescimento: -2.1 }
        ],
        ai_insights: {
            alertas: [
                { tipo: 'warning', mensagem: '3 contratos vencem esta semana' },
                { tipo: 'info', mensagem: 'Novo cliente potencial identificado' }
            ],
            score_risco: { pontuacao: 75, nivel: 'Moderado' },
            analise_metricas: 'As métricas indicam crescimento saudável...',
            tendencias: 'Projeção de aumento de 10% no próximo trimestre...'
        }
    };
}

// Criar seção de alertas
function criarSecaoAlertas(alertas) {
    const container = document.getElementById('alertasIA');
    if (!container || !alertas || alertas.length === 0) return;
    
    container.innerHTML = alertas.map(alerta => `
        <div class="alert-card alert-${alerta.severidade.toLowerCase()}">
            <div class="alert-header">
                <span class="alert-icon">${alerta.icone}</span>
                <div class="alert-title">${alerta.titulo}</div>
                <span class="badge badge-${alerta.severidade === 'Alta' ? 'danger' : 'warning'}">
                    ${alerta.severidade}
                </span>
            </div>
            <div class="alert-message">${alerta.mensagem}</div>
            <div class="alert-action">
                <strong>Ação sugerida:</strong> ${alerta.acao_sugerida}
            </div>
        </div>
    `).join('');
}

// Criar score de risco
function criarScoreRisco(scoreData) {
    const container = document.getElementById('scoreRisco');
    if (!container || !scoreData) return;
    
    container.innerHTML = `
        <div class="risk-score-card">
            <div class="risk-score-header">
                <h3>Score de Risco do Portfólio</h3>
            </div>
            <div class="risk-score-value ${scoreData.cor}">
                <div class="score-number">${scoreData.score}</div>
                <div class="score-label">${scoreData.classificacao}</div>
            </div>
            <div class="risk-factors">
                <div class="factor">
                    <span class="factor-label">Inadimplência</span>
                    <div class="factor-bar">
                        <div class="factor-fill" style="width: ${Formatters.percent(scoreData.fatores.inadimplencia)}"></div>
                    </div>
                    <span class="factor-value">${scoreData.fatores.inadimplencia}</span>
                </div>
                <div class="factor">
                    <span class="factor-label">Renovação</span>
                    <div class="factor-bar">
                        <div class="factor-fill" style="width: ${Formatters.percent(scoreData.fatores.renovacao)}"></div>
                    </div>
                    <span class="factor-value">${scoreData.fatores.renovacao}</span>
                </div>
                <div class="factor">
                    <span class="factor-label">Crescimento</span>
                    <div class="factor-bar">
                        <div class="factor-fill" style="width: ${Formatters.percent(scoreData.fatores.crescimento)}"></div>
                    </div>
                    <span class="factor-value">${scoreData.fatores.crescimento}</span>
                </div>
            </div>
            <div class="risk-recommendation">
                <strong>Recomendação:</strong> ${scoreData.recomendacao}
            </div>
        </div>
    `;
}

// Criar insights de IA
function criarInsightsIA(analise) {
    const container = document.getElementById('insightsIA');
    if (!container || !analise) return;
    
    container.innerHTML = `
        <div class="insights-card">
            <h3>🤖 Análise Inteligente</h3>
            <div class="insight-section">
                <h4>Análise Geral</h4>
                <p>${analise.analise || 'Análise não disponível'}</p>
            </div>
            ${analise.pontos_atencao && analise.pontos_atencao.length > 0 ? `
                <div class="insight-section">
                    <h4>⚠️ Pontos de Atenção</h4>
                    <ul>
                        ${analise.pontos_atencao.map(ponto => `<li>${ponto}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            ${analise.recomendacoes && analise.recomendacoes.length > 0 ? `
                <div class="insight-section">
                    <h4>💡 Recomendações</h4>
                    <ul>
                        ${analise.recomendacoes.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
    `;
}

// Criar previsões
function criarPrevisoes(tendencias) {
    const container = document.getElementById('previsoesIA');
    if (!container || !tendencias) return;
    
    const previsao = tendencias.previsao_proximo_mes;
    if (!previsao) return;
    
    container.innerHTML = `
        <div class="forecast-card">
            <h3>🔮 Previsões</h3>
            <div class="forecast-grid">
                <div class="forecast-item">
                    <div class="forecast-label">Próximo Mês - Valor</div>
                    <div class="forecast-value">${Formatters.currency(previsao.valor)}</div>
                    <div class="forecast-trend ${tendencias.tendencia_valor}">
                        ${tendencias.tendencia_valor === 'crescente' ? '↗' : '↘'} ${tendencias.tendencia_valor}
                    </div>
                </div>
                <div class="forecast-item">
                    <div class="forecast-label">Próximo Mês - Quantidade</div>
                    <div class="forecast-value">${previsao.quantidade}</div>
                    <div class="forecast-trend ${tendencias.tendencia_quantidade}">
                        ${tendencias.tendencia_quantidade === 'crescente' ? '↗' : '↘'} ${tendencias.tendencia_quantidade}
                    </div>
                </div>
            </div>
            <div class="forecast-note">
                <small>Confiança: ${tendencias.confianca} | ${tendencias.observacao}</small>
            </div>
        </div>
    `;
}

// Analisar gráfico com IA
async function analisarGrafico(tipo, dados) {
    try {
        const response = await fetch('/api/analisar-grafico', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ tipo, dados })
        });
        
        if (!response.ok) throw new Error('Erro na análise');
        
        const result = await response.json();
        mostrarAnaliseGrafico(tipo, result.analise);
        
    } catch (error) {
        console.error('Erro ao analisar gráfico:', error);
    }
}

// Mostrar análise do gráfico
function mostrarAnaliseGrafico(tipo, analise) {
    const modal = document.getElementById('modalAnalise');
    const conteudo = document.getElementById('analiseConteudo');
    
    if (modal && conteudo) {
        conteudo.innerHTML = `
            <h3>Análise: ${tipo}</h3>
            <p>${analise}</p>
        `;
        modal.style.display = 'block';
    }
}

// Perguntar sobre dados
async function perguntarDados() {
    const input = document.getElementById('perguntaIA');
    const pergunta = input ? input.value.trim() : '';
    
    if (!pergunta) return;
    
    const btnPerguntar = document.getElementById('btnPerguntar');
    if (btnPerguntar) {
        btnPerguntar.disabled = true;
        btnPerguntar.textContent = 'Analisando...';
    }
    
    try {
        const response = await fetch('/api/perguntar-dados', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ pergunta })
        });
        
        if (!response.ok) throw new Error('Erro ao processar pergunta');
        
        const result = await response.json();
        mostrarRespostaPergunta(pergunta, result.resposta);
        
        if (input) input.value = '';
        
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao processar sua pergunta. Tente novamente.');
    } finally {
        if (btnPerguntar) {
            btnPerguntar.disabled = false;
            btnPerguntar.textContent = 'Perguntar';
        }
    }
}

// Mostrar resposta da pergunta
function mostrarRespostaPergunta(pergunta, resposta) {
    const container = document.getElementById('respostasIA');
    if (!container) return;
    
    const div = document.createElement('div');
    div.className = 'qa-item';
    div.innerHTML = `
        <div class="question">
            <strong>Você:</strong> ${pergunta}
        </div>
        <div class="answer">
            <strong>IA:</strong> ${resposta}
        </div>
    `;
    
    container.insertBefore(div, container.firstChild);
}

// Atualizar dados manualmente
function atualizarDados() {
    loadDashboardData();
}

// Limpar recursos ao sair
function cleanup() {
    if (DashboardState.updateInterval) {
        clearInterval(DashboardState.updateInterval);
    }
    
    Object.values(DashboardState.charts).forEach(chart => {
        if (chart && typeof chart.destroy === 'function') {
            chart.destroy();
        }
    });
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();
    
    // Atualizar a cada 30 segundos
    DashboardState.updateInterval = setInterval(atualizarDados, CONSTANTS.INTERVALS.DASHBOARD_REFRESH);
});

// Limpar ao sair da página
window.addEventListener('beforeunload', cleanup);

// Exportar funções para uso em outros módulos
export {
    DashboardState,
    loadDashboardData,
    atualizarTimestamp,
    renderDashboard,
    updateLoadingState
};