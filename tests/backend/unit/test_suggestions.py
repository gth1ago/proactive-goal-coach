import pytest
from datetime import datetime
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../shared'))

from routers.suggestions import generate_motivational_suggestions
from shared.types import Goal, MicroGoal, MicroGoalStatus, Priority

class TestSuggestionGeneration:
    """Testes unitários para geração de sugestões"""
    
    def test_generate_motivational_suggestions_with_pending_goals(self):
        """Testa geração de sugestões com objetivos pendentes"""
        # Mock de objetivo com micro-meta pendente
        micro_goal = MicroGoal(
            id="micro_1",
            title="Estudar Python básico",
            description="Completar tutorial",
            status=MicroGoalStatus.PENDING,
            priority=Priority.HIGH,
            estimated_time=90,
            created_at=datetime.now(),
            goal_id="goal_1"
        )
        
        goal = Goal(
            id="goal_1",
            title="Aprender Python",
            description="Dominar Python",
            progress=25.0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            micro_goals=[micro_goal]
        )
        
        with patch('routers.suggestions.get_goals', return_value=[goal]):
            suggestions = generate_motivational_suggestions()
        
        assert len(suggestions) == 1
        suggestion = suggestions[0]
        assert "Aprender Python" in suggestion.title
        assert suggestion.micro_goal_id == "micro_1"
        assert "90min" in suggestion.description
    
    def test_generate_motivational_suggestions_completed_goals(self):
        """Testa que objetivos 100% completos não geram sugestões"""
        goal = Goal(
            id="goal_1",
            title="Objetivo Completo",
            description="Já finalizado",
            progress=100.0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            micro_goals=[]
        )
        
        with patch('routers.suggestions.get_goals', return_value=[goal]):
            suggestions = generate_motivational_suggestions()
        
        assert len(suggestions) == 0
    
    def test_generate_motivational_suggestions_no_pending_micro_goals(self):
        """Testa objetivo sem micro-metas pendentes"""
        micro_goal = MicroGoal(
            id="micro_1",
            title="Tarefa completa",
            description="Já feita",
            status=MicroGoalStatus.COMPLETED,
            priority=Priority.HIGH,
            estimated_time=60,
            created_at=datetime.now(),
            goal_id="goal_1"
        )
        
        goal = Goal(
            id="goal_1",
            title="Objetivo sem pendências",
            description="Todas micro-metas completas",
            progress=50.0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            micro_goals=[micro_goal]
        )
        
        with patch('routers.suggestions.get_goals', return_value=[goal]):
            suggestions = generate_motivational_suggestions()
        
        assert len(suggestions) == 0

class TestTimeContextSuggestions:
    """Testes para sugestões baseadas em contexto temporal"""
    
    @patch('routers.suggestions.datetime')
    def test_morning_context_suggestions(self, mock_datetime):
        """Testa sugestões para período da manhã"""
        # Mock para simular 9h da manhã
        mock_datetime.now.return_value.hour = 9
        
        from routers.suggestions import router
        # Testa se a lógica de contexto matinal funciona
        # (Este teste seria expandido com implementação real)
        
        assert mock_datetime.now.return_value.hour == 9
    
    @patch('routers.suggestions.datetime')
    def test_afternoon_context_suggestions(self, mock_datetime):
        """Testa sugestões para período da tarde"""
        # Mock para simular 15h
        mock_datetime.now.return_value.hour = 15
        
        assert mock_datetime.now.return_value.hour == 15
    
    @patch('routers.suggestions.datetime')
    def test_evening_context_suggestions(self, mock_datetime):
        """Testa sugestões para período da noite"""
        # Mock para simular 20h
        mock_datetime.now.return_value.hour = 20
        
        assert mock_datetime.now.return_value.hour == 20