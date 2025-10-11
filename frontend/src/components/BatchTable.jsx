import React from "react";
import { FaTrashAlt } from "react-icons/fa";
import SentimentChart from "./SentimentChart";

export default function BatchTable({ data, onClear }) {
  // Prepare data for chart
  const chartData = [
    { name: "Positive", value: data.filter(d => d.label === "positive").length },
    { name: "Negative", value: data.filter(d => d.label === "negative").length },
    { name: "Neutral", value: data.filter(d => d.label === "neutral").length },
  ];

  return (
    <div>
      <div className="flex justify-between items-center mb-3">
        <h2 className="text-xl font-semibold">Batch Results ({data.length})</h2>
        <button onClick={onClear} className="text-red-400 hover:text-red-500">
          <FaTrashAlt />
        </button>
      </div>

      <div className="overflow-x-auto mb-6">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="text-gray-400 border-b border-gray-700">
              <th className="py-2 px-2">#</th>
              <th className="py-2 px-2">Text</th>
              <th className="py-2 px-2">Label</th>
              <th className="py-2 px-2">Accuracy</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr
                key={index}
                className="border-b border-gray-800 hover:bg-gray-800/40 transition-all"
              >
                <td className="py-2 px-2">{index + 1}</td>
                <td className="py-2 px-2 truncate max-w-xs">{item.text}</td>
                <td
                  className={`py-2 px-2 font-semibold ${
                    item.label === "positive"
                      ? "text-green-400"
                      : item.label === "negative"
                      ? "text-red-400"
                      : "text-yellow-400"
                  }`}
                >
                  {item.label.toUpperCase()}
                </td>
                <td className="py-2 px-2">{(item.score * 100).toFixed(1)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4">
        <SentimentChart probabilities={chartData.reduce((acc, d) => {
          acc[d.name.toLowerCase()] = d.value / data.length;
          return acc;
        }, {})} />
      </div>
    </div>
  );
}
