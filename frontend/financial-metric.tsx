export function FinancialMetric({ label, score }: { label: string; score: number | undefined }) {
  const percentage = score ? score * 100 : 0;
  const color = percentage >= 80 ? "bg-green-500" : percentage >= 60 ? "bg-yellow-500" : "bg-red-500"

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-sm">
        <span className="text-gray-700">{label}</span>
        <span
          className={`font-medium ${
            percentage >= 80 ? "text-green-600" : percentage >= 60 ? "text-yellow-600" : "text-red-600"
          }`}
        >
          {percentage.toFixed(0)}%
        </span>
      </div>
      <div className="h-2 rounded-full bg-gray-200">
        <div
          className={`h-full rounded-full transition-all duration-500 ${color}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}

