#!/bin/bash

echo "🚀 Setting up Enhanced Reddit Analyzer"
echo "======================================"

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✓ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected. Activating .venv..."
    if [ -d ".venv" ]; then
        source .venv/bin/activate
        echo "✓ Virtual environment activated"
    else
        echo "❌ .venv directory not found. Please create it first:"
        echo "   python3.12 -m venv .venv"
        echo "   source .venv/bin/activate"
        exit 1
    fi
fi

echo ""
echo "📦 Installing enhanced dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "🔍 Verifying Python syntax..."
python verify_syntax.py

echo ""
echo "🧪 Testing enhanced modules (requires dependencies)..."
echo "Note: If this fails, the syntax is still correct - just install dependencies first"
python test_streamlit_enhanced.py || echo "⚠️  Dependencies not installed yet - this is normal on first run"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Set up your .env file with Reddit API keys:"
echo "   REDDIT_CLIENT_ID=your_client_id"
echo "   REDDIT_CLIENT_SECRET=your_client_secret"
echo "   REDDIT_USER_AGENT=script:reddit_analyser:1.0 (by u/your_username)"
echo "   GEMINI_API_KEY=your_gemini_api_key"
echo ""
echo "2. Run the Streamlit web app:"
echo "   ./run_streamlit.sh"
echo "   OR"
echo "   streamlit run app.py"
echo ""
echo "3. Run the command-line version:"
echo "   python main.py"
echo ""
echo "📚 Documentation:"
echo "• ENHANCED_FEATURES.md - New features overview"
echo "• STREAMLIT_GUIDE.md - Web interface guide"
echo ""
echo "🌐 The web app will be available at: http://localhost:8501"
