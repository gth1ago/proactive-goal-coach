from fastapi import APIRouter
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from shared.types import UserStats, Badge
from mock_data import get_goals, get_badges
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/", response_model=UserStats)
async def get_user_stats():
    """Obtém estatísticas do usuário"""
    goals = get_goals()
    badges = get_badges()
    
    # Calcula estatísticas
    total_goals = len(goals)
    completed_goals = len([g for g in goals if g.progress >= 100])
    active_goals = len([g for g in goals if g.status.value == "active"])
    
    # Micro-metas
    all_micro_goals = []
    for goal in goals:
        all_micro_goals.extend(goal.micro_goals)
    
    total_micro_goals = len(all_micro_goals)
    completed_micro_goals = len([mg for mg in all_micro_goals if mg.status.value == "completed"])
    
    # Calcula streak (dias consecutivos trabalhando)
    current_streak = calculate_streak(all_micro_goals)
    
    # Progresso semanal (últimos 7 dias)
    weekly_progress = calculate_weekly_progress(all_micro_goals)
    
    return UserStats(
        total_goals=total_goals,
        completed_goals=completed_goals,
        active_goals=active_goals,
        total_micro_goals=total_micro_goals,
        completed_micro_goals=completed_micro_goals,
        current_streak=current_streak,
        badges=badges,
        weekly_progress=weekly_progress
    )

@router.get("/dashboard")
async def get_dashboard_data():
    """Dados para o dashboard principal"""
    stats = await get_user_stats()
    goals = get_goals()
    
    # Progresso geral
    if stats.total_goals > 0:
        overall_progress = sum(goal.progress for goal in goals) / len(goals)
    else:
        overall_progress = 0
    
    # Objetivos em destaque (com maior progresso)
    featured_goals = sorted(goals, key=lambda g: g.progress, reverse=True)[:3]
    
    # Conquistas recentes
    recent_badges = sorted(get_badges(), key=lambda b: b.earned_at, reverse=True)[:3]
    
    return {
        "stats": stats,
        "overall_progress": overall_progress,
        "featured_goals": featured_goals,
        "recent_badges": recent_badges,
        "motivational_message": generate_dashboard_message(stats, overall_progress)
    }

def calculate_streak(micro_goals) -> int:
    """Calcula quantos dias consecutivos o usuário trabalhou em objetivos"""
    if not micro_goals:
        return 0
    
    # Pega datas de conclusão das últimas micro-metas
    completed_dates = []
    for mg in micro_goals:
        if mg.completed_at:
            date_only = mg.completed_at.date()
            if date_only not in completed_dates:
                completed_dates.append(date_only)
    
    if not completed_dates:
        return 0
    
    completed_dates.sort(reverse=True)
    
    # Conta dias consecutivos a partir de hoje
    streak = 0
    current_date = datetime.now().date()
    
    for date in completed_dates:
        if date == current_date or date == current_date - timedelta(days=streak):
            streak += 1
            current_date = date
        else:
            break
    
    return streak

def calculate_weekly_progress(micro_goals) -> dict:
    """Calcula progresso dos últimos 7 dias"""
    weekly_data = {}
    
    for i in range(7):
        date = datetime.now().date() - timedelta(days=i)
        day_name = date.strftime("%A")
        
        # Conta micro-metas completadas neste dia
        completed_count = 0
        for mg in micro_goals:
            if mg.completed_at and mg.completed_at.date() == date:
                completed_count += 1
        
        weekly_data[day_name] = completed_count
    
    return weekly_data

def generate_dashboard_message(stats: UserStats, overall_progress: float) -> str:
    """Gera mensagem motivacional para o dashboard"""
    
    if stats.current_streak >= 7:
        return f"🔥 Incrível! {stats.current_streak} dias de consistência!"
    elif stats.current_streak >= 3:
        return f"💪 Ótimo! {stats.current_streak} dias seguidos trabalhando em seus objetivos!"
    elif stats.completed_goals > 0:
        return f"🏆 Parabéns! Você já completou {stats.completed_goals} objetivo(s)!"
    elif overall_progress >= 50:
        return "🌟 Você está no caminho certo! Continue assim!"
    else:
        return "🚀 Vamos começar? Cada pequeno passo conta!"