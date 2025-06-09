import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { InsightsFilters } from "@/components/insights/insights-filters"
import { MetricCards } from "@/components/insights/metric-cards"
import { TopSkusRevenue } from "@/components/insights/top-skus-revenue"
import { TopDiscountRevenue } from "@/components/insights/top-discount-revenue"

export default function InsightsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Insights Dashboard</h1>
        <p className="text-muted-foreground">Discover key metrics and insights about your business performance.</p>
      </div>

      <InsightsFilters />

      <MetricCards />

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Top SKUs by Revenue</CardTitle>
            <CardDescription>Highest performing products ranked by total revenue</CardDescription>
          </CardHeader>
          <CardContent>
            <TopSkusRevenue />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Top Discount Codes by Revenue</CardTitle>
            <CardDescription>Most profitable discount campaigns ranked by revenue</CardDescription>
          </CardHeader>
          <CardContent>
            <TopDiscountRevenue />
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
