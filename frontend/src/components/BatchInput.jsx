import React, { useState } from "react";
import axios from "axios";
import SentimentChart from "./SentimentChart";
import { LABEL_COLORS, LABEL_EMOJIS } from "./constants";

export default function BatchInput({ addHistory, results, setResults }) {
  const [batchText, setBatchText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleBatchAnalyze = async () => {
    const texts = batchText.split("\n").filter((t) => t.trim());
    if (!texts.length) return;
    setLoading(true);

    try {
      const res = await axios.post("https://h7fqj3ch-8000.inc1.devtunnels.ms/batch_analyze", { texts });
      const batchResults = res.data.results || [];
      const cleanResults = batchResults.map((r) => ({
        text: r.text || "",
        label: r.label || "neutral",
        score: r.score || 0,
        emoji: LABEL_EMOJIS[r.label] || "😐",
      }));

      setResults(cleanResults);
      addHistory({ type: "batch", result: cleanResults, timestamp: new Date() });
    } catch (err) {
      console.error("Batch analyze error:", err);
    }
    setLoading(false);
  };

  const summary = results.reduce(
    (acc, r) => {
      if (r.label === "positive") acc.positive++;
      else if (r.label === "negative") acc.negative++;
      else acc.neutral++;
      return acc;
    },
    { positive: 0, negative: 0, neutral: 0 }
  );

  return (
    <div className="w-full flex flex-col gap-4">
      <textarea
        rows="6"
        value={batchText}
        onChange={(e) => setBatchText(e.target.value)}
        placeholder="Enter one text per line..."
        className="w-full p-4 bg-white/80 border border-gray-200 rounded-xl text-gray-800 focus:ring-2 focus:ring-blue-300 outline-none resize-none shadow-sm"
      />

      <button
        onClick={handleBatchAnalyze}
        disabled={loading}
        className={`py-3 rounded-xl text-lg font-medium transition-all ${
          loading
            ? "bg-gray-300 text-gray-500 cursor-not-allowed"
            : "bg-blue-400 hover:bg-blue-500 text-white shadow-sm hover:shadow-md"
        }`}
      >
        {loading ? "Analyzing..." : "Analyze Batch"}
      </button>

      {results.length > 0 && (
        <div className="mt-6 flex flex-col lg:flex-row gap-6 items-stretch">
          <div className="flex-1 bg-white border border-gray-200 rounded-2xl p-6 shadow-md flex flex-col justify-center items-center">
            <h3 className="font-semibold text-gray-700 mb-3 text-center">
              Batch Sentiment Summary
            </h3>
            <SentimentChart result={{ label: "batch", counts: summary }} />
          </div>

          <div className="flex-1 bg-white border border-gray-200 rounded-2xl p-6 shadow-md overflow-y-auto max-h-[400px]">
            <h3 className="font-semibold text-gray-700 mb-3 text-center">Analyzed Texts</h3>
            <div className="space-y-3">
              {results.map((r, i) => (
                <div
                  key={i}
                  className="bg-gray-100/50 p-3 rounded-xl border border-gray-300 flex justify-between items-center shadow-sm"
                >
                  <div className="w-[75%]">
                    <p className="font-medium text-gray-800 truncate">{r.text}</p>
                    <p className={`text-sm text-${LABEL_COLORS[r.label]}`}>
                      {r.label.toUpperCase()} ({(r.score * 100).toFixed(1)}%)
                    </p>
                  </div>
                  <span className={`text-xl text-${LABEL_COLORS[r.label]}`}>
                    {r.emoji}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
