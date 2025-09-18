import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// Configura servidor MSW para interceptar requests durante testes
export const server = setupServer(...handlers);