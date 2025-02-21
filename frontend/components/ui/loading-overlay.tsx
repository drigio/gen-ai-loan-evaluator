export function LoadingOverlay() {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-white/80 backdrop-blur-sm">
        <div className="space-y-4 text-center">
          <div className="relative mx-auto h-32 w-32">
            <div className="absolute inset-0 animate-pulse rounded-full bg-blue-100" />
            <div className="absolute inset-4 animate-spin rounded-full border-b-2 border-blue-600" />
            <div className="absolute inset-8 animate-pulse rounded-full bg-blue-50" />
          </div>
          <div className="space-y-2">
            <h2 className="text-xl font-semibold">Analyzing your statement</h2>
            <p className="text-sm text-gray-500">This will only take a moment...</p>
          </div>
        </div>
      </div>
    )
  }
  
  