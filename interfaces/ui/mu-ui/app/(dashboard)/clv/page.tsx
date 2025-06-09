import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CLVLeaderboard } from "@/components/clv/clv-leaderboard"
import { CLVDistribution } from "@/components/clv/clv-distribution"
import { CLVMetrics } from "@/components/clv/clv-metrics"

export default function CLVPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Customer Lifetime Value</h1>
        <p className="text-muted-foreground">
          Analyze and predict customer lifetime value across different time periods.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>CLV Leaderboard</CardTitle>
          <CardDescription>Top customers ranked by their predicted lifetime value</CardDescription>
        </CardHeader>
        <CardContent>
          <CLVLeaderboard />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>CLV Distribution</CardTitle>
          <CardDescription>Distribution of customers across different CLV ranges</CardDescription>
        </CardHeader>
        <CardContent>
          <CLVDistribution />
        </CardContent>
      </Card>

      <CLVMetrics />
    </div>
  )
}
