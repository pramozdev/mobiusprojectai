/**
 * Ponto de entrada principal da aplicação
 * Inicializa todos os módulos e configurações
 */

import { config } from './config.js';
import { errorHandler } from './utils/errorHandler.js';
import { Formatters } from './utils/formatters.js';
import apiService from './services/api.js';

// Configuração global de tratamento de erros
window.addEventListener('error', (event) => {
    errorHandler.handle(event.error || new Error(event.message), 'Erro não tratado', {
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno
    });
});

window.addEventListener('unhandledrejection', (event) => {
    errorHandler.handle(event.reason || new Error('Promise rejeitada'), 'Promise não tratada');
});

// Configuração de listeners de erro
errorHandler.onError((errorData) => {
    // Aqui você pode adicionar lógica para:
    // - Enviar erros para um serviço de monitoramento (ex: Sentry)
    // - Mostrar notificações ao usuário
    // - Logar em arquivo
    
    if (config.development.enableDebugMode) {
        console.group('🚨 Erro Capturado');
        console.error(errorData);
        console.groupEnd();
    }
});

// Inicialização da aplicação
class App {
    constructor() {
        this.modules = new Map();
        this.isInitialized = false;
    }

    /**
     * Inicializa a aplicação
     */
    async init() {
        if (this.isInitialized) return;

        try {
            console.log('🚀 Inicializando aplicação...');

            // Inicializa módulos
            await this.initModules();

            // Configura eventos globais
            this.setupGlobalEvents();

            // Mostra informações de desenvolvimento
            if (config.development.enableDebugMode) {
                this.showDevInfo();
            }

            this.isInitialized = true;
            console.log('✅ Aplicação inicializada com sucesso!');

        } catch (error) {
            errorHandler.handle(error, 'Erro na inicialização da aplicação');
        }
    }

    /**
     * Inicializa os módulos da aplicação
     */
    async initModules() {
        // Importa e inicializa o dashboard
        try {
            const { loadDashboardData } = await import('./dashboard.js');
            this.modules.set('dashboard', { loadDashboardData });
            console.log('✓ Dashboard carregado');
        } catch (error) {
            errorHandler.handle(error, 'Erro ao carregar dashboard');
        }
    }

    /**
     * Configura eventos globais
     */
    setupGlobalEvents() {
        // Evento de visibilidade da página
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                // Pausar atualizações quando a página não está visível
                console.log('📄 Página oculta - pausando atualizações');
            } else {
                // Retomar atualizações quando a página fica visível
                console.log('📄 Página visível - retomando atualizações');
                this.refreshData();
            }
        });

        // Evento de conexão online/offline
        window.addEventListener('online', () => {
            console.log('🌐 Conexão restaurada');
            this.showConnectionStatus(true);
            this.refreshData();
        });

        window.addEventListener('offline', () => {
            console.log('📡 Sem conexão');
            this.showConnectionStatus(false);
        });
    }

    /**
     * Atualiza os dados da aplicação
     */
    async refreshData() {
        const dashboardModule = this.modules.get('dashboard');
        if (dashboardModule && dashboardModule.loadDashboardData) {
            await dashboardModule.loadDashboardData();
        }
    }

    /**
     * Mostra status da conexão
     */
    showConnectionStatus(isOnline) {
        const statusElement = document.getElementById('connectionStatus');
        if (statusElement) {
            statusElement.className = isOnline ? 'online' : 'offline';
            statusElement.textContent = isOnline ? 'Online' : 'Offline';
        }
    }

    /**
     * Mostra informações de desenvolvimento
     */
    showDevInfo() {
        console.group('ℹ️ Informações de Desenvolvimento');
        console.log('Configurações:', config);
        console.log('Formatters disponíveis:', Object.keys(Formatters));
        console.log('API Service:', apiService);
        console.log('Error Handler:', errorHandler);
        console.groupEnd();

        // Expõe utilitários globalmente para depuração
        window.appUtils = {
            config,
            Formatters,
            apiService,
            errorHandler,
            app: this
        };
    }
}

// Cria e inicializa a aplicação
const app = new App();

// Inicializa quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => app.init());
} else {
    app.init();
}

// Exporta a instância da aplicação
export default app;
