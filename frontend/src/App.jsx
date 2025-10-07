import React, { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/analyze", { text });
      setResult(res.data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4">
      <motion.div
        className="bg-gray-800/40 backdrop-blur-lg p-8 rounded-2xl shadow-2xl w-full max-w-xl border border-gray-700"
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="text-3xl font-bold mb-6 text-center">
          🧠 Sentiment Analysis App
        </h1>

        <textarea
          rows="5"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type your sentence here..."
          className="w-full p-4 bg-gray-900/70 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-blue-500 outline-none resize-none"
        />

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className={`mt-5 w-full py-3 rounded-lg text-lg font-medium transition-all ${
            loading
              ? "bg-gray-600 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading ? "Analyzing..." : "Analyze Sentiment"}
        </button>

        {result && (
          <motion.div
            className="mt-8 text-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <h3
              className={`text-2xl font-semibold ${
                result.label === "positive" ? "text-green-400" : "text-red-400"
              }`}
            >
              {result.label === "positive" ? "😊 Positive" : "😞 Negative"}
            </h3>
            <p className="text-gray-300 mt-2">
              Confidence: <span className="font-bold">{result.score}</span>
            </p>
          </motion.div>
        )}
      </motion.div>

    
    </div>
  );
}

export default App;
