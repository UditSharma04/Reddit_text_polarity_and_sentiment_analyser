import os
import json
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

class ResearchExporter:
    def __init__(self, output_dir="research_output"):
        """Initialize research exporter with high-quality output settings."""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Set high-quality matplotlib defaults
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['savefig.dpi'] = 300
        plt.rcParams['savefig.bbox'] = 'tight'
        plt.rcParams['savefig.pad_inches'] = 0.1
        
    def export_raw_data(self, results, filename="reddit_data"):
        """Export raw data in multiple formats for research use."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON export
        json_file = f"{self.output_dir}/{filename}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str, ensure_ascii=False)
        
        # CSV export
        csv_file = f"{self.output_dir}/{filename}_{timestamp}.csv"
        
        # Flatten the data for CSV
        flattened_data = []
        for item in results:
            flat_item = {
                'type': item.get('type', ''),
                'title': item.get('title', item.get('post_title', '')),
                'author': item.get('author', ''),
                'score': item.get('score', 0),
                'text': item.get('text', ''),
                'sentiment': item.get('sentiment', ''),
                'subreddit': item.get('subreddit', ''),
                'created_utc': item.get('created_utc', ''),
                'num_comments': item.get('num_comments', 0),
                'upvote_ratio': item.get('upvote_ratio', 0),
                'id': item.get('id', item.get('comment_id', '')),
                'post_id': item.get('post_id', ''),
                'url': item.get('url', item.get('post_url', ''))
            }
            flattened_data.append(flat_item)
        
        df = pd.DataFrame(flattened_data)
        df.to_csv(csv_file, index=False, encoding='utf-8')
        
        print(f"Raw data exported to:")
        print(f"  - JSON: {json_file}")
        print(f"  - CSV: {csv_file}")
        
        return json_file, csv_file
    
    def export_analysis_summary(self, analysis_results, filename="analysis_summary"):
        """Export analysis summary in LaTeX table format for research papers."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create comprehensive summary
        summary_file = f"{self.output_dir}/{filename}_{timestamp}.tex"
        
        with open(summary_file, 'w') as f:
            f.write("% Reddit Analysis Summary - LaTeX Tables for Research Papers\n")
            f.write("% Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            
            # Basic statistics table
            if 'basic_stats' in analysis_results:
                f.write("% Basic Statistics Table\n")
                f.write("\\begin{table}[h]\n")
                f.write("\\centering\n")
                f.write("\\caption{Reddit Analysis Basic Statistics}\n")
                f.write("\\begin{tabular}{|l|l|}\n")
                f.write("\\hline\n")
                f.write("\\textbf{Metric} & \\textbf{Value} \\\\\n")
                f.write("\\hline\n")
                
                for metric, value in zip(analysis_results['basic_stats']['Metric'], 
                                       analysis_results['basic_stats']['Value']):
                    f.write(f"{metric} & {value} \\\\\n")
                
                f.write("\\hline\n")
                f.write("\\end{tabular}\n")
                f.write("\\label{tab:basic_stats}\n")
                f.write("\\end{table}\n\n")
            
            # Sentiment distribution table
            if 'sentiment_table' in analysis_results:
                f.write("% Sentiment Distribution Table\n")
                f.write("\\begin{table}[h]\n")
                f.write("\\centering\n")
                f.write("\\caption{Sentiment Distribution Analysis}\n")
                f.write("\\begin{tabular}{|l|c|c|}\n")
                f.write("\\hline\n")
                f.write("\\textbf{Sentiment} & \\textbf{Count} & \\textbf{Percentage} \\\\\n")
                f.write("\\hline\n")
                
                for sentiment, count, pct in zip(
                    analysis_results['sentiment_table']['Sentiment'],
                    analysis_results['sentiment_table']['Count'],
                    analysis_results['sentiment_table']['Percentage']
                ):
                    f.write(f"{sentiment} & {count} & {pct} \\\\\n")
                
                f.write("\\hline\n")
                f.write("\\end{tabular}\n")
                f.write("\\label{tab:sentiment_dist}\n")
                f.write("\\end{table}\n\n")
        
        print(f"LaTeX analysis summary exported to: {summary_file}")
        return summary_file
    
    def create_publication_ready_figures(self, results, output_prefix="figure"):
        """Create publication-ready figures with proper formatting."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Set publication style
        plt.style.use('default')
        plt.rcParams.update({
            'font.size': 12,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 11,
            'figure.titlesize': 16,
            'font.family': 'serif'
        })
        
        df = pd.DataFrame(results)
        df['created_utc'] = pd.to_datetime(df['created_utc'])
        
        figure_files = []
        
        # Figure 1: Temporal Activity Pattern
        fig, ax = plt.subplots(figsize=(10, 6))
        daily_activity = df.groupby(df['created_utc'].dt.date).size()
        
        ax.plot(daily_activity.index, daily_activity.values, 'o-', linewidth=2, markersize=6)
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Posts/Comments')
        ax.set_title('Reddit Activity Over Time')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        fig1_file = f"{self.output_dir}/{output_prefix}_temporal_{timestamp}.png"
        plt.savefig(fig1_file, dpi=300, bbox_inches='tight')
        figure_files.append(fig1_file)
        plt.close()
        
        # Figure 2: Sentiment Distribution
        fig, ax = plt.subplots(figsize=(8, 6))
        sentiment_counts = df['sentiment'].value_counts()
        colors = ['#2E8B57', '#DC143C', '#4682B4']  # Professional colors
        
        wedges, texts, autotexts = ax.pie(sentiment_counts.values, 
                                         labels=sentiment_counts.index,
                                         autopct='%1.1f%%',
                                         colors=colors,
                                         startangle=90)
        
        ax.set_title('Sentiment Distribution in Reddit Data')
        
        fig2_file = f"{self.output_dir}/{output_prefix}_sentiment_{timestamp}.png"
        plt.savefig(fig2_file, dpi=300, bbox_inches='tight')
        figure_files.append(fig2_file)
        plt.close()
        
        # Figure 3: Subreddit Activity
        if 'subreddit' in df.columns:
            fig, ax = plt.subplots(figsize=(12, 8))
            top_subreddits = df['subreddit'].value_counts().head(10)
            
            bars = ax.barh(range(len(top_subreddits)), top_subreddits.values)
            ax.set_yticks(range(len(top_subreddits)))
            ax.set_yticklabels([f'r/{sub}' for sub in top_subreddits.index])
            ax.set_xlabel('Number of Posts/Comments')
            ax.set_title('Top 10 Most Active Subreddits')
            
            # Add value labels on bars
            for i, (bar, value) in enumerate(zip(bars, top_subreddits.values)):
                ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                       str(value), va='center', ha='left')
            
            fig3_file = f"{self.output_dir}/{output_prefix}_subreddits_{timestamp}.png"
            plt.savefig(fig3_file, dpi=300, bbox_inches='tight')
            figure_files.append(fig3_file)
            plt.close()
        
        print(f"Publication-ready figures created:")
        for fig_file in figure_files:
            print(f"  - {fig_file}")
        
        return figure_files
    
    def generate_methodology_section(self, results, query, keywords):
        """Generate a methodology section for research papers."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        methodology_file = f"{self.output_dir}/methodology_{timestamp}.tex"
        
        df = pd.DataFrame(results)
        
        with open(methodology_file, 'w') as f:
            f.write("% Methodology Section for Research Paper\n")
            f.write("% Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            
            f.write("\\section{Methodology}\n\n")
            
            f.write("\\subsection{Data Collection}\n")
            f.write(f"Data was collected from Reddit using the Reddit API (PRAW) with the search query: ``{query}''. ")
            f.write(f"The analysis included {len(df)} total data points comprising both posts and comments ")
            f.write(f"from {df['subreddit'].nunique()} unique subreddits. ")
            f.write(f"Data collection spanned from {df['created_utc'].min().date()} to {df['created_utc'].max().date()}.\n\n")
            
            f.write("\\subsection{Data Processing}\n")
            f.write("The collected data underwent several preprocessing steps:\n")
            f.write("\\begin{itemize}\n")
            f.write("\\item Language detection to filter English-only content\n")
            f.write("\\item Text cleaning and normalization\n")
            f.write("\\item Sentiment analysis using VADER sentiment analyzer\n")
            f.write("\\item Temporal analysis based on post/comment timestamps\n")
            f.write("\\end{itemize}\n\n")
            
            f.write("\\subsection{Analysis Methods}\n")
            f.write("The analysis employed multiple computational methods:\n")
            f.write("\\begin{itemize}\n")
            f.write("\\item Sentiment analysis for emotional tone classification\n")
            f.write("\\item Temporal trend analysis for activity pattern identification\n")
            f.write("\\item Subreddit comparison for community behavior analysis\n")
            f.write("\\item Engagement metrics calculation (scores, comments, upvote ratios)\n")
            f.write("\\end{itemize}\n\n")
        
        print(f"Methodology section generated: {methodology_file}")
        return methodology_file
    
    def create_complete_research_package(self, results, analysis_results, query, keywords):
        """Create a complete research package with all exports."""
        print("Creating complete research package...")
        
        package_files = []
        
        # Export raw data
        json_file, csv_file = self.export_raw_data(results)
        package_files.extend([json_file, csv_file])
        
        # Export analysis summary
        summary_file = self.export_analysis_summary(analysis_results)
        package_files.append(summary_file)
        
        # Create publication figures
        figure_files = self.create_publication_ready_figures(results)
        package_files.extend(figure_files)
        
        # Generate methodology
        methodology_file = self.generate_methodology_section(results, query, keywords)
        package_files.append(methodology_file)
        
        # Create README for the package
        readme_file = f"{self.output_dir}/README_research_package.txt"
        with open(readme_file, 'w') as f:
            f.write("REDDIT ANALYSIS RESEARCH PACKAGE\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Search query: {query}\n")
            f.write(f"Keywords: {', '.join(keywords) if keywords else 'N/A'}\n\n")
            
            f.write("PACKAGE CONTENTS:\n")
            f.write("-" * 20 + "\n")
            for file_path in package_files:
                filename = os.path.basename(file_path)
                f.write(f"- {filename}\n")
            
            f.write("\nFILE DESCRIPTIONS:\n")
            f.write("-" * 20 + "\n")
            f.write("- *.json: Raw data in JSON format\n")
            f.write("- *.csv: Raw data in CSV format for spreadsheet analysis\n")
            f.write("- *.tex: LaTeX formatted tables and methodology section\n")
            f.write("- *.png: High-resolution publication-ready figures (300 DPI)\n")
            f.write("- README_research_package.txt: This file\n")
        
        package_files.append(readme_file)
        
        print(f"\nComplete research package created in: {self.output_dir}/")
        print("Package includes:")
        print("  ✓ Raw data (JSON, CSV)")
        print("  ✓ LaTeX formatted tables")
        print("  ✓ Publication-ready figures (300 DPI)")
        print("  ✓ Methodology section")
        print("  ✓ Package documentation")
        
        return package_files
