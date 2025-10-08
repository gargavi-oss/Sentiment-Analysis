import React from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

export default function SentimentChart({ result }) {
  // For batch results — use counts
  if (result.label === "batch" && result.counts) {
    const data = [
      { name: "Positive", value: result.counts.positive },
      { name: "Negative", value: result.counts.negative },
      { name: "Neutral", value: result.counts.neutral },
    ];

    const COLORS = ["#22c55e", "#ef4444", "#eab308"];

    return (
      <div className="w-full h-72 sm:h-80 bg-white/70 rounded-2xl p-4 shadow-sm flex flex-col items-center">
        <h3 className="text-lg font-semibold text-gray-700 mb-3">
          Sentiment Distribution
        </h3>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              outerRadius="80%"
              innerRadius="50%"
              label
            >
              {data.map((_, index) => (
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend verticalAlign="bottom" height={36} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    );
  }

  // For single input — use score visualization
  const confidence = (result.score * 100).toFixed(1);
  const color =
    result.label === "positive"
      ? "#22c55e"
      : result.label === "negative"
      ? "#ef4444"
      : "#eab308";

  const data = [
    { name: "Confidence", value: result.score },
    { name: "Remaining", value: 1 - result.score },
  ];

  return (
    <div className="w-full h-72 sm:h-80 bg-white/70 rounded-2xl p-4 shadow-sm flex flex-col items-center justify-center">
      <h3 className="text-lg font-semibold text-gray-700 mb-3 text-center">
        Sentiment Confidence ({confidence}%)
      </h3>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            outerRadius="80%"
            innerRadius="60%"
            startAngle={90}
            endAngle={-270}
          >
            <Cell key="confidence" fill={color} />
            <Cell key="remaining" fill="#e5e7eb" />
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
      <div
        className={`text-xl font-semibold mt-2 ${
          result.label === "positive"
            ? "text-green-500"
            : result.label === "negative"
            ? "text-red-500"
            : "text-yellow-500"
        }`}
      >
        {result.emoji} {result.label.toUpperCase()}
      </div>
    </div>
  );
}
