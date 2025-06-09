import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ClusterDistribution } from "@/components/segments/cluster-distribution"
import { ModelAccuracy } from "@/components/segments/model-accuracy"
import { ClusterCards } from "@/components/segments/cluster-cards"
import { ClustersByCountry } from "@/components/segments/clusters-by-country"

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
            <CardTitle>Model Accuracy</CardTitle>
            <CardDescription>Segmentation model performance and accuracy metrics</CardDescription>
          </CardHeader>
          <CardContent>
            <ModelAccuracy />
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

      <ClusterCards />
    </div>
  )
}
