"use client"

export function ModelAccuracy() {
  const accuracy =  45.8 // DBSCAN accuracy percentage

  return (
    <div className="flex flex-col items-center justify-center h-[300px] space-y-4">
      <div className="text-center">
        <div className="text-6xl font-bold text-purple-600 mb-2">{accuracy}%</div>
        <div className="text-lg font-semibold text-gray-700 mb-1">DBSCAN Model</div>
        <div className="text-sm text-gray-500">Clustering Accuracy</div>
      </div>

      {/* Optional: Add a progress ring or bar */}
      <div className="w-full max-w-xs">
        <div className="bg-gray-200 rounded-full h-2">
          <div
            className="bg-purple-600 h-2 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${accuracy}%` }}
          ></div>
        </div>
      </div>
    </div>
  )
}
