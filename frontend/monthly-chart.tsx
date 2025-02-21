"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

interface ChartData {
  month: string;
  credit: number;
  debit: number;
  currency: string;
}

interface MonthlyChartProps {
  chartData: ChartData[];
}

export function MonthlyChart({ chartData }: MonthlyChartProps) {
  const currency = chartData?.[0]?.currency || '$';
  // console.log(chartData);
  return (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={chartData}>
        <XAxis dataKey="month" stroke="#4b5563" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis
          stroke="#4b5563"
          fontSize={12}
          tickLine={false}
          axisLine={false}
          tickFormatter={(value) => `${currency} ${value}`}
        />
        <Tooltip
          content={({ active, payload }) => {
            if (active && payload && payload.length) {
              return (
                <div className="rounded-lg border bg-white p-2 shadow-md">
                  <div className="grid grid-cols-2 gap-2">
                    <div className="flex flex-col">
                      <span className="text-[0.70rem] uppercase text-gray-500">Credit</span>
                      <span className="font-bold text-green-600">{currency} {Number(payload?.[0]?.value)?.toFixed(2) ?? "0.00"}</span>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-[0.70rem] uppercase text-gray-500">Debit</span>
                      <span className="font-bold text-red-600">{currency} {Number(payload?.[1]?.value)?.toFixed(2) ?? "0.00"}</span>
                    </div>
                  </div>
                </div>
              )
            }
            return null
          }}
        />
        <Bar dataKey="credit" fill="#22c55e" radius={[4, 4, 0, 0]} />
        <Bar dataKey="debit" fill="#ef4444" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}