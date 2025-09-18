from fastapi import APIRouter
from typing import List
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from shared.types import Suggestion, Priority
from mock_data import get_suggestions, get_goals
from datetime import datetime
import random

router = APIRouter()

@router.get("/", response_model=List[Suggestion])
async def get_contextual_suggestions():
    """Obtém sugestões contextuais baseadas no horário e hábitos"""
    current_hour = datetime.now().hour
    
    # Determina período do dia
    if 6 <= current_hour < 12:
        time_context = "morning"
        time_message = "Bom dia! Você costuma ser mais produtivo pela manhã."
    elif 12 <= current_hour < 18:
        time_context = "afternoon"
        time_message = "Boa tarde! Hora perfeita para tarefas criativas."
    else:
        time_context = "evening"
        time_message = "Boa noite! Que tal revisar o progresso do dia?"
    
    # Pega sugestões existentes e adiciona contexto
    base_suggestions = get_suggestions()
    contextual_suggestions = []
    
    for suggestion in base_suggestions:
        if suggestion.suggested_time == time_context:
            # Personaliza a mensagem baseada no horário
            enhanced_suggestion = Suggestion(
                id=suggestion.id,
                title=f"💡 {suggestion.title}",
                description=f"{time_message} {suggestion.description}",
                micro_goal_id=suggestion.micro_goal_id,
                priority=suggestion.priority,
                suggested_time=suggestion.suggested_time,
                created_at=suggestion.created_at
            )
            contextual_suggestions.append(enhanced_suggestion)
    
    # Adiciona sugestões motivacionais
    motivational_suggestions = generate_motivational_suggestions()
    contextual_suggestions.extend(motivational_suggestions)
    
    return contextual_suggestions[:3]  # Limita a 3 sugestões

@router.get("/motivational")
async def get_motivational_message():
    """Gera mensagem motivacional baseada no progresso"""
    goals = get_goals()
    
    if not goals:
        return {"message": "🎯 Pronto para começar? Crie seu primeiro objetivo!"}
    
    # Calcula estatísticas
    total_progress = sum(goal.progress for goal in goals) / len(goals)
    completed_goals = len([g for g in goals if g.progress >= 100])
    
    messages = []
    
    if total_progress >= 75:
        messages.append("🔥 Incrível! Você está quase lá!")
    elif total_progress >= 50:
        messages.append("💪 Ótimo progresso! Continue assim!")
    elif total_progress >= 25:
        messages.append("🌱 Você está crescendo! Cada passo conta!")
    else:
        messages.append("🚀 Toda jornada começa com o primeiro passo!")
    
    if completed_goals > 0:
        messages.append(f"🏆 Parabéns! Você já completou {completed_goals} objetivo(s)!")
    
    return {
        "message": random.choice(messages),
        "progress": total_progress,
        "completed_goals": completed_goals
    }

def generate_motivational_suggestions() -> List[Suggestion]:
    """Gera sugestões motivacionais dinâmicas"""
    goals = get_goals()
    suggestions = []
    
    for goal in goals:
        if goal.progress < 100:
            # Encontra próxima micro-meta pendente
            next_micro_goal = None
            for mg in goal.micro_goals:
                if mg.status.value == "pending":
                    next_micro_goal = mg
                    break
            
            if next_micro_goal:
                suggestion = Suggestion(
                    id=f"motivational_{goal.id}",
                    title=f"🎯 Continue com '{goal.title}'",
                    description=f"Próximo passo: {next_micro_goal.title} (≈{next_micro_goal.estimated_time}min)",
                    micro_goal_id=next_micro_goal.id,
                    priority=Priority.MEDIUM,
                    created_at=datetime.now()
                )
                suggestions.append(suggestion)
    
    return suggestions