'use client';

import React, { useState } from 'react';
import { Download } from 'lucide-react';
import { exportData } from '@/lib/api';

interface DataTableProps {
  data: any[];
  title: string;
}

export default function DataTable({ data, title }: DataTableProps) {
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const itemsPerPage = 10;

  const totalPages = Math.ceil(data.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentData = data.slice(startIndex, endIndex);

  const handleExport = async (format: 'json' | 'csv') => {
    setLoading(true);
    try {
      const response = await exportData({ results: data }, format);
      if (response.success) {
        // Create download link
        const blob = new Blob([response.data], {
          type: format === 'json' ? 'application/json' : 'text/csv',
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `reddit_analysis_${Date.now()}.${format}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Export failed:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">{title}</h3>
        <p className="text-gray-500 text-center py-8">No data available</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-gray-900">{title}</h3>
        <div className="flex gap-2">
          <button
            onClick={() => handleExport('csv')}
            disabled={loading}
            className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors disabled:opacity-50 flex items-center gap-2 text-sm"
          >
            <Download size={16} />
            CSV
          </button>
          <button
            onClick={() => handleExport('json')}
            disabled={loading}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 flex items-center gap-2 text-sm"
          >
            <Download size={16} />
            JSON
          </button>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b-2 border-gray-200">
              <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Type</th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Content</th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Author</th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Score</th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Sentiment</th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Subreddit</th>
            </tr>
          </thead>
          <tbody>
            {currentData.map((item, index) => (
              <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4 text-sm">
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      item.type === 'post'
                        ? 'bg-blue-100 text-blue-700'
                        : 'bg-gray-100 text-gray-700'
                    }`}
                  >
                    {item.type}
                  </span>
                </td>
                <td className="py-3 px-4 text-sm text-gray-900 max-w-md truncate">
                  {item.title || item.text || 'N/A'}
                </td>
                <td className="py-3 px-4 text-sm text-gray-700">{item.author || 'N/A'}</td>
                <td className="py-3 px-4 text-sm font-semibold text-gray-900">
                  {item.score || 0}
                </td>
                <td className="py-3 px-4 text-sm">
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      item.sentiment === 'positive'
                        ? 'bg-green-100 text-green-700'
                        : item.sentiment === 'negative'
                        ? 'bg-red-100 text-red-700'
                        : 'bg-gray-100 text-gray-700'
                    }`}
                  >
                    {item.sentiment || 'neutral'}
                  </span>
                </td>
                <td className="py-3 px-4 text-sm text-gray-700">{item.subreddit || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between mt-4">
          <p className="text-sm text-gray-600">
            Showing {startIndex + 1} to {Math.min(endIndex, data.length)} of {data.length} results
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
              disabled={currentPage === 1}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed text-sm text-gray-900 font-medium"
            >
              Previous
            </button>
            <span className="px-4 py-2 text-sm text-gray-700 font-medium">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
              disabled={currentPage === totalPages}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed text-sm text-gray-900 font-medium"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}


