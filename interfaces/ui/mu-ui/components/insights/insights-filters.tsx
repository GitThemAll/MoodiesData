"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Calendar, RefreshCw } from "lucide-react"

export function InsightsFilters() {
  const [startDate, setStartDate] = useState("2024-03-01")
  const [endDate, setEndDate] = useState("2025-06-01")

  const handleRefresh = () => {
    // Trigger refresh of all components
    window.location.reload()
  }

  const handleApplyFilters = () => {
    // Here you would typically call an API with the date range
    console.log("Applying filters:", { startDate, endDate })
    // You can add your API call logic here
  }

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex flex-wrap items-end gap-4">
          <div className="flex items-center gap-2">
            <Calendar className="h-4 w-4 text-muted-foreground" />
            <div className="space-y-2">
              <Label htmlFor="start-date" className="text-sm font-medium text-gray-500">
                Start Date
              </Label>
              <Input
                id="start-date"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="w-[150px] bg-gray-100 text-gray-500 cursor-not-allowed"
                disabled
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="end-date" className="text-sm font-medium text-gray-500">
              End Date
            </Label>
            <Input
              id="end-date"
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-[150px] bg-gray-100 text-gray-500 cursor-not-allowed"
              disabled
            />
          </div>

          <Button onClick={handleApplyFilters} className="bg-blue-600 hover:bg-blue-700" disabled>
            Apply Filters
          </Button>

          <Button variant="outline" onClick={handleRefresh}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
