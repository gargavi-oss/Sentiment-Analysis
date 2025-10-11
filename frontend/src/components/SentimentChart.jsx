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

  // ---------------- Batch sentiment ----------------
  if (result.label === "batch" && result.counts) {
    const data = [
      { name: "Positive", value: result.counts.positive },
      { name: "Negative", value: result.counts.negative },
      { name: "Neutral", value: result.counts.neutral },
    ];

    return (
      <div className="w-full h-72 sm:h-80 bg-white/70 rounded-2xl p-4 shadow-sm flex flex-col items-center">
        <h3 className="text-lg font-semibold text-gray-700 mb-3 text-center">
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
              {data.map((entry, index) => (
                <Cell
                  key={index}
                  fill={COLORS[entry.name.toLowerCase()] || "#6b7280"}
                />
              ))}
            </Pie>
            <Tooltip />
            <Legend verticalAlign="bottom" height={36} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    );
  }

  // ---------------- Single prediction ----------------
  const label = (result.label || "neutral").toLowerCase();
  const color = COLORS[label] || "#6b7280";
  const emoji = EMOJIS[label] || "😐";
  const accuracy = (result.score * 100).toFixed(1);

  const data = [
    { name: "Confidence", value: result.score },
    { name: "Remaining", value: 1 - result.score },
  ];

  return (
    <div className="w-full h-72 sm:h-80 bg-white/70 rounded-2xl p-4 shadow-sm flex flex-col items-center justify-center">
      <h3 className="text-lg font-semibold text-gray-700 mb-3 text-center">
        Sentiment Confidence ({accuracy}%)
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
      <div className="text-xl font-semibold mt-2" style={{ color }}>
        {emoji} {label.toUpperCase()}
      </div>
    </div>
  );
}
