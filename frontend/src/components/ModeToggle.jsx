import React from "react";
import { FaListUl, FaPen } from "react-icons/fa";

export default function ModeToggle({ mode, setMode }) {
  return (
    <div className="flex justify-center mb-5 gap-3">
      <button
        className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
          mode === "single" ? "bg-blue-600 text-white" : "bg-gray-200 hover:bg-gray-300"
        }`}
        onClick={() => setMode("single")}
      >
        <FaPen /> Single
      </button>
      <button
        className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
          mode === "batch" ? "bg-blue-600 text-white" : "bg-gray-200 hover:bg-gray-300"
        }`}
        onClick={() => setMode("batch")}
      >
        <FaListUl /> Batch
      </button>
    </div>
  );
}
