import pytest
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../shared'))

from routers.goals import generate_micro_goals
from shared.types import Goal, MicroGoal, GoalStatus, MicroGoalStatus

class TestGoalGeneration:
    """Testes unitários para geração de objetivos e micro-metas"""
    
    def test_generate_micro_goals_learning_category(self):
        """Testa geração de micro-metas para categoria 'aprender'"""
        title = "Aprender Python"
        description = "Dominar programação Python"
        goal_id = "test_goal_1"
        
        micro_goals = generate_micro_goals(title, description, goal_id)
        
        assert len(micro_goals) == 4
        assert all(isinstance(mg, MicroGoal) for mg in micro_goals)
        assert all(mg.goal_id == goal_id for mg in micro_goals)
        assert all(mg.status == MicroGoalStatus.PENDING for mg in micro_goals)
        
        # Verifica se contém palavras-chave esperadas
        titles = [mg.title for mg in micro_goals]
        assert any("recursos" in title.lower() for title in titles)
        assert any("tutorial" in title.lower() for title in titles)
    
    def test_generate_micro_goals_writing_category(self):
        """Testa geração de micro-metas para categoria 'escrever'"""
        title = "Escrever um livro"
        description = "Publicar meu primeiro livro sobre produtividade"
        goal_id = "test_goal_2"
        
        micro_goals = generate_micro_goals(title, description, goal_id)
        
        assert len(micro_goals) == 4
        titles = [mg.title for mg in micro_goals]
        assert any("estrutura" in title.lower() for title in titles)
        assert any("rascunho" in title.lower() for title in titles)
    
    def test_generate_micro_goals_fitness_category(self):
        """Testa geração de micro-metas para categoria 'fitness'"""
        title = "Melhorar condicionamento físico"
        description = "Começar rotina de exercícios na academia"
        goal_id = "test_goal_3"
        
        micro_goals = generate_micro_goals(title, description, goal_id)
        
        assert len(micro_goals) == 4
        titles = [mg.title for mg in micro_goals]
        assert any("rotina" in title.lower() for title in titles)
        assert any("exercício" in title.lower() for title in titles)
    
    def test_micro_goal_estimated_time_progression(self):
        """Testa se o tempo estimado cresce progressivamente"""
        micro_goals = generate_micro_goals("Teste", "Descrição teste", "test_id")
        
        times = [mg.estimated_time for mg in micro_goals]
        
        # Verifica se os tempos estão em ordem crescente
        assert times == sorted(times)
        assert times[0] == 60  # Primeiro deve ser 60min
        assert times[-1] > times[0]  # Último deve ser maior que primeiro

class TestGoalModel:
    """Testes unitários para modelo Goal"""
    
    def test_goal_creation(self):
        """Testa criação de objetivo"""
        goal = Goal(
            id="test_1",
            title="Teste Goal",
            description="Descrição teste",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        assert goal.id == "test_1"
        assert goal.title == "Teste Goal"
        assert goal.status == GoalStatus.ACTIVE
        assert goal.progress == 0.0
        assert len(goal.micro_goals) == 0
        assert len(goal.tags) == 0
    
    def test_goal_with_micro_goals(self):
        """Testa objetivo com micro-metas"""
        micro_goal = MicroGoal(
            id="micro_1",
            title="Micro teste",
            description="Descrição micro",
            estimated_time=60,
            created_at=datetime.now(),
            goal_id="test_1"
        )
        
        goal = Goal(
            id="test_1",
            title="Teste Goal",
            description="Descrição teste",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            micro_goals=[micro_goal]
        )
        
        assert len(goal.micro_goals) == 1
        assert goal.micro_goals[0].id == "micro_1"