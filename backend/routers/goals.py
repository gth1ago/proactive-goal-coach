from fastapi import APIRouter, HTTPException
from typing import List
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from shared.types import Goal, MicroGoal, GoalStatus, MicroGoalStatus
from mock_data import get_goals, get_goal, goals_db
from datetime import datetime
import uuid

router = APIRouter()

@router.get("/", response_model=List[Goal])
async def list_goals():
    """Lista todos os objetivos"""
    return get_goals()

@router.get("/{goal_id}", response_model=Goal)
async def get_goal_detail(goal_id: str):
    """Obtém detalhes de um objetivo específico"""
    goal = get_goal(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Objetivo não encontrado")
    return goal

@router.post("/", response_model=Goal)
async def create_goal(goal_data: dict):
    """Cria um novo objetivo"""
    goal_id = str(uuid.uuid4())
    
    # Simula IA quebrando objetivo em micro-metas
    micro_goals = generate_micro_goals(goal_data["title"], goal_data["description"], goal_id)
    
    goal = Goal(
        id=goal_id,
        title=goal_data["title"],
        description=goal_data["description"],
        status=GoalStatus.ACTIVE,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        micro_goals=micro_goals,
        tags=goal_data.get("tags", [])
    )
    
    goals_db[goal_id] = goal
    return goal

@router.put("/{goal_id}/micro-goals/{micro_goal_id}/complete")
async def complete_micro_goal(goal_id: str, micro_goal_id: str):
    """Marca uma micro-meta como completa"""
    goal = get_goal(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Objetivo não encontrado")
    
    for micro_goal in goal.micro_goals:
        if micro_goal.id == micro_goal_id:
            micro_goal.status = MicroGoalStatus.COMPLETED
            micro_goal.completed_at = datetime.now()
            
            # Atualiza progresso do objetivo
            completed_count = sum(1 for mg in goal.micro_goals if mg.status == MicroGoalStatus.COMPLETED)
            goal.progress = (completed_count / len(goal.micro_goals)) * 100
            goal.updated_at = datetime.now()
            
            return {"message": "Micro-meta completada!", "progress": goal.progress}
    
    raise HTTPException(status_code=404, detail="Micro-meta não encontrada")

def generate_micro_goals(title: str, description: str, goal_id: str) -> List[MicroGoal]:
    """Simula IA gerando micro-metas baseadas no objetivo"""
    
    # Templates baseados em palavras-chave
    templates = {
        "aprender": [
            "Pesquisar recursos básicos sobre {topic}",
            "Fazer tutorial introdutório",
            "Praticar conceitos fundamentais",
            "Criar primeiro projeto prático"
        ],
        "escrever": [
            "Definir estrutura e outline",
            "Escrever primeiro rascunho",
            "Revisar e editar conteúdo",
            "Finalizar e formatar"
        ],
        "fitness": [
            "Definir rotina de exercícios",
            "Começar com 15min diários",
            "Aumentar intensidade gradualmente",
            "Manter consistência por 30 dias"
        ]
    }
    
    # Detecta categoria baseada no título/descrição
    category = "aprender"  # default
    text = (title + " " + description).lower()
    
    if any(word in text for word in ["escrever", "livro", "artigo", "blog"]):
        category = "escrever"
    elif any(word in text for word in ["exercício", "fitness", "academia", "correr"]):
        category = "fitness"
    
    # Gera micro-metas
    micro_goals = []
    for i, template in enumerate(templates[category]):
        micro_goal = MicroGoal(
            id=f"micro_{goal_id}_{i+1}",
            title=template.format(topic=title.split()[-1] if "{topic}" in template else ""),
            description=f"Passo {i+1} para atingir: {title}",
            status=MicroGoalStatus.PENDING,
            estimated_time=60 + (i * 30),  # Tempo crescente
            created_at=datetime.now(),
            goal_id=goal_id
        )
        micro_goals.append(micro_goal)
    
    return micro_goals