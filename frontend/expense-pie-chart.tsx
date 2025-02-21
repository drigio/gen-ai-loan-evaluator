"use client"

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip, Legend } from "recharts"

const data = [
  { name: "Housing", value: 1000 },
  { name: "Transportation", value: 300 },
  { name: "Food", value: 400 },
  { name: "Utilities", value: 200 },
  { name: "Entertainment", value: 150 },
]

const COLORS = ["#22c55e", "#3b82f6", "#eab308", "#ec4899", "#8b5cf6"]

export function ExpensePieChart() {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={80}
          fill="#8884d8"
          paddingAngle={5}
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip
          content={({ active, payload }) => {
            if (active && payload && payload.length) {
              return (
                <div className="rounded-lg border bg-white p-2 shadow-md">
                  <div className="flex flex-col">
                    <span className="text-[0.70rem] uppercase text-gray-500">{payload[0].name}</span>
                    <span className="font-bold text-gray-900">${payload[0].value}</span>
                  </div>
                </div>
              )
            }
            return null
          }}
        />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  )
}

