/**
 * Constantes da aplicação
 * Centraliza valores fixos e magic numbers
 */

export const CONSTANTS = {
    // Intervalos de tempo (em milissegundos)
    INTERVALS: {
        DASHBOARD_REFRESH: 5 * 60 * 1000, // 5 minutos
        CHART_ANIMATION: 1000,
        LOADING_DELAY: 300,
        NOTIFICATION_DURATION: 5000
    },

    // Limites
    LIMITS: {
        MAX_DATA_POINTS: 1000,
        MAX_CACHE_SIZE: 50,
        MAX_ERROR_HISTORY: 50,
        MAX_VISIBLE_NOTIFICATIONS: 5
    },

    // Status
    STATUS: {
        CONTRACT: {
            ACTIVE: 'Ativo',
            PENDING: 'Pendente',
            CANCELLED: 'Cancelado',
            EXPIRED: 'Expirado'
        },
        NOTIFICATION: {
            INFO: 'info',
            WARNING: 'warning',
            ERROR: 'error',
            SUCCESS: 'success'
        }
    },

    // Mensagens padrão
    MESSAGES: {
        LOADING: 'Carregando...',
        ERROR_DEFAULT: 'Ocorreu um erro inesperado',
        NETWORK_ERROR: 'Erro de conexão',
        EMPTY_DATA: 'Nenhum dado encontrado'
    },

    // Selectores CSS
    SELECTORS: {
        LOADING: '#loading',
        DASHBOARD: '#dashboard',
        METRICS: '#metricas',
        CHARTS: {
            STATUS: '#chartStatus',
            CLIENTS: '#chartClientes',
            SECTOR: '#chartSetor',
            REGION: '#chartRegiao',
            TIMELINE: '#chartTimeline'
        }
    }
};

export default CONSTANTS;
