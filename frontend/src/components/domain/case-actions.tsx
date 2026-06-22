"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { toast } from "sonner"
import { Loader2 } from "lucide-react"

export function CaseActions({ caseId }: { caseId: string }) {
  const [pendingAction, setPendingAction] = useState<string | null>(null)

  const handleAction = async (actionName: string, type: "success" | "error" = "success") => {
    setPendingAction(actionName)
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    setPendingAction(null)
    
    if (type === "success") {
      toast.success(`${actionName} executed successfully for case ${caseId}`)
    } else {
      toast.error(`Failed to execute ${actionName}`)
    }
  }

  return (
    <div className="space-y-2">
      <Button 
        variant="outline" 
        className="w-full justify-start"
        onClick={() => handleAction("Run Playbook")}
        disabled={pendingAction !== null}
      >
        {pendingAction === "Run Playbook" && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        Run Playbook
      </Button>
      <Button 
        variant="outline" 
        className="w-full justify-start"
        onClick={() => handleAction("Block IP (Firewall)")}
        disabled={pendingAction !== null}
      >
        {pendingAction === "Block IP (Firewall)" && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        Block IP (Firewall)
      </Button>
      <Button 
        variant="outline" 
        className="w-full justify-start"
        onClick={() => handleAction("Lock User Account", "error")} // Simulate error for demo
        disabled={pendingAction !== null}
      >
        {pendingAction === "Lock User Account" && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        Lock User Account (Demo Error)
      </Button>
      <Separator className="my-4" />
      <Button 
        variant="secondary" 
        className="w-full justify-start"
        onClick={() => handleAction("Escalate to Tier 2")}
        disabled={pendingAction !== null}
      >
        {pendingAction === "Escalate to Tier 2" && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        Escalate to Tier 2
      </Button>
    </div>
  )
}
