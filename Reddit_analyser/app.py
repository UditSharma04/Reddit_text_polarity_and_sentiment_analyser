import asyncio
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64

from config.config import REDDIT_CONFIG
from src.reddit_client import RedditClient
from src.text_analysis import TextAnalyzer
from src.sentiment_analysis import calculate_sentiment_distribution
from src.entity_analysis import EntityAnalyzer
from src.visualization import Visualizer
from src.advanced_visualization import AdvancedVisualizer
from src.trend_analysis import TrendAnalyzer
from src.research_export import ResearchExporter
from src.content_generator import ContentGenerator


st.set_page_config(page_title="Enhanced Reddit Analyzer", page_icon="📊", layout="wide")

# Show notifications at the top
if 'export_status' in st.session_state:
    # Success notifications
    if st.session_state.export_status.get('report') == 'completed':
        st.success("🎉 Trend Report completed successfully! Check the logs for details.")
    if st.session_state.export_status.get('visualizations') == 'completed':
        st.success("🎉 Research visualizations created! Files saved to 'streamlit_visualizations/' folder.")
    
    # Error notifications
    if st.session_state.export_status.get('report') == 'error':
        st.error("❌ Trend Report failed. Check the debug logs for error details.")
    if st.session_state.export_status.get('visualizations') == 'error':
        st.error("❌ Visualization creation failed. Check the debug logs for error details.")
    
    # Processing notifications
    if st.session_state.export_status.get('report') == 'processing':
        st.info("⏳ Trend Report is currently being generated...")
    if st.session_state.export_status.get('visualizations') == 'processing':
        st.info("⏳ Research visualizations are being created...")

st.title("🚀 Enhanced Reddit Analyzer")
st.caption("Advanced Reddit analysis with research-grade visualizations and trend analysis")


@st.cache_resource
def get_cached_components():
    return (
        RedditClient(**REDDIT_CONFIG),
        TextAnalyzer(),
        EntityAnalyzer(),
        Visualizer(),
        AdvancedVisualizer(output_dir="streamlit_visualizations"),
        TrendAnalyzer(),
        ResearchExporter(output_dir="streamlit_research_output")
    )


reddit_client, text_analyzer, entity_analyzer, visualizer, advanced_visualizer, trend_analyzer, research_exporter = get_cached_components()
content_generator = ContentGenerator()

# Sidebar for analysis options
st.sidebar.header("📊 Analysis Options")
analysis_type = st.sidebar.selectbox(
    "Choose Analysis Type",
    ["Basic Analysis", "Advanced Research Analysis", "Trend Analysis", "All Features"]
)

show_tables = st.sidebar.checkbox("Show Data Tables", value=True)
show_exports = st.sidebar.checkbox("Enable Research Exports", value=False)

# Main input
col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("What topic do you want to analyze?", placeholder="e.g., AI in education, climate change, cryptocurrency")
with col2:
    limit = st.slider("Number of results", min_value=10, max_value=200, value=50, step=10)

analyze_clicked = st.button("🔍 Analyze Reddit Data", type="primary")


async def analyze(query_text: str, limit_num: int):
    keywords = text_analyzer.extract_keywords(query_text)
    search_query = " ".join(keywords) or query_text
    results = await reddit_client.search_reddit(search_query, limit=limit_num)
    return keywords, results


def create_temporal_chart(results):
    """Create interactive temporal trend chart for Streamlit."""
    df = pd.DataFrame(results)
    if 'created_utc' not in df.columns:
        return None
    
    df['created_utc'] = pd.to_datetime(df['created_utc'])
    df['date'] = df['created_utc'].dt.date
    
    # Group by date and sentiment
    temporal_data = df.groupby(['date', 'sentiment']).size().reset_index(name='count')
    
    fig = px.line(temporal_data, x='date', y='count', color='sentiment',
                 title='Reddit Activity Trends Over Time',
                 labels={'count': 'Number of Posts/Comments', 'date': 'Date'})
    
    fig.update_layout(height=400)
    return fig

def create_subreddit_chart(results):
    """Create subreddit comparison chart."""
    df = pd.DataFrame(results)
    if 'subreddit' not in df.columns:
        return None
    
    subreddit_stats = df.groupby('subreddit').agg({
        'score': ['count', 'mean'],
        'sentiment': lambda x: (x == 'positive').mean() * 100
    }).round(2)
    
    subreddit_stats.columns = ['post_count', 'avg_score', 'positive_pct']
    top_subreddits = subreddit_stats.nlargest(10, 'post_count').reset_index()
    
    fig = px.bar(top_subreddits, x='subreddit', y='post_count',
                color='positive_pct', color_continuous_scale='RdYlGn',
                title='Top Subreddits by Activity (Color = Positive Sentiment %)',
                labels={'post_count': 'Number of Posts/Comments'})
    
    fig.update_layout(height=400, xaxis_tickangle=-45)
    return fig

def create_engagement_scatter(results):
    """Create engagement scatter plot."""
    posts = [r for r in results if r.get('type') == 'post']
    if not posts:
        return None
    
    df = pd.DataFrame(posts)
    required_cols = ['score', 'num_comments', 'upvote_ratio']
    if not all(col in df.columns for col in required_cols):
        return None
    
    fig = px.scatter(df, x='score', y='num_comments', color='upvote_ratio',
                    size='upvote_ratio', hover_data=['title'],
                    title='Post Engagement: Score vs Comments',
                    color_continuous_scale='viridis')
    
    fig.update_layout(height=400)
    return fig

if analyze_clicked and query:
    # Clear previous export status and auto-generation flags when starting new analysis
    if 'export_status' in st.session_state:
        st.session_state.export_status = {}
    if 'export_logs' in st.session_state:
        st.session_state.export_logs = []
    
    # Reset auto-generation flags for new analysis
    st.session_state.trend_report_generated = False
    st.session_state.visualizations_generated = False
    
    # Progress bar for analysis
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🔍 Initializing Reddit search...")
        progress_bar.progress(10)
        
        status_text.text("🌐 Connecting to Reddit API...")
        progress_bar.progress(20)
        
        # Run the analysis
        keywords, results = asyncio.run(analyze(query, limit))
        
        progress_bar.progress(60)
        status_text.text(f"📊 Processing {len(results) if results else 0} results...")
        
        progress_bar.progress(80)
        status_text.text("🧠 Performing sentiment analysis...")
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
    except RuntimeError:
        # In case of running inside an existing event loop (rare in Streamlit)
        status_text.text("🔄 Retrying with new event loop...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        keywords, results = loop.run_until_complete(analyze(query, limit))
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        progress_bar.empty()
        status_text.empty()
    
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Analysis failed: {str(e)}")
        st.info("💡 Try reducing the number of results or check your internet connection")
        results = None

    if results:
        # Store results in session state for export
        st.session_state['analysis_results'] = results
        st.session_state['analysis_query'] = query
        st.session_state['analysis_keywords'] = keywords
        
        sentiments = calculate_sentiment_distribution(results)
        texts = [r['text'] for r in results if r.get('text')]
        combined = " ".join(texts)
        top_keywords = text_analyzer.extract_top_keywords(combined)
        entities = entity_analyzer.extract_entities(combined)
        
        # Create main metrics row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Posts/Comments", len(results))
        with col2:
            st.metric("Unique Subreddits", len(set(r.get('subreddit', 'unknown') for r in results)))
        with col3:
            st.metric("Positive Sentiment", f"{sentiments['positive']:.1f}%")
        with col4:
            avg_score = sum(r.get('score', 0) for r in results) / len(results)
            st.metric("Average Score", f"{avg_score:.1f}")
        
        # Analysis tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "🏘️ Communities", "📋 Data"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Sentiment Distribution")
                fig = visualizer.figure_sentiment_distribution(sentiments)
                st.pyplot(fig)
            
            with col2:
                st.subheader("Top Keywords")
                if top_keywords and len(top_keywords) > 0:
                    # Automatically generate keyword chart without user interaction
                    keyword_data = []
                    for count, keyword in top_keywords[:15]:
                        keyword_data.append({'Count': count, 'Keyword': keyword})
                    
                    keyword_df = pd.DataFrame(keyword_data)
                    
                    if not keyword_df.empty:
                        fig = px.bar(keyword_df, x='Count', y='Keyword', orientation='h',
                                   title='Most Frequent Keywords',
                                   color='Count',
                                   color_continuous_scale='viridis')
                        fig.update_layout(height=400, showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Processing keywords...")
                else:
                    st.info("No keywords extracted. This might happen with short text content.")

        st.subheader("Named Entities")
        if entities:
            for etype, elist in entities.items():
                if elist:
                    st.markdown(f"**{etype}**: " + ", ".join(sorted(set(elist))[:30]))
        else:
            st.write("No entities detected.")

        with tab2:
            st.subheader("📈 Temporal Trends Analysis")
            
            # Interactive temporal chart
            temporal_fig = create_temporal_chart(results)
            if temporal_fig:
                st.plotly_chart(temporal_fig, use_container_width=True)
            else:
                st.info("Temporal data not available for trend analysis")
            
            # Engagement scatter plot
            if analysis_type in ["Advanced Research Analysis", "All Features"]:
                engagement_fig = create_engagement_scatter(results)
                if engagement_fig:
                    st.subheader("Post Engagement Analysis")
                    st.plotly_chart(engagement_fig, use_container_width=True)
        
        with tab3:
            st.subheader("🏘️ Subreddit Community Analysis")
            
            # Subreddit comparison chart
            subreddit_fig = create_subreddit_chart(results)
            if subreddit_fig:
                st.plotly_chart(subreddit_fig, use_container_width=True)
            else:
                st.info("Subreddit data not available")
            
            # Community stats table
            if show_tables:
                df = pd.DataFrame(results)
                if 'subreddit' in df.columns:
                    community_stats = df.groupby('subreddit').agg({
                        'score': ['count', 'mean', 'sum'],
                        'sentiment': lambda x: (x == 'positive').mean() * 100
                    }).round(2)
                    community_stats.columns = ['Posts/Comments', 'Avg Score', 'Total Score', 'Positive %']
                    st.subheader("Community Statistics")
                    st.dataframe(community_stats.head(10))
        
        with tab4:
            st.subheader("📋 Raw Data & Export")
            
            if show_tables:
                # Display sample data
                df = pd.DataFrame(results)
                st.subheader("Sample Data (First 10 rows)")
                display_cols = ['type', 'title', 'author', 'score', 'sentiment', 'subreddit', 'created_utc']
                available_cols = [col for col in display_cols if col in df.columns]
                st.dataframe(df[available_cols].head(10))
                
                # Data summary
                st.subheader("Data Summary")
                st.write(f"**Total Records:** {len(df)}")
                st.write(f"**Date Range:** {df['created_utc'].min()} to {df['created_utc'].max()}" if 'created_utc' in df.columns else "Date information not available")
                st.write(f"**Sentiment Breakdown:** Positive: {sentiments['positive']:.1f}%, Negative: {sentiments['negative']:.1f}%, Neutral: {sentiments['neutral']:.1f}%")
        
        # Research Export Section
        if show_exports and analysis_type in ["Advanced Research Analysis", "All Features"]:
            st.subheader("🔬 Research Export")
            
            # Initialize session state for export operations
            if 'export_status' not in st.session_state:
                st.session_state.export_status = {}
            if 'export_logs' not in st.session_state:
                st.session_state.export_logs = []
            
            # Create columns for export buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("📊 Data Export")
                
                # CSV Export with immediate download
                df = pd.DataFrame(results)
                csv_data = df.to_csv(index=False)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"reddit_analysis_{query.replace(' ', '_')}_{timestamp}.csv"
                
                st.download_button(
                    label="📥 Download CSV Data",
                    data=csv_data,
                    file_name=filename,
                    mime="text/csv",
                    help="Download raw data in CSV format"
                )
                
                # JSON Export
                import json
                json_data = json.dumps(results, indent=2, default=str)
                json_filename = f"reddit_analysis_{query.replace(' ', '_')}_{timestamp}.json"
                
                st.download_button(
                    label="📥 Download JSON Data",
                    data=json_data,
                    file_name=json_filename,
                    mime="application/json",
                    help="Download raw data in JSON format"
                )
            
            with col2:
                st.subheader("📈 Generate Report")
                
                # Auto-generate trend report without button click
                if 'trend_report_generated' not in st.session_state:
                    st.session_state.trend_report_generated = False
                
                if not st.session_state.trend_report_generated:
                    with st.spinner("🔍 Auto-generating trend report..."):
                        try:
                            # Auto-generate trend analysis
                            trend_results = trend_analyzer.generate_trend_report(results, keywords)
                            
                            # Store results in session state
                            st.session_state['trend_results'] = trend_results
                            st.session_state.trend_report_generated = True
                            
                            st.success("✅ Trend report auto-generated!")
                            
                        except Exception as e:
                            st.error(f"❌ Error generating report: {str(e)}")
                            st.session_state.trend_report_generated = True  # Prevent infinite retry
                
                # Show report status
                if st.session_state.trend_report_generated:
                    st.success("✅ Trend Report: Ready")
                    
                    # Show some key insights from the trend report
                    if 'trend_results' in st.session_state:
                        trend_data = st.session_state['trend_results']
                        if 'temporal_patterns' in trend_data:
                            patterns = trend_data['temporal_patterns']
                            if 'hourly_activity' in patterns:
                                peak_hour = patterns['hourly_activity'].idxmax()
                                peak_count = patterns['hourly_activity'].max()
                                st.info(f"📊 Peak activity: {peak_hour}:00 ({peak_count} posts)")
                else:
                    st.info("⏳ Generating trend analysis...")
            
            with col3:
                st.subheader("🎨 Create Visualizations")
                
                # Auto-generate visualizations without button click
                if 'visualizations_generated' not in st.session_state:
                    st.session_state.visualizations_generated = False
                
                if not st.session_state.visualizations_generated:
                    with st.spinner("🎨 Auto-creating research visualizations..."):
                        try:
                            # Generate comprehensive report automatically
                            analysis_tables = advanced_visualizer.create_comprehensive_report(results, keywords)
                            
                            # Store results
                            st.session_state['visualization_results'] = analysis_tables
                            st.session_state.visualizations_generated = True
                            
                            st.success("✅ Research visualizations auto-created!")
                            
                            # Show created files
                            import os
                            viz_dir = "streamlit_visualizations"
                            if os.path.exists(viz_dir):
                                files = [f for f in os.listdir(viz_dir) if f.endswith(('.png', '.html', '.txt'))]
                                if files:
                                    st.info(f"📁 Created {len(files)} files in 'streamlit_visualizations/'")
                                    
                                    # Show some key files
                                    key_files = [f for f in files if any(key in f for key in ['temporal', 'subreddit', 'engagement'])]
                                    for file in key_files[:3]:
                                        st.text(f"  • {file}")
                            
                        except Exception as e:
                            st.error(f"❌ Error creating visualizations: {str(e)}")
                            st.session_state.visualizations_generated = True  # Prevent infinite retry
                
                # Show visualization status
                if st.session_state.visualizations_generated:
                    st.success("✅ Visualizations: Ready")
                    
                    # Show visualization summary
                    if 'visualization_results' in st.session_state:
                        viz_data = st.session_state['visualization_results']
                        if viz_data and 'basic_stats' in viz_data:
                            stats = viz_data['basic_stats']
                            if isinstance(stats, dict) and 'Value' in stats:
                                total_posts = stats['Value'][0] if len(stats['Value']) > 0 else 'N/A'
                                st.info(f"📊 Analysis complete: {total_posts} posts/comments processed")
                else:
                    st.info("⏳ Creating visualizations...")
            
            # Debug Logs Section
            with st.expander("🔍 Debug Logs & Processing Details", expanded=False):
                
                # Clear logs button
                col_clear, col_refresh = st.columns([1, 1])
                with col_clear:
                    if st.button("🗑️ Clear Logs"):
                        st.session_state.export_logs = []
                        st.session_state.export_status = {}
                        st.rerun()
                
                with col_refresh:
                    if st.button("🔄 Refresh Status"):
                        st.rerun()
                
                # Display logs with auto-refresh
                if st.session_state.export_logs:
                    st.subheader("📋 Processing Logs")
                    log_container = st.container()
                    with log_container:
                        # Show logs in reverse chronological order (newest first)
                        recent_logs = st.session_state.export_logs[-20:]
                        st.code("\n".join(recent_logs), language="text")
                        
                        # Show log count
                        st.caption(f"Showing last {len(recent_logs)} of {len(st.session_state.export_logs)} total logs")
                else:
                    st.info("No logs yet. Click export buttons to see processing logs.")
                
                # Real-time status indicators
                st.subheader("⚡ Real-time Status")
                
                # Processing indicators
                if st.session_state.export_status.get('report') == 'processing':
                    st.warning("⏳ Trend Report: Currently processing...")
                    st.progress(50)
                
                if st.session_state.export_status.get('visualizations') == 'processing':
                    st.warning("⏳ Visualizations: Currently creating...")
                    st.progress(75)
                
                # System information
                st.subheader("🔧 System Information")
                st.text(f"Analysis Query: {st.session_state.get('analysis_query', 'None')}")
                st.text(f"Total Results: {len(st.session_state.get('analysis_results', []))}")
                st.text(f"Keywords: {', '.join(st.session_state.get('analysis_keywords', []))}")
                st.text(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Auto-Generation Status Summary
            st.subheader("📊 Auto-Generation Status")
            status_col1, status_col2 = st.columns(2)
            
            with status_col1:
                if st.session_state.get('trend_report_generated', False):
                    st.success("✅ Trend Report: Auto-generated")
                else:
                    st.info("⏳ Trend Report: Processing...")
            
            with status_col2:
                if st.session_state.get('visualizations_generated', False):
                    st.success("✅ Visualizations: Auto-created")
                else:
                    st.info("⏳ Visualizations: Processing...")
        
        # AI Content Generation
        st.subheader("🤖 AI-Generated Summary Post")
        content_generator.set_context(topic=query, keywords=top_keywords, sentiment_data=sentiments, entities=entities)

        post = content_generator.generate_content(query=query, keywords=top_keywords, sentiment_data=sentiments)
        if post and post[0]:
            st.success(post[0])
        else:
            st.info("Could not generate content right now. Try again or adjust the topic.")
    
    else:
        st.error("No results found. Try a different search query or increase the result limit.")

st.subheader("Chat: Ask for help or refine your post")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_analyzed_query" not in st.session_state:
    st.session_state.last_analyzed_query = None

# Reset chat history if the analyzed query changed
if st.session_state.last_analyzed_query != query and query:
    st.session_state.chat_history = []
    st.session_state.last_analyzed_query = query

# Render chat messages in order using Streamlit's chat UI
for role, msg in st.session_state.chat_history:
    with st.chat_message("user" if role == "you" else "assistant"):
        st.markdown(msg)

# Chat input at the bottom; show loader while generating
user_msg = st.chat_input("Ask a question or request a rewrite…")
if user_msg:
    st.session_state.chat_history.append(("you", user_msg))
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            reply = content_generator.chat_reply(user_msg)
            reply = reply or "I'm having trouble responding right now. Please try again."
            st.markdown(reply)
    st.session_state.chat_history.append(("assistant", reply))



