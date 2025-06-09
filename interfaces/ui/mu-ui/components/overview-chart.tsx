"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

const data = [
  { name: "Jan", predictions: 120, accuracy: 94 },
  { name: "Feb", predictions: 150, accuracy: 96 },
  { name: "Mar", predictions: 180, accuracy: 93 },
  { name: "Apr", predictions: 200, accuracy: 95 },
  { name: "May", predictions: 170, accuracy: 97 },
  { name: "Jun", predictions: 220, accuracy: 94 },
]

export function OverviewChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="predictions" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  )
}
