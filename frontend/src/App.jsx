import React, { useState } from "react";
import ModeToggle from "./components/ModeToggle";
import SingleInput from "./components/SingleInput";
import BatchInput from "./components/BatchInput";
import HistoryPanel from "./components/HistoryPanel";

export default function App() {
  const [mode, setMode] = useState("single");
  const [history, setHistory] = useState([]);

  const [singleResult, setSingleResult] = useState(null);
  const [batchResults, setBatchResults] = useState([]);

  const addHistory = (item) => setHistory((prev) => [item, ...prev]);
  const clearHistory = () => setHistory([]);

  const clearAll = () => {
    clearHistory();
    setSingleResult(null);
    setBatchResults([]);
  };

  return (
    <div className="min-h-screen w-full relative overflow-hidden bg-gradient-to-b from-indigo-50 via-white to-gray-50">
      {/* Animated background */}
      <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-indigo-100 via-white to-gray-50 animate-gradientBackground -z-10" />

      <div className="relative flex flex-col lg:flex-row justify-center items-start p-4 md:p-6 gap-6 max-w-6xl mx-auto w-full">
        {/* Input Panel */}
        <div className="flex-1 bg-white/90 backdrop-blur-md border border-gray-200 rounded-3xl shadow-lg p-4 md:p-6 flex flex-col gap-6 transition-all hover:scale-[1.01] hover:shadow-xl">
          <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-extrabold text-gray-800 text-center md:text-left mb-4 drop-shadow-sm">
            🧠 Sentiment Analyzer
          </h1>

          <ModeToggle mode={mode} setMode={setMode} />


          <div className="mt-4 w-full">
            {mode === "single" ? (
              <SingleInput
                addHistory={addHistory}
                result={singleResult}
                setResult={setSingleResult}
              />
            ) : (
              <BatchInput
                addHistory={addHistory}
                results={batchResults}
                setResults={setBatchResults}
              />
            )}
          </div>
        </div>

        {/* History Panel */}
        <div className="w-full lg:w-1/3 flex flex-col h-auto lg:h-[calc(100vh-4rem)]">
          <HistoryPanel history={history} clearHistory={clearHistory} />
        </div>
      </div>
    </div>
  );
}
