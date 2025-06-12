import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, Clock, DollarSign, Activity } from "lucide-react"

const metrics = [
  {
    title: "Avg Time",
    value: "2.4 days",
    description: "Average time between purchases",
    icon: Clock,
    trend: "+12%",
  },
  {
    title: "Next Purchase Date",
    value: "Jan 15, 2024",
    description: "Predicted next purchase",
    icon: TrendingUp,
    trend: "3 days",
  },
  {
    title: "Avg CLV This Month",
    value: "$1,234",
    description: "Customer lifetime value",
    icon: DollarSign,
    trend: "+8%",
  },
  {
    title: "Prediction Accuracy",
    value: "94.2%",
    description: "Model accuracy rate",
    icon: Activity,
    trend: "+2.1%",
  },
]

export function MetricsCards() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      
    </div>
  )
}
