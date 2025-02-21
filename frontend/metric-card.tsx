export function MetricCard({ metric, value }: { metric: string; value: number }) {
 
    return (
      <div className="">
        <div className="flex items-center gap-2 text-md p-2 bg-main-light border-2 ">
            <span className="text-gray-900 font-bold">{metric}</span>
            <span className="text-gray-300 text-lg"> | </span>
            <span className="text-gray-500">{value}</span>
        </div>
      </div>
    )
  }