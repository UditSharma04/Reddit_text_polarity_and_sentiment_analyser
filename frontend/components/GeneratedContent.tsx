'use client';

import React, { useState, useEffect } from 'react';
import { Sparkles, Copy, Check, Loader2 } from 'lucide-react';
import { generateContent, ContentGenerationRequest } from '@/lib/api';

interface GeneratedContentProps {
  query: string;
  keywords: [number, string][];
  sentimentData: {
    positive: number;
    negative: number;
    neutral: number;
  };
  entities?: { [key: string]: string[] };
}

export default function GeneratedContent({
  query,
  keywords,
  sentimentData,
  entities,
}: GeneratedContentProps) {
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    generateInitialContent();
  }, [query]);

  const generateInitialContent = async () => {
    setLoading(true);
    setError('');
    try {
      const request: ContentGenerationRequest = {
        query,
        keywords: keywords.slice(0, 10),
        sentiment_data: sentimentData,
        entities,
      };

      const response = await generateContent(request);
      if (response.success) {
        setContent(response.content);
      } else {
        setError(response.error || 'Failed to generate content');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to generate content');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-gradient-to-br from-indigo-50 to-gray-50 rounded-2xl shadow-sm border border-gray-100 p-8">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
          <Sparkles className="text-indigo-600" size={24} />
          AI-Generated Summary
        </h3>
        {content && (
          <button
            onClick={handleCopy}
            className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2"
          >
            {copied ? (
              <>
                <Check className="text-green-500" size={16} />
                <span className="text-sm text-green-600 font-medium">Copied!</span>
              </>
            ) : (
              <>
                <Copy className="text-gray-700" size={16} />
                <span className="text-sm text-gray-900 font-medium">Copy</span>
              </>
            )}
          </button>
        )}
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <Loader2 className="animate-spin mx-auto mb-4 text-indigo-600" size={48} />
            <p className="text-gray-600">Generating AI content...</p>
          </div>
        </div>
      ) : error ? (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4">
          <p className="text-red-700">{error}</p>
          <button
            onClick={generateInitialContent}
            className="mt-2 px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors text-sm"
          >
            Try Again
          </button>
        </div>
      ) : content ? (
        <div className="bg-white rounded-xl p-6">
          <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{content}</p>
        </div>
      ) : (
        <div className="bg-white rounded-xl p-6">
          <p className="text-gray-400 text-center">No content generated yet</p>
        </div>
      )}
    </div>
  );
}

