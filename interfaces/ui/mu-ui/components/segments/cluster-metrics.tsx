"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

// Updated data structure to match the provided JSON
const data = [
  { label: "Cluster -1", avg_items: 5.55 },
  { label: "High Value", avg_items: 2.67 },
  { label: "Regular", avg_items: 2.67 },
  { label: "At Risk", avg_items: 3.06 },
  { label: "New", avg_items: 3.1 },
]

export function ClusterMetrics() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis dataKey="label" />
        <YAxis />
        <Tooltip formatter={(value) => [`${value.toFixed(2)} items`, "Average Items"]} />
        <Bar dataKey="avg_items" name="Average Items" fill="#82ca9d" />
      </BarChart>
    </ResponsiveContainer>
  )
}
