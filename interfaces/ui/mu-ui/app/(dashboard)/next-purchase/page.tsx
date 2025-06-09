import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { NPDLeaderboard } from "@/components/npd/npd-leaderboard"
import { NPDMetrics } from "@/components/npd/npd-metrics"

export default function NextPurchasePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Next Purchase Date</h1>
        <p className="text-muted-foreground">Predict when customers are likely to make their next purchase.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>NPD Leaderboard</CardTitle>
          <CardDescription>Customers ranked by their predicted next purchase date</CardDescription>
        </CardHeader>
        <CardContent>
          <NPDLeaderboard />
        </CardContent>
      </Card>

      <NPDMetrics />
    </div>
  )
}
