"use client"

import { useState, useEffect } from "react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Input } from "@/components/ui/input"
import { Search } from "lucide-react"

interface NPDData {
  email: string
  days_to_purchase: number
  purchase_probability: number
  predicted_date: string
}

export function NPDLeaderboard() {
  const [data, setData] = useState<NPDData[]>([])
  const [filteredData, setFilteredData] = useState<NPDData[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        // Mock data for NPD
        const mockData: NPDData[] = [
          {
            email: "John@moodies.com",
            days_to_purchase: 5,
            purchase_probability: 0.87,
            predicted_date: "2024-06-15",
          },
          {
            email: "Silvia@moodies.com",
            days_to_purchase: 12,
            purchase_probability: 0.76,
            predicted_date: "2024-06-22",
          },
          {
            email: "Maria@moodies.com",
            days_to_purchase: 8,
            purchase_probability: 0.82,
            predicted_date: "2024-06-18",
          },
          {
            email: "David@moodies.com",
            days_to_purchase: 15,
            purchase_probability: 0.71,
            predicted_date: "2024-06-25",
          },
          {
            email: "Sarah@moodies.com",
            days_to_purchase: 3,
            purchase_probability: 0.92,
            predicted_date: "2024-06-13",
          },
          {
            email: "Michael@moodies.com",
            days_to_purchase: 21,
            purchase_probability: 0.65,
            predicted_date: "2024-07-01",
          },
          {
            email: "Emma@moodies.com",
            days_to_purchase: 7,
            purchase_probability: 0.84,
            predicted_date: "2024-06-17",
          },
          {
            email: "James@moodies.com",
            days_to_purchase: 18,
            purchase_probability: 0.68,
            predicted_date: "2024-06-28",
          },
          {
            email: "Lisa@moodies.com",
            days_to_purchase: 10,
            purchase_probability: 0.79,
            predicted_date: "2024-06-20",
          },
          {
            email: "Robert@moodies.com",
            days_to_purchase: 14,
            purchase_probability: 0.73,
            predicted_date: "2024-06-24",
          },
          {
            email: "Jennifer@moodies.com",
            days_to_purchase: 6,
            purchase_probability: 0.85,
            predicted_date: "2024-06-16",
          },
          {
            email: "William@moodies.com",
            days_to_purchase: 25,
            purchase_probability: 0.61,
            predicted_date: "2024-07-05",
          },
          {
            email: "Jessica@moodies.com",
            days_to_purchase: 9,
            purchase_probability: 0.81,
            predicted_date: "2024-06-19",
          },
          {
            email: "Christopher@moodies.com",
            days_to_purchase: 16,
            purchase_probability: 0.7,
            predicted_date: "2024-06-26",
          },
          {
            email: "Amanda@moodies.com",
            days_to_purchase: 4,
            purchase_probability: 0.89,
            predicted_date: "2024-06-14",
          },
        ]

        // Sort by days to purchase (ascending)
        const sortedData = mockData.sort((a, b) => a.days_to_purchase - b.days_to_purchase)

        // Simulate API delay
        await new Promise((resolve) => setTimeout(resolve, 1000))
        setData(sortedData)
        setFilteredData(sortedData)
      } catch (err) {
        console.error("Failed to fetch NPD data:", err)
        setError(err instanceof Error ? err.message : "Failed to fetch data")
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  // Filter data based on search term
  useEffect(() => {
    if (!searchTerm) {
      setFilteredData(data)
    } else {
      const filtered = data.filter(
        (customer) =>
          customer.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
          customer.days_to_purchase.toString().includes(searchTerm) ||
          customer.predicted_date.includes(searchTerm),
      )
      setFilteredData(filtered)
    }
  }, [searchTerm, data])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[200px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-2"></div>
          <p className="text-sm text-gray-500">Loading NPD data...</p>
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
    <div className="space-y-4">
      {/* Search Bar */}
      <div className="flex items-center gap-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Search by email, days, or date..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <div className="text-sm text-gray-500">
          {filteredData.length} of {data.length} customers
        </div>
      </div>

      {/* Table */}
      <div className="bg-gray-900 rounded-lg p-4">
        <div className="max-h-96 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
          <Table>
            <TableHeader className="sticky top-0 bg-gray-900 z-10">
              <TableRow className="border-gray-700 hover:bg-gray-800">
                <TableHead className="text-gray-300 font-medium w-8 text-center">#</TableHead>
                <TableHead className="text-gray-300 font-medium">Email</TableHead>
                <TableHead className="text-gray-300 font-medium text-center">Days to Purchase</TableHead>
                <TableHead className="text-gray-300 font-medium text-center">Probability</TableHead>
                <TableHead className="text-gray-300 font-medium text-center">Predicted Date</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredData.map((customer, index) => (
                <TableRow key={customer.email} className="border-gray-700 hover:bg-gray-800">
                  <TableCell className="text-gray-400 text-center font-medium">{index + 1}</TableCell>
                  <TableCell className="text-white font-medium">{customer.email}</TableCell>
                  <TableCell className="text-white text-center">{customer.days_to_purchase} days</TableCell>
                  <TableCell className="text-white text-center">
                    {(customer.purchase_probability * 100).toFixed(0)}%
                  </TableCell>
                  <TableCell className="text-white text-center">{customer.predicted_date}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
        <div className="mt-2 text-xs text-gray-400 text-center">
          Showing {filteredData.length} customers • Scroll to see more
        </div>
      </div>
    </div>
  )
}
