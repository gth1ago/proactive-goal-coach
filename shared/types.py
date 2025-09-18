from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class GoalStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"

class MicroGoalStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class BadgeType(str, Enum):
    STREAK = "streak"
    MILESTONE = "milestone"
    CONSISTENCY = "consistency"
    ACHIEVEMENT = "achievement"

class MicroGoal(BaseModel):
    id: str
    title: str
    description: str
    status: MicroGoalStatus = MicroGoalStatus.PENDING
    priority: Priority = Priority.MEDIUM
    estimated_time: int  # em minutos
    created_at: datetime
    completed_at: Optional[datetime] = None
    goal_id: str

class Goal(BaseModel):
    id: str
    title: str
    description: str
    status: GoalStatus = GoalStatus.ACTIVE
    target_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    progress: float = 0.0  # 0-100
    micro_goals: List[MicroGoal] = []
    tags: List[str] = []

class Badge(BaseModel):
    id: str
    name: str
    description: str
    type: BadgeType
    icon: str
    earned_at: datetime
    goal_id: Optional[str] = None

class Suggestion(BaseModel):
    id: str
    title: str
    description: str
    micro_goal_id: str
    priority: Priority
    suggested_time: Optional[str] = None  # "morning", "afternoon", "evening"
    created_at: datetime

class UserStats(BaseModel):
    total_goals: int
    completed_goals: int
    active_goals: int
    total_micro_goals: int
    completed_micro_goals: int
    current_streak: int
    badges: List[Badge] = []
    weekly_progress: Dict[str, float] = {}