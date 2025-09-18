// Comandos customizados para testes E2E

Cypress.Commands.add('createGoal', (goalData) => {
  cy.get('[data-testid="add-goal-fab"]').click();
  cy.get('[data-testid="goal-title-input"]').type(goalData.title);
  cy.get('[data-testid="goal-description-input"]').type(goalData.description);
  if (goalData.tags) {
    cy.get('[data-testid="goal-tags-input"]').type(goalData.tags);
  }
  cy.get('[data-testid="create-goal-button"]').click();
});

Cypress.Commands.add('completeMicroGoal', (goalTitle, microGoalTitle) => {
  cy.contains('.MuiCard-root', goalTitle).within(() => {
    cy.contains('.MuiListItem-root', microGoalTitle).within(() => {
      cy.get('[type="checkbox"]').check();
    });
  });
});

Cypress.Commands.add('navigateToTab', (tabName) => {
  cy.get(`[role="tab"]`).contains(tabName).click();
});

Cypress.Commands.add('waitForDashboardLoad', () => {
  cy.wait('@getDashboard');
  cy.wait('@getSuggestions');
  cy.get('[data-testid="dashboard-content"]').should('be.visible');
});

Cypress.Commands.add('waitForGoalsLoad', () => {
  cy.wait('@getGoals');
  cy.get('[data-testid="goals-list"]').should('be.visible');
});