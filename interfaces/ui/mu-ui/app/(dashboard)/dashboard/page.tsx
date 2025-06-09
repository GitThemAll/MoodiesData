import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { MetricsCards } from "@/components/metrics-cards"
import { RecentActivities } from "@/components/recent-activities"
import { PredictionActivity } from "@/components/prediction-activity"
import { OverviewChart } from "@/components/overview-chart"

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard Overview</h1>
        <p className="text-muted-foreground">Welcome back! Here's what's happening with your AI predictions.</p>
      </div>

      <MetricsCards />

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Analytics Overview</CardTitle>
            <CardDescription>Monthly performance metrics and trends</CardDescription>
          </CardHeader>
          <CardContent>
            <OverviewChart />
          </CardContent>
        </Card>

        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Recent Activities</CardTitle>
            <CardDescription>Latest system activities and updates</CardDescription>
          </CardHeader>
          <CardContent>
            <RecentActivities />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Prediction Activity</CardTitle>
          <CardDescription>Latest AI predictions and their accuracy scores</CardDescription>
        </CardHeader>
        <CardContent>
          <PredictionActivity />
        </CardContent>
      </Card>
    </div>
  )
}
