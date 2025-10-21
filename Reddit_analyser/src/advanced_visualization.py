import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from wordcloud import WordCloud
from tabulate import tabulate
import os

class AdvancedVisualizer:
    def __init__(self, output_dir="visualizations"):
        """Initialize the advanced visualizer with output directory for saving plots."""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Set style for matplotlib/seaborn
        plt.style.use('default')
        sns.set_palette("husl")
        
    def create_dataframe(self, results):
        """Convert results to pandas DataFrame for easier analysis."""
        df_data = []
        for result in results:
            df_data.append({
                'type': result['type'],
                'author': result['author'],
                'score': result['score'],
                'text': result['text'],
                'sentiment': result['sentiment'],
                'created_utc': result['created_utc'],
                'subreddit': result.get('subreddit', 'unknown'),
                'title': result.get('title', result.get('post_title', '')),
                'num_comments': result.get('num_comments', 0),
                'upvote_ratio': result.get('upvote_ratio', 0.5)
            })
        return pd.DataFrame(df_data)
    
    def plot_temporal_trends(self, results, save=True):
        """Create time-based trend analysis showing activity over time."""
        df = self.create_dataframe(results)
        
        # Group by date and sentiment
        df['date'] = df['created_utc'].dt.date
        temporal_data = df.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
        
        # Create the plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Plot 1: Activity over time by sentiment
        temporal_data.plot(kind='bar', stacked=True, ax=ax1, 
                          color=['#ff4444', '#44ff44', '#4444ff'])
        ax1.set_title('Reddit Activity Trends Over Time by Sentiment', fontsize=16, fontweight='bold')
        ax1.set_xlabel('Date', fontsize=12)
        ax1.set_ylabel('Number of Posts/Comments', fontsize=12)
        ax1.legend(title='Sentiment')
        ax1.tick_params(axis='x', rotation=45)
        
        # Plot 2: Daily total activity
        daily_total = df.groupby('date').size()
        ax2.plot(daily_total.index, daily_total.values, marker='o', linewidth=2, markersize=6)
        ax2.set_title('Total Daily Activity', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Total Posts/Comments', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/temporal_trends.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def plot_subreddit_analysis(self, results, save=True):
        """Analyze and visualize subreddit engagement patterns."""
        df = self.create_dataframe(results)
        
        # Get top subreddits
        subreddit_stats = df.groupby('subreddit').agg({
            'score': ['mean', 'sum', 'count'],
            'sentiment': lambda x: (x == 'positive').mean() * 100
        }).round(2)
        
        subreddit_stats.columns = ['avg_score', 'total_score', 'post_count', 'positive_sentiment_pct']
        top_subreddits = subreddit_stats.nlargest(10, 'post_count')
        
        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: Top subreddits by post count
        top_subreddits['post_count'].plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_title('Top Subreddits by Activity', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Number of Posts/Comments')
        ax1.tick_params(axis='x', rotation=45)
        
        # Plot 2: Average score by subreddit
        top_subreddits['avg_score'].plot(kind='bar', ax=ax2, color='lightcoral')
        ax2.set_title('Average Score by Subreddit', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Average Score')
        ax2.tick_params(axis='x', rotation=45)
        
        # Plot 3: Positive sentiment percentage
        top_subreddits['positive_sentiment_pct'].plot(kind='bar', ax=ax3, color='lightgreen')
        ax3.set_title('Positive Sentiment Percentage by Subreddit', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Positive Sentiment %')
        ax3.tick_params(axis='x', rotation=45)
        
        # Plot 4: Sentiment distribution heatmap
        sentiment_pivot = df.groupby(['subreddit', 'sentiment']).size().unstack(fill_value=0)
        sentiment_pivot_pct = sentiment_pivot.div(sentiment_pivot.sum(axis=1), axis=0) * 100
        top_sentiment = sentiment_pivot_pct.loc[top_subreddits.index[:8]]
        
        sns.heatmap(top_sentiment, annot=True, fmt='.1f', cmap='RdYlGn', ax=ax4)
        ax4.set_title('Sentiment Distribution Heatmap', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Subreddit')
        
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/subreddit_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig, top_subreddits
    
    def create_engagement_metrics_chart(self, results, save=True):
        """Create comprehensive engagement metrics visualization."""
        df = self.create_dataframe(results)
        
        # Calculate engagement metrics
        posts_df = df[df['type'] == 'post'].copy()
        
        if len(posts_df) == 0:
            print("No posts found for engagement analysis")
            return None
            
        # Create engagement score (combination of score, comments, and upvote ratio)
        posts_df['engagement_score'] = (
            posts_df['score'] * 0.4 + 
            posts_df['num_comments'] * 0.4 + 
            posts_df['upvote_ratio'] * 100 * 0.2
        )
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: Score vs Comments scatter
        scatter = ax1.scatter(posts_df['score'], posts_df['num_comments'], 
                            c=posts_df['upvote_ratio'], cmap='viridis', alpha=0.6, s=60)
        ax1.set_xlabel('Post Score')
        ax1.set_ylabel('Number of Comments')
        ax1.set_title('Post Engagement: Score vs Comments', fontweight='bold')
        plt.colorbar(scatter, ax=ax1, label='Upvote Ratio')
        
        # Plot 2: Engagement by sentiment
        engagement_by_sentiment = posts_df.groupby('sentiment')['engagement_score'].mean()
        engagement_by_sentiment.plot(kind='bar', ax=ax2, color=['red', 'gray', 'green'])
        ax2.set_title('Average Engagement by Sentiment', fontweight='bold')
        ax2.set_ylabel('Engagement Score')
        ax2.tick_params(axis='x', rotation=0)
        
        # Plot 3: Upvote ratio distribution
        ax3.hist(posts_df['upvote_ratio'], bins=20, alpha=0.7, color='purple', edgecolor='black')
        ax3.set_xlabel('Upvote Ratio')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Upvote Ratio Distribution', fontweight='bold')
        ax3.axvline(posts_df['upvote_ratio'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {posts_df["upvote_ratio"].mean():.2f}')
        ax3.legend()
        
        # Plot 4: Top engaging posts
        top_posts = posts_df.nlargest(10, 'engagement_score')
        y_pos = range(len(top_posts))
        ax4.barh(y_pos, top_posts['engagement_score'], color='gold')
        ax4.set_yticks(y_pos)
        ax4.set_yticklabels([title[:40] + '...' if len(title) > 40 else title 
                           for title in top_posts['title']], fontsize=8)
        ax4.set_xlabel('Engagement Score')
        ax4.set_title('Top Engaging Posts', fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/engagement_metrics.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_word_cloud(self, results, save=True):
        """Generate word cloud from all text content."""
        df = self.create_dataframe(results)
        
        # Combine all text
        all_text = ' '.join(df['text'].fillna('') + ' ' + df['title'].fillna(''))
        
        # Create word cloud
        wordcloud = WordCloud(
            width=1200, height=600, 
            background_color='white',
            max_words=100,
            colormap='viridis'
        ).generate(all_text)
        
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Most Frequent Words in Reddit Content', fontsize=20, fontweight='bold')
        
        if save:
            plt.savefig(f'{self.output_dir}/wordcloud.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_interactive_timeline(self, results, save=True):
        """Create interactive timeline using Plotly."""
        df = self.create_dataframe(results)
        
        # Prepare data for timeline
        timeline_data = df.groupby([df['created_utc'].dt.date, 'sentiment']).size().reset_index()
        timeline_data.columns = ['date', 'sentiment', 'count']
        
        # Create interactive plot
        fig = px.line(timeline_data, x='date', y='count', color='sentiment',
                     title='Interactive Timeline: Reddit Activity by Sentiment',
                     labels={'count': 'Number of Posts/Comments', 'date': 'Date'})
        
        fig.update_layout(
            title_font_size=16,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            legend_title_font_size=14
        )
        
        if save:
            fig.write_html(f'{self.output_dir}/interactive_timeline.html')
        
        fig.show()
        return fig
    
    def generate_summary_tables(self, results, keywords=None):
        """Generate formatted summary tables for research papers."""
        df = self.create_dataframe(results)
        
        print("="*80)
        print("REDDIT ANALYSIS SUMMARY TABLES")
        print("="*80)
        
        # Table 1: Basic Statistics
        basic_stats = {
            'Metric': ['Total Posts', 'Total Comments', 'Unique Authors', 'Unique Subreddits',
                      'Average Score', 'Date Range'],
            'Value': [
                len(df[df['type'] == 'post']),
                len(df[df['type'] == 'comment']),
                df['author'].nunique(),
                df['subreddit'].nunique(),
                f"{df['score'].mean():.2f}",
                f"{df['created_utc'].min().date()} to {df['created_utc'].max().date()}"
            ]
        }
        
        print("\nTable 1: Basic Statistics")
        print(tabulate(basic_stats, headers='keys', tablefmt='grid'))
        
        # Table 2: Sentiment Distribution
        sentiment_stats = df['sentiment'].value_counts()
        sentiment_pct = df['sentiment'].value_counts(normalize=True) * 100
        
        sentiment_table = {
            'Sentiment': sentiment_stats.index,
            'Count': sentiment_stats.values,
            'Percentage': [f"{pct:.1f}%" for pct in sentiment_pct.values]
        }
        
        print("\nTable 2: Sentiment Distribution")
        print(tabulate(sentiment_table, headers='keys', tablefmt='grid'))
        
        # Table 3: Top Subreddits
        subreddit_stats = df.groupby('subreddit').agg({
            'score': ['count', 'mean', 'sum'],
            'sentiment': lambda x: (x == 'positive').mean() * 100
        }).round(2)
        
        subreddit_stats.columns = ['Posts/Comments', 'Avg Score', 'Total Score', 'Positive %']
        top_subreddits = subreddit_stats.nlargest(10, 'Posts/Comments')
        
        print("\nTable 3: Top 10 Subreddits by Activity")
        print(tabulate(top_subreddits, headers='keys', tablefmt='grid'))
        
        # Table 4: Daily Activity Summary
        daily_activity = df.groupby(df['created_utc'].dt.date).agg({
            'score': ['count', 'mean'],
            'sentiment': lambda x: (x == 'positive').mean() * 100
        }).round(2)
        
        daily_activity.columns = ['Daily Posts/Comments', 'Avg Daily Score', 'Daily Positive %']
        
        print("\nTable 4: Daily Activity Summary")
        print(tabulate(daily_activity.tail(10), headers='keys', tablefmt='grid'))
        
        # Save tables to file
        with open(f'{self.output_dir}/summary_tables.txt', 'w') as f:
            f.write("REDDIT ANALYSIS SUMMARY TABLES\n")
            f.write("="*50 + "\n\n")
            
            f.write("Table 1: Basic Statistics\n")
            f.write(tabulate(basic_stats, headers='keys', tablefmt='grid'))
            f.write("\n\n")
            
            f.write("Table 2: Sentiment Distribution\n")
            f.write(tabulate(sentiment_table, headers='keys', tablefmt='grid'))
            f.write("\n\n")
            
            f.write("Table 3: Top 10 Subreddits by Activity\n")
            f.write(tabulate(top_subreddits, headers='keys', tablefmt='grid'))
            f.write("\n\n")
            
            f.write("Table 4: Daily Activity Summary\n")
            f.write(tabulate(daily_activity.tail(10), headers='keys', tablefmt='grid'))
        
        print(f"\nTables saved to: {self.output_dir}/summary_tables.txt")
        
        return {
            'basic_stats': basic_stats,
            'sentiment_table': sentiment_table,
            'top_subreddits': top_subreddits,
            'daily_activity': daily_activity
        }
    
    def create_comprehensive_report(self, results, keywords=None):
        """Generate a comprehensive visual and statistical report."""
        print("Generating comprehensive Reddit analysis report...")
        
        # Create all visualizations
        self.plot_temporal_trends(results)
        subreddit_fig, subreddit_data = self.plot_subreddit_analysis(results)
        self.create_engagement_metrics_chart(results)
        self.create_word_cloud(results)
        self.create_interactive_timeline(results)
        
        # Generate summary tables
        tables = self.generate_summary_tables(results, keywords)
        
        print(f"\nComprehensive report generated! Check the '{self.output_dir}' folder for:")
        print("- temporal_trends.png: Time-based activity analysis")
        print("- subreddit_analysis.png: Subreddit comparison and engagement")
        print("- engagement_metrics.png: Post engagement patterns")
        print("- wordcloud.png: Most frequent words visualization")
        print("- interactive_timeline.html: Interactive timeline (open in browser)")
        print("- summary_tables.txt: Formatted data tables")
        
        return tables
