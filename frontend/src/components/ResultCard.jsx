import React from "react";
import { LABEL_COLORS, LABEL_EMOJIS } from "./constants";

export default function ResultCard({ result }) {
  if (!result) return null;

  return (
    <div className="bg-white/80 p-4 rounded-xl border border-gray-200 shadow-md w-full transition hover:shadow-lg">
      <p className="text-gray-700 mb-2">
        <span className="font-semibold text-gray-800">Text:</span> {result.text}
      </p>
      <p
        className={`text-xl font-semibold text-${LABEL_COLORS[result.label]}`}
      >
        {LABEL_EMOJIS[result.label]} {result.label?.toUpperCase() || "N/A"}
      </p>
      <p className="text-gray-600 mt-1">
        Accuracy: <span className="font-bold">{(result.score * 100).toFixed(1)}%</span>
      </p>
    </div>
  );
}
