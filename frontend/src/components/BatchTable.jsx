import React from "react";
import { FaTrashAlt } from "react-icons/fa";
import SentimentChart from "./SentimentChart";
import { LABEL_COLORS } from "./constants";

export default function BatchTable({ data, onClear }) {
  const chartCounts = data.reduce(
    (acc, r) => {
      if (r.label === "positive") acc.positive++;
      else if (r.label === "negative") acc.negative++;
      else acc.neutral++;
      return acc;
    },
    { positive: 0, negative: 0, neutral: 0 }
  );

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
                  className="py-2 px-2 font-semibold"
                  style={{ color: LABEL_COLORS[item.label] }}
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
        <SentimentChart
          result={{
            label: "batch",
            counts: chartCounts,
          }}
        />
      </div>
    </div>
  );
}
