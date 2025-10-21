'use client';

import React, { useState } from 'react';
import { BarChart3, TrendingUp, MessageSquare, Users, ThumbsUp } from 'lucide-react';
import SearchBar from '@/components/SearchBar';
import MetricCard from '@/components/MetricsCard';
import SentimentChart from '@/components/SentimentChart';
import KeywordsChart from '@/components/KeywordsChart';
import SubredditChart from '@/components/SubredditChart';
import DataTable from '@/components/DataTable';
import RedditPostsView from '@/components/RedditPostsView';
import ChatInterface from '@/components/ChatInterface';
import GeneratedContent from '@/components/GeneratedContent';
import WordCloudChart from '@/components/WordCloudChart';
import TemporalGraph from '@/components/TemporalGraph';
import { analyzeReddit, AnalysisRequest } from '@/lib/api';

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [error, setError] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'overview' | 'visualizations' | 'communities' | 'data'>('overview');
  const [loadingMessage, setLoadingMessage] = useState('Starting analysis...');

  const handleSearch = async (query: string, limit: number, analysisType: string) => {
    setLoading(true);
    setError('');
    setAnalysisData(null);

    // Fun loading messages
    const messages = [
      'Connecting to Reddit... 🔌',
      'Fetching posts and comments... 📝',
      'Analyzing sentiment... 😊😐😢',
      'Extracting keywords... 🔑',
      'Crunching numbers... 🔢',
      'Almost there... ⏳',
      'This might take a moment... Grab some water! 💧'
    ];

    let messageIndex = 0;
    setLoadingMessage(messages[0]);

    // Change message every 2 seconds
    const messageInterval = setInterval(() => {
      messageIndex = (messageIndex + 1) % messages.length;
      setLoadingMessage(messages[messageIndex]);
    }, 2000);

    try {
      const request: AnalysisRequest = {
        query,
        limit,
        analysis_type: analysisType as any,
      };

      const response = await analyzeReddit(request);

      if (response.success && response.data) {
        setAnalysisData(response.data);
      } else {
        setError(response.error || 'Analysis failed');
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred during analysis');
    } finally {
      clearInterval(messageInterval);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="container mx-auto px-6 py-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-1">Reddit Analyzer</h1>
          <p className="text-gray-600">
            Advanced insights with AI-powered sentiment analysis and trend detection
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {/* Search Bar */}
        <div className="mb-8">
          <SearchBar onSearch={handleSearch} loading={loading} />
        </div>

        {/* Loading State */}
        {loading && (
          <div className="mb-8 min-h-[400px] flex items-center justify-center">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600 mb-6"></div>
              <h3 className="text-2xl font-semibold text-gray-900 mb-2">{loadingMessage}</h3>
              <p className="text-gray-600 max-w-md mx-auto">
                Analyzing Reddit data takes time. Feel free to stretch, grab a coffee ☕, or stay hydrated! 💧
              </p>
              <div className="mt-6 flex items-center justify-center gap-2">
                <div className="h-2 w-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="h-2 w-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="h-2 w-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}

        {/* Error Display */}
        {!loading && error && (
          <div className="mb-8 bg-red-50 border border-red-200 rounded-2xl p-6">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg
                  className="h-6 w-6 text-red-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-lg font-semibold text-red-900">Analysis Error</h3>
                <p className="mt-1 text-red-700">{error}</p>
                <p className="mt-2 text-sm text-red-600">
                  Make sure the backend server is running on port 8000
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {!loading && analysisData && (
          <div className="space-y-8">
            {/* Metrics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <MetricCard
              title="Total Posts/Comments"
              value={analysisData.metrics.total_posts}
              icon={<BarChart3 className="text-indigo-600" size={24} />}
            />
            <MetricCard
              title="Unique Subreddits"
              value={analysisData.metrics.unique_subreddits}
              icon={<Users className="text-indigo-600" size={24} />}
            />
            <MetricCard
              title="Positive Sentiment"
              value={`${analysisData.metrics.sentiment.positive.toFixed(1)}%`}
              icon={<ThumbsUp className="text-indigo-600" size={24} />}
              trend="up"
            />
            <MetricCard
              title="Average Score"
              value={analysisData.metrics.average_score}
              icon={<TrendingUp className="text-indigo-600" size={24} />}
            />
            </div>

            {/* Tabs */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
              <div className="border-b border-gray-100">
                <nav className="flex -mb-px">
                  {[
                    { id: 'overview', label: 'Overview', icon: BarChart3 },
                    { id: 'visualizations', label: 'Visualizations', icon: TrendingUp },
                    { id: 'communities', label: 'Communities', icon: Users },
                    { id: 'data', label: 'Data', icon: MessageSquare },
                  ].map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id as any)}
                      className={`flex-1 py-4 px-6 text-center font-medium text-sm transition-all ${
                        activeTab === tab.id
                          ? 'border-b-2 border-indigo-500 text-indigo-600 bg-indigo-50'
                          : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      {tab.label}
                    </button>
                  ))}
                </nav>
              </div>

              <div className="p-6">
                {/* Overview Tab */}
                {activeTab === 'overview' && (
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <SentimentChart sentimentData={analysisData.metrics.sentiment} />
                    {analysisData.analysis.top_keywords.length > 0 && (
                      <KeywordsChart keywords={analysisData.analysis.top_keywords} />
                    )}
                  </div>
                )}

                {/* Visualizations Tab */}
                {activeTab === 'visualizations' && (
                  <div className="space-y-6">
                    {analysisData.results && analysisData.results.length > 0 && (
                      <WordCloudChart results={analysisData.results} />
                    )}
                    {analysisData.temporal_analysis && (
                      <TemporalGraph temporalData={analysisData.temporal_analysis} />
                    )}
                    {(!analysisData.temporal_analysis && (!analysisData.results || analysisData.results.length === 0)) && (
                      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-12">
                        <p className="text-gray-400 text-center">
                          No visualization data available. Try running an advanced or all features analysis.
                        </p>
                      </div>
                    )}
                  </div>
                )}

                {/* Communities Tab */}
                {activeTab === 'communities' && (
                  <div className="space-y-6">
                    {analysisData.subreddit_analysis?.top_subreddits ? (
                      <SubredditChart
                        subredditData={analysisData.subreddit_analysis.top_subreddits}
                      />
                    ) : (
                      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-12">
                        <p className="text-gray-400 text-center">
                          Subreddit analysis data not available. Try running an advanced or all features analysis.
                        </p>
                      </div>
                    )}
                  </div>
                )}

                {/* Data Tab */}
                {activeTab === 'data' && (
                  <RedditPostsView data={analysisData.results} />
                )}
              </div>
            </div>

            {/* AI Generated Content */}
            <GeneratedContent
              query={analysisData.query}
              keywords={analysisData.analysis.top_keywords}
              sentimentData={analysisData.metrics.sentiment}
              entities={analysisData.analysis.entities}
            />

            {/* Chat Interface */}
            <ChatInterface
              context={{
                topic: analysisData.query,
                keywords: analysisData.analysis.top_keywords,
                sentiment_data: analysisData.metrics.sentiment,
                entities: analysisData.analysis.entities,
              }}
            />
          </div>
        )}

        {/* Welcome State */}
        {!loading && !analysisData && !error && (
          <div className="text-center py-16">
            <div className="mb-8">
              <BarChart3 className="mx-auto text-indigo-200" size={64} />
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-3">
              Welcome to Reddit Analyzer
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto mb-12">
              Get deep insights from Reddit with advanced sentiment analysis, keyword extraction, and AI-powered visualizations. Enter a topic above to get started.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
              <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 hover:shadow-md transition-all">
                <div className="bg-indigo-50 w-14 h-14 rounded-xl flex items-center justify-center mb-4 mx-auto">
                  <ThumbsUp className="text-indigo-600" size={28} />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Sentiment Analysis
                </h3>
                <p className="text-sm text-gray-600">
                  Understand the emotional tone of Reddit discussions
                </p>
              </div>
              <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 hover:shadow-md transition-all">
                <div className="bg-indigo-50 w-14 h-14 rounded-xl flex items-center justify-center mb-4 mx-auto">
                  <TrendingUp className="text-indigo-600" size={28} />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Trend Detection</h3>
                <p className="text-sm text-gray-600">
                  Identify patterns and trends in Reddit activity
                </p>
              </div>
              <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 hover:shadow-md transition-all">
                <div className="bg-indigo-50 w-14 h-14 rounded-xl flex items-center justify-center mb-4 mx-auto">
                  <MessageSquare className="text-indigo-600" size={28} />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Insights</h3>
                <p className="text-sm text-gray-600">
                  Generate summaries and insights with AI assistance
                </p>
              </div>
            </div>
        </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-8 mt-16">
        <div className="container mx-auto px-6 text-center">
          <p className="text-gray-500 text-sm">
            Reddit Analyzer • Built with Next.js and FastAPI
          </p>
        </div>
      </footer>
    </div>
  );
}
