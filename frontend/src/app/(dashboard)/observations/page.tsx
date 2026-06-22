import { getObservations } from "@/lib/api/observations"
import { ObservationsClient } from "@/components/domain/observations-client"
import { Observation } from "@/types"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { cookies } from "next/headers"

export const dynamic = 'force-dynamic';

export default async function ObservationsPage({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined }
}) {
  const cookieStore = await cookies()
  const token = cookieStore.get("astra_token")?.value
  
  const searchParamsResolved = await searchParams

  // Parse Search Params
  const page = parseInt((searchParamsResolved.page as string) || "1", 10)
  const pageSize = 50
  const skip = (page - 1) * pageSize
  
  const statusFilter = searchParamsResolved.status as string | undefined
  const riskCategory = searchParamsResolved.risk_category as string | undefined
  const sortBy = (searchParamsResolved.sort_by as string) || "created_at"
  const sortOrder = (searchParamsResolved.sort_order as string) || "desc"

  let observations: Observation[] = []
  let total = 0
  let error = null

  try {
    const res = await getObservations({
      skip,
      limit: pageSize,
      status: statusFilter,
      risk_category: riskCategory,
      sort_by: sortBy,
      sort_order: sortOrder
    }, token)
    
    observations = res.data || []
    total = res.total || 0
  } catch (e: any) {
    error = e.message
  }

  const totalPages = Math.ceil(total / pageSize)
  const hasNextPage = page < totalPages

  // Helper for generating filter URLs while preserving sort
  const getFilterUrl = (key: string, value: string) => {
    const params = new URLSearchParams()
    if (sortBy !== "created_at") params.set("sort_by", sortBy)
    if (sortOrder !== "desc") params.set("sort_order", sortOrder)
    if (key === "status" && value !== "ALL") params.set("status", value)
    if (key === "risk_category" && value !== "ALL") params.set("risk_category", value)
    
    // Preserve the other filter if changing one
    if (key === "status" && riskCategory && riskCategory !== "ALL") params.set("risk_category", riskCategory)
    if (key === "risk_category" && statusFilter && statusFilter !== "ALL") params.set("status", statusFilter)

    return `?${params.toString()}`
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Observations Explorer</h1>
          <p className="text-muted-foreground">
            Filter, sort, and triage security observations. ({total} total)
          </p>
        </div>
      </div>

      {/* URL-based Filters */}
      <div className="flex items-center gap-6 bg-card p-4 rounded-md border border-border">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-muted-foreground">Status:</span>
          <Button variant={!statusFilter || statusFilter === "ALL" ? "default" : "outline"} size="sm" asChild>
            <Link href={getFilterUrl("status", "ALL")}>All</Link>
          </Button>
          <Button variant={statusFilter === "NEW" ? "default" : "outline"} size="sm" asChild>
            <Link href={getFilterUrl("status", "NEW")}>New</Link>
          </Button>
          <Button variant={statusFilter === "TRIAGED" ? "default" : "outline"} size="sm" asChild>
            <Link href={getFilterUrl("status", "TRIAGED")}>Triaged</Link>
          </Button>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-muted-foreground">Risk:</span>
          <Button variant={!riskCategory || riskCategory === "ALL" ? "default" : "outline"} size="sm" asChild>
            <Link href={getFilterUrl("risk_category", "ALL")}>All</Link>
          </Button>
          <Button variant={riskCategory === "CRITICAL" ? "default" : "outline"} size="sm" asChild>
            <Link href={getFilterUrl("risk_category", "CRITICAL")}>Critical</Link>
          </Button>
          <Button variant={riskCategory === "HIGH" ? "default" : "outline"} size="sm" asChild>
            <Link href={getFilterUrl("risk_category", "HIGH")}>High</Link>
          </Button>
        </div>
      </div>

      {error && (
        <div className="bg-destructive/15 text-destructive p-4 rounded-md text-sm border border-destructive/20">
          Failed to load observations: {error}
        </div>
      )}

      {!error && (
        <>
          <ObservationsClient observations={observations} sortBy={sortBy} sortOrder={sortOrder} />

          {/* Pagination Controls */}
          <div className="flex items-center justify-end p-4 border border-border rounded-md bg-card gap-2">
            <Button 
              variant="outline" 
              size="sm" 
              disabled={page <= 1}
              asChild={page > 1}
            >
              {page > 1 ? (
                <Link href={`?page=${page - 1}&sort_by=${sortBy}&sort_order=${sortOrder}${statusFilter ? `&status=${statusFilter}` : ""}${riskCategory ? `&risk_category=${riskCategory}` : ""}`}>
                  Previous
                </Link>
              ) : "Previous"}
            </Button>
            <div className="text-sm text-muted-foreground mx-2">
              Page {page} of {totalPages || 1}
            </div>
            <Button 
              variant="outline" 
              size="sm" 
              disabled={!hasNextPage}
              asChild={hasNextPage}
            >
              {hasNextPage ? (
                <Link href={`?page=${page + 1}&sort_by=${sortBy}&sort_order=${sortOrder}${statusFilter ? `&status=${statusFilter}` : ""}${riskCategory ? `&risk_category=${riskCategory}` : ""}`}>
                  Next
                </Link>
              ) : "Next"}
            </Button>
          </div>
        </>
      )}
    </div>
  )
}
