"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Observation, ObservationStatus } from "@/types"
import { getObservationById, updateObservationStatus } from "@/lib/api/observations"
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from "@/components/ui/sheet"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Loader2 } from "lucide-react"
import { toast } from "sonner"

interface ObservationDrawerProps {
  observationId: string | null
  onClose: () => void
}

export function ObservationDrawer({ observationId, onClose }: ObservationDrawerProps) {
  const [observation, setObservation] = useState<Observation | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isUpdating, setIsUpdating] = useState(false)
  const router = useRouter()

  useEffect(() => {
    if (!observationId) {
      setObservation(null)
      return
    }

    const fetchObservation = async () => {
      setIsLoading(true)
      try {
        const res = await getObservationById(observationId)
        setObservation(res.data)
      } catch (error: any) {
        toast.error("Failed to load observation details")
        onClose()
      } finally {
        setIsLoading(false)
      }
    }

    fetchObservation()
  }, [observationId, onClose])

  const handleStatusUpdate = async (newStatus: ObservationStatus) => {
    if (!observation) return

    setIsUpdating(true)
    try {
      const res = await updateObservationStatus(observation.id, newStatus)
      setObservation(res.data)
      toast.success(`Observation marked as ${newStatus}`)
      router.refresh()
    } catch (error: any) {
      toast.error(error.message || "Failed to update status")
    } finally {
      setIsUpdating(false)
    }
  }

  const getRiskColor = (score: number) => {
    if (score >= 90) return "destructive"
    if (score >= 70) return "destructive"
    if (score >= 40) return "default" // Using default as secondary/warning if not configured
    return "secondary"
  }

  return (
    <Sheet open={!!observationId} onOpenChange={(open) => !open && onClose()}>
      <SheetContent className="w-[400px] sm:w-[540px] flex flex-col h-full overflow-hidden">
        <SheetHeader className="pb-4 border-b border-border">
          <div className="flex items-center justify-between">
            <SheetTitle>Observation Details</SheetTitle>
            {observation && (
              <Badge variant={getRiskColor(observation.risk_score)}>
                Risk: {observation.risk_score}
              </Badge>
            )}
          </div>
          <SheetDescription>
            {observationId}
          </SheetDescription>
        </SheetHeader>

        <ScrollArea className="flex-1 py-4">
          {isLoading ? (
            <div className="flex items-center justify-center h-40">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          ) : observation ? (
            <div className="space-y-6 pr-4">
              <div>
                <h3 className="font-semibold mb-1">Title</h3>
                <p className="text-sm text-muted-foreground">{observation.title}</p>
              </div>
              
              <div>
                <h3 className="font-semibold mb-1">Description</h3>
                <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                  {observation.description}
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h3 className="font-semibold mb-1">Status</h3>
                  <Badge variant={observation.status === ObservationStatus.NEW ? "default" : "secondary"}>
                    {observation.status}
                  </Badge>
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Classification</h3>
                  <Badge variant="outline">{observation.classification}</Badge>
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Correlation ID</h3>
                  <span className="text-xs font-mono break-all">{observation.correlation_id}</span>
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Evidence Count</h3>
                  <span className="text-sm">{observation.evidence_count}</span>
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Created At</h3>
                  <span className="text-sm text-muted-foreground">
                    {new Date(observation.created_at).toLocaleString()}
                  </span>
                </div>
              </div>

            </div>
          ) : (
            <div className="text-center text-muted-foreground mt-8">
              No observation loaded.
            </div>
          )}
        </ScrollArea>

        {observation && (
          <div className="pt-4 border-t border-border flex flex-col gap-2">
            <h3 className="text-sm font-semibold mb-2">Actions</h3>
            <div className="flex flex-wrap gap-2">
              {observation.status !== ObservationStatus.TRIAGED && (
                <Button 
                  size="sm" 
                  onClick={() => handleStatusUpdate(ObservationStatus.TRIAGED)}
                  disabled={isUpdating}
                >
                  Mark Triaged
                </Button>
              )}
              {observation.status !== ObservationStatus.ESCALATED && (
                <Button 
                  size="sm" 
                  variant="destructive"
                  onClick={() => handleStatusUpdate(ObservationStatus.ESCALATED)}
                  disabled={isUpdating}
                >
                  Escalate
                </Button>
              )}
              {observation.status !== ObservationStatus.CLOSED && (
                <Button 
                  size="sm" 
                  variant="secondary"
                  onClick={() => handleStatusUpdate(ObservationStatus.CLOSED)}
                  disabled={isUpdating}
                >
                  Close (False Positive)
                </Button>
              )}
            </div>
          </div>
        )}
      </SheetContent>
    </Sheet>
  )
}
