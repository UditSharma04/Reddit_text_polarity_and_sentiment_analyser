#!/bin/bash

echo "🧹 Cleaning up unnecessary files from Reddit Analyzer..."
echo "=================================================="

# Remove test and demo files
echo "🗑️  Removing test and demo files..."
rm -f demo_enhanced.py
rm -f test_streamlit_enhanced.py
rm -f verify_syntax.py
rm -rf test_output/
rm -rf test_viz/

# Remove redundant documentation files (keep main ones)
echo "📚 Cleaning up documentation..."
rm -f SYNTAX_FIX_SUMMARY.md
rm -f STREAMLIT_FIXES_SUMMARY.md
# Keep: ENHANCED_FEATURES.md, STREAMLIT_GUIDE.md, README.md

# Remove Python cache files
echo "🐍 Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Remove empty output directories
echo "📁 Cleaning up empty directories..."
rmdir research_output/ 2>/dev/null || true
rmdir streamlit_research_output/ 2>/dev/null || true

# Remove old results file if it exists
echo "📄 Cleaning up old result files..."
rm -f reddit_results.txt 2>/dev/null || true

# Clean up any temporary files
echo "🧽 Removing temporary files..."
rm -f *.tmp *.log 2>/dev/null || true

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📁 Kept important files:"
echo "  • Core application files (app.py, main.py)"
echo "  • Source code modules (src/)"
echo "  • Configuration files"
echo "  • Setup and run scripts"
echo "  • Key documentation (README.md, ENHANCED_FEATURES.md, STREAMLIT_GUIDE.md)"
echo "  • Generated visualizations (streamlit_visualizations/)"
echo "  • NLTK data (nltk_data/)"
echo ""
echo "🗑️  Removed unnecessary files:"
echo "  • Test and demo scripts"
echo "  • Python cache files (__pycache__/)"
echo "  • Temporary documentation files"
echo "  • Empty output directories"
echo "  • Old result files"
echo ""
echo "🚀 Your Reddit Analyzer is now clean and ready for production!"
