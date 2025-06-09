"use client"

import { useState, useEffect } from "react"
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend } from "recharts"

interface CountryData {
  "Highly Engaged Dutch Customers": number
  "Inactive Belgian Shoppers": number
  "Low-Intent Pay-Later Shoppers": number
  "NL Dormant Value Buyers": number
  country: string
}

interface ApiResponse {
  data: CountryData[]
  status: string
}

export function ClustersByCountry() {
  const [data, setData] = useState<CountryData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const response = await fetch("http://localhost:5000/ml/country-distribution")

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const result: ApiResponse = await response.json()

        if (result.status === "success" && result.data) {
          setData(result.data)
        } else {
          throw new Error("Invalid response format")
        }
      } catch (err) {
        console.error("Failed to fetch country distribution:", err)
        setError(err instanceof Error ? err.message : "Failed to fetch data")
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-2"></div>
          <p className="text-sm text-gray-500">Loading country data...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-[400px]">
        <div className="text-center">
          <p className="text-sm text-red-500 mb-2">Error loading data</p>
          <p className="text-xs text-gray-400">{error}</p>
        </div>
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-[400px]">
        <p className="text-sm text-gray-500">No country data available</p>
      </div>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <XAxis dataKey="country" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar
          dataKey="Highly Engaged Dutch Customers"
          stackId="a"
          fill="#9b8df2"
          name="Highly Engaged Dutch Customers"
        />
        <Bar dataKey="Inactive Belgian Shoppers" stackId="a" fill="#88cc99" name="Inactive Belgian Shoppers" />
        <Bar dataKey="Low-Intent Pay-Later Shoppers" stackId="a" fill="#f8c15c" name="Low-Intent Pay-Later Shoppers" />
        <Bar dataKey="NL Dormant Value Buyers" stackId="a" fill="#ff8c1a" name="NL Dormant Value Buyers" />
      </BarChart>
    </ResponsiveContainer>
  )
}
