import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ClusterDistribution } from "@/components/cluster-distribution"
import { ClusterMetrics } from "@/components/cluster-metrics"
import { ClusterCards } from "@/components/cluster-cards"
import { ClustersByCity } from "@/components/clusters-by-city"

export default function SegmentsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Customer Segments</h1>
        <p className="text-muted-foreground">Analyze customer clusters and their behavior patterns.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Cluster Distribution</CardTitle>
            <CardDescription>Distribution of customers across different segments</CardDescription>
          </CardHeader>
          <CardContent>
            <ClusterDistribution />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Items per Cluster</CardTitle>
            <CardDescription>Average number of purchased items by cluster</CardDescription>
          </CardHeader>
          <CardContent>
            <ClusterMetrics />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Clusters by City</CardTitle>
          <CardDescription>Geographic distribution of customer segments</CardDescription>
        </CardHeader>
        <CardContent>
          <ClustersByCity />
        </CardContent>
      </Card>

      <ClusterCards />
    </div>
  )
}
