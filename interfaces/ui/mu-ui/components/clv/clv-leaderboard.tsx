"use client"

import { useState, useEffect } from "react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

interface CLVData {
  email: string
  next_month: number
  next_3_month: number
  lifetime: number
}

export function CLVLeaderboard() {
  const [data, setData] = useState<CLVData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        // Extended mock data with more customers
        const mockData: CLVData[] = [
          {
            email: "John@moodies.com",
            next_month: 15,
            next_3_month: 45,
            lifetime: 423,
          },
          {
            email: "Silvia@moodies.com",
            next_month: 39,
            next_3_month: 200,
            lifetime: 350,
          },
          {
            email: "Maria@moodies.com",
            next_month: 28,
            next_3_month: 85,
            lifetime: 298,
          },
          {
            email: "David@moodies.com",
            next_month: 22,
            next_3_month: 67,
            lifetime: 245,
          },
          {
            email: "Sarah@moodies.com",
            next_month: 18,
            next_3_month: 54,
            lifetime: 189,
          },
          {
            email: "Michael@moodies.com",
            next_month: 32,
            next_3_month: 96,
            lifetime: 312,
          },
          {
            email: "Emma@moodies.com",
            next_month: 25,
            next_3_month: 75,
            lifetime: 267,
          },
          {
            email: "James@moodies.com",
            next_month: 19,
            next_3_month: 57,
            lifetime: 198,
          },
          {
            email: "Lisa@moodies.com",
            next_month: 35,
            next_3_month: 105,
            lifetime: 389,
          },
          {
            email: "Robert@moodies.com",
            next_month: 21,
            next_3_month: 63,
            lifetime: 234,
          },
          {
            email: "Jennifer@moodies.com",
            next_month: 27,
            next_3_month: 81,
            lifetime: 276,
          },
          {
            email: "William@moodies.com",
            next_month: 16,
            next_3_month: 48,
            lifetime: 167,
          },
          {
            email: "Jessica@moodies.com",
            next_month: 31,
            next_3_month: 93,
            lifetime: 325,
          },
          {
            email: "Christopher@moodies.com",
            next_month: 24,
            next_3_month: 72,
            lifetime: 256,
          },
          {
            email: "Amanda@moodies.com",
            next_month: 20,
            next_3_month: 60,
            lifetime: 213,
          },
        ]

        // Sort by lifetime value (descending)
        const sortedData = mockData.sort((a, b) => b.lifetime - a.lifetime)

        // Simulate API delay
        await new Promise((resolve) => setTimeout(resolve, 1000))
        setData(sortedData)
      } catch (err) {
        console.error("Failed to fetch CLV data:", err)
        setError(err instanceof Error ? err.message : "Failed to fetch data")
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[200px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-2"></div>
          <p className="text-sm text-gray-500">Loading CLV data...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-[200px]">
        <div className="text-center">
          <p className="text-sm text-red-500 mb-2">Error loading data</p>
          <p className="text-xs text-gray-400">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-gray-900 rounded-lg p-4">
      <div className="max-h-96 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
        <Table>
          <TableHeader className="sticky top-0 bg-gray-900 z-10">
            <TableRow className="border-gray-700 hover:bg-gray-800">
              <TableHead className="text-gray-300 font-medium w-8 text-center">#</TableHead>
              <TableHead className="text-gray-300 font-medium">Email</TableHead>
              <TableHead className="text-gray-300 font-medium text-center">Next month</TableHead>
              <TableHead className="text-gray-300 font-medium text-center">Next 3 month</TableHead>
              <TableHead className="text-gray-300 font-medium text-center">Lifetime</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.map((customer, index) => (
              <TableRow key={customer.email} className="border-gray-700 hover:bg-gray-800">
                <TableCell className="text-gray-400 text-center font-medium">{index + 1}</TableCell>
                <TableCell className="text-white font-medium">{customer.email}</TableCell>
                <TableCell className="text-white text-center">€{customer.next_month}</TableCell>
                <TableCell className="text-white text-center">€{customer.next_3_month}</TableCell>
                <TableCell className="text-white text-center">€{customer.lifetime}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <div className="mt-2 text-xs text-gray-400 text-center">Showing {data.length} customers • Scroll to see more</div>
    </div>
  )
}
