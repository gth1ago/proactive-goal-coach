// Comandos customizados para testes E2E
import './commands';

// Configurações globais
Cypress.on('uncaught:exception', (err, runnable) => {
  // Previne que erros não capturados falhem os testes
  return false;
});

// Intercepta chamadas de API para testes mais estáveis
beforeEach(() => {
  // Intercepta API de objetivos
  cy.intercept('GET', '/api/goals/', { fixture: 'goals.json' }).as('getGoals');
  cy.intercept('GET', '/api/stats/dashboard', { fixture: 'dashboard.json' }).as('getDashboard');
  cy.intercept('GET', '/api/suggestions/', { fixture: 'suggestions.json' }).as('getSuggestions');
});