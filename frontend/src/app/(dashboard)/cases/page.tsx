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
import { getCases } from "@/lib/api/cases"
import { Case } from "@/types"

export const dynamic = 'force-dynamic';

export default async function CasesPage({
  searchParams,
}: {
  searchParams: { page?: string; status?: string; sort?: string }
}) {
  // Parse Search Params
  const page = parseInt(searchParams.page || "1", 10)
  const statusFilter = searchParams.status
  const sortBy = searchParams.sort || "date"
  const pageSize = 10
  const skip = (page - 1) * pageSize

  // Fetch from API
  // Note: Backend might not support generic "sort" out of the box, we only pass what is supported.
  const queryParams: any = { skip, limit: pageSize }
  if (statusFilter && statusFilter !== "all") {
    queryParams.case_status = statusFilter
  }
  // If backend supports severity filtering
  if (searchParams.sort === "severity") {
     // Sorting is generally handled by the backend. Since the backend signature is:
     // list_cases(skip, limit, case_status, priority, severity, assigned_to)
     // It does not have a "sort_by" parameter. We will rely on default backend sort.
  }

  let paginatedCases: Case[] = []
  let error = null
  try {
    paginatedCases = await getCases(queryParams)
  } catch (e: any) {
    error = e.message
  }

  // Next.js doesn't natively return "total count" in our current FastAPI endpoint setup, 
  // so we approximate pagination logic. If it returns `pageSize` items, assume there's a next page.
  const hasNextPage = paginatedCases.length === pageSize

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
      </div>

      {error && (
        <div className="bg-destructive/15 text-destructive p-4 rounded-md text-sm border border-destructive/20">
          Failed to load cases: {error}. Check if NEXT_PUBLIC_DEV_TOKEN is set and backend is running.
        </div>
      )}

      <div className="rounded-md border border-border bg-card">
        {paginatedCases.length === 0 && !error ? (
          <EmptyState
            icon={Shield}
            title="No Cases Found"
            description="There are currently no active security cases matching your criteria."
          />
        ) : (paginatedCases.length > 0 && (
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
                        {c.id.split('-')[0]}...
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
                      {c.assigned_to || "Unassigned"}
                    </TableCell>
                    <TableCell className="text-right text-muted-foreground">
                      {new Date(c.created_at).toLocaleString()}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            
            {/* Pagination Controls */}
            <div className="flex items-center justify-end p-4 border-t border-border gap-2">
              <Button 
                variant="outline" 
                size="sm" 
                disabled={page <= 1}
                asChild={page > 1}
              >
                {page > 1 ? (
                  <Link href={`?page=${page - 1}&status=${statusFilter || "all"}`}>Previous</Link>
                ) : "Previous"}
              </Button>
              <div className="text-sm text-muted-foreground mx-2">
                Page {page}
              </div>
              <Button 
                variant="outline" 
                size="sm" 
                disabled={!hasNextPage}
                asChild={hasNextPage}
              >
                {hasNextPage ? (
                  <Link href={`?page=${page + 1}&status=${statusFilter || "all"}`}>Next</Link>
                ) : "Next"}
              </Button>
            </div>
          </>
        ))}
      </div>
    </div>
  )
}
