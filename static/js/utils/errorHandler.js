/**
 * Gerenciador centralizado de erros
 * Fornece tratamento consistente de erros em toda a aplicação
 */

class ErrorHandler {
    constructor() {
        this.listeners = new Set();
        this.errorHistory = [];
        this.maxHistorySize = 50;
    }

    /**
     * Registra um listener para erros
     * @param {Function} callback - Função a ser chamada quando ocorrer um erro
     * @returns {Function} Função para remover o listener
     */
    onError(callback) {
        this.listeners.add(callback);
        return () => this.listeners.delete(callback);
    }

    /**
     * Trata um erro
     * @param {Error} error - Objeto de erro
     * @param {string} context - Contexto onde o erro ocorreu
     * @param {Object} [metadata] - Metadados adicionais
     */
    handle(error, context = '', metadata = {}) {
        const errorData = {
            message: error.message || 'Erro desconhecido',
            context,
            timestamp: new Date().toISOString(),
            stack: error.stack,
            ...metadata
        };

        // Adiciona ao histórico
        this.errorHistory.unshift(errorData);
        if (this.errorHistory.length > this.maxHistorySize) {
            this.errorHistory.pop();
        }

        console.error(`[Erro] ${context}:`, error, metadata);
        
        // Notifica os listeners
        this.listeners.forEach(listener => {
            try {
                listener(errorData);
            } catch (e) {
                console.error('Erro no listener de erro:', e);
            }
        });

        // Retorna um objeto de erro padronizado
        return {
            success: false,
            error: errorData
        };
    }

    /**
     * Cria um handler para funções assíncronas
     * @param {Function} fn - Função a ser executada
     * @param {string} context - Contexto para mensagens de erro
     * @returns {Function} Função com tratamento de erro
     */
    asyncHandler(fn, context) {
        return async (...args) => {
            try {
                return await fn(...args);
            } catch (error) {
                return this.handle(error, context);
            }
        };
    }

    /**
     * Obtém o histórico de erros
     * @returns {Array} Lista de erros recentes
     */
    getErrorHistory() {
        return [...this.errorHistory];
    }

    /**
     * Limpa o histórico de erros
     */
    clearHistory() {
        this.errorHistory = [];
    }

    /**
     * Mostra uma notificação de erro amigável
     * @param {string} message - Mensagem amigável para o usuário
     * @param {string} [title] - Título da notificação
     */
    showUserError(message, title = 'Erro') {
        // Implementação básica - pode ser expandida com uma biblioteca de notificações
        if (typeof window !== 'undefined' && window.alert) {
            alert(`${title}: ${message}`);
        }
    }
}

// Exporta uma instância única
export const errorHandler = new ErrorHandler();
export default errorHandler;
