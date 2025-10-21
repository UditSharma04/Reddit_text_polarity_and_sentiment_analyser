'use client';

import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  ChartOptions,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

interface SentimentChartProps {
  sentimentData: {
    positive: number;
    negative: number;
    neutral: number;
  };
}

export default function SentimentChart({ sentimentData }: SentimentChartProps) {
  const data = {
    labels: ['Positive', 'Negative', 'Neutral'],
    datasets: [
      {
        data: [sentimentData.positive, sentimentData.negative, sentimentData.neutral],
        backgroundColor: [
          'rgba(99, 102, 241, 0.8)',  // Indigo for positive
          'rgba(107, 114, 128, 0.6)',   // Gray for negative
          'rgba(229, 231, 235, 0.8)', // Light gray for neutral
        ],
        borderColor: [
          'rgba(99, 102, 241, 1)',
          'rgba(107, 114, 128, 1)',
          'rgba(209, 213, 219, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const options: ChartOptions<'doughnut'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
          font: {
            size: 12,
          },
        },
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            return `${context.label}: ${context.parsed.toFixed(1)}%`;
          },
        },
      },
    },
  };

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
      <h3 className="text-xl font-semibold text-gray-800 mb-6">Sentiment Distribution</h3>
      <div className="h-64">
        <Doughnut data={data} options={options} />
      </div>
    </div>
  );
}


