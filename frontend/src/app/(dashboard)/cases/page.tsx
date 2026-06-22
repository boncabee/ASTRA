import { mockCases } from "@/lib/mock-data"
import { SeverityBadge, StatusBadge } from "@/components/domain/status-badge"
import { EmptyState } from "@/components/domain/empty-state"
import { Shield } from "lucide-react"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function CasesPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Cases</h1>
          <p className="text-muted-foreground">
            Manage and investigate security incidents.
          </p>
        </div>
        <Button>Create Case</Button>
      </div>

      <div className="rounded-md border border-border">
        {mockCases.length === 0 ? (
          <EmptyState
            icon={Shield}
            title="No Cases Found"
            description="There are currently no active security cases matching your criteria."
          />
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[100px]">ID</TableHead>
                <TableHead>Title</TableHead>
                <TableHead>Severity</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Assignee</TableHead>
                <TableHead className="text-right">Created</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockCases.map((c) => (
                <TableRow key={c.id}>
                  <TableCell className="font-medium">
                    <Link href={`/cases/${c.id}`} className="hover:underline text-primary">
                      {c.id}
                    </Link>
                  </TableCell>
                  <TableCell>{c.title}</TableCell>
                  <TableCell>
                    <SeverityBadge severity={c.severity} />
                  </TableCell>
                  <TableCell>
                    <StatusBadge status={c.status} />
                  </TableCell>
                  <TableCell className="text-muted-foreground">
                    {c.assignee?.name || "Unassigned"}
                  </TableCell>
                  <TableCell className="text-right text-muted-foreground">
                    {new Date(c.createdAt).toLocaleString()}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  )
}
