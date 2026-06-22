import { TimelineEvent } from "@/types"
import { Activity, AlertTriangle, Settings, User } from "lucide-react"

export function CaseTimeline({ events }: { events: TimelineEvent[] }) {
  if (events.length === 0) {
    return <div className="text-sm text-muted-foreground p-4">No events found for this case.</div>
  }

  const getIcon = (type: TimelineEvent["type"]) => {
    switch (type) {
      case "alert": return <AlertTriangle className="h-4 w-4 text-destructive" />
      case "observation": return <Activity className="h-4 w-4 text-primary" />
      case "system": return <Settings className="h-4 w-4 text-muted-foreground" />
      case "user": return <User className="h-4 w-4 text-secondary-foreground" />
    }
  }

  return (
    <div className="space-y-4">
      {events.map((event, index) => (
        <div key={event.id} className="relative flex gap-4">
          {/* Vertical line connector */}
          {index !== events.length - 1 && (
            <div className="absolute left-4 top-8 bottom-[-16px] w-px bg-border" />
          )}
          
          <div className="relative z-10 flex h-8 w-8 items-center justify-center rounded-full border border-border bg-background">
            {getIcon(event.type)}
          </div>
          
          <div className="flex-1 pb-4">
            <div className="flex items-center justify-between">
              <p className="text-sm font-medium">{event.title}</p>
              <time className="text-xs text-muted-foreground">
                {new Date(event.timestamp).toLocaleString()}
              </time>
            </div>
            <p className="text-sm text-muted-foreground mt-1">{event.description}</p>
            {event.metadata && (
              <pre className="mt-2 text-xs bg-muted p-2 rounded-md border border-border overflow-x-auto">
                {JSON.stringify(event.metadata, null, 2)}
              </pre>
            )}
            <p className="text-xs text-muted-foreground mt-2">
              Actor: {typeof event.actor === "string" ? event.actor : event.actor?.name}
            </p>
          </div>
        </div>
      ))}
    </div>
  )
}
