"""
FastAPI Backend for Reddit Analyzer
Provides REST API endpoints for Reddit data analysis
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import asyncio
from datetime import datetime
import json

from config.config import REDDIT_CONFIG
from src.reddit_client import RedditClient
from src.text_analysis import TextAnalyzer
from src.sentiment_analysis import calculate_sentiment_distribution

# Try to import entity analysis, but make it optional
try:
    from src.entity_analysis import EntityAnalyzer
    ENTITY_ANALYSIS_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Warning: Entity analysis unavailable due to: {e}")
    EntityAnalyzer = None
    ENTITY_ANALYSIS_AVAILABLE = False

from src.visualization import Visualizer
from src.advanced_visualization import AdvancedVisualizer
from src.trend_analysis import TrendAnalyzer
from src.research_export import ResearchExporter
from src.content_generator import ContentGenerator

# Initialize FastAPI app
app = FastAPI(
    title="Reddit Analyzer API",
    description="Advanced Reddit analysis with sentiment analysis, trends, and AI content generation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components (singleton pattern)
reddit_client = RedditClient(**REDDIT_CONFIG)
text_analyzer = TextAnalyzer()
entity_analyzer = EntityAnalyzer() if ENTITY_ANALYSIS_AVAILABLE else None
visualizer = Visualizer()
advanced_visualizer = AdvancedVisualizer(output_dir="streamlit_visualizations")
trend_analyzer = TrendAnalyzer()
research_exporter = ResearchExporter(output_dir="streamlit_research_output")
content_generator = ContentGenerator()

# Pydantic models for request/response validation
class AnalysisRequest(BaseModel):
    query: str
    limit: int = 50
    analysis_type: str = "basic"  # basic, advanced, trend, all

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ContentGenerationRequest(BaseModel):
    query: str
    keywords: List[tuple]
    sentiment_data: Dict[str, float]
    entities: Optional[Dict[str, List[str]]] = None

class AnalysisResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Reddit Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/api/search",
            "analyze": "/api/analyze",
            "sentiment": "/api/sentiment",
            "trends": "/api/trends",
            "generate-content": "/api/generate-content",
            "chat": "/api/chat",
            "export": "/api/export"
        }
    }

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Search Reddit
@app.post("/api/search")
async def search_reddit(request: AnalysisRequest):
    """
    Search Reddit and return raw results
    """
    try:
        # Extract keywords from query
        keywords = text_analyzer.extract_keywords(request.query)
        search_query = " ".join(keywords) or request.query
        
        # Search Reddit
        results = await reddit_client.search_reddit(search_query, limit=request.limit)
        
        if not results:
            return AnalysisResponse(
                success=False,
                error="No results found for the given query"
            )
        
        return AnalysisResponse(
            success=True,
            data={
                "query": request.query,
                "keywords": keywords,
                "results": results,
                "count": len(results)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Comprehensive analysis endpoint
@app.post("/api/analyze")
async def analyze(request: AnalysisRequest):
    """
    Perform comprehensive Reddit analysis including sentiment, entities, and keywords
    """
    try:
        # Extract keywords
        keywords = text_analyzer.extract_keywords(request.query)
        search_query = " ".join(keywords) or request.query
        
        # Search Reddit
        results = await reddit_client.search_reddit(search_query, limit=request.limit)
        
        if not results:
            return AnalysisResponse(
                success=False,
                error="No results found"
            )
        
        # Calculate sentiment distribution
        sentiments = calculate_sentiment_distribution(results)
        
        # Extract text content
        texts = [r['text'] for r in results if r.get('text')]
        combined_text = " ".join(texts)
        
        # Extract keywords and entities
        top_keywords = text_analyzer.extract_top_keywords(combined_text)
        entities = entity_analyzer.extract_entities(combined_text) if entity_analyzer else {}
        
        # Calculate basic metrics
        avg_score = sum(r.get('score', 0) for r in results) / len(results) if results else 0
        unique_subreddits = len(set(r.get('subreddit', 'unknown') for r in results))
        
        # Prepare response data
        response_data = {
            "query": request.query,
            "keywords": keywords,
            "results": results,
            "metrics": {
                "total_posts": len(results),
                "unique_subreddits": unique_subreddits,
                "average_score": round(avg_score, 2),
                "sentiment": sentiments
            },
            "analysis": {
                "top_keywords": top_keywords[:20] if top_keywords else [],
                "entities": entities
            }
        }
        
        # Add advanced analysis if requested
        if request.analysis_type in ["advanced", "all"]:
            # Temporal analysis
            temporal_data = _analyze_temporal_patterns(results)
            response_data["temporal_analysis"] = temporal_data
            
            # Subreddit analysis
            subreddit_data = _analyze_subreddits(results)
            response_data["subreddit_analysis"] = subreddit_data
        
        # Add trend analysis if requested
        if request.analysis_type in ["trend", "all"]:
            try:
                # Just use temporal patterns instead of full trend report
                # to avoid serialization issues
                temporal_patterns = _analyze_temporal_patterns(results)
                response_data["trend_analysis"] = {
                    "temporal_patterns": temporal_patterns,
                    "message": "Trend analysis completed"
                }
            except Exception as trend_error:
                print(f"Trend analysis error: {trend_error}")
                response_data["trend_analysis"] = {
                    "error": "Trend analysis temporarily unavailable"
                }
        
        return AnalysisResponse(success=True, data=response_data)
        
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}"
        print(f"❌ ERROR in /api/analyze: {error_detail}")
        print(traceback.format_exc())
        return AnalysisResponse(success=False, error=str(e))

# Sentiment analysis endpoint
@app.post("/api/sentiment")
async def sentiment_analysis(results: List[Dict[str, Any]]):
    """
    Calculate sentiment distribution for provided results
    """
    try:
        sentiments = calculate_sentiment_distribution(results)
        return {"success": True, "sentiment": sentiments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Trend analysis endpoint
@app.post("/api/trends")
async def trend_analysis(request: AnalysisRequest):
    """
    Generate detailed trend analysis report
    """
    try:
        keywords = text_analyzer.extract_keywords(request.query)
        search_query = " ".join(keywords) or request.query
        
        results = await reddit_client.search_reddit(search_query, limit=request.limit)
        
        if not results:
            return {"success": False, "error": "No results found"}
        
        trend_results = trend_analyzer.generate_trend_report(results, keywords)
        
        return {
            "success": True,
            "trends": trend_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Content generation endpoint
@app.post("/api/generate-content")
async def generate_content(request: ContentGenerationRequest):
    """
    Generate AI-powered content based on analysis
    """
    try:
        # Set context for content generator
        content_generator.set_context(
            topic=request.query,
            keywords=request.keywords,
            sentiment_data=request.sentiment_data,
            entities=request.entities or {}
        )
        
        # Generate content
        generated_posts = content_generator.generate_content(
            query=request.query,
            keywords=request.keywords,
            sentiment_data=request.sentiment_data
        )
        
        if generated_posts and generated_posts[0]:
            return {
                "success": True,
                "content": generated_posts[0]
            }
        else:
            return {
                "success": False,
                "error": "Could not generate content at this time"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Chat endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Interactive chat for content refinement and questions
    """
    try:
        # Set context if provided
        if request.context:
            content_generator.set_context(**request.context)
        
        # Get chat reply
        reply = content_generator.chat_reply(request.message)
        
        if reply:
            return {
                "success": True,
                "reply": reply
            }
        else:
            return {
                "success": False,
                "error": "Could not generate reply"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Export endpoint
@app.post("/api/export")
async def export_data(
    data: Dict[str, Any],
    export_format: str = "json"
):
    """
    Export analysis data in various formats
    """
    try:
        if export_format == "json":
            return {
                "success": True,
                "data": json.dumps(data, indent=2, default=str),
                "format": "json"
            }
        elif export_format == "csv":
            # Convert to CSV format
            import pandas as pd
            df = pd.DataFrame(data.get("results", []))
            csv_data = df.to_csv(index=False)
            return {
                "success": True,
                "data": csv_data,
                "format": "csv"
            }
        else:
            return {
                "success": False,
                "error": f"Unsupported format: {export_format}"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions
def _analyze_temporal_patterns(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze temporal patterns in results"""
    import pandas as pd
    
    df = pd.DataFrame(results)
    if 'created_utc' not in df.columns:
        return {}
    
    df['created_utc'] = pd.to_datetime(df['created_utc'])
    df['date'] = df['created_utc'].dt.date
    df['hour'] = df['created_utc'].dt.hour
    
    # Daily activity
    daily_activity = df.groupby('date').size().to_dict()
    
    # Hourly activity
    hourly_activity = df.groupby('hour').size().to_dict()
    
    # Sentiment over time
    sentiment_over_time = df.groupby(['date', 'sentiment']).size().reset_index(name='count')
    
    return {
        "daily_activity": {str(k): int(v) for k, v in daily_activity.items()},
        "hourly_activity": {str(k): int(v) for k, v in hourly_activity.items()},
        "sentiment_timeline": sentiment_over_time.to_dict('records')
    }

def _analyze_subreddits(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze subreddit statistics"""
    import pandas as pd
    
    df = pd.DataFrame(results)
    if 'subreddit' not in df.columns:
        return {}
    
    # Subreddit statistics
    subreddit_stats = df.groupby('subreddit').agg({
        'score': ['count', 'mean', 'sum'],
        'sentiment': lambda x: (x == 'positive').mean() * 100
    }).round(2)
    
    subreddit_stats.columns = ['post_count', 'avg_score', 'total_score', 'positive_pct']
    top_subreddits = subreddit_stats.nlargest(10, 'post_count').reset_index()
    
    return {
        "top_subreddits": top_subreddits.to_dict('records'),
        "total_subreddits": len(df['subreddit'].unique())
    }

# Word cloud generation endpoint
@app.post("/api/generate-wordcloud")
async def generate_wordcloud(results: List[Dict[str, Any]]):
    """
    Generate word cloud image from results
    """
    try:
        from wordcloud import WordCloud
        import io
        import base64
        from PIL import Image
        import matplotlib.pyplot as plt
        
        # Combine all text
        all_text = ' '.join([
            str(r.get('text', '')) + ' ' + str(r.get('title', ''))
            for r in results
        ])
        
        if not all_text.strip():
            return {"success": False, "error": "No text content available"}
        
        # Create word cloud with same settings as original
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            max_words=100,
            colormap='viridis',
            relative_scaling=0.5,
            min_font_size=10
        ).generate(all_text)
        
        # Convert to image
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        
        # Save to bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        # Convert to base64
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        return {
            "success": True,
            "image": f"data:image/png;base64,{img_base64}"
        }
        
    except Exception as e:
        import traceback
        print(f"❌ ERROR generating wordcloud: {str(e)}")
        print(traceback.format_exc())
        return {"success": False, "error": str(e)}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)


