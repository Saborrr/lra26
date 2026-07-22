export type Role = 'participant' | 'admin' | 'superadmin';

export interface CurrentUser {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  role: Role;
  trainer_id: number | null;
}

export interface Team {
  id: number;
  name: string;
  trainer?: number | null;
  trainer_name: string | null;
  score: number;
  penalty: number;
  total_score: number;
  color: string;
  logo?: string | null;
  position?: number | null;
}

export interface Quest {
  id: string;
  title: string;
  description: string;
  points: number;
  category: string;
  order: number;
  active: boolean;
}

export interface Score {
  id: number;
  team: number;
  team_name: string;
  quest: string;
  quest_title: string;
  points: number;
  verified: boolean;
  notes: string;
  updated_at: string;
}

export interface Trainer {
  id: number;
  user: number | null;
  username: string | null;
  name: string;
  telegram_id?: number | null;
  teams_count: number;
}

export interface ParticipantAccount {
  id: number;
  username: string;
  display_name: string;
  trainer_id: number | null;
  is_active: boolean;
}

export interface Penalty {
  id: number;
  team: number;
  team_name: string;
  reason: string;
  penalty: number;
  created_at: string;
}

export interface ManagedUser {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  is_active: boolean;
  current_role: Role;
}

export interface AuditEvent {
  id: number;
  actor_name: string | null;
  action: string;
  target_type: string;
  target_id: string;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
