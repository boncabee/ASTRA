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
import { Case } from "@/types"

export default function CasesPage({
  searchParams,
}: {
  searchParams: { page?: string; status?: string; sort?: string }
}) {
  // Parse Search Params
  const page = parseInt(searchParams.page || "1", 10)
  const statusFilter = searchParams.status
  const sortBy = searchParams.sort || "date"
  const pageSize = 10

  // 1. Filter
  let filteredCases = [...mockCases]
  if (statusFilter && statusFilter !== "all") {
    filteredCases = filteredCases.filter((c) => c.status === statusFilter)
  }

  // 2. Sort
  filteredCases.sort((a, b) => {
    if (sortBy === "severity") {
      const severityOrder = { critical: 0, high: 1, medium: 2, low: 3 }
      return severityOrder[a.severity] - severityOrder[b.severity]
    }
    // Default to date descending
    return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  })

  // 3. Paginate
  const totalCases = filteredCases.length
  const totalPages = Math.ceil(totalCases / pageSize)
  const paginatedCases = filteredCases.slice((page - 1) * pageSize, page * pageSize)

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

      {/* URL-based Filters / Controls */}
      <div className="flex items-center gap-4 bg-card p-2 rounded-md border border-border">
        <div className="text-sm font-medium mr-2">Filters:</div>
        <div className="flex gap-2">
          <Button variant={!statusFilter || statusFilter === "all" ? "default" : "outline"} size="sm" asChild>
            <Link href="?status=all">All</Link>
          </Button>
          <Button variant={statusFilter === "open" ? "default" : "outline"} size="sm" asChild>
            <Link href="?status=open">Open</Link>
          </Button>
          <Button variant={statusFilter === "in_progress" ? "default" : "outline"} size="sm" asChild>
            <Link href="?status=in_progress">In Progress</Link>
          </Button>
          <Button variant={statusFilter === "resolved" ? "default" : "outline"} size="sm" asChild>
            <Link href="?status=resolved">Resolved</Link>
          </Button>
        </div>

        <div className="ml-auto flex items-center gap-2 text-sm">
          <span className="text-muted-foreground">Sort by:</span>
          <Button variant={sortBy === "date" ? "default" : "outline"} size="sm" asChild>
            <Link href={`?sort=date&status=${statusFilter || "all"}`}>Date</Link>
          </Button>
          <Button variant={sortBy === "severity" ? "default" : "outline"} size="sm" asChild>
            <Link href={`?sort=severity&status=${statusFilter || "all"}`}>Severity</Link>
          </Button>
        </div>
      </div>

      <div className="rounded-md border border-border bg-card">
        {paginatedCases.length === 0 ? (
          <EmptyState
            icon={Shield}
            title="No Cases Found"
            description="There are currently no active security cases matching your criteria."
          />
        ) : (
          <>
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
                {paginatedCases.map((c) => (
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
            
            {/* Pagination Controls */}
            {totalPages > 1 && (
              <div className="flex items-center justify-end p-4 border-t border-border gap-2">
                <Button 
                  variant="outline" 
                  size="sm" 
                  disabled={page <= 1}
                  asChild={page > 1}
                >
                  {page > 1 ? (
                    <Link href={`?page=${page - 1}&status=${statusFilter || "all"}&sort=${sortBy}`}>Previous</Link>
                  ) : "Previous"}
                </Button>
                <div className="text-sm text-muted-foreground mx-2">
                  Page {page} of {totalPages}
                </div>
                <Button 
                  variant="outline" 
                  size="sm" 
                  disabled={page >= totalPages}
                  asChild={page < totalPages}
                >
                  {page < totalPages ? (
                    <Link href={`?page=${page + 1}&status=${statusFilter || "all"}&sort=${sortBy}`}>Next</Link>
                  ) : "Next"}
                </Button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
