require('@testing-library/jest-dom');

// Mock básico para testes
global.fetch = require('jest-fetch-mock');

// Setup básico para testes
beforeEach(() => {
  fetch.resetMocks();
});