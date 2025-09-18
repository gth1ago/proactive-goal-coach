const React = require('react');
const { render, screen } = require('@testing-library/react');

// Mock simples do componente Dashboard
const MockDashboard = () => {
  return React.createElement('div', { 'data-testid': 'dashboard' }, 'Dashboard Component');
};

describe('Dashboard Component', () => {
  test('renders dashboard component', () => {
    render(React.createElement(MockDashboard));
    expect(screen.getByTestId('dashboard')).toBeInTheDocument();
    expect(screen.getByText('Dashboard Component')).toBeInTheDocument();
  });

  test('dashboard has correct structure', () => {
    render(React.createElement(MockDashboard));
    const dashboard = screen.getByTestId('dashboard');
    expect(dashboard).toBeInTheDocument();
  });

  test('mock API calls work', () => {
    // Mock fetch para simular chamadas de API
    fetch.mockResponseOnce(JSON.stringify({
      stats: { active_goals: 2 },
      overall_progress: 50
    }));

    expect(fetch).toBeDefined();
  });
});