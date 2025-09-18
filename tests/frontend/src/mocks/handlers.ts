import { http, HttpResponse } from 'msw';

const mockGoals = [
  {
    id: 'goal_1',
    title: 'Aprender React Testing',
    description: 'Dominar testes em React',
    progress: 45.0,
    status: 'active',
    created_at: '2024-01-01T10:00:00Z',
    updated_at: '2024-01-01T10:00:00Z',
    tags: ['react', 'testing'],
    micro_goals: [
      {
        id: 'micro_1',
        title: 'Configurar Jest',
        description: 'Setup inicial do Jest',
        status: 'completed',
        priority: 'high',
        estimated_time: 60,
        created_at: '2024-01-01T10:00:00Z',
        completed_at: '2024-01-01T11:00:00Z',
        goal_id: 'goal_1'
      },
      {
        id: 'micro_2',
        title: 'Escrever primeiro teste',
        description: 'Criar teste básico',
        status: 'pending',
        priority: 'medium',
        estimated_time: 90,
        created_at: '2024-01-01T10:00:00Z',
        goal_id: 'goal_1'
      }
    ]
  }
];

const mockSuggestions = [
  {
    id: 'sugg_1',
    title: '💡 Continue com React Testing',
    description: 'Que tal escrever seu primeiro teste agora?',
    micro_goal_id: 'micro_2',
    priority: 'high',
    suggested_time: 'morning',
    created_at: '2024-01-01T10:00:00Z'
  }
];

const mockStats = {
  total_goals: 1,
  completed_goals: 0,
  active_goals: 1,
  total_micro_goals: 2,
  completed_micro_goals: 1,
  current_streak: 3,
  badges: [],
  weekly_progress: {
    'Monday': 1,
    'Tuesday': 0,
    'Wednesday': 1,
    'Thursday': 0,
    'Friday': 1,
    'Saturday': 0,
    'Sunday': 0
  }
};

export const handlers = [
  // Goals endpoints
  http.get('http://localhost:8000/api/goals/', () => {
    return HttpResponse.json(mockGoals);
  }),

  http.get('http://localhost:8000/api/goals/:id', ({ params }) => {
    const goal = mockGoals.find(g => g.id === params.id);
    if (goal) {
      return HttpResponse.json(goal);
    }
    return new HttpResponse(null, { status: 404 });
  }),

  http.post('http://localhost:8000/api/goals/', async ({ request }) => {
    const newGoal = await request.json() as any;
    const goal = {
      id: 'new_goal_' + Date.now(),
      ...newGoal,
      progress: 0,
      status: 'active',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      micro_goals: [
        {
          id: 'micro_new_1',
          title: 'Primeiro passo gerado pela IA',
          description: 'Passo inicial para ' + newGoal.title,
          status: 'pending',
          priority: 'medium',
          estimated_time: 60,
          created_at: new Date().toISOString(),
          goal_id: 'new_goal_' + Date.now()
        }
      ]
    };
    return HttpResponse.json(goal);
  }),

  http.put('http://localhost:8000/api/goals/:goalId/micro-goals/:microId/complete', () => {
    return HttpResponse.json({
      message: 'Micro-meta completada!',
      progress: 50.0
    });
  }),

  // Suggestions endpoints
  http.get('http://localhost:8000/api/suggestions/', () => {
    return HttpResponse.json(mockSuggestions);
  }),

  http.get('http://localhost:8000/api/suggestions/motivational', () => {
    return HttpResponse.json({
      message: '🚀 Você está indo bem! Continue assim!',
      progress: 45.0,
      completed_goals: 0
    });
  }),

  // Stats endpoints
  http.get('http://localhost:8000/api/stats/', () => {
    return HttpResponse.json(mockStats);
  }),

  http.get('http://localhost:8000/api/stats/dashboard', () => {
    return HttpResponse.json({
      stats: mockStats,
      overall_progress: 45.0,
      featured_goals: mockGoals,
      recent_badges: [],
      motivational_message: '🔥 Ótimo progresso! Continue assim!'
    });
  })
];