import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

const predictions = [
  {
    id: "PRED-001",
    customer: "Alice Cooper",
    type: "CLV Prediction",
    value: "$2,450",
    accuracy: "96%",
    status: "completed",
    date: "2024-01-10",
  },
  {
    id: "PRED-002",
    customer: "Bob Johnson",
    type: "Next Purchase",
    value: "Jan 18, 2024",
    accuracy: "89%",
    status: "completed",
    date: "2024-01-10",
  },
  {
    id: "PRED-003",
    customer: "Carol Smith",
    type: "CLV Prediction",
    value: "$1,890",
    accuracy: "94%",
    status: "processing",
    date: "2024-01-10",
  },
  {
    id: "PRED-004",
    customer: "David Wilson",
    type: "Churn Risk",
    value: "Low Risk",
    accuracy: "92%",
    status: "completed",
    date: "2024-01-09",
  },
]

export function PredictionActivity() {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>ID</TableHead>
          <TableHead>Customer</TableHead>
          <TableHead>Type</TableHead>
          <TableHead>Prediction</TableHead>
          <TableHead>Accuracy</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Date</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {predictions.map((prediction) => (
          <TableRow key={prediction.id}>
            <TableCell className="font-medium">{prediction.id}</TableCell>
            <TableCell>{prediction.customer}</TableCell>
            <TableCell>{prediction.type}</TableCell>
            <TableCell>{prediction.value}</TableCell>
            <TableCell>{prediction.accuracy}</TableCell>
            <TableCell>
              <Badge variant={prediction.status === "completed" ? "default" : "secondary"}>{prediction.status}</Badge>
            </TableCell>
            <TableCell>{prediction.date}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
