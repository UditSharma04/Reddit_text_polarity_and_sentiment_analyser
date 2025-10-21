'use client';

import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ChartOptions,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface TemporalGraphProps {
  temporalData: {
    daily_activity?: { [key: string]: number };
    hourly_activity?: { [key: string]: number };
  };
}

export default function TemporalGraph({ temporalData }: TemporalGraphProps) {
  if (!temporalData || (!temporalData.daily_activity && !temporalData.hourly_activity)) {
    return (
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">Temporal Activity</h3>
        <p className="text-gray-400 text-center py-12">No temporal data available</p>
      </div>
    );
  }

  // Hourly activity chart
  const hourlyData = temporalData.hourly_activity || {};
  const hours = Object.keys(hourlyData).sort((a, b) => parseInt(a) - parseInt(b));
  const hourlyCounts = hours.map(h => hourlyData[h]);

  const hourlyChartData = {
    labels: hours.map(h => `${h}:00`),
    datasets: [
      {
        label: 'Posts/Comments',
        data: hourlyCounts,
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: '#6366f1',
      },
    ],
  };

  // Daily activity chart
  const dailyData = temporalData.daily_activity || {};
  const dates = Object.keys(dailyData).sort();
  const dailyCounts = dates.map(d => dailyData[d]);

  const dailyChartData = {
    labels: dates,
    datasets: [
      {
        label: 'Posts/Comments',
        data: dailyCounts,
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: '#6366f1',
      },
    ],
  };

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 12,
        borderColor: '#6366f1',
        borderWidth: 1,
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
        ticks: {
          color: '#6b7280',
        },
      },
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
        ticks: {
          color: '#6b7280',
        },
      },
    },
  };

  return (
    <div className="space-y-6">
      {/* Hourly Activity */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-6">
          Activity by Hour (UTC)
        </h3>
        <div className="h-64">
          <Line data={hourlyChartData} options={options} />
        </div>
      </div>

      {/* Daily Activity */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-6">
          Activity Over Time
        </h3>
        <div className="h-64">
          <Line data={dailyChartData} options={options} />
        </div>
      </div>
    </div>
  );
}

