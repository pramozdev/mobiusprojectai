# 📊 Dashboard Avançado - Documentação

## Visão Geral

O Dashboard Avançado é uma interface completa de análise e visualização de dados para gestão de contratos, oferecendo métricas em tempo real, gráficos interativos e indicadores de mercado.

## 🎯 Recursos Principais

### 1. Métricas Principais

Quatro cards principais exibindo:
- **Total de Contratos**: Quantidade total de contratos ativos
- **Valor Total**: Soma de todos os valores de contratos
- **Taxa de Renovação**: Percentual de contratos renovados
- **Inadimplência**: Índice de inadimplência atual

Cada métrica inclui:
- ✅ Valor principal em destaque
- ✅ Indicador de tendência (alta/baixa)
- ✅ Variação percentual
- ✅ Cores dinâmicas baseadas em performance

### 2. Gráficos Interativos

#### 📊 Distribuição por Status
- **Tipo**: Gráfico de rosca (doughnut)
- **Dados**: Quantidade de contratos por status (Ativo, Pendente, Vencido, Renovado, Cancelado)
- **Recursos**: 
  - Cores personalizadas por status
  - Tooltips informativos
  - Legenda interativa

#### 👥 Top 5 Clientes
- **Tipo**: Gráfico de barras horizontal
- **Dados**: Clientes com maior valor em contratos
- **Recursos**:
  - Valores formatados em R$
  - Ordenação automática
  - Barras com bordas arredondadas

#### 🏢 Valor por Setor
- **Tipo**: Gráfico de pizza
- **Dados**: Distribuição de valores por setor econômico
- **Setores**: Tecnologia, Indústria, Comércio, Serviços, Saúde, Educação
- **Recursos**:
  - Cores vibrantes e distintas
  - Percentuais automáticos
  - Tooltips com valores detalhados

#### 🗺️ Valor por Região
- **Tipo**: Gráfico de barras vertical
- **Dados**: Distribuição geográfica dos contratos
- **Regiões**: Sudeste, Sul, Nordeste, Centro-Oeste, Norte
- **Recursos**:
  - Comparação visual rápida
  - Valores em moeda brasileira
  - Animações suaves

#### 📅 Timeline de Vencimentos
- **Tipo**: Gráfico de linha dupla
- **Período**: Próximos 12 meses
- **Dados**: 
  - Linha azul: Quantidade de vencimentos
  - Linha verde: Valor total dos vencimentos
- **Recursos**:
  - Dois eixos Y (quantidade e valor)
  - Área preenchida
  - Interação por índice
  - Zoom e pan

### 3. Indicadores de Mercado

Painel com 6 indicadores econômicos em tempo real:

| Indicador | Descrição |
|-----------|-----------|
| **Taxa de Juros** | Taxa Selic atual |
| **IPCA** | Índice de Preços ao Consumidor Amplo |
| **IGPM** | Índice Geral de Preços do Mercado |
| **CDI** | Certificado de Depósito Interbancário |
| **Dólar** | Cotação USD/BRL |
| **Ibovespa** | Índice da Bolsa de Valores |

Cada indicador mostra:
- ✅ Valor atual
- ✅ Variação percentual
- ✅ Tendência (alta/baixa)
- ✅ Ícone de direção
- ✅ Cores dinâmicas

### 4. Comparação por Setor

Tabela interativa com análise detalhada por setor:

**Colunas:**
- Setor
- Crescimento (%)
- Inadimplência (%)
- Taxa de Renovação (%)
- Status (badge colorido)

**Recursos:**
- Ordenação por coluna
- Badges de status (Excelente, Bom, Atenção)
- Hover effects
- Indicadores visuais de tendência

## 🎨 Design e UX

### Tema Escuro Moderno
- Fundo gradiente escuro (#0f172a → #1e293b)
- Cards com bordas sutis
- Tipografia Inter (Google Fonts)
- Cores vibrantes para dados

### Responsividade
- ✅ Desktop (1600px+): Layout completo em grid
- ✅ Tablet (768px-1200px): Grid adaptativo
- ✅ Mobile (<768px): Layout em coluna única

### Interatividade
- Tooltips informativos em todos os gráficos
- Animações suaves (0.3s transitions)
- Hover effects em cards
- Loading states
- Atualização automática a cada 30 segundos

## 🔄 Atualização de Dados

### Automática
- **Intervalo**: 30 segundos
- **Método**: Polling via JavaScript
- **Feedback**: Timestamp de última atualização

### Manual
- Botão "🔄 Atualizar" no header
- Feedback visual durante atualização (opacity)
- Preserva estado dos gráficos

## 📡 API Endpoints

### GET `/api/dashboard`

Retorna todos os dados do dashboard em formato JSON.

**Response:**
```json
{
  "metricas": {
    "total_contratos": 120,
    "valor_total": 1500000.00,
    "taxa_renovacao": 85.5,
    "inadimplencia": 3.2,
    "contratos_ativos": 95,
    "contratos_pendentes": 12,
    "crescimento_mensal": 8.5
  },
  "distribuicao_status": [...],
  "top_clientes": [...],
  "valor_por_setor": [...],
  "valor_por_regiao": [...],
  "timeline_vencimentos": [...],
  "mapa_calor": [...],
  "indicadores_mercado": {...},
  "comparacao_setores": [...]
}
```

## 🚀 Como Usar

### Acesso
1. Inicie o servidor: `python app.py`
2. Acesse: `http://localhost:5000/dashboard`
3. Ou clique no botão "📊 Dashboard Avançado" na página principal

### Navegação
- **Voltar**: Botão no header retorna à página principal
- **Atualizar**: Recarrega todos os dados
- **Scroll**: Navegue pelas seções do dashboard

### Interação com Gráficos
- **Hover**: Veja detalhes em tooltips
- **Click na Legenda**: Oculte/mostre datasets
- **Mobile**: Toque para interagir

## 🛠️ Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Gráficos**: Chart.js 4.x
- **Backend**: Flask (Python)
- **Dados**: Mock data gerado dinamicamente

## 📊 Estrutura de Dados

### Formato das Métricas
```javascript
{
  total_contratos: Number,
  valor_total: Float,
  taxa_renovacao: Float,
  inadimplencia: Float,
  contratos_ativos: Number,
  contratos_pendentes: Number,
  crescimento_mensal: Float
}
```

### Formato dos Gráficos
```javascript
// Distribuição por Status
[
  { status: String, quantidade: Number, cor: String }
]

// Top Clientes
[
  { cliente: String, valor: Float }
]

// Timeline
[
  { mes: String, quantidade: Number, valor: Float }
]
```

## 🎯 Casos de Uso

1. **Análise Executiva**: Visão rápida de métricas-chave
2. **Planejamento Financeiro**: Timeline de vencimentos
3. **Análise de Risco**: Inadimplência por setor
4. **Gestão Regional**: Distribuição geográfica
5. **Monitoramento de Mercado**: Indicadores econômicos

## 🔮 Funcionalidades Futuras

- [ ] Exportar dados para Excel/PDF
- [ ] Filtros por período
- [ ] Comparação de períodos
- [ ] Alertas personalizados
- [ ] Integração com banco de dados real
- [ ] Gráfico de mapa de calor
- [ ] Drill-down em gráficos
- [ ] Dashboards personalizáveis
- [ ] Modo claro/escuro toggle
- [ ] Compartilhamento de relatórios

## 📝 Notas Técnicas

### Performance
- Gráficos otimizados com Chart.js
- Lazy loading de dados
- Debounce em atualizações
- Cleanup de recursos ao sair

### Compatibilidade
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Acessibilidade
- Cores com contraste adequado
- Labels descritivos
- Navegação por teclado (em desenvolvimento)
- ARIA labels (em desenvolvimento)

## 🐛 Troubleshooting

### Gráficos não aparecem
- Verifique console do navegador
- Confirme que Chart.js foi carregado
- Verifique conexão com API

### Dados não atualizam
- Verifique se o servidor está rodando
- Confirme endpoint `/api/dashboard`
- Veja logs do servidor

### Layout quebrado
- Limpe cache do navegador
- Verifique resolução da tela
- Teste em modo responsivo

## 📧 Suporte

Para dúvidas ou problemas:
1. Consulte esta documentação
2. Verifique logs do servidor
3. Abra uma issue no repositório

---

**Versão**: 1.0.0  
**Última atualização**: 2024  
**Desenvolvido com** ❤️ **para gestão eficiente de contratos**