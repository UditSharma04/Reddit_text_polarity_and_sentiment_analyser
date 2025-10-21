#!/bin/bash

echo "🚀 Starting Enhanced Reddit Analyzer Streamlit App"
echo "=================================================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✓ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected. Activating .venv..."
    if [ -d ".venv" ]; then
        source .venv/bin/activate
        echo "✓ Virtual environment activated"
    else
        echo "❌ .venv directory not found. Please run setup first:"
        echo "   ./setup_enhanced.sh"
        exit 1
    fi
fi

echo ""
echo "📦 Checking dependencies..."
python -c "import streamlit, plotly, pandas, seaborn" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ All dependencies available"
else
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
fi

echo ""
echo "🌐 Starting Streamlit app..."
echo "📍 The app will open in your browser automatically"
echo "🔗 URL: http://localhost:8501"
echo ""
echo "📊 Features available:"
echo "  • Interactive temporal trend analysis"
echo "  • Subreddit comparison charts"
echo "  • Engagement metrics visualization"
echo "  • Research-grade data exports"
echo "  • Real-time sentiment analysis"
echo ""

streamlit run app.py
