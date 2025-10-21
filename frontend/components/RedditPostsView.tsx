'use client';

import React, { useState, useMemo } from 'react';
import { ChevronDown, ChevronUp, MessageSquare, ThumbsUp, User, Calendar, Download } from 'lucide-react';
import { exportData } from '@/lib/api';

interface RedditPostsViewProps {
  data: any[];
}

export default function RedditPostsView({ data }: RedditPostsViewProps) {
  const [expandedPosts, setExpandedPosts] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const postsPerPage = 10;

  // Organize data: posts with their comments
  const postsWithComments = useMemo(() => {
    const posts = data.filter(item => item.type === 'post');
    const comments = data.filter(item => item.type === 'comment');

    return posts.map(post => ({
      ...post,
      comments: comments.filter(comment => 
        comment.post_title === post.title || 
        comment.post_id === post.id
      )
    }));
  }, [data]);

  // Pagination calculations
  const totalPages = Math.ceil(postsWithComments.length / postsPerPage);
  const startIndex = (currentPage - 1) * postsPerPage;
  const endIndex = startIndex + postsPerPage;
  const currentPosts = postsWithComments.slice(startIndex, endIndex);

  // Reset to page 1 when data changes
  React.useEffect(() => {
    setCurrentPage(1);
    setExpandedPosts(new Set());
  }, [data]);

  const togglePost = (index: number) => {
    const newExpanded = new Set(expandedPosts);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedPosts(newExpanded);
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return 'bg-indigo-100 text-indigo-700';
      case 'negative':
        return 'bg-gray-100 text-gray-700';
      default:
        return 'bg-gray-50 text-gray-600';
    }
  };

  const handleExport = async (format: 'json' | 'csv') => {
    setLoading(true);
    try {
      const response = await exportData({ results: data }, format);
      if (response.success) {
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

  if (!postsWithComments || postsWithComments.length === 0) {
    return (
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-12">
        <p className="text-gray-400 text-center">No posts available</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header with export buttons */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-semibold text-gray-900">Reddit Posts & Comments</h3>
          <p className="text-sm text-gray-600 mt-1">
            {postsWithComments.length} total posts • Showing {startIndex + 1}-{Math.min(endIndex, postsWithComments.length)} • Click to expand
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => handleExport('csv')}
            disabled={loading}
            className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors disabled:opacity-50 flex items-center gap-2 text-sm font-medium"
          >
            <Download size={16} />
            CSV
          </button>
          <button
            onClick={() => handleExport('json')}
            disabled={loading}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 flex items-center gap-2 text-sm font-medium"
          >
            <Download size={16} />
            JSON
          </button>
        </div>
      </div>

      {/* Posts list */}
      <div className="space-y-3">
        {currentPosts.map((post, index) => {
          const globalIndex = startIndex + index;
          return (
          <div
            key={globalIndex}
            className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-all"
          >
            {/* Post Header - Clickable */}
            <button
              onClick={() => togglePost(globalIndex)}
              className="w-full px-6 py-4 text-left hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <h4 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                    {post.title || post.text?.substring(0, 100)}
                  </h4>
                  
                  {/* Post metadata */}
                  <div className="flex flex-wrap items-center gap-4 text-sm">
                    <div className="flex items-center gap-1 text-gray-600">
                      <User size={14} />
                      <span>u/{post.author}</span>
                    </div>
                    
                    <div className="flex items-center gap-1 text-gray-600">
                      <ThumbsUp size={14} />
                      <span className="font-semibold">{post.score}</span>
                    </div>
                    
                    {post.num_comments !== undefined && (
                      <div className="flex items-center gap-1 text-gray-600">
                        <MessageSquare size={14} />
                        <span>{post.comments?.length || 0} comments in data</span>
                      </div>
                    )}
                    
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSentimentColor(post.sentiment)}`}>
                      {post.sentiment}
                    </span>
                    
                    <div className="flex items-center gap-1 text-gray-500 text-xs">
                      <Calendar size={12} />
                      <span>r/{post.subreddit}</span>
                    </div>
                  </div>
                </div>
                
                {/* Expand/Collapse icon */}
                <div className="flex-shrink-0 mt-1">
                  {expandedPosts.has(globalIndex) ? (
                    <ChevronUp className="text-indigo-600" size={24} />
                  ) : (
                    <ChevronDown className="text-gray-400" size={24} />
                  )}
                </div>
              </div>
            </button>

            {/* Expanded Comments */}
            {expandedPosts.has(globalIndex) && (
              <div className="border-t border-gray-100 bg-gray-50">
                {post.text && (
                  <div className="px-6 py-4 border-b border-gray-100 bg-white">
                    <p className="text-sm font-medium text-gray-700 mb-2">Post Content:</p>
                    <p className="text-gray-800 text-sm leading-relaxed whitespace-pre-wrap">
                      {post.text}
                    </p>
                  </div>
                )}
                
                {post.comments && post.comments.length > 0 ? (
                  <div className="px-6 py-4 space-y-3">
                    <p className="text-sm font-semibold text-gray-700 mb-3">
                      Comments ({post.comments.length}):
                    </p>
                    
                    {post.comments.map((comment: any, commentIndex: number) => (
                      <div
                        key={commentIndex}
                        className="bg-white rounded-xl p-4 border border-gray-200 hover:border-indigo-200 transition-colors"
                      >
                        <div className="flex items-start justify-between gap-3 mb-2">
                          <div className="flex items-center gap-3 text-xs">
                            <span className="text-gray-700 font-medium">
                              u/{comment.author}
                            </span>
                            <span className="flex items-center gap-1 text-gray-600">
                              <ThumbsUp size={12} />
                              {comment.score}
                            </span>
                            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${getSentimentColor(comment.sentiment)}`}>
                              {comment.sentiment}
                            </span>
                          </div>
                        </div>
                        
                        <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">
                          {comment.text}
                        </p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="px-6 py-8 text-center text-gray-500 text-sm">
                    No comments available for this post
                  </div>
                )}
              </div>
            )}
          </div>
        );
        })}
      </div>

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between mt-6 px-4 py-4 bg-white rounded-2xl shadow-sm border border-gray-100">
          <div className="text-sm text-gray-600">
            Page {currentPage} of {totalPages} • {postsWithComments.length} total posts
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                setCurrentPage(1);
                setExpandedPosts(new Set());
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
              disabled={currentPage === 1}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed text-sm text-gray-900 font-medium transition-colors"
            >
              First
            </button>
            
            <button
              onClick={() => {
                setCurrentPage(prev => Math.max(prev - 1, 1));
                setExpandedPosts(new Set());
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
              disabled={currentPage === 1}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed text-sm text-gray-900 font-medium transition-colors"
            >
              Previous
            </button>
            
            {/* Page numbers */}
            <div className="flex items-center gap-1">
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                let pageNum;
                if (totalPages <= 5) {
                  pageNum = i + 1;
                } else if (currentPage <= 3) {
                  pageNum = i + 1;
                } else if (currentPage >= totalPages - 2) {
                  pageNum = totalPages - 4 + i;
                } else {
                  pageNum = currentPage - 2 + i;
                }
                
                return (
                  <button
                    key={pageNum}
                    onClick={() => {
                      setCurrentPage(pageNum);
                      setExpandedPosts(new Set());
                      window.scrollTo({ top: 0, behavior: 'smooth' });
                    }}
                    className={`w-10 h-10 rounded-lg text-sm font-medium transition-colors ${
                      currentPage === pageNum
                        ? 'bg-indigo-600 text-white'
                        : 'border border-gray-300 text-gray-900 hover:bg-gray-50'
                    }`}
                  >
                    {pageNum}
                  </button>
                );
              })}
            </div>
            
            <button
              onClick={() => {
                setCurrentPage(prev => Math.min(prev + 1, totalPages));
                setExpandedPosts(new Set());
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
              disabled={currentPage === totalPages}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed text-sm text-gray-900 font-medium transition-colors"
            >
              Next
            </button>
            
            <button
              onClick={() => {
                setCurrentPage(totalPages);
                setExpandedPosts(new Set());
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
              disabled={currentPage === totalPages}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed text-sm text-gray-900 font-medium transition-colors"
            >
              Last
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

