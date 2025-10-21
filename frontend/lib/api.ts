/**
 * API Client for Reddit Analyzer Backend
 * Handles all communication with the FastAPI backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface AnalysisRequest {
  query: string;
  limit?: number;
  analysis_type?: 'basic' | 'advanced' | 'trend' | 'all';
}

export interface ChatRequest {
  message: string;
  context?: any;
}

export interface ContentGenerationRequest {
  query: string;
  keywords: [number, string][];
  sentiment_data: {
    positive: number;
    negative: number;
    neutral: number;
  };
  entities?: { [key: string]: string[] };
}

export interface AnalysisResponse {
  success: boolean;
  data?: any;
  error?: string;
}

// API Functions

/**
 * Search Reddit for posts and comments
 */
export const searchReddit = async (request: AnalysisRequest): Promise<AnalysisResponse> => {
  try {
    const response = await api.post('/api/search', request);
    return response.data;
  } catch (error: any) {
    console.error('Search error:', error);
    throw new Error(error.response?.data?.detail || 'Search failed');
  }
};

/**
 * Perform comprehensive analysis
 */
export const analyzeReddit = async (request: AnalysisRequest): Promise<AnalysisResponse> => {
  try {
    const response = await api.post('/api/analyze', request);
    return response.data;
  } catch (error: any) {
    console.error('Analysis error:', error);
    throw new Error(error.response?.data?.detail || 'Analysis failed');
  }
};

/**
 * Calculate sentiment distribution
 */
export const analyzeSentiment = async (results: any[]): Promise<any> => {
  try {
    const response = await api.post('/api/sentiment', results);
    return response.data;
  } catch (error: any) {
    console.error('Sentiment analysis error:', error);
    throw new Error(error.response?.data?.detail || 'Sentiment analysis failed');
  }
};

/**
 * Generate trend analysis
 */
export const analyzeTrends = async (request: AnalysisRequest): Promise<any> => {
  try {
    const response = await api.post('/api/trends', request);
    return response.data;
  } catch (error: any) {
    console.error('Trend analysis error:', error);
    throw new Error(error.response?.data?.detail || 'Trend analysis failed');
  }
};

/**
 * Generate AI content
 */
export const generateContent = async (request: ContentGenerationRequest): Promise<any> => {
  try {
    const response = await api.post('/api/generate-content', request);
    return response.data;
  } catch (error: any) {
    console.error('Content generation error:', error);
    throw new Error(error.response?.data?.detail || 'Content generation failed');
  }
};

/**
 * Chat with AI assistant
 */
export const chat = async (request: ChatRequest): Promise<any> => {
  try {
    const response = await api.post('/api/chat', request);
    return response.data;
  } catch (error: any) {
    console.error('Chat error:', error);
    throw new Error(error.response?.data?.detail || 'Chat failed');
  }
};

/**
 * Export data
 */
export const exportData = async (data: any, format: 'json' | 'csv' = 'json'): Promise<any> => {
  try {
    const response = await api.post('/api/export', data, {
      params: { export_format: format }
    });
    return response.data;
  } catch (error: any) {
    console.error('Export error:', error);
    throw new Error(error.response?.data?.detail || 'Export failed');
  }
};

/**
 * Health check
 */
export const healthCheck = async (): Promise<any> => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error: any) {
    console.error('Health check error:', error);
    throw new Error('Backend is not responding');
  }
};

export default api;


