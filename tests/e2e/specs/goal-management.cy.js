describe('Goal Management E2E Tests', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('should display dashboard on initial load', () => {
    cy.waitForDashboardLoad();
    
    // Verifica elementos principais do dashboard
    cy.get('[data-testid="motivational-message"]').should('be.visible');
    cy.get('[data-testid="stats-cards"]').should('be.visible');
    cy.get('[data-testid="featured-goals"]').should('be.visible');
    cy.get('[data-testid="suggestions-panel"]').should('be.visible');
  });

  it('should navigate between tabs', () => {
    cy.navigateToTab('Meus Objetivos');
    cy.waitForGoalsLoad();
    
    cy.url().should('include', '#goals');
    cy.get('[data-testid="goals-list"]').should('be.visible');
    
    cy.navigateToTab('Dashboard');
    cy.waitForDashboardLoad();
    
    cy.get('[data-testid="dashboard-content"]').should('be.visible');
  });

  it('should create a new goal successfully', () => {
    cy.navigateToTab('Meus Objetivos');
    cy.waitForGoalsLoad();
    
    // Intercepta criação de objetivo
    cy.intercept('POST', '/api/goals/', {
      statusCode: 200,
      body: {
        id: 'new_goal_123',
        title: 'Aprender Cypress',
        description: 'Dominar testes E2E com Cypress',
        progress: 0,
        tags: ['testing', 'cypress'],
        micro_goals: [
          {
            id: 'micro_1',
            title: 'Instalar Cypress',
            description: 'Setup inicial',
            status: 'pending',
            estimated_time: 30
          }
        ]
      }
    }).as('createGoal');
    
    const goalData = {
      title: 'Aprender Cypress',
      description: 'Dominar testes E2E com Cypress',
      tags: 'testing, cypress'
    };
    
    cy.createGoal(goalData);
    
    cy.wait('@createGoal');
    
    // Verifica se objetivo foi criado
    cy.contains('.MuiCard-root', goalData.title).should('be.visible');
    cy.contains(goalData.description).should('be.visible');
  });

  it('should complete micro-goals and update progress', () => {
    cy.navigateToTab('Meus Objetivos');
    cy.waitForGoalsLoad();
    
    // Intercepta conclusão de micro-meta
    cy.intercept('PUT', '/api/goals/*/micro-goals/*/complete', {
      statusCode: 200,
      body: {
        message: 'Micro-meta completada!',
        progress: 25.0
      }
    }).as('completeMicroGoal');
    
    // Assume que existe um objetivo com micro-metas
    cy.get('.MuiCard-root').first().within(() => {
      // Clica no primeiro checkbox disponível
      cy.get('[type="checkbox"]').first().check();
    });
    
    cy.wait('@completeMicroGoal');
    
    // Verifica se progresso foi atualizado
    cy.get('.MuiLinearProgress-root').should('be.visible');
  });

  it('should display suggestions contextually', () => {
    cy.waitForDashboardLoad();
    
    // Verifica se sugestões são exibidas
    cy.get('[data-testid="suggestions-panel"]').within(() => {
      cy.get('.MuiListItem-root').should('have.length.at.least', 1);
      
      // Verifica estrutura das sugestões
      cy.get('.MuiListItemText-primary').should('be.visible');
      cy.get('.MuiListItemText-secondary').should('be.visible');
    });
  });

  it('should show motivational messages', () => {
    cy.intercept('GET', '/api/suggestions/motivational', {
      statusCode: 200,
      body: {
        message: '🚀 Você está indo muito bem!',
        progress: 65.5,
        completed_goals: 2
      }
    }).as('getMotivational');
    
    cy.visit('/');
    cy.wait('@getMotivational');
    
    cy.get('[data-testid="motivational-message"]')
      .should('contain', '🚀 Você está indo muito bem!');
  });

  it('should handle empty states gracefully', () => {
    // Intercepta com dados vazios
    cy.intercept('GET', '/api/goals/', { body: [] }).as('getEmptyGoals');
    
    cy.navigateToTab('Meus Objetivos');
    cy.wait('@getEmptyGoals');
    
    // Verifica estado vazio
    cy.get('[data-testid="empty-goals-state"]').should('be.visible');
    cy.contains('Nenhum objetivo encontrado').should('be.visible');
  });

  it('should be responsive on mobile viewport', () => {
    cy.viewport('iphone-x');
    cy.visit('/');
    
    cy.waitForDashboardLoad();
    
    // Verifica se layout mobile funciona
    cy.get('[data-testid="stats-cards"]').should('be.visible');
    cy.get('.MuiGrid-container').should('be.visible');
    
    // Testa navegação mobile
    cy.navigateToTab('Meus Objetivos');
    cy.get('[data-testid="add-goal-fab"]').should('be.visible');
  });

  it('should persist data across page reloads', () => {
    cy.navigateToTab('Meus Objetivos');
    cy.waitForGoalsLoad();
    
    // Pega o título do primeiro objetivo
    cy.get('.MuiCard-root').first().find('h6').invoke('text').as('firstGoalTitle');
    
    // Recarrega a página
    cy.reload();
    cy.waitForGoalsLoad();
    
    // Verifica se dados persistiram
    cy.get('@firstGoalTitle').then((title) => {
      cy.contains(title).should('be.visible');
    });
  });
});