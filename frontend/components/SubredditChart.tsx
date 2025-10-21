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

interface SubredditChartProps {
  subredditData: Array<{
    subreddit: string;
    post_count: number;
    avg_score: number;
    positive_pct: number;
  }>;
}

export default function SubredditChart({ subredditData }: SubredditChartProps) {
  if (!subredditData || subredditData.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Subreddit Analysis</h3>
        <p className="text-gray-500 text-center py-8">No subreddit data available</p>
      </div>
    );
  }

  const data = {
    labels: subredditData.map((item) => item.subreddit),
    datasets: [
      {
        label: 'Post Count',
        data: subredditData.map((item) => item.post_count),
        backgroundColor: subredditData.map((item) => {
          // Color based on positive sentiment percentage
          const pct = item.positive_pct;
          if (pct >= 60) return 'rgba(34, 197, 94, 0.8)'; // Green
          if (pct >= 40) return 'rgba(234, 179, 8, 0.8)'; // Yellow
          return 'rgba(239, 68, 68, 0.8)'; // Red
        }),
        borderColor: subredditData.map((item) => {
          const pct = item.positive_pct;
          if (pct >= 60) return 'rgba(34, 197, 94, 1)';
          if (pct >= 40) return 'rgba(234, 179, 8, 1)';
          return 'rgba(239, 68, 68, 1)';
        }),
        borderWidth: 1,
      },
    ],
  };

  const options: ChartOptions<'bar'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
      tooltip: {
        callbacks: {
          afterLabel: function (context) {
            const item = subredditData[context.dataIndex];
            return [
              `Avg Score: ${item.avg_score.toFixed(1)}`,
              `Positive: ${item.positive_pct.toFixed(1)}%`,
            ];
          },
        },
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
      },
    },
  };

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
      <h3 className="text-xl font-semibold text-gray-800 mb-2">
        Top Subreddits by Activity
      </h3>
      <p className="text-sm text-gray-500 mb-6">
        Color indicates sentiment distribution across communities
      </p>
      <div className="h-80">
        <Bar data={data} options={options} />
      </div>
    </div>
  );
}

