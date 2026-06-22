import { notFound } from "next/navigation"
import { SeverityBadge, StatusBadge } from "@/components/domain/status-badge"
import { CaseTimeline } from "@/components/domain/case-timeline"
import { CaseActions } from "@/components/domain/case-actions"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { getCaseById, getCaseTimeline } from "@/lib/api/cases"

export const dynamic = 'force-dynamic';

export default async function CaseDetailPage({ params }: { params: { id: string } }) {
  const caseId = params.id
  
  let caseData
  let events = []
  
  try {
    const [fetchedCase, fetchedEvents] = await Promise.all([
      getCaseById(caseId),
      getCaseTimeline(caseId)
    ])
    caseData = fetchedCase
    events = fetchedEvents
  } catch (error: any) {
    if (error.message.includes("404")) {
      notFound()
    }
    throw error // Let the error boundary catch it
  }

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold tracking-tight">{caseData.title}</h1>
            <SeverityBadge severity={caseData.severity} />
            <StatusBadge status={caseData.status} />
          </div>
          <p className="text-muted-foreground">
            {caseData.id} • Assigned to {caseData.assigned_to || "Unassigned"} • Created {new Date(caseData.created_at).toLocaleString()}
          </p>
        </div>
        <div className="flex gap-2">
          {caseData.status !== "closed" && (
            <>
              <Button variant="outline">Assign to Me</Button>
              <Button variant="destructive">Close Case</Button>
            </>
          )}
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <div className="md:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Description</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm">{caseData.description || "No description provided."}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <CaseTimeline events={events} />
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent>
              <CaseActions caseId={caseData.id} />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
