import React from "react";

export default function ResultCard({ result }) {
  // Hardcoded colors and emojis
  const COLORS = {
    positive: "#22c55e", // green
    negative: "#ef4444", // red
    neutral: "#eab308",  // yellow
  };

  const EMOJIS = {
    positive: "😊",
    negative: "😞",
    neutral: "😐",
  };

  const label = (result.label || "neutral").toLowerCase();
  const color = COLORS[label] || "#6b7280";
  const emoji = EMOJIS[label] || "😐";

  return (
    <div className="p-4 bg-gray-50 rounded-xl border border-gray-200 shadow-sm">
      <p className="text-gray-800 mb-2 font-medium">{result.text}</p>
      <div className="flex items-center justify-between">
        <span className="text-xl">{emoji}</span>
        <span className="font-semibold" style={{ color }}>
          {label.toUpperCase()} ({(result.score * 100).toFixed(1)}%)
        </span>
      </div>
    </div>
  );
}
