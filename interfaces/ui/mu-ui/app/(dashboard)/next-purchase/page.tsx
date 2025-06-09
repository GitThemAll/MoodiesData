import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

export default function NextPurchasePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Next Purchase Date</h1>
        <p className="text-muted-foreground">Predict when customers are likely to make their next purchase.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            Purchase Prediction
            <Badge variant="secondary">Coming Soon</Badge>
          </CardTitle>
          <CardDescription>This component will provide next purchase date predictions and analysis.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground">The Next Purchase Date component will include:</p>
          <ul className="list-disc list-inside space-y-2 text-sm text-muted-foreground">
            <li>Individual customer purchase predictions</li>
            <li>Purchase probability scores</li>
            <li>Seasonal purchase patterns</li>
            <li>Prediction confidence intervals</li>
            <li>Recommended marketing timing</li>
          </ul>
          <Button variant="outline" disabled>
            Configure Prediction Model
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
