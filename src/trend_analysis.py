import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns

class TrendAnalyzer:
    def __init__(self):
        """Initialize trend analyzer for Reddit data."""
        pass
    
    def analyze_temporal_patterns(self, results):
        """Analyze temporal patterns in Reddit data."""
        df = pd.DataFrame(results)
        df['created_utc'] = pd.to_datetime(df['created_utc'])
        df['hour'] = df['created_utc'].dt.hour
        df['day_of_week'] = df['created_utc'].dt.day_name()
        df['date'] = df['created_utc'].dt.date
        
        patterns = {
            'hourly_activity': df.groupby('hour').size(),
            'daily_activity': df.groupby('day_of_week').size(),
            'date_activity': df.groupby('date').size(),
            'hourly_sentiment': df.groupby(['hour', 'sentiment']).size().unstack(fill_value=0),
            'daily_sentiment': df.groupby(['day_of_week', 'sentiment']).size().unstack(fill_value=0)
        }
        
        return patterns
    
    def detect_trending_periods(self, results, window_hours=6):
        """Detect periods of high activity (trending periods)."""
        df = pd.DataFrame(results)
        df['created_utc'] = pd.to_datetime(df['created_utc'])
        
        # Create time windows
        df['time_window'] = df['created_utc'].dt.floor(f'{window_hours}H')
        
        # Count activity per window
        window_activity = df.groupby('time_window').agg({
            'score': ['count', 'sum', 'mean'],
            'sentiment': lambda x: (x == 'positive').mean()
        }).round(3)
        
        window_activity.columns = ['post_count', 'total_score', 'avg_score', 'positive_ratio']
        
        # Identify trending periods (top 20% by activity)
        threshold = window_activity['post_count'].quantile(0.8)
        trending_periods = window_activity[window_activity['post_count'] >= threshold]
        
        return trending_periods.sort_values('post_count', ascending=False)
    
    def analyze_keyword_trends(self, results, keywords):
        """Analyze how specific keywords trend over time."""
        df = pd.DataFrame(results)
        df['created_utc'] = pd.to_datetime(df['created_utc'])
        df['date'] = df['created_utc'].dt.date
        
        # Combine text fields for keyword search
        df['full_text'] = (df['text'].fillna('') + ' ' + 
                          df.get('title', df.get('post_title', '')).fillna('')).str.lower()
        
        keyword_trends = {}
        
        for keyword in keywords:
            # Find posts/comments containing the keyword
            keyword_mask = df['full_text'].str.contains(keyword.lower(), na=False)
            keyword_data = df[keyword_mask]
            
            if len(keyword_data) > 0:
                daily_mentions = keyword_data.groupby('date').agg({
                    'score': ['count', 'mean', 'sum'],
                    'sentiment': lambda x: (x == 'positive').mean()
                }).round(3)
                
                daily_mentions.columns = ['mentions', 'avg_score', 'total_score', 'positive_ratio']
                keyword_trends[keyword] = daily_mentions
        
        return keyword_trends
    
    def calculate_engagement_velocity(self, results):
        """Calculate engagement velocity - how quickly posts gain engagement."""
        posts = [r for r in results if r['type'] == 'post']
        
        if not posts:
            return {}
        
        df = pd.DataFrame(posts)
        df['created_utc'] = pd.to_datetime(df['created_utc'])
        
        # Calculate time since posting (assuming current time as reference)
        current_time = datetime.now()
        df['hours_since_post'] = (current_time - df['created_utc']).dt.total_seconds() / 3600
        
        # Calculate engagement velocity (score per hour)
        df['engagement_velocity'] = df['score'] / (df['hours_since_post'] + 1)  # +1 to avoid division by zero
        
        velocity_stats = {
            'mean_velocity': df['engagement_velocity'].mean(),
            'median_velocity': df['engagement_velocity'].median(),
            'top_velocity_posts': df.nlargest(10, 'engagement_velocity')[
                ['title', 'score', 'hours_since_post', 'engagement_velocity']
            ].to_dict('records')
        }
        
        return velocity_stats
    
    def analyze_subreddit_trends(self, results):
        """Analyze trending patterns across different subreddits."""
        df = pd.DataFrame(results)
        df['created_utc'] = pd.to_datetime(df['created_utc'])
        df['date'] = df['created_utc'].dt.date
        
        # Subreddit activity over time
        subreddit_trends = df.groupby(['subreddit', 'date']).agg({
            'score': ['count', 'mean', 'sum'],
            'sentiment': lambda x: (x == 'positive').mean()
        }).round(3)
        
        subreddit_trends.columns = ['daily_posts', 'avg_score', 'total_score', 'positive_ratio']
        
        # Calculate trend momentum for each subreddit
        subreddit_momentum = {}
        
        for subreddit in df['subreddit'].unique():
            subreddit_data = subreddit_trends.xs(subreddit, level='subreddit')
            
            if len(subreddit_data) > 1:
                # Calculate linear trend in activity
                dates_numeric = pd.to_datetime(subreddit_data.index).astype(int) / 10**9
                activity_trend = np.polyfit(dates_numeric, subreddit_data['daily_posts'], 1)[0]
                
                subreddit_momentum[subreddit] = {
                    'activity_trend': activity_trend,
                    'total_activity': subreddit_data['daily_posts'].sum(),
                    'avg_daily_activity': subreddit_data['daily_posts'].mean(),
                    'peak_activity': subreddit_data['daily_posts'].max(),
                    'avg_sentiment': subreddit_data['positive_ratio'].mean()
                }
        
        return subreddit_momentum
    
    def generate_trend_report(self, results, keywords=None):
        """Generate a comprehensive trend analysis report."""
        print("="*80)
        print("REDDIT TREND ANALYSIS REPORT")
        print("="*80)
        
        # Temporal patterns
        patterns = self.analyze_temporal_patterns(results)
        
        print("\n1. TEMPORAL ACTIVITY PATTERNS")
        print("-" * 40)
        
        print("\nPeak Activity Hours:")
        top_hours = patterns['hourly_activity'].nlargest(5)
        for hour, count in top_hours.items():
            print(f"  {hour:02d}:00 - {count} posts/comments")
        
        print("\nActivity by Day of Week:")
        for day, count in patterns['daily_activity'].items():
            print(f"  {day}: {count} posts/comments")
        
        # Trending periods
        trending_periods = self.detect_trending_periods(results)
        
        print(f"\n2. TRENDING PERIODS (Top 5)")
        print("-" * 40)
        
        for i, (period, data) in enumerate(trending_periods.head().iterrows(), 1):
            print(f"{i}. {period}: {data['post_count']} posts/comments")
            print(f"   Avg Score: {data['avg_score']:.2f}, Positive Ratio: {data['positive_ratio']:.2f}")
        
        # Keyword trends
        if keywords:
            keyword_trends = self.analyze_keyword_trends(results, keywords)
            
            print(f"\n3. KEYWORD TRENDS")
            print("-" * 40)
            
            for keyword, trend_data in keyword_trends.items():
                if not trend_data.empty:
                    total_mentions = trend_data['mentions'].sum()
                    avg_sentiment = trend_data['positive_ratio'].mean()
                    print(f"\n'{keyword}': {total_mentions} total mentions")
                    print(f"  Average positive sentiment: {avg_sentiment:.2f}")
                    print(f"  Peak day: {trend_data['mentions'].idxmax()} ({trend_data['mentions'].max()} mentions)")
        
        # Engagement velocity
        velocity_stats = self.calculate_engagement_velocity(results)
        
        print(f"\n4. ENGAGEMENT VELOCITY")
        print("-" * 40)
        print(f"Mean engagement velocity: {velocity_stats['mean_velocity']:.2f} score/hour")
        print(f"Median engagement velocity: {velocity_stats['median_velocity']:.2f} score/hour")
        
        print("\nTop 3 High-Velocity Posts:")
        for i, post in enumerate(velocity_stats['top_velocity_posts'][:3], 1):
            print(f"{i}. '{post['title'][:50]}...' - {post['engagement_velocity']:.2f} score/hour")
        
        # Subreddit trends
        subreddit_momentum = self.analyze_subreddit_trends(results)
        
        print(f"\n5. SUBREDDIT MOMENTUM")
        print("-" * 40)
        
        # Sort by activity trend (growing subreddits)
        growing_subreddits = sorted(subreddit_momentum.items(), 
                                  key=lambda x: x[1]['activity_trend'], reverse=True)
        
        print("Top Growing Subreddits:")
        for subreddit, data in growing_subreddits[:5]:
            print(f"  r/{subreddit}: trend={data['activity_trend']:.3f}, "
                  f"avg_daily={data['avg_daily_activity']:.1f}")
        
        return {
            'temporal_patterns': patterns,
            'trending_periods': trending_periods,
            'keyword_trends': keyword_trends if keywords else {},
            'velocity_stats': velocity_stats,
            'subreddit_momentum': subreddit_momentum
        }
