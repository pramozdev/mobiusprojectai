/**
 * Configurações da aplicação
 * Centraliza todas as configurações e constantes
 */

export const config = {
    // Configurações da API
    api: {
        baseUrl: '', // URL base da API
        timeout: 30000, // 30 segundos
        retries: 2,
        retryDelay: 1000 // 1 segundo
    },

    // Configurações do Dashboard
    dashboard: {
        refreshInterval: 5 * 60 * 1000, // 5 minutos
        maxDataPoints: 1000,
        chartAnimationDuration: 1000,
        loadingDelay: 300 // delay mínimo para mostrar loading
    },

    // Cores do tema
    theme: {
        colors: {
            primary: '#3b82f6',
            success: '#10b981',
            warning: '#f59e0b',
            danger: '#ef4444',
            info: '#06b6d4',
            purple: '#8b5cf6',
            pink: '#ec4899',
            gray: {
                50: '#f9fafb',
                100: '#f3f4f6',
                200: '#e5e7eb',
                300: '#d1d5db',
                400: '#9ca3af',
                500: '#6b7280',
                600: '#4b5563',
                700: '#374151',
                800: '#1f2937',
                900: '#111827'
            }
        },
        breakpoints: {
            sm: '640px',
            md: '768px',
            lg: '1024px',
            xl: '1280px',
            '2xl': '1536px'
        }
    },

    // Configurações de cache
    cache: {
        duration: 5 * 60 * 1000, // 5 minutos
        maxSize: 50 // número máximo de itens em cache
    },

    // Configurações de notificações
    notifications: {
        duration: 5000, // 5 segundos
        position: 'top-right',
        maxVisible: 5
    },

    // Configurações de desenvolvimento
    development: {
        enableDebugMode: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1',
        logApiCalls: false,
        showPerformanceMetrics: false
    },

    // Configurações de gráficos
    charts: {
        defaultOptions: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom'
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#333',
                    borderWidth: 1
                }
            }
        },
        colors: [
            '#3b82f6', '#10b981', '#f59e0b', '#ef4444', 
            '#06b6d4', '#8b5cf6', '#ec4899', '#6366f1'
        ]
    },

    // Configurações de animação
    animations: {
        duration: 300,
        easing: 'ease-in-out'
    }
};

// Configurações específicas do ambiente
export const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
export const isProduction = !isDevelopment;

// Exporta configurações padrão
export default config;
