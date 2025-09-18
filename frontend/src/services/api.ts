import axios from 'axios';
import { Goal, Suggestion, UserStats, DashboardData } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const goalService = {
  // Listar todos os objetivos
  getGoals: async (): Promise<Goal[]> => {
    const response = await api.get('/goals/');
    return response.data;
  },

  // Obter objetivo específico
  getGoal: async (goalId: string): Promise<Goal> => {
    const response = await api.get(`/goals/${goalId}`);
    return response.data;
  },

  // Criar novo objetivo
  createGoal: async (goalData: {
    title: string;
    description: string;
    tags?: string[];
  }): Promise<Goal> => {
    const response = await api.post('/goals/', goalData);
    return response.data;
  },

  // Completar micro-meta
  completeMicroGoal: async (goalId: string, microGoalId: string) => {
    const response = await api.put(`/goals/${goalId}/micro-goals/${microGoalId}/complete`);
    return response.data;
  },
};

export const suggestionService = {
  // Obter sugestões contextuais
  getSuggestions: async (): Promise<Suggestion[]> => {
    const response = await api.get('/suggestions/');
    return response.data;
  },

  // Obter mensagem motivacional
  getMotivationalMessage: async () => {
    const response = await api.get('/suggestions/motivational');
    return response.data;
  },
};

export const statsService = {
  // Obter estatísticas do usuário
  getUserStats: async (): Promise<UserStats> => {
    const response = await api.get('/stats/');
    return response.data;
  },

  // Obter dados do dashboard
  getDashboardData: async (): Promise<DashboardData> => {
    const response = await api.get('/stats/dashboard');
    return response.data;
  },
};

export default api;