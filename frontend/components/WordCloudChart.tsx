'use client';

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Loader2 } from 'lucide-react';

interface WordCloudChartProps {
  results: any[];
}

export default function WordCloudChart({ results }: WordCloudChartProps) {
  const [imageUrl, setImageUrl] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    generateWordCloud();
  }, [results]);

  const generateWordCloud = async () => {
    setLoading(true);
    setError('');
    
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await axios.post(`${API_URL}/api/generate-wordcloud`, results);
      
      if (response.data.success && response.data.image) {
        setImageUrl(response.data.image);
      } else {
        setError(response.data.error || 'Failed to generate word cloud');
      }
    } catch (err: any) {
      console.error('Word cloud error:', err);
      setError('Failed to generate word cloud');
    } finally {
      setLoading(false);
    }
  };

  if (!results || results.length === 0) {
    return (
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">Word Cloud</h3>
        <p className="text-gray-400 text-center py-12">No data available</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
      <h3 className="text-xl font-semibold text-gray-800 mb-6">Most Frequent Words</h3>
      
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="text-center">
            <Loader2 className="animate-spin mx-auto mb-4 text-indigo-600" size={48} />
            <p className="text-gray-600">Generating word cloud...</p>
          </div>
        </div>
      ) : error ? (
        <div className="bg-red-50 border border-red-200 rounded-xl p-6">
          <p className="text-red-700">{error}</p>
          <button
            onClick={generateWordCloud}
            className="mt-3 px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors text-sm"
          >
            Try Again
          </button>
        </div>
      ) : imageUrl ? (
        <div className="flex justify-center">
          <img 
            src={imageUrl} 
            alt="Word Cloud" 
            className="w-full max-w-4xl rounded-lg"
          />
        </div>
      ) : (
        <p className="text-gray-400 text-center py-12">No word cloud generated</p>
      )}
    </div>
  );
}
