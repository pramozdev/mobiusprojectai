/**
 * Dashboard Avançado - JavaScript
 * Gerenciamento de gráficos e dados do dashboard
 */

// Estado global
const DashboardState = {
    charts: {},
    updateInterval: null,
    isLoading: false,
    aiInsights: null,
    currentData: null
};

// Utilitários de formatação
const Formatters = {
    moeda: (valor) => {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(valor);
    },

    numero: (valor) => {
        return new Intl.NumberFormat('pt-BR').format(valor);
    },

    percentual: (valor) => {
        return `${valor.toFixed(2)}%`;
    }
};

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
            <div class="metric-value">${Formatters.numero(metricas.total_contratos)}</div>
            <div class="metric-change positive">
                <span>↗</span> ${metricas.contratos_ativos} ativos
            </div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Valor Total</div>
            <div class="metric-value">${Formatters.moeda(metricas.valor_total)}</div>
            <div class="metric-change ${metricas.crescimento_mensal >= 0 ? 'positive' : 'negative'}">
                <span>${metricas.crescimento_mensal >= 0 ? '↗' : '↘'}</span> 
                ${Math.abs(metricas.crescimento_mensal)}% este mês
            </div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Taxa de Renovação</div>
            <div class="metric-value">${metricas.taxa_renovacao}%</div>
            <div class="metric-change positive">
                <span>↗</span> Acima da média
            </div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Inadimplência</div>
            <div class="metric-value">${metricas.inadimplencia}%</div>
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
            valorFormatado = Formatters.numero(data.valor);
        } else {
            valorFormatado = `${data.valor}%`;
        }

        return `
            <div class="indicator-card">
                <div class="indicator-name">${nome}</div>
                <div class="indicator-value">${valorFormatado}</div>
                <div class="indicator-change ${colorClass}">
                    <span class="trend-icon">${icon}</span>
                    ${isPositive ? '+' : ''}${data.variacao}%
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
                        label: (context) => Formatters.moeda(context.parsed.x)
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: '#334155' },
                    ticks: { 
                        color: '#94a3b8',
                        callback: (value) => Formatters.moeda(value)
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
                            const value = Formatters.moeda(context.parsed);
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
                        label: (context) => Formatters.moeda(context.parsed.y)
                    }
                }
            },
            scales: {
                y: {
                    grid: { color: '#334155' },
                    ticks: { 
                        color: '#94a3b8',
                        callback: (value) => Formatters.moeda(value)
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
                                label += ': ' + Formatters.moeda(context.parsed.y);
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
                        callback: (value) => Formatters.moeda(value)
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
                    ${d.crescimento >= 0 ? '↗' : '↘'} ${Math.abs(d.crescimento)}%
                </span>
            </td>
            <td>
                <span class="metric-change ${d.inadimplencia < 5 ? 'positive' : 'negative'}">
                    ${d.inadimplencia}%
                </span>
            </td>
            <td>${d.renovacao}%</td>
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

// Carregar dados do dashboard
async function carregarDados() {
    if (DashboardState.isLoading) return;
    
    DashboardState.isLoading = true;
    
    try {
        const response = await fetch('/api/dashboard');
        if (!response.ok) {
            throw new Error('Erro ao carregar dados');
        }
        
        const data = await response.json();
        DashboardState.currentData = data;
        DashboardState.aiInsights = data.ai_insights;
        
        // Criar todas as visualizações
        criarMetricas(data.metricas);
        criarIndicadores(data.indicadores_mercado);
        criarGraficoStatus(data.distribuicao_status);
        criarGraficoClientes(data.top_clientes);
        criarGraficoSetor(data.valor_por_setor);
        criarGraficoRegiao(data.valor_por_regiao);
        criarTimeline(data.timeline_vencimentos);
        criarTabelaSetores(data.comparacao_setores);
        
        // Criar seções de IA
        if (data.ai_insights) {
            criarSecaoAlertas(data.ai_insights.alertas);
            criarScoreRisco(data.ai_insights.score_risco);
            criarInsightsIA(data.ai_insights.analise_metricas);
            criarPrevisoes(data.ai_insights.tendencias);
        }
        
        // Mostrar dashboard e ocultar loading
        const loading = document.getElementById('loading');
        const dashboard = document.getElementById('dashboard');
        
        if (loading) loading.style.display = 'none';
        if (dashboard) dashboard.style.display = 'block';
        
        atualizarTimestamp();
        
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        const loading = document.getElementById('loading');
        if (loading) {
            loading.innerHTML = `
                <p style="color: var(--danger);">❌ Erro ao carregar dados. Tente novamente.</p>
                <button class="btn btn-primary" onclick="carregarDados()">Tentar Novamente</button>
            `;
        }
    } finally {
        DashboardState.isLoading = false;
    }
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
                        <div class="factor-fill" style="width: ${scoreData.fatores.inadimplencia}%"></div>
                    </div>
                    <span class="factor-value">${scoreData.fatores.inadimplencia}</span>
                </div>
                <div class="factor">
                    <span class="factor-label">Renovação</span>
                    <div class="factor-bar">
                        <div class="factor-fill" style="width: ${scoreData.fatores.renovacao}%"></div>
                    </div>
                    <span class="factor-value">${scoreData.fatores.renovacao}</span>
                </div>
                <div class="factor">
                    <span class="factor-label">Crescimento</span>
                    <div class="factor-bar">
                        <div class="factor-fill" style="width: ${scoreData.fatores.crescimento}%"></div>
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
                    <div class="forecast-value">${Formatters.moeda(previsao.valor)}</div>
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
    const dashboard = document.getElementById('dashboard');
    if (dashboard) {
        dashboard.style.opacity = '0.5';
    }
    
    carregarDados().then(() => {
        if (dashboard) {
            dashboard.style.opacity = '1';
        }
    });
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
    carregarDados();
    
    // Atualizar a cada 30 segundos
    DashboardState.updateInterval = setInterval(atualizarDados, 30000);
});

// Limpar ao sair da página
window.addEventListener('beforeunload', cleanup);