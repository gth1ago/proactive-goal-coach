import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, timedelta
from shared.types import Goal, MicroGoal, Badge, Suggestion, GoalStatus, MicroGoalStatus, Priority, BadgeType

# Storage em memória (será substituído por banco)
goals_db = {}
suggestions_db = {}
badges_db = {}

def initialize_mock_data():
    """Inicializa dados mock para desenvolvimento"""
    
    # Objetivo 1: Aprender Python
    goal1_id = "goal_1"
    goal1 = Goal(
        id=goal1_id,
        title="Aprender Python",
        description="Dominar programação Python para desenvolvimento web",
        status=GoalStatus.ACTIVE,
        target_date=datetime.now() + timedelta(days=90),
        created_at=datetime.now() - timedelta(days=10),
        updated_at=datetime.now(),
        progress=35.0,
        tags=["programação", "carreira", "python"]
    )
    
    # Micro-metas para Python
    micro_goals_1 = [
        MicroGoal(
            id="micro_1_1",
            title="Completar tutorial básico",
            description="Fazer o tutorial oficial do Python.org",
            status=MicroGoalStatus.COMPLETED,
            priority=Priority.HIGH,
            estimated_time=120,
            created_at=datetime.now() - timedelta(days=8),
            completed_at=datetime.now() - timedelta(days=6),
            goal_id=goal1_id
        ),
        MicroGoal(
            id="micro_1_2",
            title="Criar primeiro projeto",
            description="Desenvolver uma calculadora simples",
            status=MicroGoalStatus.IN_PROGRESS,
            priority=Priority.HIGH,
            estimated_time=180,
            created_at=datetime.now() - timedelta(days=5),
            goal_id=goal1_id
        ),
        MicroGoal(
            id="micro_1_3",
            title="Estudar estruturas de dados",
            description="Aprender listas, dicionários e tuplas",
            status=MicroGoalStatus.PENDING,
            priority=Priority.MEDIUM,
            estimated_time=90,
            created_at=datetime.now() - timedelta(days=2),
            goal_id=goal1_id
        )
    ]
    
    goal1.micro_goals = micro_goals_1
    goals_db[goal1_id] = goal1
    
    # Objetivo 2: Escrever um livro
    goal2_id = "goal_2"
    goal2 = Goal(
        id=goal2_id,
        title="Escrever meu primeiro livro",
        description="Publicar um livro sobre produtividade pessoal",
        status=GoalStatus.ACTIVE,
        target_date=datetime.now() + timedelta(days=180),
        created_at=datetime.now() - timedelta(days=15),
        updated_at=datetime.now(),
        progress=20.0,
        tags=["escrita", "criatividade", "publicação"]
    )
    
    # Micro-metas para o livro
    micro_goals_2 = [
        MicroGoal(
            id="micro_2_1",
            title="Definir estrutura do livro",
            description="Criar outline com capítulos principais",
            status=MicroGoalStatus.COMPLETED,
            priority=Priority.HIGH,
            estimated_time=60,
            created_at=datetime.now() - timedelta(days=12),
            completed_at=datetime.now() - timedelta(days=10),
            goal_id=goal2_id
        ),
        MicroGoal(
            id="micro_2_2",
            title="Escrever introdução",
            description="Redigir as primeiras 1000 palavras",
            status=MicroGoalStatus.PENDING,
            priority=Priority.HIGH,
            estimated_time=120,
            created_at=datetime.now() - timedelta(days=3),
            goal_id=goal2_id
        )
    ]
    
    goal2.micro_goals = micro_goals_2
    goals_db[goal2_id] = goal2
    
    # Badges
    badge1 = Badge(
        id="badge_1",
        name="Primeiro Passo",
        description="Completou sua primeira micro-meta!",
        type=BadgeType.MILESTONE,
        icon="🎯",
        earned_at=datetime.now() - timedelta(days=6),
        goal_id=goal1_id
    )
    
    badge2 = Badge(
        id="badge_2",
        name="Consistência",
        description="Trabalhou em objetivos por 3 dias seguidos",
        type=BadgeType.STREAK,
        icon="🔥",
        earned_at=datetime.now() - timedelta(days=2)
    )
    
    badges_db["badge_1"] = badge1
    badges_db["badge_2"] = badge2
    
    # Sugestões
    suggestion1 = Suggestion(
        id="sugg_1",
        title="Hora de programar!",
        description="Você geralmente programa melhor pela manhã. Que tal continuar sua calculadora?",
        micro_goal_id="micro_1_2",
        priority=Priority.HIGH,
        suggested_time="morning",
        created_at=datetime.now()
    )
    
    suggestion2 = Suggestion(
        id="sugg_2",
        title="Momento criativo",
        description="Aproveite a tarde para escrever. Comece com 200 palavras da introdução.",
        micro_goal_id="micro_2_2",
        priority=Priority.MEDIUM,
        suggested_time="afternoon",
        created_at=datetime.now()
    )
    
    suggestions_db["sugg_1"] = suggestion1
    suggestions_db["sugg_2"] = suggestion2

def get_goals():
    return list(goals_db.values())

def get_goal(goal_id: str):
    return goals_db.get(goal_id)

def get_suggestions():
    return list(suggestions_db.values())

def get_badges():
    return list(badges_db.values())