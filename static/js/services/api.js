/**
 * Serviço de API
 * Gerencia todas as chamadas à API com tratamento de erros
 */

class ApiService {
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        };
    }

    async _fetch(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        console.log(`🌐 API Request: ${options.method || 'GET'} ${url}`);
        
        const headers = { ...this.defaultHeaders, ...options.headers };
        
        try {
            console.log('📤 Enviando requisição...');
            const response = await fetch(url, { ...options, headers });
            
            console.log(`📥 Response status: ${response.status} ${response.statusText}`);
            
            if (!response.ok) {
                const error = new Error(`HTTP error! status: ${response.status}`);
                error.status = response.status;
                throw error;
            }

            const contentType = response.headers.get('content-type');
            console.log('📄 Content-Type:', contentType);
            
            if (contentType && contentType.includes('application/json')) {
                const data = await response.json();
                console.log('📋 JSON Response:', data);
                return data;
            }
            const text = await response.text();
            console.log('📄 Text Response:', text);
            return text;
        } catch (error) {
            console.error(`💥 API Error in ${endpoint}:`, error);
            return {
                success: false,
                error: error.message || 'Erro ao comunicar com o servidor'
            };
        }
    }

    get(endpoint, params = {}) {
        const query = new URLSearchParams(params).toString();
        const url = query ? `${endpoint}?${query}` : endpoint;
        return this._fetch(url);
    }

    post(endpoint, data) {
        return this._fetch(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    put(endpoint, data) {
        return this._fetch(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    delete(endpoint) {
        return this._fetch(endpoint, { method: 'DELETE' });
    }

    // Métodos específicos da aplicação
    async getDashboardData() {
        return this.get('/api/dashboard/data');
    }

    async getChartData(chartId, params = {}) {
        return this.get(`/api/charts/${chartId}`, params);
    }

    async getNotifications() {
        return this.get('/api/notifications');
    }

    async markNotificationRead(notificationId) {
        return this.post(`/api/notifications/${notificationId}/read`);
    }

    async getContracts() {
        return this.get('/api/contratos');
    }

    async getClients() {
        return this.get('/api/clients');
    }

    async createContract(contractData) {
        return this.post('/api/contracts', contractData);
    }

    async createClient(clientData) {
        return this.post('/api/clients', clientData);
    }

    async analyzeChart(chartType, data) {
        return this.post('/api/analise/grafico', { type: chartType, data });
    }

    async askQuestion(question) {
        return this.post('/api/perguntar', { question });
    }

    async generateReport(reportType, format) {
        return this.get(`/api/reports/${reportType}/${format}`);
    }
}

// Exporta uma instância única
export const apiService = new ApiService();
export default apiService;
