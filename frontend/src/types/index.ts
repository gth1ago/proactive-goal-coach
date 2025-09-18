export enum GoalStatus {
  ACTIVE = "active",
  COMPLETED = "completed",
  PAUSED = "paused"
}

export enum MicroGoalStatus {
  PENDING = "pending",
  IN_PROGRESS = "in_progress",
  COMPLETED = "completed"
}

export enum Priority {
  LOW = "low",
  MEDIUM = "medium",
  HIGH = "high"
}

export enum BadgeType {
  STREAK = "streak",
  MILESTONE = "milestone",
  CONSISTENCY = "consistency",
  ACHIEVEMENT = "achievement"
}

export interface MicroGoal {
  id: string;
  title: string;
  description: string;
  status: MicroGoalStatus;
  priority: Priority;
  estimated_time: number;
  created_at: string;
  completed_at?: string;
  goal_id: string;
}

export interface Goal {
  id: string;
  title: string;
  description: string;
  status: GoalStatus;
  target_date?: string;
  created_at: string;
  updated_at: string;
  progress: number;
  micro_goals: MicroGoal[];
  tags: string[];
}

export interface Badge {
  id: string;
  name: string;
  description: string;
  type: BadgeType;
  icon: string;
  earned_at: string;
  goal_id?: string;
}

export interface Suggestion {
  id: string;
  title: string;
  description: string;
  micro_goal_id: string;
  priority: Priority;
  suggested_time?: string;
  created_at: string;
}

export interface UserStats {
  total_goals: number;
  completed_goals: number;
  active_goals: number;
  total_micro_goals: number;
  completed_micro_goals: number;
  current_streak: number;
  badges: Badge[];
  weekly_progress: Record<string, number>;
}

export interface DashboardData {
  stats: UserStats;
  overall_progress: number;
  featured_goals: Goal[];
  recent_badges: Badge[];
  motivational_message: string;
}