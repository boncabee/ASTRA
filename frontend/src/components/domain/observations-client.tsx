"use client"

import { useState } from "react"
import Link from "next/link"
import { Observation } from "@/types"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { ObservationDrawer } from "@/components/domain/observation-drawer"
import { EmptyState } from "@/components/domain/empty-state"
import { Activity } from "lucide-react"

interface ObservationsClientProps {
  observations: Observation[]
  sortBy: string
  sortOrder: string
}

export function ObservationsClient({ observations, sortBy, sortOrder }: ObservationsClientProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null)

  const getSortLink = (column: string) => {
    // If clicking the currently sorted column, reverse the order
    const newOrder = sortBy === column && sortOrder === "asc" ? "desc" : "asc"
    // Keep existing filters? Yes, in a real app we'd preserve searchParams. 
    // Since this is a simple string return, we'll rely on the parent or handle it cleanly.
    // A robust way is to preserve current query params. We will assume window.location.search parsing.
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search)
      params.set("sort_by", column)
      params.set("sort_order", newOrder)
      return `?${params.toString()}`
    }
    return `?sort_by=${column}&sort_order=${newOrder}`
  }

  const renderSortIndicator = (column: string) => {
    if (sortBy !== column) return null
    return sortOrder === "asc" ? " ↑" : " ↓"
  }

  const getRiskColor = (score: number) => {
    if (score >= 90) return "destructive"
    if (score >= 70) return "destructive"
    if (score >= 40) return "default"
    return "secondary"
  }

  if (observations.length === 0) {
    return (
      <EmptyState
        icon={Activity}
        title="No Observations Found"
        description="Try adjusting your filters or search criteria."
      />
    )
  }

  return (
    <>
      <div className="rounded-md border border-border bg-card">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[120px]">ID</TableHead>
              <TableHead>
                <Link href={getSortLink("risk_score")} className="hover:underline">
                  Risk{renderSortIndicator("risk_score")}
                </Link>
              </TableHead>
              <TableHead>
                <Link href={getSortLink("status")} className="hover:underline">
                  Status{renderSortIndicator("status")}
                </Link>
              </TableHead>
              <TableHead>
                <Link href={getSortLink("classification")} className="hover:underline">
                  Classification{renderSortIndicator("classification")}
                </Link>
              </TableHead>
              <TableHead>Title</TableHead>
              <TableHead className="text-right">
                <Link href={getSortLink("created_at")} className="hover:underline">
                  Created At{renderSortIndicator("created_at")}
                </Link>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {observations.map((obs) => (
              <TableRow 
                key={obs.id} 
                className="cursor-pointer hover:bg-muted/50"
                onClick={() => setSelectedId(obs.id)}
              >
                <TableCell className="font-mono text-xs">{obs.id.split("-")[0]}</TableCell>
                <TableCell>
                  <Badge variant={getRiskColor(obs.risk_score)}>{obs.risk_score}</Badge>
                </TableCell>
                <TableCell>
                  <Badge variant={obs.status === "NEW" ? "default" : "secondary"}>
                    {obs.status}
                  </Badge>
                </TableCell>
                <TableCell>{obs.classification}</TableCell>
                <TableCell className="max-w-[300px] truncate">{obs.title}</TableCell>
                <TableCell className="text-right text-muted-foreground whitespace-nowrap">
                  {new Date(obs.created_at).toLocaleString()}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <ObservationDrawer 
        observationId={selectedId} 
        onClose={() => setSelectedId(null)} 
      />
    </>
  )
}
