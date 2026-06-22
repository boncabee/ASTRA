"use client"

import { useEffect } from "react"
import { EmptyState } from "@/components/domain/empty-state"
import { AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error)
  }, [error])

  return (
    <div className="h-full flex items-center justify-center">
      <EmptyState
        icon={AlertCircle}
        title="Something went wrong!"
        description={error.message || "An unexpected error occurred while loading this page."}
        action={
          <Button onClick={() => reset()} variant="outline">
            Try again
          </Button>
        }
      />
    </div>
  )
}
