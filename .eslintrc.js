module.exports = {
  env: {
    browser: true,
    es2022: true,
    jest: true,
    node: true
  },
  extends: [
    'eslint:recommended',
    'prettier'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  globals: {
    Chart: 'readonly',
    fetch: 'readonly',
    document: 'readonly',
    window: 'readonly',
    console: 'readonly'
  },
  rules: {
    // Regras principais
    'no-console': 'warn',
    'no-unused-vars': 'error',
    'prefer-const': 'error',
    'no-var': 'error',
    
    // Formatação e estilo
    'object-shorthand': 'error',
    'prefer-arrow-callback': 'error',
    'prefer-template': 'error',
    'template-curly-spacing': 'error',
    'arrow-spacing': 'error',
    'comma-dangle': ['error', 'never'],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always'],
    'indent': ['error', 2],
    'max-len': ['warn', { code: 100 }],
    
    // Qualidade de código
    'no-magic-numbers': ['warn', { ignore: [-1, 0, 1, 2, 100, 1000] }],
    'complexity': ['warn', 10],
    'max-depth': ['warn', 4],
    'max-params': ['warn', 4],
    'max-lines-per-function': ['warn', 50],
    
    // Boas práticas
    'eqeqeq': 'error',
    'curly': 'error',
    'no-eval': 'error',
    'no-implied-eval': 'error',
    'no-new-func': 'error',
    'no-script-url': 'error',
    'no-self-compare': 'error',
    'no-sequences': 'error',
    'no-throw-literal': 'error',
    'no-unmodified-loop-condition': 'error',
    'no-unused-expressions': 'error',
    'no-useless-call': 'error',
    'no-useless-concat': 'error',
    'no-useless-return': 'error',
    'radix': 'error',
    'yoda': 'error',
    
    // ES6+
    'arrow-body-style': 'error',
    'no-confusing-arrow': 'error',
    'prefer-rest-params': 'error',
    'prefer-spread': 'error',
    'prefer-template': 'error',
    
    // Import/Export
    'no-duplicate-imports': 'error',
    'no-useless-rename': 'error'
  },
  overrides: [
    {
      files: ['*.test.js', '**/__tests__/**/*.js'],
      env: {
        jest: true
      },
      rules: {
        'no-magic-numbers': 'off'
      }
    }
  ]
};
