import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Activity, AlertTriangle, ShieldAlert, Zap } from "lucide-react"
import { mockHealth, mockCases, mockAlerts } from "@/lib/mock-data"
import { SeverityBadge } from "@/components/domain/status-badge"
import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function DashboardPage() {
  const openCases = mockCases.filter(c => c.status !== "closed" && c.status !== "resolved")
  const criticalCases = openCases.filter(c => c.severity === "critical")
  const unassignedAlerts = mockAlerts.filter(a => !a.isAssigned)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Overview of your security posture and operational health.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">API Uptime</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockHealth.apiUptime}%</div>
            <p className="text-xs text-muted-foreground">Last 30 days</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Automation Queue</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockHealth.automationQueue}</div>
            <p className="text-xs text-muted-foreground">Pending actions</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical Cases</CardTitle>
            <ShieldAlert className="h-4 w-4 text-destructive" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-destructive">{criticalCases.length}</div>
            <p className="text-xs text-muted-foreground">Require immediate triage</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Unassigned Alerts</CardTitle>
            <AlertTriangle className="h-4 w-4 text-warning" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{unassignedAlerts.length}</div>
            <p className="text-xs text-muted-foreground">Waiting for correlation</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Active Cases</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {openCases.length === 0 ? (
                <div className="text-sm text-muted-foreground">No active cases.</div>
              ) : (
                openCases.slice(0, 5).map(c => (
                  <div key={c.id} className="flex items-center justify-between">
                    <div className="space-y-1">
                      <p className="text-sm font-medium leading-none">{c.title}</p>
                      <p className="text-xs text-muted-foreground">{c.id} • Assigned to: {c.assignee?.name || "Unassigned"}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <SeverityBadge severity={c.severity} />
                      <Button variant="outline" size="sm" asChild>
                        <Link href={`/cases/${c.id}`}>View</Link>
                      </Button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
