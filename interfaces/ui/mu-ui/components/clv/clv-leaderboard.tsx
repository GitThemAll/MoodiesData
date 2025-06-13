"use client"

import { useState, useEffect } from "react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Input } from "@/components/ui/input"
import { Search } from "lucide-react"

interface CLVData {
  email: string
  next_month: number
  next_3_month: number
  lifetime: number
}

interface NextMonthData {
  Email: string
  next_1_months_spend: number // Changed from "Next Month CLV"
}

interface Next3MonthData {
  Email: string
  next_3_months_spend: number
}

interface LifetimeData {
  Email: string
  "Lifetime CLV": number
}

export function CLVLeaderboard() {
  const [data, setData] = useState<CLVData[]>([])
  const [filteredData, setFilteredData] = useState<CLVData[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)

        // Fetch data from all three endpoints
        const [nextMonthRes, next3MonthRes, lifetimeRes] = await Promise.all([
          fetch("http://localhost:8004/clv/predictions/next-month"),
          fetch("http://localhost:8004/clv/predictions/next-three-months"),
          fetch("http://localhost:8004/clv/lifetime"),
        ])

        if (!nextMonthRes.ok || !next3MonthRes.ok || !lifetimeRes.ok) {
          throw new Error("Failed to fetch one or more CLV endpoints")
        }

        const [nextMonthData, next3MonthData, lifetimeData]: [NextMonthData[], Next3MonthData[], LifetimeData[]] =
          await Promise.all([nextMonthRes.json(), next3MonthRes.json(), lifetimeRes.json()])

        console.log("Next Month Data:", nextMonthData.slice(0, 3))
        console.log("Next 3 Month Data:", next3MonthData.slice(0, 3))
        console.log("Lifetime Data:", lifetimeData.slice(0, 3))

        // Create maps for efficient lookup by email
        const nextMonthMap = new Map<string, number>()
        const next3MonthMap = new Map<string, number>()
        const lifetimeMap = new Map<string, number>()

        // Populate maps with email as key
        nextMonthData.forEach((item) => {
          const email = item.Email?.trim().toLowerCase()
          if (email) {
            nextMonthMap.set(email, item.next_1_months_spend || 0) // Changed from item["Next Month CLV"]
          }
        })

        next3MonthData.forEach((item) => {
          const email = item.Email?.trim().toLowerCase()
          if (email) {
            next3MonthMap.set(email, item.next_3_months_spend || 0)
          }
        })

        lifetimeData.forEach((item) => {
          const email = item.Email?.trim().toLowerCase()
          if (email) {
            lifetimeMap.set(email, item["Lifetime CLV"] || 0)
          }
        })

        console.log("Next Month Map size:", nextMonthMap.size)
        console.log("Next 3 Month Map size:", next3MonthMap.size)
        console.log("Lifetime Map size:", lifetimeMap.size)

        // Get all unique emails from all datasets (use lifetime as primary source)
        const allEmails = new Set<string>()

        // Add emails from all sources
        nextMonthData.forEach((item) => {
          const email = item.Email?.trim().toLowerCase()
          if (email) allEmails.add(email)
        })

        next3MonthData.forEach((item) => {
          const email = item.Email?.trim().toLowerCase()
          if (email) allEmails.add(email)
        })

        lifetimeData.forEach((item) => {
          const email = item.Email?.trim().toLowerCase()
          if (email) allEmails.add(email)
        })

        console.log("Total unique emails:", allEmails.size)

        // Combine data for each email by matching across all datasets
        const combinedData: CLVData[] = Array.from(allEmails).map((emailKey) => {
          // Find the original email format from one of the datasets (preserve original case)
          let originalEmail = emailKey

          // Try to find original email format from lifetime data first
          const lifetimeItem = lifetimeData.find((item) => item.Email?.trim().toLowerCase() === emailKey)
          if (lifetimeItem) {
            originalEmail = lifetimeItem.Email
          } else {
            // Fallback to next3Month data
            const next3MonthItem = next3MonthData.find((item) => item.Email?.trim().toLowerCase() === emailKey)
            if (next3MonthItem) {
              originalEmail = next3MonthItem.Email
            } else {
              // Fallback to nextMonth data
              const nextMonthItem = nextMonthData.find((item) => item.Email?.trim().toLowerCase() === emailKey)
              if (nextMonthItem) {
                originalEmail = nextMonthItem.Email
              }
            }
          }

          return {
            email: originalEmail,
            next_month: nextMonthMap.get(emailKey) || 0,
            next_3_month: next3MonthMap.get(emailKey) || 0,
            lifetime: lifetimeMap.get(emailKey) || 0,
          }
        })

        // Filter out entries where all values are 0 (no data found)
        const validData = combinedData.filter(
          (item) => item.next_month > 0 || item.next_3_month > 0 || item.lifetime > 0,
        )

        // Sort by lifetime value (descending), then by next_3_month, then by next_month
        const sortedData = validData.sort((a, b) => {
          if (b.lifetime !== a.lifetime) return b.lifetime - a.lifetime
          if (b.next_3_month !== a.next_3_month) return b.next_3_month - a.next_3_month
          return b.next_month - a.next_month
        })

        console.log("Final combined data:", sortedData.slice(0, 5))
        console.log("Total valid customers:", sortedData.length)

        setData(sortedData)
        setFilteredData(sortedData)
      } catch (err) {
        console.error("Failed to fetch CLV data:", err)
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
          customer.next_month.toString().includes(searchTerm) ||
          customer.next_3_month.toString().includes(searchTerm) ||
          customer.lifetime.toString().includes(searchTerm),
      )
      setFilteredData(filtered)
    }
  }, [searchTerm, data])

  // Format currency values
  const formatCurrency = (value: number) => {
    return `$${value.toFixed(2)}`
  }

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
    <div className="space-y-4">
      {/* Search Bar */}
      <div className="flex items-center gap-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Search by email or CLV values..."
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
                <TableHead className="text-gray-300 font-medium text-center">Next month</TableHead>
                <TableHead className="text-gray-300 font-medium text-center">Next 3 month</TableHead>
                <TableHead className="text-gray-300 font-medium text-center">Lifetime</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredData.map((customer, index) => (
                <TableRow key={customer.email} className="border-gray-700 hover:bg-gray-800">
                  <TableCell className="text-gray-400 text-center font-medium">{index + 1}</TableCell>
                  <TableCell className="text-white font-medium">{customer.email}</TableCell>
                  <TableCell className="text-white text-center">{formatCurrency(customer.next_month)}</TableCell>
                  <TableCell className="text-white text-center">{formatCurrency(customer.next_3_month)}</TableCell>
                  <TableCell className="text-white text-center">{formatCurrency(customer.lifetime)}</TableCell>
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
