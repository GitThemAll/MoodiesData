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

interface CombinedCLVEntry {
  email: string
  next_month: number
  next_3_month: number
  lifetime: number
}

export function CLVLeaderboard() {
  const [data, setData] = useState<CLVData[]>([])
  const [filteredData, setFilteredData] = useState<CLVData[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const sanitizeEmail = (rawEmail?: string) =>
    rawEmail?.trim().toLowerCase().replace(/^'+|'+$/g, "") || ""

  async function buildCLVLeaderboardData(): Promise<CombinedCLVEntry[]> {
    try {
      const [res1, res3, resLifetime] = await Promise.all([
        fetch("http://localhost:5000/clv/predictions/next-month"),
        fetch("http://localhost:5000/clv/predictions/next-three-months"),
        fetch("http://localhost:5000/clv/lifetime"),
      ])

      if (!res1.ok || !res3.ok || !resLifetime.ok) {
        throw new Error("Failed to fetch one or more CLV datasets")
      }

      const [data1, data3, dataLifetime] = await Promise.all([
        res1.json(),
        res3.json(),
        resLifetime.json(),
      ])

      const map1 = new Map<string, number>()
      const map3 = new Map<string, number>()
      const mapL = new Map<string, number>()

      data1.forEach((item: any) => {
        const email = sanitizeEmail(item.Email)
        if (email) map1.set(email, item["next_1_months_spend"] ?? 0)
      })

      data3.forEach((item: any) => {
        const email = sanitizeEmail(item.Email)
        if (email) map3.set(email, item["next_3_months_spend"] ?? 0)
      })

      dataLifetime.forEach((item: any) => {
        const email = sanitizeEmail(item.Email)
        if (email) mapL.set(email, item["Lifetime CLV"] ?? 0)
      })

      const allEmails = new Set<string>()
      for (const map of [map1, map3, mapL]) {
        for (const email of map.keys()) {
          allEmails.add(email)
        }
      }

      const leaderboard: CombinedCLVEntry[] = Array.from(allEmails).map((email) => {
        return {
          email,
          next_month: map1.get(email) || 0,
          next_3_month: map3.get(email) || 0,
          lifetime: mapL.get(email) || 0,
        }
      })

      return leaderboard.filter(
        (entry) => entry.next_month > 0 || entry.next_3_month > 0 || entry.lifetime > 0,
      )
    } catch (error) {
      console.error("Error building leaderboard:", error)
      throw error
    }
  }

  useEffect(() => {
    const loadData = async () => {
      try {
        const leaderboard = await buildCLVLeaderboardData()
        setData(leaderboard)
        setFilteredData(leaderboard)
      } catch (e: any) {
        setError("Failed to load leaderboard data.")
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  useEffect(() => {
    if (!searchTerm) {
      setFilteredData(data)
    } else {
      const term = searchTerm.toLowerCase()
      const filtered = data.filter((item) =>
        item.email.toLowerCase().includes(term) ||
        item.next_month.toString().includes(term) ||
        item.next_3_month.toString().includes(term) ||
        item.lifetime.toString().includes(term)
      )
      setFilteredData(filtered)
    }
  }, [searchTerm, data])

  const formatCurrency = (value: number) => `€${value.toFixed(2)}`

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
