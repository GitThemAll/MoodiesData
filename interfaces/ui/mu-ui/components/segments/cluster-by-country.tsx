"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend } from "recharts"

const data = [
  { country: "United States", highValue: 150, regular: 280, atRisk: 120, new: 60 },
  { country: "Canada", highValue: 80, regular: 160, atRisk: 70, new: 35 },
  { country: "United Kingdom", highValue: 90, regular: 180, atRisk: 85, new: 40 },
  { country: "Australia", highValue: 60, regular: 140, atRisk: 55, new: 25 },
  { country: "Germany", highValue: 70, regular: 150, atRisk: 60, new: 30 },
]

export function ClustersByCountry() {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <XAxis dataKey="country" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="highValue" stackId="a" fill="#9b8df2" name="High Value" />
        <Bar dataKey="regular" stackId="a" fill="#88cc99" name="Regular" />
        <Bar dataKey="atRisk" stackId="a" fill="#f8c15c" name="At Risk" />
        <Bar dataKey="new" stackId="a" fill="#ff8c1a" name="New" />
      </BarChart>
    </ResponsiveContainer>
  )
}
