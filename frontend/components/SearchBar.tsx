'use client';

import React, { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string, limit: number, analysisType: string) => void;
  loading?: boolean;
}

export default function SearchBar({ onSearch, loading = false }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [limit, setLimit] = useState(50);
  const [analysisType, setAnalysisType] = useState('basic');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !loading) {
      onSearch(query, limit, analysisType);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Main search input */}
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="What topic do you want to analyze? (e.g., AI in education, climate change)"
            className="w-full px-6 py-4 pr-12 text-lg text-gray-900 bg-white border border-gray-300 rounded-xl focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-all placeholder:text-gray-400"
            disabled={loading}
          />
          <Search className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400" size={24} />
        </div>

          {/* Options */}
        <div className="flex flex-wrap gap-4 items-center justify-between">
          {/* Limit slider */}
          <div className="flex items-center gap-3">
            <label className="text-sm font-medium text-gray-700">Results:</label>
            <input
              type="range"
              min="10"
              max="200"
              step="10"
              value={limit}
              onChange={(e) => setLimit(parseInt(e.target.value))}
              className="w-32 accent-indigo-600"
              disabled={loading}
            />
            <span className="text-sm font-semibold text-gray-900 w-8">{limit}</span>
          </div>

          {/* Analysis type */}
          <div className="flex items-center gap-3">
            <label className="text-sm font-medium text-gray-700">Analysis Type:</label>
            <select
              value={analysisType}
              onChange={(e) => setAnalysisType(e.target.value)}
              className="px-4 py-2 text-gray-900 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-500"
              disabled={loading}
            >
              <option value="basic" className="text-gray-900">Basic</option>
              <option value="advanced" className="text-gray-900">Advanced</option>
              <option value="trend" className="text-gray-900">Trend Analysis</option>
              <option value="all" className="text-gray-900">All Features</option>
            </select>
          </div>

          {/* Submit button */}
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="px-8 py-3 bg-indigo-600 text-white font-semibold rounded-xl hover:bg-indigo-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shadow-sm"
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin" size={20} />
                Analyzing...
              </>
            ) : (
              <>
                <Search size={20} />
                Analyze
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}


