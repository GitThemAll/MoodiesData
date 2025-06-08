"use client"

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts"

const data = [
  { name: "Cluster -1", value: 38.79, color: "#ccc" },
  { name: "Regular", value: 25.73, color: "#88cc99" },
  { name: "High Value", value: 7.35, color: "#9b8df2" },
  { name: "At Risk", value: 22.99, color: "#f8c15c" },
  { name: "New", value: 5.14, color: "#ff8c1a" },
]

export function ClusterDistribution() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
          label={({ name, value }) => `${name} ${value.toFixed(1)}%`}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  )
}
