export type Severity = "critical" | "high" | "medium" | "low"

export type CaseStatus = "open" | "in_progress" | "resolved" | "closed"

export interface User {
  id: string
  name: string
  email: string
  avatarUrl?: string
}

export interface Case {
  id: string
  title: string
  description: string
  severity: Severity
  status: CaseStatus
  assignee: User | null
  createdAt: string
  updatedAt: string
}

export type TimelineEventType = "alert" | "observation" | "system" | "user"

export interface TimelineEvent {
  id: string
  caseId: string
  type: TimelineEventType
  title: string
  description: string
  timestamp: string
  actor?: User | "System"
  metadata?: Record<string, any>
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
