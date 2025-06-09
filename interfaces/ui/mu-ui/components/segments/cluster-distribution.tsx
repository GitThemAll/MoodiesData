"use client"

import { useState, useEffect } from "react"
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Cell } from "recharts"

interface ClusterData {
  color: string
  label: string
  value: number
}

interface ApiResponse {
  data: ClusterData[]
  status: string
}

export function ClusterDistribution() {
  const [data, setData] = useState<ClusterData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const response = await fetch("http://localhost:5000/ml/distribution")

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const result: ApiResponse = await response.json()

        if (result.status === "success" && result.data) {
          // Filter out "Cluster -1" data point and sort by value (descending)
          const filteredData = result.data
            .filter((item) => item.label !== "Cluster -1")
            .sort((a, b) => b.value - a.value)
          setData(filteredData)
        } else {
          throw new Error("Invalid response format")
        }
      } catch (err) {
        console.error("Failed to fetch cluster distribution:", err)
        setError(err instanceof Error ? err.message : "Failed to fetch data")
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[300px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-2"></div>
          <p className="text-sm text-gray-500">Loading cluster data...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-[300px]">
        <div className="text-center">
          <p className="text-sm text-red-500 mb-2">Error loading data</p>
          <p className="text-xs text-gray-400">{error}</p>
        </div>
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-[300px]">
        <p className="text-sm text-gray-500">No cluster data available</p>
      </div>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart layout="vertical" data={data} margin={{ top: 5, right: 30, left: 100, bottom: 20 }}>
        <XAxis
          type="number"
          tick={{ fontSize: 12 }}
          axisLine={{ stroke: "#e5e7eb" }}
          domain={[0, "dataMax"]}
          label={{ value: "Percentage (%)", position: "insideBottom", offset: -5 }}
        />
        <YAxis type="category" dataKey="label" tick={{ fontSize: 12 }} axisLine={{ stroke: "#e5e7eb" }} width={90} />
        <Tooltip
          formatter={(value) => [`${Number(value).toFixed(1)}%`, "Percentage"]}
          labelStyle={{ color: "#374151" }}
          contentStyle={{
            backgroundColor: "#f9fafb",
            border: "1px solid #e5e7eb",
            borderRadius: "6px",
          }}
        />
        <Bar dataKey="value" radius={[0, 4, 4, 0]} name="Cluster Distribution" barSize={30}>
          {data.map((entry, index) => {
            // The highest percentage cluster is the first one (index 0) since we sorted in descending order
            const color = index === 0 ? "#ef4444" : "rgb(198, 187, 206)"
            return <Cell key={`cell-${index}`} fill={color} />
          })}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
