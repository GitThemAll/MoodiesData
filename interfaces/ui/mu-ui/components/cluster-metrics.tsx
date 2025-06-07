"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

const data = [
  { cluster: "High Value", items: 8.5 },
  { cluster: "Regular", items: 4.2 },
  { cluster: "At Risk", items: 2.1 },
  { cluster: "New", items: 1.8 },
]

export function ClusterMetrics() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis dataKey="cluster" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="items" fill="#82ca9d" />
      </BarChart>
    </ResponsiveContainer>
  )
}
