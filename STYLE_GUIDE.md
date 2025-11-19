# 🎨 Guia de Estilo de Código

## Python

### Formatação

```python
# ✅ BOM
def calcular_total_contratos(contratos: list[dict]) -> float:
    """
    Calcula o valor total dos contratos.
    
    Args:
        contratos: Lista de dicionários com dados dos contratos
        
    Returns:
        Valor total em float
    """
    return sum(c['valor'] for c in contratos)


# ❌ RUIM
def calc(c):
    return sum(c['valor'] for c in c)
```

### Convenções

- **Indentação**: 4 espaços
- **Linha máxima**: 100 caracteres
- **Imports**: Agrupados e ordenados
- **Docstrings**: Google style
- **Type hints**: Sempre que possível

### Imports

```python
# ✅ BOM - Ordem correta
import os
import sys
from datetime import datetime

from flask import Flask, render_template
from dotenv import load_dotenv

from models import User, Contract
from utils import formatar_moeda
```

## JavaScript

### Formatação

```javascript
// ✅ BOM
function criarGrafico(dados) {
    const ctx = document.getElementById('chart');
    if (!ctx) return;
    
    const chart = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: dados
    });
    
    return chart;
}

// ❌ RUIM
function criarGrafico(dados){
const ctx=document.getElementById('chart')
return new Chart(ctx.getContext('2d'),{type:'bar',data:dados})
}
```

### Convenções

- **Indentação**: 4 espaços
- **Ponto e vírgula**: Sempre
- **Aspas**: Simples para strings
- **Const/Let**: Nunca var
- **Arrow functions**: Preferir quando apropriado

### Nomenclatura

```javascript
// ✅ BOM
const DashboardState = {
    charts: {},
    isLoading: false
};

function atualizarDados() {
    // ...
}

const TAXA_MAXIMA = 100;

// ❌ RUIM
var dashboard_state = {
    Charts: {},
    is_loading: false
};

function AtualizarDados() {
    // ...
}
```

## CSS

### Formatação

```css
/* ✅ BOM */
.metric-card {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 24px;
    border: 1px solid var(--border);
    transition: all 0.3s;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

/* ❌ RUIM */
.metric-card{background:var(--bg-card);border-radius:16px;padding:24px}
.metric-card:hover{transform:translateY(-4px)}
```

### Convenções

- **Indentação**: 4 espaços
- **Nomenclatura**: kebab-case
- **Ordem**: Alfabética dentro do bloco
- **Variáveis CSS**: Usar custom properties
- **Comentários**: Descrever seções

### Ordem de Propriedades

```css
.elemento {
    /* Posicionamento */
    position: relative;
    top: 0;
    left: 0;
    z-index: 1;
    
    /* Display & Box Model */
    display: flex;
    flex-direction: column;
    width: 100%;
    height: auto;
    margin: 0;
    padding: 20px;
    
    /* Tipografia */
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: var(--text-primary);
    
    /* Visual */
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    
    /* Animação */
    transition: all 0.3s;
}
```

## HTML

### Formatação

```html
<!-- ✅ BOM -->
<div class="metric-card">
    <div class="metric-label">Total de Contratos</div>
    <div class="metric-value">120</div>
    <div class="metric-change positive">
        <span>↗</span> 15% este mês
    </div>
</div>

<!-- ❌ RUIM -->
<div class="metric-card"><div class="metric-label">Total de Contratos</div><div class="metric-value">120</div></div>
```

### Convenções

- **Indentação**: 4 espaços
- **Atributos**: Aspas duplas
- **Semântica**: Usar tags apropriadas
- **Acessibilidade**: ARIA labels quando necessário
- **Comentários**: Descrever seções

## Comentários

### Python

```python
# ✅ BOM
def processar_dados(dados: list) -> dict:
    """
    Processa e agrega dados de contratos.
    
    Args:
        dados: Lista de contratos brutos
        
    Returns:
        Dicionário com dados agregados
        
    Raises:
        ValueError: Se dados estiverem vazios
    """
    if not dados:
        raise ValueError("Dados não podem estar vazios")
    
    # Filtra apenas contratos ativos
    ativos = [d for d in dados if d['status'] == 'ativo']
    
    return {
        'total': len(ativos),
        'valor': sum(d['valor'] for d in ativos)
    }
```

### JavaScript

```javascript
// ✅ BOM
/**
 * Cria um gráfico de barras com os dados fornecidos
 * @param {Array} dados - Array de objetos com dados do gráfico
 * @param {string} elementId - ID do elemento canvas
 * @returns {Chart} Instância do Chart.js
 */
function criarGraficoBarras(dados, elementId) {
    const ctx = document.getElementById(elementId);
    
    // Verifica se o elemento existe
    if (!ctx) {
        console.error(`Elemento ${elementId} não encontrado`);
        return null;
    }
    
    // Cria e retorna o gráfico
    return new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: dados
    });
}
```

### CSS

```css
/* ✅ BOM */

/* ==========================================================================
   Métricas - Cards de métricas principais
   ========================================================================== */

.metric-card {
    /* Card container com efeito de elevação */
    background: var(--bg-card);
    border-radius: 16px;
}

.metric-card:hover {
    /* Efeito de hover - eleva o card */
    transform: translateY(-4px);
}
```

## Estrutura de Arquivos

### Python

```python
"""
Módulo de utilitários para o dashboard.

Este módulo contém funções auxiliares para geração de dados
e formatação de valores.
"""

# Imports padrão
import os
import sys
from datetime import datetime

# Imports de terceiros
from flask import Flask
from dotenv import load_dotenv

# Imports locais
from models import Contract
from config import Config

# Constantes
TAXA_MAXIMA = 100
VALOR_MINIMO = 1000

# Classes
class DataGenerator:
    """Gerador de dados mock para o dashboard."""
    pass

# Funções
def formatar_moeda(valor: float) -> str:
    """Formata valor como moeda brasileira."""
    pass

# Main
if __name__ == "__main__":
    pass
```

### JavaScript

```javascript
/**
 * Dashboard - Gerenciamento de gráficos e visualizações
 * @module dashboard
 */

// Estado global
const DashboardState = {
    charts: {},
    isLoading: false
};

// Constantes
const COLORS = {
    primary: '#3b82f6',
    success: '#10b981'
};

// Utilitários
const Formatters = {
    moeda: (valor) => { /* ... */ },
    numero: (valor) => { /* ... */ }
};

// Funções principais
function carregarDados() {
    // ...
}

function criarGraficos() {
    // ...
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    carregarDados();
});
```

## Boas Práticas Gerais

### DRY (Don't Repeat Yourself)

```javascript
// ❌ RUIM
function formatarValor1(valor) {
    return `R$ ${valor.toFixed(2)}`;
}

function formatarValor2(valor) {
    return `R$ ${valor.toFixed(2)}`;
}

// ✅ BOM
const Formatters = {
    moeda: (valor) => `R$ ${valor.toFixed(2)}`
};
```

### Single Responsibility

```python
# ❌ RUIM
def processar_e_salvar_dados(dados):
    # Processa
    processados = [d * 2 for d in dados]
    # Salva
    with open('dados.txt', 'w') as f:
        f.write(str(processados))
    return processados

# ✅ BOM
def processar_dados(dados):
    return [d * 2 for d in dados]

def salvar_dados(dados, arquivo):
    with open(arquivo, 'w') as f:
        f.write(str(dados))
```

### Error Handling

```javascript
// ❌ RUIM
async function carregarDados() {
    const response = await fetch('/api/data');
    const data = await response.json();
    return data;
}

// ✅ BOM
async function carregarDados() {
    try {
        const response = await fetch('/api/data');
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        throw error;
    }
}
```

## Checklist de Qualidade

Antes de commitar código, verifique:

- [ ] Código está formatado corretamente
- [ ] Nomes são descritivos e claros
- [ ] Funções têm uma única responsabilidade
- [ ] Comentários explicam o "porquê", não o "o quê"
- [ ] Não há código duplicado
- [ ] Tratamento de erros está implementado
- [ ] Código está testado
- [ ] Sem console.log ou print desnecessários
- [ ] Variáveis não utilizadas foram removidas
- [ ] Imports estão organizados

---

**Mantenha o código limpo, organizado e profissional!** 🚀