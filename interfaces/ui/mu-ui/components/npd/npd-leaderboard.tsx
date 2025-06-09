"use client"

import { useState, useEffect } from "react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Input } from "@/components/ui/input"
import { Search } from "lucide-react"

interface NPDData {
  email: string
  predicted_days: number
  predicted_next_purchase_date: string
  avg_interval: number
  avg_order_value: number
  last_order_date: string
  total_spend: number
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
        const response = await fetch("http://localhost:5000/npd-predictions")

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const result = await response.json()

        // Sort by predicted_days (ascending - soonest purchases first)
        const sortedData = result.sort((a: NPDData, b: NPDData) => a.predicted_days - b.predicted_days)

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
          customer.predicted_days.toString().includes(searchTerm) ||
          customer.predicted_next_purchase_date.includes(searchTerm),
      )
      setFilteredData(filtered)
    }
  }, [searchTerm, data])

  // Format date to readable format
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })
  }

  // Calculate purchase probability based on predicted days (mock calculation)
  const calculateProbability = (days: number) => {
    // Simple inverse relationship - closer dates have higher probability
    const maxDays = 100
    const probability = Math.max(0.5, 1 - days / maxDays)
    return Math.min(0.95, probability)
  }

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
                  <TableCell className="text-white text-center">{customer.predicted_days} days</TableCell>
                  <TableCell className="text-white text-center">
                    {(calculateProbability(customer.predicted_days) * 100).toFixed(0)}%
                  </TableCell>
                  <TableCell className="text-white text-center">
                    {formatDate(customer.predicted_next_purchase_date)}
                  </TableCell>
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
