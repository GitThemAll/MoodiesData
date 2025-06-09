"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ClusterDistribution } from "@/components/segments/cluster-distribution"
import { ClusterDescription } from "@/components/segments/cluster-description"
import { ClusterCards } from "@/components/segments/cluster-cards"
import { ClustersByCountry } from "@/components/segments/clusters-by-country"

export default function SegmentsPage() {
  const [selectedCluster, setSelectedCluster] = useState<string>("2") // Default to Highly Engaged

  const handleClusterChange = (clusterId: string) => {
    setSelectedCluster(clusterId)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Customer Segments</h1>
        <p className="text-muted-foreground">Analyze customer clusters and their behavior patterns.</p>
      </div>

      <ClusterCards />

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Cluster Distribution</CardTitle>
            <CardDescription>Distribution of customers across different segments</CardDescription>
          </CardHeader>
          <CardContent>
            <ClusterDistribution selectedCluster={selectedCluster} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Cluster Description</CardTitle>
            <CardDescription>Detailed insights and characteristics of each customer segment</CardDescription>
          </CardHeader>
          <CardContent>
            <ClusterDescription onClusterChange={handleClusterChange} />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Clusters by Country</CardTitle>
          <CardDescription>Geographic distribution of customer segments by country</CardDescription>
        </CardHeader>
        <CardContent>
          <ClustersByCountry />
        </CardContent>
      </Card>
    </div>
  )
}
