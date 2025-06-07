import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Users, DollarSign, TrendingUp } from "lucide-react"

const clusters = [
  {
    name: "High Value Customers",
    customers: "1,234",
    sales: "$125,000",
    conversionRate: "8.5%",
    color: "bg-blue-500",
  },
  {
    name: "Regular Customers",
    customers: "2,456",
    sales: "$89,000",
    conversionRate: "5.2%",
    color: "bg-green-500",
  },
  {
    name: "At Risk Customers",
    customers: "987",
    sales: "$34,000",
    conversionRate: "2.1%",
    color: "bg-yellow-500",
  },
  {
    name: "New Customers",
    customers: "543",
    sales: "$12,000",
    conversionRate: "1.8%",
    color: "bg-orange-500",
  },
]

export function ClusterCards() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {clusters.map((cluster) => (
        <Card key={cluster.name}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{cluster.name}</CardTitle>
            <div className={`h-3 w-3 rounded-full ${cluster.color}`} />
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center space-x-2">
              <Users className="h-4 w-4 text-muted-foreground" />
              <span className="text-2xl font-bold">{cluster.customers}</span>
            </div>
            <div className="flex items-center space-x-2">
              <DollarSign className="h-4 w-4 text-muted-foreground" />
              <span className="text-lg font-semibold">{cluster.sales}</span>
            </div>
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">{cluster.conversionRate} conversion rate</span>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
