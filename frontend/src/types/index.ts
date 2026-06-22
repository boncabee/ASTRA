export type Severity = "critical" | "high" | "medium" | "low"
export type Priority = "critical" | "high" | "medium" | "low"
export type CaseStatus = "open" | "in_progress" | "resolved" | "closed"

export interface User {
  id: string
  username: string
  email: string
  role: string
  is_active?: boolean
}

export interface Case {
  id: string
  title: string
  description: string | null
  severity: Severity
  priority: Priority
  status: CaseStatus
  assigned_to: string | null
  created_by: string
  created_at: string
  updated_at: string
}

export interface TimelineEvent {
  id: string
  case_id: string
  event_type: string
  actor: string
  event_metadata: Record<string, any> | null
  created_at: string
}

export interface Alert {
  id: string
  title: string
  severity: Severity
  policyId: string
  timestamp: string
  isAssigned: boolean
}

export interface SystemHealth {
  apiUptime: number
  automationQueue: number
  systemErrors: number
  ingestionRate: number[]
}
