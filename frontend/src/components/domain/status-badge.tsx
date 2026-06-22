import { Badge } from "@/components/ui/badge"
import { Severity, CaseStatus } from "@/types"

export function SeverityBadge({ severity }: { severity: Severity }) {
  const variantMap: Record<Severity, "default" | "destructive" | "outline" | "secondary"> = {
    critical: "destructive",
    high: "default",
    medium: "secondary",
    low: "outline",
  }

  return (
    <Badge variant={variantMap[severity]} className="capitalize">
      {severity}
    </Badge>
  )
}

export function StatusBadge({ status }: { status: CaseStatus }) {
  const variantMap: Record<CaseStatus, "default" | "secondary" | "outline"> = {
    open: "default",
    in_progress: "secondary",
    resolved: "outline",
    closed: "outline",
  }

  return (
    <Badge variant={variantMap[status]} className="capitalize">
      {status.replace("_", " ")}
    </Badge>
  )
}
