import React, { useState } from "react";
import axios from "axios";
import ResultCard from "./ResultCard";
import SentimentChart from "./SentimentChart";

export default function SingleInput({ addHistory, result, setResult }) {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post("https://lin-unsuperseded-siena.ngrok-free.dev/analyze", { text });
      const resultData = res.data || { text, label: "N/A", score: 0, emoji: "😐" };
      setResult(resultData);
      addHistory({ type: "single", result: resultData, timestamp: new Date() });
    } catch (err) {
      console.error(err);
      addHistory({
        type: "single",
        result: { text, label: "Error", score: 0, emoji: "😐" },
        timestamp: new Date(),
      });
    }
    setLoading(false);
  };

  return (
    <div className="w-full flex flex-col gap-4">
      {/* Textarea */}
      <textarea
        rows="4"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type your text..."
        className="w-full p-4 bg-white/80 border border-gray-200 rounded-xl text-gray-800 focus:ring-2 focus:ring-blue-300 outline-none resize-none shadow-sm"
      />

      {/* Button */}
      <button
        onClick={handleAnalyze}
        disabled={loading}
        className={`py-3 rounded-xl text-lg font-medium transition-all ${
          loading
            ? "bg-gray-300 text-gray-500 cursor-not-allowed"
            : "bg-blue-400 hover:bg-blue-500 text-white shadow-sm hover:shadow-md"
        }`}
      >
        {loading ? "Analyzing..." : "Analyze Sentiment"}
      </button>

      {/* Result Display */}
      {result && result.label && (
        <div className="mt-6 flex flex-col lg:flex-row gap-6 items-stretch">
          {/* Result Card */}
          <div className="flex-1 bg-white border border-gray-200 rounded-2xl p-6 shadow-md">
            <ResultCard result={result} />
          </div>

          {/* Chart */}
          <div className="flex-1 bg-white border border-gray-200 rounded-2xl p-6 shadow-md flex justify-center items-center">
            <SentimentChart key={result.label + result.score} result={result} />
          </div>
        </div>
      )}
    </div>
  );
}
