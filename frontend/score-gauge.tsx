"use client"

export function ScoreGauge({ score }: { score: number }) {
  const rotation = (score / 100) * 180

  return (
    <div className="relative mx-auto w-48 h-24 overflow-hidden">
      <div className="absolute w-48 h-48 rounded-full border-[16px] border-[#2a2d3d]" />
      <div
        className="absolute w-48 h-48 rounded-full border-[16px] border-t-transparent border-r-transparent transition-all duration-1000 ease-out"
        style={{
          transform: `rotate(${rotation}deg)`,
          borderColor: score >= 80 ? "#22c55e" : score >= 60 ? "#eab308" : "#ef4444",
        }}
      />
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-4xl font-bold text-gray-700">{score}</span>
      </div>
    </div>
  )
}

