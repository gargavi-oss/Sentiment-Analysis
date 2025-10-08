import React from "react";

export default function HistoryPanel({ history, clearHistory }) {
  return (
    <div className="h-full flex flex-col bg-white/80 backdrop-blur-md border border-gray-200 rounded-3xl shadow-lg p-4 overflow-hidden">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-gray-700">History</h2>
        <button
          onClick={clearHistory}
          className="px-3 py-1 bg-red-400 hover:bg-red-500 text-white rounded-lg text-sm transition-all"
        >
          Clear All
        </button>
      </div>

      {/* Content */}
      {history.length === 0 ? (
        <p className="text-gray-500 text-center mt-10">No history yet.</p>
      ) : (
        <div className="flex-1 overflow-y-auto space-y-3 pr-2">
          {history.map((item, idx) => (
            <div
              key={idx}
              className="bg-gray-100/50 p-3 rounded-xl border border-gray-300 flex flex-col gap-2 shadow-sm"
            >
              <div className="flex justify-between items-center">
                <span className="font-semibold text-gray-800 capitalize">
                  {item.type === "batch" ? "Batch Analysis" : "Single Input"}
                </span>
                <span className="text-xs text-gray-500">
                  {new Date(item.timestamp).toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </span>
              </div>

              {/* Show batch or single results */}
              {item.type === "batch" ? (
                <div className="space-y-1 mt-1">
                  {item.result.map((r, i) => (
                    <div
                      key={i}
                      className="flex justify-between items-center text-sm border-b border-gray-200 last:border-none pb-1"
                    >
                      <span className="text-gray-700 truncate w-[70%]">
                        {r.text.length > 40 ? r.text.slice(0, 40) + "..." : r.text}
                      </span>
                      <span
                        className={`${
                          r.label === "positive"
                            ? "text-green-500"
                            : r.label === "negative"
                            ? "text-red-500"
                            : "text-yellow-500"
                        }`}
                      >
                        {r.emoji}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="flex justify-between items-center">
                  <span
                    className={`text-lg ${
                      item.result.label === "positive"
                        ? "text-green-500"
                        : item.result.label === "negative"
                        ? "text-red-500"
                        : "text-yellow-500"
                    }`}
                  >
                    {item.result.emoji}
                  </span>
                  <span className="text-sm text-gray-600">
                    Confidence: {(item.result.score * 100).toFixed(1)}%
                  </span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
