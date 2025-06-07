"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend } from "recharts"

const data = [
  { city: "New York", highValue: 120, regular: 200, atRisk: 80, new: 40 },
  { city: "Los Angeles", highValue: 100, regular: 180, atRisk: 70, new: 35 },
  { city: "Chicago", highValue: 80, regular: 150, atRisk: 60, new: 30 },
  { city: "Houston", highValue: 70, regular: 140, atRisk: 55, new: 25 },
  { city: "Phoenix", highValue: 60, regular: 120, atRisk: 45, new: 20 },
]

export function ClustersByCity() {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <XAxis dataKey="city" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="highValue" stackId="a" fill="#8884d8" name="High Value" />
        <Bar dataKey="regular" stackId="a" fill="#82ca9d" name="Regular" />
        <Bar dataKey="atRisk" stackId="a" fill="#ffc658" name="At Risk" />
        <Bar dataKey="new" stackId="a" fill="#ff7300" name="New" />
      </BarChart>
    </ResponsiveContainer>
  )
}
