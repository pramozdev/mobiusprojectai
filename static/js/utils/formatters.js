/**
 * Utilitários de formatação
 * Centraliza todas as funções de formatação do dashboard
 */

export const Formatters = {
    /**
     * Formata valores monetários
     * @param {number} value - Valor a ser formatado
     * @returns {string} Valor formatado como moeda
     */
    currency: (value) => {
        if (value === null || value === undefined) return 'R$ 0,00';
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(Number(value));
    },

    /**
     * Formata números inteiros
     * @param {number} value - Valor a ser formatado
     * @returns {string} Número formatado
     */
    number: (value) => {
        if (value === null || value === undefined) return '0';
        return new Intl.NumberFormat('pt-BR').format(Number(value));
    },

    /**
     * Formata percentuais
     * @param {number} value - Valor a ser formatado (0-100)
     * @param {number} decimals - Número de casas decimais
     * @returns {string} Percentual formatado
     */
    percent: (value, decimals = 2) => {
        if (value === null || value === undefined) return '0%';
        return `${Number(value).toFixed(decimals)}%`;
    },

    /**
     * Formata datas
     * @param {string|Date} date - Data a ser formatada
     * @returns {string} Data formatada
     */
    date: (date) => {
        if (!date) return '-';
        return new Date(date).toLocaleDateString('pt-BR');
    },

    /**
     * Formata data e hora
     * @param {string|Date} datetime - Data e hora a serem formatadas
     * @returns {string} Data e hora formatadas
     */
    datetime: (datetime) => {
        if (!datetime) return '-';
        return new Date(datetime).toLocaleString('pt-BR');
    }
};

export default Formatters;
