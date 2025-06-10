"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ChevronDown } from "lucide-react"
import { Label } from "@/components/ui/label"

interface NextMonthData {
  Email: string
  next_1_months_spend: number
}

interface Next3MonthData {
  Email: string
  next_3_months_spend: number
}

interface LifetimeData {
  Email: string
  "Lifetime CLV": number
}

interface CLVStats {
  highest: {
    next_month: number
    next_3_month: number
    lifetime: number
  }
  average: {
    next_month: number
    next_3_month: number
    lifetime: number
  }
}

export function CLVMetrics() {
  // All useState hooks first
  const [highestPeriod, setHighestPeriod] = useState("next_month")
  const [avgPeriod, setAvgPeriod] = useState("lifetime")
  const [showHighestDropdown, setShowHighestDropdown] = useState(false)
  const [showAvgDropdown, setShowAvgDropdown] = useState(false)
  const [clvStats, setCLVStats] = useState<CLVStats>({
    highest: { next_month: 0, next_3_month: 0, lifetime: 0 },
    average: { next_month: 0, next_3_month: 0, lifetime: 0 },
  })
  const [allCLVData, setAllCLVData] = useState<{
    nextMonth: NextMonthData[]
    next3Month: Next3MonthData[]
    lifetime: LifetimeData[]
  }>({
    nextMonth: [],
    next3Month: [],
    lifetime: [],
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // All useEffect hooks after useState
  useEffect(() => {
    const fetchCLVData = async () => {
      try {
        setLoading(true)

        // Fetch data from all three endpoints
        const [nextMonthRes, next3MonthRes, lifetimeRes] = await Promise.all([
          fetch("http://localhost:5000/clv/predictions/next-month"),
          fetch("http://localhost:5000/clv/predictions/next-three-months"),
          fetch("http://localhost:5000/clv/lifetime"),
        ])

        if (!nextMonthRes.ok || !next3MonthRes.ok || !lifetimeRes.ok) {
          throw new Error("Failed to fetch one or more CLV endpoints")
        }

        const [nextMonthData, next3MonthData, lifetimeData]: [NextMonthData[], Next3MonthData[], LifetimeData[]] =
          await Promise.all([nextMonthRes.json(), next3MonthRes.json(), lifetimeRes.json()])

        console.log("CLV Data loaded:", {
          nextMonth: nextMonthData.length,
          next3Month: next3MonthData.length,
          lifetime: lifetimeData.length,
        })

        console.log("Sample next month data:", nextMonthData.slice(0, 3))
        console.log("Sample next 3 month data:", next3MonthData.slice(0, 3))
        console.log("Sample lifetime data:", lifetimeData.slice(0, 3))

        // Store all data
        setAllCLVData({
          nextMonth: nextMonthData,
          next3Month: next3MonthData,
          lifetime: lifetimeData,
        })

        // Calculate statistics
        const stats = calculateStats(nextMonthData, next3MonthData, lifetimeData)
        setCLVStats(stats)
      } catch (err) {
        console.error("Failed to fetch CLV data:", err)
        setError(err instanceof Error ? err.message : "Failed to fetch CLV data")
      } finally {
        setLoading(false)
      }
    }

    fetchCLVData()
  }, [])

  // Constants and helper functions after hooks
  const periods = [
    { value: "next_month", label: "Next month" },
    { value: "next_3_month", label: "Next 3 month" },
    { value: "lifetime", label: "Lifetime" },
  ]

  // Calculate highest and average CLV for each period
  const calculateStats = (
    nextMonthData: NextMonthData[],
    next3MonthData: Next3MonthData[],
    lifetimeData: LifetimeData[],
  ): CLVStats => {
    // Next Month stats - using next_1_months_spend
    const nextMonthValues = nextMonthData.map((item) => item.next_1_months_spend).filter((val) => val > 0)
    const highestNextMonth = nextMonthValues.length > 0 ? Math.max(...nextMonthValues) : 0
    const avgNextMonth =
      nextMonthValues.length > 0 ? nextMonthValues.reduce((sum, val) => sum + val, 0) / nextMonthValues.length : 0

    // Next 3 Month stats
    const next3MonthValues = next3MonthData.map((item) => item.next_3_months_spend).filter((val) => val > 0)
    const highestNext3Month = next3MonthValues.length > 0 ? Math.max(...next3MonthValues) : 0
    const avgNext3Month =
      next3MonthValues.length > 0 ? next3MonthValues.reduce((sum, val) => sum + val, 0) / next3MonthValues.length : 0

    // Lifetime stats
    const lifetimeValues = lifetimeData.map((item) => item["Lifetime CLV"]).filter((val) => val > 0)
    const highestLifetime = lifetimeValues.length > 0 ? Math.max(...lifetimeValues) : 0
    const avgLifetime =
      lifetimeValues.length > 0 ? lifetimeValues.reduce((sum, val) => sum + val, 0) / lifetimeValues.length : 0

    console.log("Calculated stats:", {
      highest: {
        next_month: highestNextMonth,
        next_3_month: highestNext3Month,
        lifetime: highestLifetime,
      },
      average: {
        next_month: avgNextMonth,
        next_3_month: avgNext3Month,
        lifetime: avgLifetime,
      },
    })

    return {
      highest: {
        next_month: highestNextMonth,
        next_3_month: highestNext3Month,
        lifetime: highestLifetime,
      },
      average: {
        next_month: avgNextMonth,
        next_3_month: avgNext3Month,
        lifetime: avgLifetime,
      },
    }
  }

  const getHighestCLV = () => {
    const value = clvStats.highest[highestPeriod as keyof typeof clvStats.highest] || 0
    return `€${value.toFixed(2)}`
  }

  const getAvgCLV = () => {
    const value = clvStats.average[avgPeriod as keyof typeof clvStats.average] || 0
    return `€${value.toFixed(2)}`
  }

  const CustomDropdown = ({
    value,
    onChange,
    options,
    isOpen,
    setIsOpen,
  }: {
    value: string
    onChange: (value: string) => void
    options: { value: string; label: string }[]
    isOpen: boolean
    setIsOpen: (open: boolean) => void
  }) => (
    <div className="relative">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-3 py-2 text-sm border border-gray-300 rounded-md bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <span>{options.find((opt) => opt.value === value)?.label}</span>
        <ChevronDown className="h-4 w-4 text-gray-400" />
      </button>
      {isOpen && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg">
          {options.map((option) => (
            <button
              key={option.value}
              type="button"
              onClick={() => {
                onChange(option.value)
                setIsOpen(false)
              }}
              className="w-full px-3 py-2 text-sm text-left hover:bg-gray-100 focus:outline-none focus:bg-gray-100"
            >
              {option.label}
            </button>
          ))}
        </div>
      )}
    </div>
  )

  if (loading) {
    return (
      <div className="grid gap-6 md:grid-cols-2">
        {[...Array(2)].map((_, index) => (
          <Card key={index}>
            <CardHeader>
              <CardTitle className="text-lg">
                <div className="h-6 bg-gray-200 rounded animate-pulse"></div>
              </CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col h-full">
              <div className="space-y-2 mb-auto">
                <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
                <div className="h-8 bg-gray-200 rounded animate-pulse"></div>
              </div>
              <div className="text-center mt-4">
                <div className="h-12 bg-gray-200 rounded animate-pulse mb-4"></div>
                <div className="h-8 bg-gray-200 rounded animate-pulse"></div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">CLV Data Error</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <p className="text-sm text-red-500 mb-2">Failed to load CLV data</p>
              <p className="text-xs text-gray-400">{error}</p>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="grid gap-6 md:grid-cols-2">
      {/* Highest CLV */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Highest CLV</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col h-full">
          <div className="space-y-2 mb-auto">
            <Label htmlFor="highest-period" className="text-sm font-medium">
              Period
            </Label>
            <CustomDropdown
              value={highestPeriod}
              onChange={setHighestPeriod}
              options={periods}
              isOpen={showHighestDropdown}
              setIsOpen={setShowHighestDropdown}
            />
          </div>

          <div className="text-center mt-4">
            <div className="text-4xl font-bold mb-4">{getHighestCLV()}</div>
          </div>
        </CardContent>
      </Card>

      {/* Average CLV */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Avg CLV</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col h-full">
          <div className="space-y-2 mb-auto">
            <Label htmlFor="avg-period" className="text-sm font-medium">
              Period
            </Label>
            <CustomDropdown
              value={avgPeriod}
              onChange={setAvgPeriod}
              options={periods}
              isOpen={showAvgDropdown}
              setIsOpen={setShowAvgDropdown}
            />
          </div>

          <div className="text-center mt-4">
            <div className="text-4xl font-bold mb-4">{getAvgCLV()}</div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
