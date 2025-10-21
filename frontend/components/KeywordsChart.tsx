'use client';

import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface KeywordsChartProps {
  keywords: [number, string][];
}

export default function KeywordsChart({ keywords }: KeywordsChartProps) {
  // Take top 15 keywords
  const topKeywords = keywords.slice(0, 15);
  
  const data = {
    labels: topKeywords.map(([_, keyword]) => keyword),
    datasets: [
      {
        label: 'Frequency',
        data: topKeywords.map(([count, _]) => count),
        backgroundColor: 'rgba(99, 102, 241, 0.8)',
        borderColor: 'rgba(99, 102, 241, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options: ChartOptions<'bar'> = {
    indexAxis: 'y' as const,
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
      },
      y: {
        grid: {
          display: false,
        },
      },
    },
  };

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
      <h3 className="text-xl font-semibold text-gray-800 mb-6">Top Keywords</h3>
      <div className="h-96">
        <Bar data={data} options={options} />
      </div>
    </div>
  );
}


